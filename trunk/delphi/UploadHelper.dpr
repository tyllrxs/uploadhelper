program UploadHelper;

uses
  Forms,
  untMain in 'untMain.pas' {frmMain},
  untShare in 'untShare.pas',
  untLogin in 'untLogin.pas' {frmLogin},
  untFeedback in 'untFeedback.pas' {frmFeedback},
  untSetting in 'untSetting.pas' {frmSetting},
  MultInst in 'MultInst.pas',
  untAbout in 'untAbout.pas' {frmAbout};

{$R *.res}

begin
  Application.Initialize;
  Application.Title := '日月光华上传助手';
  Application.CreateForm(TfrmMain, frmMain);
  Application.Run;
end.
