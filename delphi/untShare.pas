unit untShare;

interface
uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics,
  Controls, Forms, PerlRegEx, ComCtrls, IniFiles, Dialogs,
  JPEG, IDHTTP, TypInfo,SHDocVw, ShellAPI, StrUtils, Wincodec;
  function trimHTML(const sstr:string):string;
  function GetBoard(const sstr:string):string;
  function GetBID(const sstr:string):string;
  function GetFileURL(const sstr:string):string;
  function myFileSize(const sstr:string):LongInt;
  Function EncrypKey (Src:String; Key:String):string;
  Function UncrypKey (Src:String; Key:String):string;
  function Perfect_Connect(const surl:string;const req:TStringList=nil):boolean;
  function CheckType(const sstr,iregx:string):boolean;
  function bmp2jpg(FromBMP, ToJPG: string):boolean;
  function JPEGCompress(Fromstr, Tostr: string; Quality:Integer):boolean;
  function GetImages(const sstr:string):TstringList;
  function GetSrcUrl(const sstr:string):string;
  function GetHost(const sstr:string):string;
  function GetHostPath(const sstr:string):string;
  function DownloadFile(const sstr:string):string;
  function HTMLConv(const sstr:string):string;
  function TextConv(const sstr:string):string;
  function ClearDirectory(const DirName: string; const IncludeSub: Boolean = false; ToRecyle: Boolean = false): Boolean; stdcall;
const
  APPVERSION:string='3.6';
  APPAUTHOR:string='tyllr@日月光华';
  APPHOMEPAGE:string='http://homepage.fudan.edu.cn/~tyllr/uh/';
  BBSPATH:string='bbs/';
  BBSHOSTLIST:array[0..3] of string=('bbs.fudan.edu.cn (教育网)','bbs.fudan.sh.cn (公众网)','202.120.225.9 (教育网IP)','61.129.42.9 (公众网IP)');
  CRLF=#13#10;
  LOGINID:string='<请输入您的BBS帐号>';
  ERR_NETWORK:string='网络连接错误';
var
  bbshost: string;
  myini: TIniFile;
  
implementation
uses untMain, untLogin, untSetting;

function trimHTML(const sstr:string):string;
var re:TPerlRegEx;
strtmp:string;
begin
re:=TPerlRegEx.Create(nil);
re.Subject:=LowerCase(sstr);
re.regEx:='<br(\s+\/)?>';
re.Replacement:=CRLF;
re.ReplaceAll;
re.regEx:='<\/?p[^>]*>';
re.Replacement:=CRLF;
re.ReplaceAll;
re.regEx:='<[^>]*>';
re.Replacement:='';
re.ReplaceAll;
strtmp:=StringReplace(re.Subject,'&nbsp;',' ',[rfReplaceAll]);
strtmp:=StringReplace(strtmp,'&gt;','>',[rfReplaceAll]);
strtmp:=StringReplace(strtmp,'&lt;','<',[rfReplaceAll]);
strtmp:=StringReplace(strtmp,'&amp;','&',[rfReplaceAll]);
Result:=Trim(strtmp);
end;

//加密函数
Function EncrypKey (Src:String; Key:String):string;
var
KeyLen :Integer;
KeyPos :Integer;
offset :Integer;
dest :string;
SrcPos :Integer;
SrcAsc :Integer;
Range :Integer;

begin
KeyLen:=Length(Key);
if KeyLen = 0 then key:='Think Space';
KeyPos:=0;
Range:=256;

Randomize;
offset:=Random(Range);
dest:=format('%1.2x',[offset]);
for SrcPos := 1 to Length(Src) do
begin
SrcAsc:=(Ord(Src[SrcPos]) + offset) MOD 255;
if KeyPos < KeyLen then KeyPos:= KeyPos + 1 else KeyPos:=1;
SrcAsc:= SrcAsc xor Ord(Key[KeyPos]);
dest:=dest + format('%1.2x',[SrcAsc]);
offset:=SrcAsc;
end;
Result:=Dest;
end;

//解密函数
Function UncrypKey (Src:String; Key:String):string;
var
KeyLen :Integer;
KeyPos :Integer;
offset :Integer;
dest :string;
SrcPos :Integer;
SrcAsc :Integer;
TmpSrcAsc :Integer;
begin
KeyLen:=Length(Key);
if KeyLen = 0 then key:='Think Space';
KeyPos:=0;
offset:=StrToInt('$'+ copy(src,1,2));
SrcPos:=3;
repeat
SrcAsc:=StrToInt('$'+ copy(src,SrcPos,2));
if KeyPos < KeyLen Then KeyPos := KeyPos + 1 else KeyPos := 1;
TmpSrcAsc := SrcAsc xor Ord(Key[KeyPos]);
if TmpSrcAsc <= offset then
TmpSrcAsc := 255 + TmpSrcAsc - offset
else
TmpSrcAsc := TmpSrcAsc - offset;
dest := dest + chr(TmpSrcAsc);
offset:=srcAsc;
SrcPos:=SrcPos + 2;
until SrcPos >= Length(Src);
Result:=Dest;
end;

function GetBoard(const sstr:string):string;
var re:TPerlRegEx;
begin
re:=TPerlRegEx.Create(nil);
re.Subject:=sstr;
re.RegEx:='^[^\s]+';
if re.Match then
  Result:=re.MatchedExpression
else
  Result:='';
end;

function GetBID(const sstr:string):string;
var re:TPerlRegEx;
var tmp:string;
begin
re:=TPerlRegEx.Create(nil);
re.Subject:=sstr;
re.RegEx:='\[(\d+)\]';
if re.Match then
  Result:=re.SubExpressions[1]
else
  Result:='';
end;

function GetFileURL(const sstr:string):string;
var re:TPerlRegEx;
begin
re:=TPerlRegEx.Create(nil);
re.Subject:=sstr;
re.RegEx:='>http\:\/\/bbs\.fudan\.edu\.cn(.*?)<';
if re.Match then
  Result:='http://'+GetBoard(BBSHOSTLIST[myini.ReadInteger('Personal','urlhost',0)])+re.SubExpressions[1]
else
  Result:='';
end;

function myFileSize(const sstr:string):LongInt;
var
f: file of Byte;
begin
try
  AssignFile(f, sstr);
  Reset(f);
  Result:= FileSize(f);
  CloseFile(f);
except
  Result:=-1;
end;
end;

function Perfect_Connect(const surl:string;const req:TStringList=nil):boolean;
var i:integer;
s1, s3:TStrings;
resp, s2, s4:TStringStream;
idhttp1:TIDHTTP;
ts, ts2:TStringList;
begin
  Result:=false;
  ts2:=TStringList.Create;
  if req<>nil then ts2.Assign(req);
  for i:=0 to 1 do
  begin
    resp:=TStringStream.Create('');
    IDHTTP1:=TIDHTTP.Create(nil);
    IDHTTP1.HTTPOptions:=[hoKeepOrigProtocol];
    IDHTTP1.Request.CustomHeaders.Values['Cookie']:=myini.ReadString('Login','cookie','');
    try
      IDHTTP1.Post(surl,ts2,resp);
      if Pos('错误',resp.DataString)<=0 then
      begin
        Result:=true;
        exit;
      end
      else if (i > 0) or (Pos('登录',resp.DataString) <= 0) then
      begin
        showmessage(trimHTML(resp.DataString));
        exit;
      end
      else
      begin
        if myini.ReadString('Login','id','')='' then
          begin
          if frmLogin = nil then
            frmLogin:=TfrmLogin.Create(Application);
          frmLogin.ShowModal;
          end
        else
          begin
          s1:=TStringList.Create;
          s2:=TStringStream.Create('');
          s1.Add('id='+myini.ReadString('Login','id','')
          +'&pw='+UncrypKey(myini.ReadString('Login','pwd',''),'thankyou'));
          try
            IDHTTP1.Post(bbshost+BBSPATH+'login',s1,s2);
            showmessage(trimHTML(s2.DataString));
            exit;
          except
            if IdHTTP1.ResponseCode=302 then
            begin
              ts:=TStringList.Create;
              ts.Delimiter:=';';
              IdHTTP1.Response.RawHeaders.Extract('Set-cookie', ts);
              myini.WriteString('Login','cookie',ts.DelimitedText);
              ts.Free;
            end
            else
            begin
              showmessage(ERR_NETWORK);
              exit;
            end;
          end;
          s1.Free;
          s2.Free;
          end;
      end;
    except
      ShowMessage(Format('%s%s错误代码：%d', [ERR_NETWORK, CRLF, IDHTTP1.ResponseCode]));
      exit;
    end;
  end;
end;

function CheckType(const sstr,iregx:string):boolean;
var re:TPerlRegEx;
begin
re:=TPerlRegEx.Create(nil);
re.Subject:=LowerCase(sstr);
re.RegEx:='\.(' + iregx + ')$';
Result:=re.Match;
end;

function bmp2jpg(FromBMP, ToJPG: string):boolean;
var WicImg:TWICImage;
begin
  Result := False;
  WicImg:=TWICImage.Create;　
  //try
    WicImg.LoadFromFile(FromBMP);
    WicImg.ImageFormat:=TWICImageFormat.wifJpeg;　
  　WicImg.SaveToFile(ToJPG);
    Result := True;　
  //finally
    WicImg.Free;
  //end;
end;

function JPEGCompress(Fromstr, Tostr: string; Quality:Integer):boolean;
var
　WicImg: TWICImage;　
　Factory: IWICImagingFactory;　
　Scaler: IWICBitmapScaler;　
begin
  Result := False;
  WicImg := TWICImage.Create;　
  try
  　WicImg.LoadFromFile(Fromstr);　　
  　Factory := WicImg.ImagingFactory;　
  　Factory.CreateBitmapScaler(Scaler);　
    Scaler.Initialize(WicImg.Handle, WicImg.Width*Quality div 100, WicImg.Height*Quality div 100, WICBitmapInterpolationModeFant);  　
  　WicImg.Handle := IWICBitmap(Scaler);
    WicImg.SaveToFile(Tostr);
  　Scaler := nil;　
  　Factory := nil;　
    Result := True;
  finally
　  WicImg.Free;
  end;　
end;

//function URLEncode(const S: ansistring; const InQueryString: Boolean=true): ansistring;
//var
//  Idx: Integer; // loops thru characters in string
//begin
//  Result := '';
//  for Idx := 1 to Length(S) do
//  begin
//    case S[Idx] of
//      'A'..'Z', 'a'..'z', '0'..'9', '-', '_', '.':
//        Result := Result + S[Idx];
//      ' ':
//        if InQueryString then
//          Result := Result + '+'
//        else
//          Result := Result + '%20';
//      else
//        Result := Result + '%' + SysUtils.IntToHex(Ord(S[Idx]), 2);
//    end;
//  end;
//end;

//function URLEncode2(const S: string): string;
////var re:TRegExpr;
//begin
////re:=TRegExpr.Create;
////re.Expression:='[^\w\d\-_\.]';
////Result:=re.Replace(s,'_',false);
//end;

function GetImages(const sstr:string):TstringList;
//var re:TRegExpr;
//ts:TstringList;
//tmp,ss:string;
//i:integer;
begin
//ts:=Tstringlist.Create;
//re:=TRegExpr.Create;
//re.ModifierI:=true;
////re.Expression:='<img\s+[^>]*?src\s*\=\s*[\x22\x27]?([^\s\x22\x27]+)[^>]*?>';
////re.Expression:='<img((\s+\w+\s*\=\s*(([\x22\x27])[^\4]*?\4|[^>\x22\x27\s]+))*)\/?>';
////re.Expression:='\s+src\s*=\s*([^<>\s]+)';
//re.Expression:='=\s*\x22[^\x22]*?[<>][^\x22]*?\x22';
//tmp:=re.Replace(sstr,'',false);
//re.Expression:='=\s*\x27[^\x27]*?[<>][^\x27]*?\x27';
//tmp:=re.Replace(tmp,'',false);
//re.Expression:='<img[^>]+?src\s*=\s*([^>\s]+)[^>]*>';
//tmp:=re.Replace(tmp,'[PICA]'+'$1'+'[PICB]',true);
////tmp:=stringreplace(tmp,'width>','',[rfReplaceAll]);
//tmp:=TrimHTML(tmp);
//  try
//    re.Expression:='\[PICA\](.*?)\[PICB\]';
//    re.Split(tmp,ts);
//    i:=1;
//    if re.Exec(tmp) then
//      repeat
//          ss:=re.Match[1];
//          ss:=StringReplace(ss,#34,'',[rfReplaceAll]);
//          ss:=StringReplace(ss,#39,'',[rfReplaceAll]);
//          ss:=Trim(ss);
//          ts.Insert(i,ss);
//          i:=i+2;
//      until not re.ExecNext;
//  finally
//    re.Free;
//  end;
//Result:=ts;
end;

function GetSrcUrl(const sstr:string):string;
//var re:TRegExpr;
begin
//re:=TRegExpr.Create;
//re.Expression:='SourceURL:([^\x0A\x0D]*)';
//if re.Exec(sstr) then
//  Result:=re.Match[1]
//else
//  Result:='';
end;

function GetHost(const sstr:string):string;
//var re:TRegExpr;
begin
//re:=TRegExpr.Create;
//re.Expression:='http:\/\/[^\/]+';
//if re.Exec(sstr) then
//  Result:=re.Match[0]
//else
//  Result:='';
end;

function GetHostPath(const sstr:string):string;
var i:integer;
begin
//i:=Pos('/',ReverseString(sstr));
//Result:=Copy(sstr,1,length(sstr)-i+1);
end;

function DownloadFile(const sstr:string):string;
var myhttp:TIdHTTP;
memStream:TFileStream;
lcpath:string;
begin
//  myhttp:=TIdHTTP.Create(nil);
//  if frmMain.chkProxy.Checked then
//    begin
//    myhttp.ProxyParams.ProxyServer:=Trim(frmMain.txtProxyURL.Text);
//    myhttp.ProxyParams.ProxyPort:=frmMain.txtProxyPort.IntValue;
//    myhttp.ProxyParams.ProxyUsername:=Trim(frmMain.txtProxyUser.Text);
//    myhttp.ProxyParams.ProxyPassword:=Trim(frmMain.txtProxyPwd.Text);
//    myhttp.ProxyParams.BasicAuthentication:=(myhttp.ProxyParams.ProxyUsername='');
//    end;
//  myhttp.HandleRedirects:=true;
//  //lcpath:=ExtractFilePath(application.ExeName)+'temp';
//  lcpath:=frmMain.txtTempDir.Text;
//  if not DirectoryExists(lcpath) then
//    begin
//      lcpath:=ExtractFilePath(application.ExeName)+'temp';
//      if not DirectoryExists(lcpath) then MkDir(lcpath);
//      frmMain.txtTempDir.Text:=lcpath;
//    end;
//  lcpath:=lcpath+'\'+URLEncode2(sstr);
//  if not CheckType(lcpath,'jpg|gif|png|bmp|pdf') then
//    lcpath:=lcpath+'.jpg';
//  memStream:=TFileStream.Create(lcpath,fmCreate);
//  try
//    myhttp.Get(sstr,memStream);
//  except
//    Result:='';
//    exit;
//  end;
//  memStream.Free;
//  myhttp.Free;
//  Result:=lcpath;
end;

function HTMLConv(const sstr:string):string;
//var re:TRegExpr;
begin
//Result:=StringReplace(sstr,'&','&amp;',[rfReplaceAll]);
//Result:=StringReplace(Result,'<','&lt;',[rfReplaceAll]);
//Result:=StringReplace(Result,'>','&gt;',[rfReplaceAll]);
//Result:=StringReplace(Result,' ','&nbsp;',[rfReplaceAll]);
//re:=TRegExpr.Create;
//re.ModifierI:=true;
//re.Expression:='(http\:\/\/[\x21-\x7f]+\.(jpg|gif|png|bmp))\b';
//Result:=re.Replace(Result,'<img src="$1" alt="图片地址: $1">',true);
//Result:=StringReplace(Result,CRLF,'<br>',[rfReplaceAll]);
//Result:='<body style="font:9pt Tahoma">'+Result+'</body>';
////showmessage(Result);
end;

function TextConv(const sstr:string):string;
//var re:TRegExpr;
begin
//re:=TRegExpr.Create;
//re.ModifierI:=true;
//re.Expression:='<img[^>]*?src=\"([^\"]+?)\"[^>]*?>';
//Result:=TrimHTML(re.Replace(sstr,'$1',true));
////showmessage(sstr);
end;

function ClearDirectory(const DirName: string; const IncludeSub: Boolean = false; ToRecyle: Boolean = false): Boolean; stdcall;
  var
      fo:   TSHFILEOPSTRUCT;
  begin
      FillChar(fo,   SizeOf(fo),   0);
      with   fo   do
      begin
          Wnd   :=   GetActiveWindow;
          wFunc   :=   FO_DELETE;
          pFrom   :=   PChar(DirName   +   '\*.*'   +   #0);
          pTo   :=   #0#0;
          fFlags   :=   FOF_SILENT   or   FOF_NOCONFIRMATION   or   FOF_NOERRORUI
                              or   (Ord(not   IncludeSub)   *   FOF_FILESONLY)
                              or   (ORd(ToRecyle)   or   FOF_ALLOWUNDO);
      end;
      Result   :=   (SHFileOperation(fo)   =   0);
end;

{procedure langchange(myform:TForm; strLang:string);
var i,j:integer;
cmpt:TComponent;
prop:TStringList;
begin
  if not DirectoryExists(ExtractFilePath(Paramstr(0))+'language') then exit;
  langini:=TIniFile.Create(ExtractFilePath(Paramstr(0))+'language\'+strLang+'.lng');
  case pos(','+strLang+',',','+langs.CommaText+',') div 4 of
    0: application.Title:='UploadHelper';
    1: application.Title:='日月光华上传助手';
    2: application.Title:='日月光華上傳助手';
  end;
  myform.Caption:=langini.ReadString(myform.Name,'Caption',myform.Caption);
  prop:=TStringList.Create;
  prop.CommaText:='Caption,Hint';
  for i := 0 to myform.ComponentCount - 1 do
    begin
      cmpt:=myform.Components[i];
      for j := 0 to prop.Count - 1 do
        begin
          if GetPropInfo(cmpt,prop[j])<>nil then
            SetPropValue(cmpt,prop[j],langini.ReadString(myform.Name,cmpt.Name+'.'+prop[j],GetPropValue(cmpt,prop[j])));
        end;
    end;
  for i:= 1 to frmMain.lstUpFile.Columns.Count - 1 do
    frmMain.lstUpFile.Columns[i].Caption:=langini.ReadString(myform.Name,'lstUpFile.Column'+Inttostr(i)+'.Caption',frmMain.lstUpFile.Columns[i].Caption);
end;

procedure langsave(myform:TForm);
var i,j:integer;
cmpt:TComponent;
prop:TStringList;
begin
  prop:=TStringList.Create;
  prop.CommaText:='Caption,Hint';
  for i := 0 to myform.ComponentCount - 1 do
    begin
      cmpt:=myform.Components[i];
      for j := 0 to prop.Count - 1 do
        begin
          if (GetPropInfo(cmpt,prop[j])<>nil) then
            langini.WriteString(myform.Name,cmpt.Name+'.'+prop[j],GetPropValue(cmpt,prop[j]));
        end;
    end;
langchange(myform,myini.ReadString('General','Language','chs'));
end;     }

{procedure addWatermark(Fromstr: string);
var
      jpg   :TJpegImage;
      bmp   :TBitMap;
begin
randomize;
      jpg:=TJpegImage.Create;
      bmp:=TBitMap.Create;
      jpg.LoadFromFile(Fromstr);
      bmp.Assign(jpg);
      bmp.Canvas.Brush.Style:=bsClear;
      bmp.Canvas.Font.Color:= RGB(random(255),random(255),random(255));
      bmp.Canvas.Font.Size:= 12;
      bmp.Canvas.Font.Style:=[fsBold];
      bmp.Canvas.Font.Name:=frmSetting.font1.Items[frmSetting.font1.Count-1-random(50)];
      bmp.Canvas.TextOut((bmp.Width  -  bmp.Canvas.Font.Size*18),(bmp.Height - bmp.Canvas.Font.Size*3),'欢迎使用 日月光华上传助手');
      bmp.Canvas.Font.Size:= 12;
      bmp.Canvas.Font.Name:=frmSetting.font2.FontName;
      bmp.Canvas.Font.Style:=[fsBold,fsUnderline];
      bmp.Canvas.TextOut((bmp.Width  -  bmp.Canvas.Font.Size*25),(bmp.Height - bmp.Canvas.Font.Size*2),'http://homepage.fudan.edu.cn/~tyllr/uh/');
      jpg.Assign(bmp);
      jpg.SaveToFile(ExtractFilePath(Paramstr(0))+'ii.jpg');
      jpg.Free;
      bmp.Free;
end; }

end.






