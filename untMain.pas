unit untMain;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, Menus,  ImgList, ComCtrls, ToolWin,
  StdCtrls, untShare, RzButton, RzListVw, RzShellDialogs, Buttons, IniFiles,
  IdHTTP, Clipbrd, xmldom, XMLIntf, msxmldom, XMLDoc, Math, RzStatus, ExtCtrls, RzPanel,
  IdAntiFreezeBase, IdAntiFreeze, RzCommon, RzSelDir, ShellAPI, RzForms,
  Mask, RzEdit, StrUtils, MultInst, IdBaseComponent, IdComponent,
  IdTCPConnection, IdTCPClient, IdMultiPartFormData,
   RzTray, RzRadChk, OleCtrls, SHDocVw,  RzTabs, RzBtnEdt, RzCmboBx,
  dwProgressBar, dwTaskbarComponents, httpapp, IOUtils, Types;

type
  TfrmMain = class(TForm)
    MainMenu1: TMainMenu;
    L1: TMenuItem;
    O1: TMenuItem;
    H1: TMenuItem;
    mnuLogin: TMenuItem;
    mnuLogout: TMenuItem;
    mnuSetting: TMenuItem;
    mnuAbout: TMenuItem;
    mnuHelpTopic: TMenuItem;
    mnuNewVersion: TMenuItem;
    N3: TMenuItem;
    ImageList1: TImageList;
    N4: TMenuItem;
    ToolBar1: TToolBar;
    ToolButton1: TToolButton;
    ToolButton2: TToolButton;
    ToolButton3: TToolButton;
    ToolButton5: TToolButton;
    ToolButton6: TToolButton;
    PageControl1: TPageControl;
    tstUpload: TTabSheet;
    ImageList2: TImageList;
    cmbZone: TComboBox;
    btnBrowse: TRzMenuButton;
    PopupMenu1: TPopupMenu;
    mnuFileSelect: TMenuItem;
    mnuFolderSelect: TMenuItem;
    mnuFeedback: TMenuItem;
    N5: TMenuItem;
    IdHTTP1: TIdHTTP;
    N7: TMenuItem;
    mnuHomepage: TMenuItem;
    ToolButton8: TToolButton;
    N8: TMenuItem;
    mnuToolbar: TMenuItem;
    mnuFterm: TMenuItem;
    mnuCterm: TMenuItem;
    xml: TXMLDocument;
    chkLocked: TCheckBox;
    N9: TMenuItem;
    mnuAlwaysOnTop: TMenuItem;
    TrayIcon: TRzTrayIcon;
    ppMenu: TPopupMenu;
    mnuRestore: TMenuItem;
    MenuItem1: TMenuItem;
    mnuExit: TMenuItem;
    lstUpFile: TRzListView;
    Label9: TLabel;
    Label10: TLabel;
    btnUpload: TBitBtn;
    diagTerm: TFileOpenDialog;
    diagOpen: TFileOpenDialog;
    diagXPOpen: TOpenDialog;
    diagXPTerm: TOpenDialog;
    diagXPFolder: TRzSelectFolderDialog;
    lblProgress: TLabel;
    RzStatusBar1: TRzStatusBar;
    RzStatusPane1: TRzStatusPane;
    tstPost: TTabSheet;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    txtTitle: TEdit;
    cmbQmd: TComboBox;
    btnPost: TBitBtn;
    txtContent: TRzMemo;
    cmbpstZone: TComboBox;
    tstZZ: TTabSheet;
    Label11: TLabel;
    Memo1: TMemo;
    RzGroupBox1: TRzGroupBox;
    grpProxy: TRzGroupBox;
    Label1: TLabel;
    Label2: TLabel;
    Label7: TLabel;
    Label8: TLabel;
    txtProxyURL: TEdit;
    txtProxyPort: TRzNumericEdit;
    txtProxyUser: TEdit;
    txtProxyPwd: TEdit;
    chkProxy: TCheckBox;
    btnZZ: TBitBtn;
    chkSourceURL: TCheckBox;
    opt0: TRadioButton;
    opt1: TRadioButton;
    txtTempDir: TRzButtonEdit;
    chkClearTempDir: TCheckBox;
    cmbpstBoard: TComboBox;
    cmbBoard: TComboBox;
    pp: TdwProgressBar;
    procedure txtTempDirButtonClick(Sender: TObject);
    procedure chkSourceURLClick(Sender: TObject);
    procedure chkProxyClick(Sender: TObject);
    procedure TrayIconMinimizeApp(Sender: TObject);
    procedure mnuExitClick(Sender: TObject);
    procedure mnuRestoreClick(Sender: TObject);
    procedure mnuAlwaysOnTopClick(Sender: TObject);
    procedure chkLockedClick(Sender: TObject);
    procedure btnZZClick(Sender: TObject);
    procedure ListViewAutoNumber(lv : TRzListView);
    procedure FormCreate(Sender: TObject);
    procedure mnuFileSelectClick(Sender: TObject);
    procedure mnuAboutClick(Sender: TObject);
    procedure mnuFeedbackClick(Sender: TObject);
    procedure mnuLoginClick(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure mnuSettingClick(Sender: TObject);
    procedure mnuRemoveClick(Sender: TObject);
    procedure mnuRemoveAllClick(Sender: TObject);
    procedure btnUploadClick(Sender: TObject);
    procedure cmbZoneChange(Sender: TObject);
    procedure mnuFolderSelectClick(Sender: TObject);
    procedure SearchFile(mypath: string);
    procedure btnPostClick(Sender: TObject);
    procedure mnuHelpTopicClick(Sender: TObject);
    procedure cmbBoardChange(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure mnuLogoutClick(Sender: TObject);
    procedure mnuRemoveInvalidClick(Sender: TObject);
    procedure mnuRemoveDuplicateClick(Sender: TObject);
    procedure mnuHomepageClick(Sender: TObject);
    procedure mnuFtermClick(Sender: TObject);
    procedure mnuNewVersionClick(Sender: TObject);
    procedure explainHTML(const sstr:string);
    procedure cmbpstZoneChange(Sender: TObject);
    procedure FormResize(Sender: TObject);
    procedure lstUpFileDragOver(Sender, Source: TObject; X, Y: Integer;
      State: TDragState; var Accept: Boolean);
    procedure lstUpFileDragDrop(Sender, Source: TObject; X, Y: Integer);
    procedure lstUpFileColumnClick(Sender: TObject; Column: TListColumn);
    procedure lstUpFileCompare(Sender: TObject; Item1, Item2: TListItem;
      Data: Integer; var Compare: Integer);
    procedure lstUpFileItemContextMenu(Sender: TObject; Item: TListItem;
      var Pos: TPoint; var Menu: TPopupMenu);
    procedure lstUpFileContextPopup(Sender: TObject; MousePos: TPoint;
      var Handled: Boolean);

  private
    { Private declarations }
  public
    { Public declarations }
    procedure DragFileProc(var Message: TMessage);
  end;

type regThread=class(TThread)
        private
              IdHTTPreg:TIdHTTP;
              fid:integer;
              flg,msg:string;
              retried:boolean;
              flname: string;
        protected
              procedure             Execute;         override;
              procedure upld;
              procedure upld2;
              procedure upld3;
              procedure upld4;
        public
              constructor         Create(myindex:integer);
              destructor           Destroy;         override;

        end;

var
  frmMain: TfrmMain;
  flgUploaded,webcopy,appendmode:boolean;
  tsPicList:Tstringlist;
  OLDWndProc:TWndMethod;
  flgCompress:boolean;
  rati,vmin,total,over,nn:integer;
  tmp:string;
  BeginIndex, EndIndex, ColumnToSort: integer;
  asc:boolean;
  smax,smin: Integer;
  strFileType: string;
  flgSize: boolean;

implementation
uses untAbout,untFeedback,untLogin,untSetting;
{$R *.dfm}

/////////////////////////////////////////////////////////////
constructor regThread.Create(myindex:integer);
begin
      inherited   Create(false);   //false   创建后立即执行
      FreeOnTerminate:=true;     //true       自动结束线程
      retried:=false;
      InterlockedIncrement(total);
      if myindex>=nn then
      begin
        self.Terminate;
        exit;
      end;
      fid:=myindex;
      IdHTTPreg:=TIDHttp.Create(nil);
      IdHTTPreg.Request.ContentType := 'multipart/form-data';
      if myini.ReadBool('General','ConnTimeOut',false) then
        IdHTTPreg.ReadTimeout:=1000*myini.ReadInteger('General','TimeOut',60);
      IdHTTPreg.Request.CustomHeaders.Values['Cookie']:=myini.ReadString('Login','cookie','');
end;
/////////////////////////////////////////////////////////////
destructor regThread.Destroy;
begin
    IdHTTPreg.Free;
    inherited   Destroy;
end;
/////////////////////////////////////////////////////////////
procedure regThread.Execute;
begin
  upld;
  synchronize(upld2);
  if flg='' then
  begin
    upld3;
  end;
  synchronize(upld4);
end;

procedure regThread.upld;
begin
  flg:='';
  msg:='上传中...';
  flname:=frmMain.lstUpFile.Items[fid].SubItems[0];
  if not fileexists(flname) then
  begin
    msg:='文件不存在';
    flg:='fail';
    exit;
  end
  else if not CheckType(flname,'jpg|png|gif|pdf|jpeg') then
  begin
    msg:='不支持此文件类型';
    flg:='fail';
    exit;
  end
  else if CheckType(flname,'bmp') then
  begin
    if bmp2jpg(flname,flname+'.jpg') then
      flname:=flname+'.jpg'
    else
    begin
      msg:='BMP格式未能成功转换成JPG格式';
      flg:='fail';
      exit;
    end;
  end;
  if flgCompress and CheckType(flname,'jpg') and (Strtoint(frmMain.lstUpFile.Items[fid].SubItems[1])>vmin) then
  begin
    if JPEGCompress(flname,flname+'.jpg',rati) then
      flname:=flname+'.jpg'
    else
    begin
      msg:='图片未能成功压缩';
      flg:='fail';
      exit;
    end;
//        frmMain.lstUpFile.Items[fid].SubItems[0]:=flname;
//        frmMain.lstUpFile.Items[fid].SubItems[1]:=Inttostr(myfilesize(flname) div 1024);
  end;
end;

procedure regThread.upld2;
begin
  frmMain.lstUpfile.Items[fid].SubItems[2]:=msg;
end;

procedure regThread.upld3;
var
Content:TIdMultiPartFormDataStream;
response:TStringStream;
begin
  try
    try
      Content:=TIdMultiPartFormDataStream.Create;
      response:=TStringStream.Create('');
      Content.AddFile('up',flname,'');
      try
        IdHTTPreg.Post(bbshost+BBSPATH+'upload?b='+GetBoard(frmMain.cmbBoard.Items[frmMain.cmbBoard.ItemIndex]),Content,response);
        if Pos('错误',response.DataString)>0 then
          flg:='fail'
        else
          flg:='OK';
        msg:=response.DataString;
      except
        flg:='fail';
        msg:=ERR_NETWORK;
      end;
    finally
      Content.Free;
      response.Free;
    end;
  except
    on e:exception do
      begin
        flg:='Except';
        msg:='失败，'+e.ClassName+' '+e.Message;
      end;
  end;
end;

procedure regThread.upld4;
begin
  if flg='OK' then
        begin
          frmMain.lstUpfile.Items[fid].SubItems[2]:='成功';
          frmMain.txtContent.Text:=StringReplace(frmMain.txtContent.Text,'[File'+Inttostr(fid+1)+' Uploading...]',GetFileURL(msg),[rfReplaceAll]);
        end
  else if flg='fail' then
        frmMain.lstUpfile.Items[fid].SubItems[2]:='失败，'+trimHTML(msg)
  else if flg='Except' then
      begin
        if (not retried) and myini.ReadBool('General','OnErrRetry',true) then
        begin
           retried:=true;
           upld3;
           exit;
        end;
        frmMain.lstUpFile.Items[fid].SubItems[2]:=msg;
      end
  else
  begin
    frmMain.lstUpfile.Items[fid].SubItems[2]:=msg;
  end;
  if flg<>'OK' then
    frmMain.txtContent.Text:=StringReplace(frmMain.txtContent.Text,'[File'+Inttostr(fid+1)+' Uploading...]','',[rfReplaceAll]);

    InterlockedIncrement(over);
    frmMain.pp.Position:=100*over div nn;
    frmMain.lblProgress.Caption:='目前进度: '+Inttostr(over)+' / '+Inttostr(nn);

    if over = nn then
    begin
      frmMain.btnUpload.Enabled:=true;
      flgUploaded:=true;
      if webcopy and frmMain.chkClearTempDir.Checked then
        ClearDirectory(frmMain.txtTempDir.Text);
      webcopy:=false;
      if myini.ReadBool('Personal','TrimBlank',true) then
        frmMain.txtContent.Text:=Trim(frmMain.txtContent.Text);
      frmMain.PageControl1.ActivePage:=frmMain.tstPost;
    end;
    if total<nn then
    begin
       regThread.Create(total);
    end;
end;

procedure TfrmMain.ListViewAutoNumber(lv : TRzListView);
var
  i:integer;
begin
  for i:=lv.Items.Count-1 downto 0 do
  begin
     lv.Items[i].Caption:=Inttostr(i+1);
  end;
  lblProgress.Caption:='选择了 '+Inttostr(lv.Items.Count)+' 个文件';
  btnUpload.Enabled:=true;
end;

procedure TfrmMain.lstUpFileColumnClick(Sender: TObject; Column: TListColumn);
begin
  ColumnToSort := Column.Index;
  asc := not asc;
  (Sender as TCustomListView).AlphaSort;
end;

procedure TfrmMain.lstUpFileCompare(Sender: TObject; Item1, Item2: TListItem;
  Data: Integer; var Compare: Integer);
var i:integer;
begin
  if ColumnToSort = 0 then
    Compare := CompareValue(StrToInt(Item1.Caption),StrToInt(Item2.Caption))
  else
    if ColumnToSort = 2 then
      Compare := CompareValue(StrToInt(Item1.SubItems[1]),StrToInt(Item2.SubItems[1]))
    else
    begin
      i := ColumnToSort - 1;
      Compare := CompareText(Item1.SubItems[i],Item2.SubItems[i]);
    end;
  if asc then
    Compare := - Compare;
end;


procedure TfrmMain.lstUpFileContextPopup(Sender: TObject; MousePos: TPoint;
  var Handled: Boolean);
begin
  lstUpFile.PopupMenu:=PopupMenu1;
end;

procedure TfrmMain.lstUpFileDragDrop(Sender, Source: TObject; X, Y: Integer);
var
  currentItem, nextItem, dragItem, dropItem : TListItem;
begin
  if Sender = Source then
  begin
    with TListView(Sender) do
    begin
      dropItem := GetItemAt(X, Y) ;
      currentItem := Selected;
      while currentItem <> nil do
      begin
        nextItem := GetNextItem(currentItem, SdAll, [IsSelected]) ;
        if Assigned(dropItem) then
          dragItem := Items.Insert(dropItem.Index)
        else
          dragItem := Items.Add;
        dragItem.Assign(currentItem) ;
        currentItem.Free;
        currentItem := nextItem;
      end;
    end;
  end;
end;

procedure TfrmMain.lstUpFileDragOver(Sender, Source: TObject; X, Y: Integer;
  State: TDragState; var Accept: Boolean);
begin
  Accept := Sender = lstUpFile;
end;

procedure TfrmMain.lstUpFileItemContextMenu(Sender: TObject; Item: TListItem;
  var Pos: TPoint; var Menu: TPopupMenu);
var
  myPopMenu:TPopupMenu;
  myMenuItem:TMenuItem;
begin
  myPopMenu:=TPopupMenu.Create(Self);
  myPopMenu.AutoHotkeys:=maManual;
  myPopMenu.Images:=ImageList1;

  if Assigned(Item) then
  begin
    myMenuItem:=TMenuItem.Create(nil);
    With myMenuItem do
    begin
      Caption:='移除选中';
      ImageIndex:=11;
      OnClick:=mnuRemoveClick;
    end;
    myPopMenu.Items.Add(myMenuItem);
  end;

  if myPopMenu.Items.Count>0 then
  begin
    myMenuItem:=TMenuItem.Create(nil);
    myMenuItem.Caption:='-';
    myPopMenu.Items.Add(myMenuItem);
  end;

  myMenuItem:=TMenuItem.Create(nil);
  With myMenuItem do
  begin
    Caption:='移除重复的';
    OnClick:=mnuRemoveDuplicateClick;
  end;
  myPopMenu.Items.Add(myMenuItem);

  myMenuItem:=TMenuItem.Create(nil);
  With myMenuItem do
  begin
    Caption:='移除无效的';
    OnClick:=mnuRemoveInvalidClick;
  end;
  myPopMenu.Items.Add(myMenuItem);

  myMenuItem:=TMenuItem.Create(nil);
    myMenuItem.Caption:='-';
    myPopMenu.Items.Add(myMenuItem);

  myMenuItem:=TMenuItem.Create(nil);
  With myMenuItem do
  begin
    Caption:='移除所有';
    ImageIndex:=10;
    OnClick:=mnuRemoveAllClick;
  end;
  myPopMenu.Items.Add(myMenuItem);

  Menu:=myPopMenu;
end;

{procedure TfrmMain.lngEngClick(Sender: TObject);
begin
  (Sender as TMenuItem).Checked:=True;
  //showmessage('重启本程序生效');
  myini.WriteString('General','Language',langs.Strings[(Sender as TMenuItem).Tag]);
  langsave(self);
end;}

procedure TfrmMain.FormCreate(Sender: TObject);
begin
  //if FormatDateTime('YYYY',DATE)<>'2009' then
  //begin
  //  ShowMessage('对不起，本测试版已经过期，请使用新版本');
  //  ShellExecute(0, 'open', PChar(APPHOMEPAGE), '','', SW_SHOWNORMAL);
  //  Application.Terminate;
  //end;
  myini:=TIniFile.Create(ExtractFilePath(Paramstr(0))+'UploadHelper.ini');
  //langini:=TIniFile.Create(ExtractFilePath(Paramstr(0))+'language\'+myini.ReadString('General','Language','chs')+'.ini');
  //rzreg1.WriteString('Command','','"'+Paramstr(0)+'" "%1"');
  //if ParamCount>0 then showmessage(Paramstr(1));
  asc:=True;
  flgUploaded:=false;
  webcopy:=false;
  appendmode:=true;
  DragAcceptFiles(lstUpfile.handle,true);
  OLDWndProc:=lstUpfile.WindowProc;
  //保存原来的WindowProc
  lstUpfile.WindowProc:=self.DragFileProc;
  //设置新的WindowProc
  self.Caption:=application.Title+' v'+APPVERSION;
  self.Width:=myini.ReadInteger('UserSettings','MainWinWidth',503);
  self.Height:=myini.ReadInteger('UserSettings','MainWinHeight',489);
  if myini.ReadBool('UserSettings','MainWinMaximized',False) then
    self.WindowState:=wsMaximized;
end;

procedure TfrmMain.FormResize(Sender: TObject);
begin
  if self.Width<503 then self.Width:=503;
  if self.Height<489 then self.Height:=489;
  PageControl1.Width:=self.ClientWidth;
  PageControl1.Height:=self.ClientHeight - PageControl1.TabHeight - 5;
  lstUpFile.Width:= PageControl1.ClientWidth - 27;
  lstUpFile.Height:= PageControl1.ClientHeight - PageControl1.TabHeight - btnBrowse.Top - btnBrowse.Height - btnUpload.Height - 20;
  lstUpFile.Columns[1].Width:= lstUpFile.Width * 7 div 14;
  lstUpFile.Columns[2].Width:= lstUpFile.Width * 2 div 14;
  lstUpFile.Columns[3].Width:= lstUpFile.Width - lstUpFile.Columns[0].Width
   - lstUpFile.Columns[1].Width - lstUpFile.Columns[2].Width - 24;
  btnUpload.Top:= lstUpFile.Top + lstUpFile.Height + 3;
  btnUpload.Left:= (PageControl1.Width - btnUpload.Width) div 2;
  lblProgress.Top:= btnUpload.Top + 4;
  lblProgress.Left:= lstUpFile.Left;
  pp.Width:= lstUpFile.Width div 3;
  pp.Top:= lblProgress.Top;
  pp.Left:= lstUpFile.Left + lstUpFile.Width - pp.Width;
  txtContent.Width:= lstUpFile.Width;
  txtContent.Height:= lstUpFile.Height;
  btnPost.Top:= btnUpload.Top;
  btnPost.Left:= btnUpload.Left;
end;

procedure TfrmMain.mnuFileSelectClick(Sender: TObject);
var i:integer;
begin
  try
    diagOpen.Options:=[fdoAllowMultiSelect];
    if not diagopen.Execute then exit;
    if flgUploaded then lstUpfile.Clear;
    flgUploaded:=false;
    for i:=0 to diagopen.Files.Count-1 do
    begin
      with lstupfile.Items.Add.SubItems do
      begin
        Add(diagopen.Files.Strings[i]);
        Add(Inttostr(myFileSize(diagopen.Files.Strings[i]) div 1024)+'');
        Add('');
      end;
    end;
  except
    diagXPOpen.Options:=[ofAllowMultiSelect];
    diagXPOpen.Filter:='所有支持的格式(*.jpg;*.jpeg;*.png;*.gif;*.pdf)|*.jpg;*.jpeg;*.png;*.gif;*.pdf'
                        +'|所有图像格式(*.jpg;*.jpeg;*.png;*.gif)|*.jpg;*.jpeg;*.png;*.gif'
                        +'|PDF 文档(*.pdf)|*.pdf'
                        +'|所有文件(*.*)|*.*';
    if not diagXPopen.Execute then exit;
    if flgUploaded then lstUpfile.Clear;
    flgUploaded:=false;
    for i:=0 to diagXPopen.Files.Count-1 do
    begin
      with lstupfile.Items.Add.SubItems do
      begin
        Add(diagXPopen.Files.Strings[i]);
        Add(Inttostr(myFileSize(diagXPopen.Files.Strings[i]) div 1024)+'');
        Add('');
      end;
    end;
  end;
  ListViewAutoNumber(lstUpfile);
end;

procedure TfrmMain.mnuAboutClick(Sender: TObject);
begin
  if frmAbout = nil then
    frmAbout:=TfrmAbout.Create(Application);
  frmAbout.Show;
end;

procedure TfrmMain.mnuAlwaysOnTopClick(Sender: TObject);
begin
  if mnuAlwaysOnTop.Checked then
    self.FormStyle:=fsStayOnTop
  else
    self.FormStyle:=fsNormal;
end;

procedure TfrmMain.mnuFeedbackClick(Sender: TObject);
begin
  if frmFeedback = nil then
    frmFeedback:=TfrmFeedback.Create(Application);
  frmFeedback.ShowModal;
end;

procedure TfrmMain.mnuLoginClick(Sender: TObject);
begin
  if frmLogin = nil then
    frmLogin:=TfrmLogin.Create(Application);
  frmLogin.ShowModal;
end;

procedure TfrmMain.FormShow(Sender: TObject);
var root:IXMLNode;
i:integer;
begin
  frmMain.Caption:=application.Title+' v'+APPVERSION+' - ['+myini.ReadString('Login','id','')+']';
  pagecontrol1.ActivePageIndex:=Min(myini.ReadInteger('UserSettings','ActivePage',0),pagecontrol1.PageCount-1);
  bbshost:='http://'+GetBoard(BBSHOSTLIST[myini.ReadInteger('Login','bbshost',0)])+'/';
  if (myini.ReadString('Login','id','')='') or (myini.ReadString('Login','pwd','')='') then
  begin
    mnuLoginClick(nil);
  end;
  try
    xml.Active:=true;
    xml.Encoding:='utf-8';
    xml.LoadFromFile('UploadHelper.xml');
    root:=xml.DocumentElement;
    for i:=0 to root.ChildNodes.Count-1 do
    begin
    cmbZone.Items.Add(Inttostr(i)+')'+root.ChildNodes[i].NodeName);
    end;
    xml.Active:=false;
  except
    showmessage('xml文件读取错误，请到官方网站下载完整版，官方地址见"帮助"菜单~~');
    exit;
  end;
  cmbpstZone.Items:=cmbZone.Items;
  cmbZone.ItemIndex:=Min(myini.ReadInteger('UserSettings','UpZone',4),cmbZone.Items.Count-1);
  cmbZoneChange(nil);
  chkLocked.Checked:=myini.ReadBool('UserSettings','Locked',false);
  chkLockedClick(nil);
  cmbpstZone.ItemIndex:=Min(myini.ReadInteger('UserSettings','PostZone',4),cmbpstZone.Items.Count-1);
  cmbpstZoneChange(nil);
  mnuAlwaysOnTop.Checked:=myini.ReadBool('UserSettings','AlwaysOnTop',false);
  mnuAlwaysOnTopClick(self);
  chkProxy.Checked:=myini.ReadBool('Network','Proxy',false);
  chkProxyClick(nil);
  txtProxyURL.Text:=myini.ReadString('Network','ProxyServer','');
  txtProxyPort.IntValue:=myini.ReadInteger('Network','ProxyPort',0);
  txtProxyUser.Text:=myini.ReadString('Network','ProxyUsername','');
  txtProxyPwd.Text:=myini.ReadString('Network','ProxyPassword','');
  chkSourceURL.Checked:=myini.ReadBool('UserSettings','SourceURL',true);
  chkSourceURLClick(nil);
  if myini.ReadInteger('UserSettings','SourceURLPosition',0)=0 then
    opt0.Checked:=true
  else
    opt1.Checked:=true;
  txtTempDir.Text:=myini.ReadString('UserSettings','TempDir',ExtractFilePath(application.ExeName)+'temp');
  chkClearTempDir.Checked:=myini.ReadBool('UserSettings','TempDirClear',true);
  {for i:= 0 to mnuLanguage.Count - 1 do
    begin
      if langs.Strings[i]=myini.ReadString('General','Language','chs') then
        begin
          mnuLanguage.Items[i].Checked:=True;
          break;
        end;
    end; }
  if myini.ReadInteger('General','TrayIcon',1)=0 then
    trayicon.Enabled:=false
  else if myini.ReadInteger('General','TrayIcon',1)=2 then
    trayicon.Animate:=true;
  trayicon.Hint:=application.Title;
end;

procedure TfrmMain.mnuSettingClick(Sender: TObject);
begin
  if frmSetting = nil then
    frmSetting:=TfrmSetting.Create(Application);
  frmSetting.ShowModal;
end;

procedure TfrmMain.mnuRemoveClick(Sender: TObject);
begin
  lstUpFile.DeleteSelected;
  ListViewAutoNumber(lstUpfile);
end;

procedure TfrmMain.mnuRemoveAllClick(Sender: TObject);
begin
  lstUpFile.Clear;
  ListViewAutoNumber(lstUpfile);
end;

procedure TfrmMain.btnUploadClick(Sender: TObject);
var
i,threads:integer;
begin
  total:=0;
  over:=0;
  if lstUpFile.Items.Count<=0 then
  begin
    showmessage('还没选择要上传的文件呢');
    exit;
  end;
  if cmbBoard.ItemIndex<0 then
  begin
    showmessage('还没选择上传版面呢');
    exit;
  end;
  nn:=lstUpFile.Items.Count;
  btnUpload.Enabled:=false;
  lblProgress.Caption:='正在检查网络...';
  tmp:=myini.ReadString('Personal','signature','Uploaded by UploadHelper v'+APPVERSION+' (by tyllr)');
  if not Perfect_Connect(bbshost+BBSPATH+'preupload?board='+GetBoard(cmbBoard.Items[cmbBoard.ItemIndex])) then
  begin
    btnUpload.Enabled:=true;
    lblProgress.Caption:=ERR_NETWORK;
    exit;
  end;
  pp.Visible:=true;
  pp.Position:=0;
  if (myini.ReadBool('Personal','ClearOld',false)) or (not appendmode) then
    txtContent.Clear;
  appendmode:=true;
  txtContent.Lines.Add(StringReplace(myini.ReadString('Personal','headtext',''),'[\n]',CRLF,[rfReplaceAll])+CRLF);
  for i := 0 to nn - 1 do
  begin
    if webcopy then
    begin
      txtContent.Lines.Add(Trim(tsPicList.Strings[i*2])+CRLF);
    end;
    txtContent.Lines.Add('[File'+Inttostr(i+1)+' Uploading...]'+DupeString(CRLF,myini.ReadInteger('Personal','picspace',1)));
  end;
  if webcopy and (tsPicList.Count mod 2=1) then
    txtContent.Lines.Add(Trim(tsPicList.Strings[tsPicList.Count-1]));
  txtContent.Lines.Add(CRLF+StringReplace(myini.ReadString('Personal','roottext',''),'[\n]',CRLF,[rfReplaceAll]));

  lblProgress.Caption:='开始上传文件...';
  flgCompress:=myini.ReadBool('Compress','Compression',true);
  vmin:=myini.ReadInteger('Compress','min',1024);
  rati:=myini.ReadInteger('Compress','ratio',60);
  threads:=myini.ReadInteger('General','Threads',3);
  if not myini.ReadBool('General','MultiThread',true) then
    threads:=1
  else if threads>10 then
  begin
    ShowMessage('你太BT了,也该歇歇了~~');
    Application.Terminate;
    exit;
  end
  else if threads<=0 then
    threads:=1;

  for i := 0 to threads - 1 do
  begin
    if i>=nn then
       break;
    regThread.Create(i);
  end;

end;

procedure TfrmMain.cmbZoneChange(Sender: TObject);
var root,patnode:IXMLNode;
i,j:integer;
begin
  cmbBoard.Clear;
  xml.Active:=true;
  xml.Encoding:='utf-8';
  xml.LoadFromFile('UploadHelper.xml');
  root:=xml.DocumentElement;
  for i:=0 to root.ChildNodes.Count-1 do
  begin
    patnode:=root.ChildNodes[i];
    if Pos(patnode.NodeName,cmbZone.Items[cmbZone.ItemIndex])>0 then
    begin
      for j:=0 to patnode.ChildNodes.Count-1 do
      begin
        cmbBoard.Items.Add(patnode.ChildNodes[j].NodeName+' ('+patnode.ChildNodes[j].Attributes['name']+') ['+patnode.ChildNodes[j].Attributes['bid']+']');
      end;
      break;
    end;
  end;
  cmbBoard.ItemIndex:=Min(myini.ReadInteger('UserSettings','UpBoard',15),cmbBoard.Items.Count-1);
  xml.Active:=false;
  cmbpstZone.ItemIndex:=cmbZone.ItemIndex;
  cmbpstZoneChange(nil);
  cmbBoardChange(nil);
end;

procedure TfrmMain.mnuFolderSelectClick(Sender: TObject);
var mypath:string;
begin
  try
    diagOpen.Options:=[fdoPickFolders];
    if not diagOpen.Execute then exit;
    mypath:=diagOpen.FileName;
  except
    diagXPFolder.Title:='浏览文件夹';
    if not diagXPFolder.Execute then exit;
    mypath:=diagXPFolder.SelectedPathName;
  end;
  if flgUploaded then lstUpfile.Clear;
  flgUploaded:=false;
  SearchFile(mypath);
  ListViewAutoNumber(lstUpfile);
end;

function fp(const Path: string; const SearchRec: TSearchRec): Boolean;
begin
  if CheckType(SearchRec.Name, strFileType) then
  begin
    if not (flgSize and ((SearchRec.Size < smin * 1024) or (SearchRec.Size > smax * 1024))) then
    begin
      with frmMain.lstupfile.Items.Add.SubItems do
      begin
        Add(Path + '\' + SearchRec.Name);
        Add(Inttostr(SearchRec.Size div 1024));
        Add('');
      end;
    end;
  end;
end;

procedure TfrmMain.SearchFile(mypath: string);
begin
  strFileType:=myini.ReadString('Search','filetype','jpg|gif|png|bmp|pdf');
  flgSize:=myini.ReadBool('Search','filesize',true);
  smax:=myini.ReadInteger('Search','maxsize',1024);
  smin:=myini.ReadInteger('Search','minsize',0);
  if myini.ReadBool('Search','child_dir',false) then
    TDirectory.GetFiles(mypath, '*.*', TSearchOption.soAllDirectories, fp)
  else
    TDirectory.GetFiles(mypath, fp);
end;

procedure TfrmMain.TrayIconMinimizeApp(Sender: TObject);
begin
if myini.ReadBool('General','TrayMsg',true) then
  trayicon.ShowBalloonHint(myini.ReadString('General','InfoTitle','嘿嘿~~'),myini.ReadString('General','InfoContent','偶已经隐藏在这里了'));
end;

procedure TfrmMain.txtTempDirButtonClick(Sender: TObject);
begin
try
  diagOpen.Options:=[fdoPickFolders];
  diagOpen.FileName:=txtTempDir.Text;
  if not diagOpen.Execute then exit;
  txtTempDir.Text:=diagOpen.FileName;
except
  diagXPFolder.Title:='浏览文件夹';
  diagXPFolder.SelectedPathName:=txtTempDir.Text;
  if not diagXPFolder.Execute then exit;
  txtTempDir.Text:=diagXPFolder.SelectedPathName;
end;
end;

procedure TfrmMain.btnZZClick(Sender: TObject);
var   fn,html:string;
          i,fl,size:integer;  
          data:thandle;
          p:pointer;             //数据指针
begin
//  lstUpFile.Clear;
//  if not (Clipboard.HasFormat(CF_TEXT) or Clipboard.HasFormat(CF_OEMTEXT)) then
//    exit;
//  html:=Clipboard..asText;
//
//  //html:=Trim(System.UTF8ToWideString(html));
//  ShowMessage(html);
//  //explainHTML(html);
end;

procedure TfrmMain.explainHTML(const sstr:string);
var ts:TStringList;
i:integer;
tmp,srcUrl:string;
begin
//    memo1.text:='=========HTML BEGIN==========';
//    memo1.Lines.Add(sstr);
//    memo1.Lines.Add('=========HTML END==========');
//    tmp:=sstr;
//    srcUrl:=GetSrcUrl(tmp);
//    Delete(tmp,1,Pos('<!--StartFragment-->',tmp)-1);
//    Delete(tmp,Pos('<!--EndFragment-->',tmp),80);
//    ts:=GetImages(tmp);
//    if chkSourceURL.Checked then
//    begin
//      if opt0.Checked then
//        ts.Strings[0]:='来源: '+srcUrl+CRLF+CRLF+ts.Strings[0]
//      else
//        ts.Strings[ts.Count - 1]:=ts.Strings[ts.Count - 1]+CRLF+CRLF+'来源: '+srcUrl;
//    end;
//    memo1.Lines.Add('=========解析开始==========');
//    for i := 0 to ts.Count - 1 do
//      begin
//        if i mod 2=0 then
//           memo1.Lines.Add(ts.Strings[i])
//        else
//           memo1.Lines.Add('图片: '+ts.Strings[i]);
//      end;
//    memo1.Lines.Add('=========解析完毕==========');
//    memo1.Lines.Add('找到'+inttostr(ts.Count div 2)+'张图片');
//    for i := 0 to ts.Count - 1 do
//      begin
//        if i mod 2=1 then
//          begin
//            if Pos('/',ts.Strings[i])=1 then
//              ts.Strings[i]:=GetHost(srcUrl)+ts.Strings[i]
//            else if Pos('http://',ts.Strings[i])<>1 then
//              ts.Strings[i]:=GetHostPath(srcUrl)+ts.Strings[i];
//            memo1.Lines.Add('正在下载图片( '+Inttostr(i div 2+1)+' / '+inttostr(ts.Count div 2)+' ): '
//            +CRLF+ts.Strings[i]);
//            ts.Strings[i]:=DownloadFile(ts.Strings[i]);
//            with lstupfile.Items.Add.SubItems do
//              begin
//                Add(ts.Strings[i]);
//                Add(Inttostr(myFileSize(ts.Strings[i]) div 1024)+'');
//                Add('');
//              end;
//            if ts.Strings[i]='' then
//              memo1.Lines.Add('下载出现错误');
//            application.ProcessMessages;
//          end;
//      end;
//    btnZZ.Enabled:=true;
//    ListViewAutoNumber(lstUpfile);
//    pagecontrol1.Activepage:=tstUpload;
//    webcopy:=true;
//    tsPicList:=ts;
//    btnUploadClick(nil);
end;

procedure TfrmMain.btnPostClick(Sender: TObject);
var tgtRequest:TStringList;
begin
  if (Trim(txtTitle.Text)='') or (Trim(txtContent.Text)='') then
  begin
    showmessage('标题和内容都不能为空');
    exit;
  end
  else if not btnUpload.Enabled then
  begin
    if messagebox(self.Handle,PChar('文件还没有上传完毕,仍要继续吗?'),PChar('提示'),mb_OKCancel+MB_ICONWARNING+MB_DEFBUTTON2)=IDCancel then
      exit;
  end;
  appendmode:=false;
  btnPost.Enabled:=false;
  tgtRequest:=TStringList.Create;
  With tgtRequest do
  begin
    Values['title']:=HTTPEncode(txtTitle.Text);
    Values['text']:=HTTPEncode(txtContent.Text);
    Values['signature']:=cmbQmd.Items[cmbQmd.ItemIndex];
  end;
  if Perfect_Connect(bbshost+BBSPATH+'snd?bid='+GetBID(cmbpstBoard.Items[cmbpstBoard.ItemIndex]),tgtRequest) then
  begin
    lstUpFile.Clear;
    showmessage('发表成功! 快去 '+GetBoard(cmbpstBoard.Items[cmbpstBoard.ItemIndex])+' 版看看吧:)');
  end;
  FreeAndNil(tgtRequest);
  btnPost.Enabled:=true;
end;

procedure TfrmMain.mnuHelpTopicClick(Sender: TObject);
begin
ShellExecute(0, 'open', PChar(APPHOMEPAGE+'faq.htm'), '','', SW_SHOWNORMAL);
end;

procedure TfrmMain.chkLockedClick(Sender: TObject);
begin
  cmbZone.Enabled:=not chkLocked.Checked;
  cmbBoard.Enabled:=not chkLocked.Checked;
end;

procedure TfrmMain.chkProxyClick(Sender: TObject);
begin
  grpProxy.Enabled:=chkProxy.Checked;
end;

procedure TfrmMain.chkSourceURLClick(Sender: TObject);
begin
  opt0.Enabled:=chkSourceURL.Checked;
  opt1.Enabled:=chkSourceURL.Checked;
end;

procedure TfrmMain.cmbBoardChange(Sender: TObject);
begin
  cmbpstBoard.ItemIndex:=cmbBoard.ItemIndex;
end;

procedure TfrmMain.cmbpstZoneChange(Sender: TObject);
var root,patnode:IXMLNode;
i,j:integer;
begin
  cmbpstBoard.Clear;
  xml.Active:=true;
  xml.Encoding:='utf-8';
  xml.LoadFromFile('UploadHelper.xml');
  root:=xml.DocumentElement;
  for i:=0 to root.ChildNodes.Count-1 do
  begin
    patnode:=root.ChildNodes[i];
    if Pos(patnode.NodeName,cmbpstZone.Items[cmbpstZone.ItemIndex])>0 then
    begin
      for j:=0 to patnode.ChildNodes.Count-1 do
      begin
        cmbpstBoard.Items.Add(patnode.ChildNodes[j].NodeName+' ('+patnode.ChildNodes[j].Attributes['name']+') ['+patnode.ChildNodes[j].Attributes['bid']+']');
      end;
      break;
    end;
  end;
  cmbpstBoard.ItemIndex:=Min(myini.ReadInteger('UserSettings','PostBoard',15),cmbpstBoard.Items.Count-1);
  xml.Active:=false;
end;

procedure TfrmMain.FormClose(Sender: TObject; var Action: TCloseAction);
begin
myini.WriteInteger('UserSettings','MainWinWidth',self.Width);
myini.WriteInteger('UserSettings','MainWinHeight',self.Height);
myini.WriteBool('UserSettings','MainWinMaximized',self.WindowState=wsMaximized);
myini.WriteInteger('UserSettings','UpZone',cmbZone.ItemIndex);
myini.WriteInteger('UserSettings','UpBoard',cmbBoard.ItemIndex);
myini.WriteBool('UserSettings','Locked',chkLocked.Checked);
myini.WriteInteger('UserSettings','PostZone',cmbpstZone.ItemIndex);
myini.WriteInteger('UserSettings','PostBoard',cmbpstBoard.ItemIndex);
myini.WriteInteger('UserSettings','ActivePage',pagecontrol1.ActivePageIndex);
myini.WriteBool('UserSettings','AlwaysOnTop',mnuAlwaysOnTop.Checked);
myini.WriteBool('Network','Proxy',chkProxy.Checked);
myini.WriteString('Network','ProxyServer',txtProxyURL.Text);
myini.WriteInteger('Network','ProxyPort',txtProxyPort.IntValue);
myini.WriteString('Network','ProxyUsername',txtProxyUser.Text);
myini.WriteString('Network','ProxyPassword',txtProxyPwd.Text);
myini.WriteBool('UserSettings','SourceURL',chkSourceURL.Checked);
if opt0.Checked then
  myini.WriteInteger('UserSettings','SourceURLPosition',0)
else
  myini.WriteInteger('UserSettings','SourceURLPosition',1);
myini.WriteString('UserSettings','TempDir',txtTempDir.Text);
myini.WriteBool('UserSettings','TempDirClear',chkClearTempDir.Checked);
end;

procedure TfrmMain.mnuLogoutClick(Sender: TObject);
var
req:TStringList;
resp:TStringStream;
begin
req:=TStringList.Create;
resp:=TStringStream.Create('');
idhttp1.Request.CustomHeaders.Values['Cookie']:=myini.ReadString('Login','cookie','');
try
  idhttp1.Post(bbshost+BBSPATH+'logout',req,resp);
  if Pos('错误',resp.DataString)>0 then
    begin
    showmessage(resp.DataString);
    exit;
    end
  else
    begin
    myini.EraseSection('Login');
    showmessage('注销成功');
    frmMain.Caption:=application.Title+' v'+APPVERSION+' - ['+myini.ReadString('Login','id','')+']';
    end;
except
  showmessage(ERR_NETWORK);
  exit;
end;
end;

procedure TfrmMain.mnuRemoveInvalidClick(Sender: TObject);
var i:integer;
begin
for i:=lstUpfile.Items.Count-1 downto 0 do
  begin
  if not fileExists(lstUpfile.Items[i].SubItems[0]) then
    lstUpfile.Items[i].Delete;
  end;
ListViewAutoNumber(lstUpfile);
end;

procedure TfrmMain.mnuRestoreClick(Sender: TObject);
begin
trayicon.RestoreApp;
end;

procedure TfrmMain.mnuRemoveDuplicateClick(Sender: TObject);
var i,j:integer;
begin
for i:=lstUpfile.Items.Count-1 downto 1 do
  for j:=i-1 downto 0 do
  begin
  if CompareText(lstUpfile.Items[j].SubItems[0],lstUpfile.Items[i].SubItems[0])=0 then
  begin
    lstUpfile.Items[i].Delete;
    break;
  end;
  end;
ListViewAutoNumber(lstUpfile);
end;

procedure TfrmMain.DragFileProc(var Message:TMessage) ;
var
  i:word;
  p:array[0..254]of char;
begin
  if Message.Msg=WM_DropFiles then
  begin
  i:=DragQueryFile(Message.WParam,$FFFFFFFF,nil,0);
  //取得拖放文件总数
  for i:=0 to i-1 do
  begin
  DragQueryFile(Message.WParam,i,p,255);
  //取得拖放文件名
  with lstupfile.Items.Add.SubItems do
    begin
      Add(StrPas(p));
      Add(Inttostr(myFileSize(StrPas(p)) div 1024)+'');
      Add('');
    end;
  end;
  ListViewAutoNumber(lstUpfile);
  end
  else //其他消息，调用原来的处理程序
  OLDWndProc(Message);
end;


procedure TfrmMain.mnuHomepageClick(Sender: TObject);
begin
ShellExecute(0, 'open', PChar(APPHOMEPAGE), '','', SW_SHOWNORMAL);
end;

procedure TfrmMain.mnuExitClick(Sender: TObject);
begin
  application.Terminate;
end;

procedure TfrmMain.mnuFtermClick(Sender: TObject);
var myTerm,myPath:string;
num:integer;
tIni:TIniFile;
ts:TStringList;
begin
myTerm:=StringReplace((Sender as TMenuItem).Caption,'&','',[rfReplaceAll]);
showmessage('请先关闭'+myTerm+'，然后选择'+myTerm+'所在目录');
try
diagTerm.Title:='选择'+myTerm+'的位置';
with diagTerm.FileTypes.Items[0] do
  begin
    DisplayName:=myTerm+'.exe';
    FileMask:=myTerm+'.exe';
  end;
if not diagTerm.Execute then exit;
myPath:=ExtractFilePath(diagTerm.FileName);
except
diagXPTerm.Title:='选择'+myTerm+'的位置';
diagXPTerm.Filter:=myTerm+'.exe|'+myTerm+'.exe';
if not diagXPTerm.Execute then exit;
myPath:=ExtractFilePath(diagXPTerm.FileName);
end;
if Lowercase(myTerm)='fterm' then
begin
  tIni:=TIniFile.Create(myPath+myTerm+'.ini');
  num:=tIni.ReadInteger('Script','TotalNumber',0);
  tIni.WriteInteger('Script','TotalNumber',num+1);
  tIni.WriteString('SCRIPT'+Inttostr(num),'DESC',application.Title+' v'+APPVERSION);
  tIni.WriteInteger('SCRIPT'+Inttostr(num),'CMDTYPE',1);
  tIni.WriteString('SCRIPT'+Inttostr(num),'CATEGORY',application.Title);
  tIni.WriteString('SCRIPT'+Inttostr(num),'COMMAND',application.ExeName);
  tIni.Free;
end
else
begin
   ts:=TStringlist.Create;
   if not FileExists(myPath+'User\mycmds.txt') then
   begin
     if not CopyFile(PChar(myPath+'User\mycmds.txt.example'), PChar(myPath+'User\mycmds.txt'), False) then
     begin
        showmessage('找不到文件：'+myPath+'User\mycmds.txt');
        exit;
     end;
   end;
   try
     ts.LoadFromFile(myPath+'User\mycmds.txt');
     ts.Add('99; ; 上传助手; true; py:import os\\nos.startfile(r\"'+StringReplace(application.ExeName,'\','\\',[rfReplaceAll])+'\");');
     ts.SaveToFile(myPath+'User\mycmds.txt');
     ts.Free;
   except
     showmessage('写入文件失败：'+myPath+'User\mycmds.txt');
     exit;
   end;
end;
showmessage('成功加入'+myTerm+'工具栏');
end;

procedure TfrmMain.mnuNewVersionClick(Sender: TObject);
var resp:string;
ts:TStringList;
idhttp3:TIdhttp;
begin
idhttp3:=TIdhttp.Create(nil);
idhttp3.Request.CacheControl:='no-cache';
try
  resp:=idhttp3.Get(APPHOMEPAGE+'version.htm');
  ts:=TStringlist.Create;
  ts.Delimiter:=#13;
  ts.DelimitedText:=resp;
  if CompareText(Trim(ts.Strings[0]),APPVERSION)>0 then
    begin
    if messagebox(handle,PChar('发现新版本 v'+Trim(ts.Strings[0])+'，'+CRLF+'是否立即升级?'),PChar(application.Title),mb_YesNo+mb_IconQuestion)=IDYES then
      ShellExecute(0, 'open', PChar(APPHOMEPAGE), '','', SW_SHOWNORMAL)
    else
      exit;
    end
  else
    begin
    showmessage('您使用的是最新版本');
    exit;
    end;
except
  showmessage(ERR_NETWORK);
  exit;
end;
idhttp3.Free;
end;

end.
