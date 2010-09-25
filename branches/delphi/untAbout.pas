unit untAbout;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, RzLabel, ExtCtrls,  untShare, RzPanel, RzEdit;

type
  TfrmAbout = class(TForm)
    RzGroupBox1: TRzGroupBox;
    Image1: TImage;
    lblAppName: TRzLabel;
    lblAppVersion: TRzLabel;
    lblAuthor: TRzLabel;
    Label1: TLabel;
    RzMemo1: TRzMemo;
    lblHomepage: TRzURLLabel;
    RzLabel1: TRzLabel;
    procedure FormCreate(Sender: TObject);
    procedure FormClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frmAbout: TfrmAbout;

implementation
uses untMain;
{$R *.DFM}

procedure TfrmAbout.FormClick(Sender: TObject);
begin
  Close;
end;

procedure TfrmAbout.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  frmAbout:=nil;
  frmAbout.Free;
end;

procedure TfrmAbout.FormCreate(Sender: TObject);
begin
  lblAppName.Caption:=application.Title;
  lblAppVersion.Caption:='版本: '+APPVERSION;
  lblAuthor.Caption:='作者: '+APPAUTHOR;
  lblHomepage.Caption:=APPHOMEPAGE;
  lblHomepage.URL:=APPHOMEPAGE;
  FormStyle:=frmMain.FormStyle;
end;

end.
