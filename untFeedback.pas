unit untFeedback;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Buttons, HTTPApp, untMain, untShare;

type
  TfrmFeedback = class(TForm)
    txtfbTitle: TEdit;
    Label1: TLabel;
    Label2: TLabel;
    txtfbContent: TMemo;
    btnMessage: TBitBtn;
    BitBtn2: TBitBtn;
    cmbfbQmd: TComboBox;
    Label3: TLabel;
    chkfbBackup: TCheckBox;
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure btnMessageClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frmFeedback: TfrmFeedback;

implementation

{$R *.dfm}

procedure TfrmFeedback.btnMessageClick(Sender: TObject);
var
  tgtRequest:TStringList;
begin
  tgtRequest:=TStringList.Create;
  With tgtRequest do
  begin
    Values['recv']:='tyllr';
    Values['title']:=HTTPEncode(txtfbTitle.Text);
    Values['text']:=HTTPEncode(txtfbContent.Text);
    Values['signature']:=cmbfbQmd.Items[cmbfbQmd.ItemIndex];
    if chkfbBackup.Checked then
      Values['backup']:='on';
  end;
  if Perfect_Connect(bbshost+BBSPATH+'sndmail',tgtRequest) then
    showmessage('已经成功寄给作者tyllr，感谢您的支持');
  FreeAndNil(tgtRequest);
end;

procedure TfrmFeedback.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  frmFeedback := nil;
  frmFeedback.Free;
end;

end.
