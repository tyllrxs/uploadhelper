unit untSetting;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Buttons, ComCtrls, ImgList, RzTreeVw, RzSpnEdt, Mask,
  RzEdit, untShare, RzLabel, RzButton, RzLstBox, RzChkLst, Math, untMain,
  RzTray, Menus, RzCmboBx, ExtCtrls, RzPanel;

type
  TfrmSetting = class(TForm)
    PageControl1: TPageControl;
    btnOK: TBitBtn;
    btnCancel: TBitBtn;
    TabSheet2: TTabSheet;
    TabSheet4: TTabSheet;
    TabSheet5: TTabSheet;
    ImageList1: TImageList;
    TabSheet7: TTabSheet;
    GroupBox4: TGroupBox;
    chkFileSize: TCheckBox;
    chkChildDir: TCheckBox;
    txtMinSize: TRzNumericEdit;
    txtMaxSize: TRzNumericEdit;
    txtPicSpace: TRzSpinEdit;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    chkCompress: TCheckBox;
    txtCompress: TRzNumericEdit;
    Label5: TLabel;
    chkTaskbar: TCheckBox;
    lstFileType: TRzCheckList;
    Label7: TLabel;
    cmbResult: TComboBox;
    txtHead: TMemo;
    txtRoot: TMemo;
    Label8: TLabel;
    Label21: TLabel;
    grpCompress: TRzGroupBox;
    Label13: TLabel;
    tbCompress: TTrackBar;
    Label14: TLabel;
    txtRatio: TRzNumericEdit;
    Label15: TLabel;
    Label16: TLabel;
    RzGroupBox1: TRzGroupBox;
    rb0: TRadioButton;
    rb2: TRadioButton;
    rb1: TRadioButton;
    chkTrayMsg: TCheckBox;
    RzGroupBox2: TRzGroupBox;
    chkMulThread: TCheckBox;
    txtMulnum: TRzSpinEdit;
    chkRetry: TCheckBox;
    chkTrimBlank: TCheckBox;
    chkTimeout: TCheckBox;
    Label10: TLabel;
    txtTimeout: TRzNumericEdit;
    chkClearOld: TCheckBox;
    gpSysTrayInfo: TRzGroupBox;
    Label11: TLabel;
    Label12: TLabel;
    txtInfoTitle: TEdit;
    txtInfoContent: TEdit;
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure FormCreate(Sender: TObject);
    procedure btnOKClick(Sender: TObject);
    procedure chkCompressClick(Sender: TObject);
    procedure tbCompressChange(Sender: TObject);
    procedure txtRatioChange(Sender: TObject);
    procedure rb0Click(Sender: TObject);
    procedure chkFileSizeClick(Sender: TObject);
    procedure chkTaskbarClick(Sender: TObject);
    procedure chkMulThreadClick(Sender: TObject);
    procedure chkTimeoutClick(Sender: TObject);
    procedure chkTrayMsgClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frmSetting: TfrmSetting;

implementation

{$R *.dfm}

procedure TfrmSetting.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  myini.WriteInteger('UserSettings','OptionPage',pagecontrol1.ActivePageIndex);
  frmSetting := nil;
  frmSetting.Free;
end;

procedure TfrmSetting.FormCreate(Sender: TObject);
var
  num,i:integer;
  ss:string;
begin
  chkMulThread.Checked:=myini.ReadBool('General','MultiThread',true);
  chkMulThreadClick(nil);
  txtMulnum.IntValue:=myini.ReadInteger('General','Threads',3);
  chkRetry.Checked:=myini.ReadBool('General','OnErrRetry',true);
  chkTimeOut.Checked:=myini.ReadBool('General','ConnTimeOut',false);
  chkTimeOutClick(nil);
  txtTimeOut.IntValue:=myini.ReadInteger('General','TimeOut',60);
  chkTaskbar.Checked:=myini.ReadBool('General','taskbar',false);
  chkTaskbarClick(nil);
  chkTrayMsg.Checked:=myini.ReadBool('General','TrayMsg',true);
  chkTrayMsgClick(nil);
  txtInfoTitle.Text:=myini.ReadString('General','InfoTitle','嘿嘿~~');
  txtInfoContent.Text:=myini.ReadString('General','InfoContent','偶已经隐藏在这里了');
  num:=myini.ReadInteger('General','trayicon',1);
  (FindComponent('rb'+inttostr(num)) as TRadioButton).Checked:=true;
  rb0Click((FindComponent('rb'+inttostr(num)) as TRadioButton));
  chkCompress.Checked:=myini.ReadBool('Compress','Compression',true);
  txtCompress.IntValue:=myini.ReadInteger('Compress','min',1024);
  chkCompressClick(nil);
  tbCompress.Position:=myini.ReadInteger('Compress','ratio',60);
  tbCompressChange(nil);
  ss:=myini.ReadString('Search','filetype','jpg|gif|png|bmp|pdf');
  for i:=0 to lstFileType.Items.Count-1 do
  begin
    if Pos('|'+lstFileType.Items[i]+'|','|'+ss+'|')>0 then
    begin
       lstFileType.ItemChecked[i]:=true;
    end;
  end;
  chkChildDir.Checked:=myini.ReadBool('Search','child_dir',false);
  chkFileSize.Checked:=myini.ReadBool('Search','filesize',true);
  chkFileSizeClick(nil);
  txtMinSize.IntValue:=myini.ReadInteger('Search','minsize',1);
  txtMaxSize.IntValue:=myini.ReadInteger('Search','maxsize',1024);
  txtPicSpace.IntValue:=myini.ReadInteger('Personal','picspace',1);
  for i := 0 to length(BBSHOSTLIST) - 1 do
    cmbResult.Items.Add(GetBoard(BBSHOSTLIST[i]));
  cmbResult.ItemIndex:=Min(myini.ReadInteger('Personal','urlhost',0),cmbResult.Items.Count-1);
  chkClearOld.Checked:=myini.ReadBool('Personal','ClearOld',false);
  txtHead.Text:=StringReplace(myini.ReadString('Personal','headtext',''),'[\n]',CRLF,[rfReplaceAll]);
  txtRoot.Text:=StringReplace(myini.ReadString('Personal','roottext',''),'[\n]',CRLF,[rfReplaceAll]);
  chkTrimBlank.Checked:=myini.ReadBool('Personal','TrimBlank',true);
  pagecontrol1.ActivePageIndex:=myini.ReadInteger('UserSettings','OptionPage',0);
end;

procedure TfrmSetting.btnOKClick(Sender: TObject);
var
  i,num:integer;
  ss:string;
begin
  myini.WriteBool('General','MultiThread',chkMulThread.Checked);
  myini.WriteInteger('General','Threads',txtMulnum.IntValue);
  myini.WriteBool('General','OnErrRetry',chkRetry.Checked);
  myini.WriteBool('General','ConnTimeOut',chkTimeOut.Checked);
  myini.WriteInteger('General','TimeOut',txtTimeOut.IntValue);
  myini.WriteBool('General','taskbar',chkTaskbar.Checked);
  myini.WriteBool('General','TrayMsg',chkTrayMsg.Checked);
  myini.WriteString('General','InfoTitle',txtInfoTitle.Text);
  myini.WriteString('General','InfoContent',txtInfoContent.Text);
  for num:=0 to 2 do
  begin
    if (FindComponent('rb'+inttostr(num)) as TRadioButton).Checked then
    begin
      myini.WriteInteger('General','trayicon',num);
      break;
    end;
  end;
  myini.WriteBool('Compress','Compression',chkCompress.Checked);
  myini.WriteInteger('Compress','min',txtCompress.IntValue);
  myini.WriteInteger('Compress','ratio',tbCompress.Position);
  ss:='';
  for i:=0 to lstFileType.Items.Count-1 do
  begin
    if lstFileType.ItemChecked[i] then
    begin
       ss:=ss+'|'+lstFileType.Items[i];
    end;
  end;
  Delete(ss,1,1);
  myini.WriteString('Search','filetype',ss);
  myini.WriteBool('Search','child_dir',chkChildDir.Checked);
  myini.WriteBool('Search','filesize',chkFileSize.Checked);
  myini.WriteInteger('Search','minsize',txtMinSize.IntValue);
  myini.WriteInteger('Search','maxsize',txtMaxSize.IntValue);
  myini.WriteInteger('Personal','urlhost',cmbResult.ItemIndex);
  myini.WriteInteger('Personal','picspace',txtPicSpace.IntValue);
  myini.WriteBool('Personal','ClearOld',chkClearOld.Checked);
  myini.WriteString('Personal','headtext',StringReplace(txtHead.Text,CRLF,'[\n]',[rfReplaceAll]));
  myini.WriteString('Personal','roottext',StringReplace(txtRoot.Text,CRLF,'[\n]',[rfReplaceAll]));
  myini.WriteBool('Personal','TrimBlank',chkTrimBlank.Checked);
end;

procedure TfrmSetting.chkCompressClick(Sender: TObject);
begin
  txtCompress.Enabled:=chkCompress.Checked;
  grpCompress.Enabled:=chkCompress.Checked;
end;

procedure TfrmSetting.tbCompressChange(Sender: TObject);
begin
  txtRatio.IntValue:=tbCompress.Position;
end;

procedure TfrmSetting.txtRatioChange(Sender: TObject);
begin
  tbCompress.Position:=txtRatio.IntValue;
end;

procedure TfrmSetting.rb0Click(Sender: TObject);
begin
  if (Sender as TRadioButton).Tag=0 then
  begin
    chkTaskbar.Checked:=true;
    chkTaskbarClick(nil);
    chkTaskbar.Enabled:=false;
    frmMain.trayicon.Enabled:=false;
  end
  else
  begin
    chkTaskbar.Enabled:=true;
    frmMain.trayicon.Enabled:=true;
  end;
  if (Sender as TRadioButton).Tag=1 then
    frmMain.trayicon.Animate:=false
  else
    frmMain.trayicon.Animate:=true;
end;

procedure TfrmSetting.chkFileSizeClick(Sender: TObject);
begin
  txtMinSize.Enabled:=chkFileSize.Checked;
  txtMaxSize.Enabled:=chkFileSize.Checked;
end;

procedure TfrmSetting.chkMulThreadClick(Sender: TObject);
begin
  txtMulnum.Enabled:=chkMulThread.Checked;
end;

procedure TfrmSetting.chkTaskbarClick(Sender: TObject);
begin
  frmMain.trayicon.HideOnMinimize:=not chkTaskbar.Checked;
end;

procedure TfrmSetting.chkTimeoutClick(Sender: TObject);
begin
  txtTimeout.Enabled:=chkTimeout.Checked;
end;

procedure TfrmSetting.chkTrayMsgClick(Sender: TObject);
begin
  gpSysTrayInfo.Enabled:=chkTrayMsg.Checked;
end;

end.
