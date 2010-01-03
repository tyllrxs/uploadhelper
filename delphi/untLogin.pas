unit untLogin;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, ExtCtrls, RzButton, IdBaseComponent,
  IdComponent, IdTCPConnection, IdTCPClient, IdHTTP, ImgList,
  Buttons, ComCtrls, RzLabel, untShare, untMain,
   RzCmboBx;

type
  TfrmLogin = class(TForm)
    Image1: TImage;
    txtPwd: TEdit;
    btnLogin: TRzBitBtn;
    ImageList1: TImageList;
    cmbBBShost: TComboBoxEx;
    IdHTTP1: TIdHTTP;
    RzURLLabel1: TRzURLLabel;
    RzLabel1: TRzLabel;
    txtId: TComboBox;
    btnDelId: TBitBtn;
    chkRemember: TCheckBox;
    procedure FormShow(Sender: TObject);
    procedure txtIdExit(Sender: TObject);
    procedure txtIdEnter(Sender: TObject);
    procedure btnDelIdClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure btnLoginClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frmLogin: TfrmLogin;

implementation

{$R *.dfm}

procedure TfrmLogin.btnDelIdClick(Sender: TObject);
begin
  txtId.Text:=LOGINID;
  txtId.Items.Delete(txtId.ItemIndex);
end;

procedure TfrmLogin.btnLoginClick(Sender: TObject);
var
  i:integer;
  inList:boolean;
  req, ts:TStringList;
  resp:TStringStream;
begin
  if (txtID.Text='') or (txtID.Text=LOGINID) or (txtPwd.Text='') then
  begin
    showmessage('请先填写完整');
    exit;
  end;
  btnLogin.Enabled:=false;
  req:=TStringList.Create;
  req.Add('id='+txtID.Text+'&pw='+txtPwd.Text);
  resp:=TStringStream.Create('');
  try
    IDHTTP1.Post(bbshost+BBSPATH+'login',req,resp);
    showmessage(trimHTML(resp.DataString));
  except
    if IdHTTP1.ResponseCode=302 then
    begin
      ts:=TStringList.Create;
      ts.Delimiter:=';';
      IdHTTP1.Response.RawHeaders.Extract('Set-cookie', ts);
      myini.WriteString('Login','cookie',ts.DelimitedText);
      FreeAndNil(ts);

      inList:=false;
      for i:=0 to txtID.Items.Count-1 do
      begin
        if txtID.Items[i]=txtID.Text then
        begin
          inList:=true;
          break;
        end;
      end;
      if not inList then
        txtID.Items.Insert(0,txtID.Text);
      myini.WriteInteger('Login','bbshost',cmbBBShost.ItemIndex);
      myini.WriteString('Login','id',txtID.Text);
      if chkRemember.Checked then
        myini.WriteString('Login','pwd',EncrypKey(txtPwd.Text,'thankyou'))
      else
        myini.DeleteKey('Login','pwd');

      showmessage('登录成功，可以开始上传文件了');
      frmMain.Caption:=application.Title+' v'+APPVERSION+' - ['+myini.ReadString('Login','id','')+']';
      self.Close;
    end
    else
    begin
      showmessage(Format('%s%s错误代码：%d', [ERR_NETWORK, CRLF, IdHTTP1.ResponseCode]));
    end;
  end;
  btnLogin.Enabled:=true;
end;

procedure TfrmLogin.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  myini.WriteString('Login','RecentID',txtID.Items.CommaText);
  myini.WriteString('Login','lastID',txtID.Text);
  myini.WriteBool('Login','RememberPwd',chkRemember.Checked);
  frmLogin := nil;
  frmLogin.Free;
end;

procedure TfrmLogin.FormCreate(Sender: TObject);
var i:integer;
begin
  for i := 0 to length(BBSHOSTLIST) - 1 do
  begin
    cmbBBShost.ItemsEx.AddItem(BBSHOSTLIST[i],i mod 2,i mod 2,-1,-1,nil);
  end;
  cmbBBShost.ItemIndex:=myini.ReadInteger('Login','bbshost',0);
  chkRemember.Checked:=myini.ReadBool('Login','RememberPwd',true);
end;

procedure TfrmLogin.FormShow(Sender: TObject);
begin
  With txtID do
  begin
    SetFocus;
    Items.CommaText:=myini.ReadString('Login','RecentID','');
    Text:=myini.ReadString('Login','lastID',LOGINID);
    SelectAll;
  end;
end;

procedure TfrmLogin.txtIdEnter(Sender: TObject);
begin
if txtId.Text=LOGINID then
  txtId.Text:='';
end;

procedure TfrmLogin.txtIdExit(Sender: TObject);
begin
if Trim(txtId.Text)='' then
  txtId.Text:=LOGINID;
end;

end.
