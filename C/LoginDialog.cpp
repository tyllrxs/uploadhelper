#include "UploadHelperApp.h"

//(*IdInit(LoginDialog)
const long LoginDialog::ID_STATICBITMAP1 = wxNewId();
const long LoginDialog::ID_STATICTEXT1 = wxNewId();
const long LoginDialog::ID_CHOICE1 = wxNewId();
const long LoginDialog::ID_STATICTEXT2 = wxNewId();
const long LoginDialog::ID_TEXTCTRL1 = wxNewId();
const long LoginDialog::ID_STATICTEXT3 = wxNewId();
const long LoginDialog::ID_TEXTCTRL2 = wxNewId();
//*)

BEGIN_EVENT_TABLE(LoginDialog,wxDialog)
    //(*EventTable(LoginDialog)
    EVT_INIT_DIALOG(LoginDialog::OnInit)
    EVT_BUTTON(wxID_OK, LoginDialog::OnbtnLoginClick)
    EVT_CLOSE(LoginDialog::OnClose)
    //*)
END_EVENT_TABLE()

LoginDialog::LoginDialog(wxWindow* parent,wxWindowID id)
{
    //(*Initialize(LoginDialog)
    wxFlexGridSizer* FlexGridSizer2;
    wxFlexGridSizer* FlexGridSizer1;

    Create(parent, wxID_ANY, _("Login"), wxDefaultPosition, wxDefaultSize, wxCAPTION|wxSYSTEM_MENU|wxCLOSE_BOX|wxTAB_TRAVERSAL|wxWANTS_CHARS, _T("wxID_ANY"));
    SetClientSize(wxSize(411,304));
    FlexGridSizer1 = new wxFlexGridSizer(3, 1, 0, 0);
    StaticBitmap1 = new wxStaticBitmap(this, ID_STATICBITMAP1, wxBitmap(wxImage(title)), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICBITMAP1"));
    FlexGridSizer1->Add(StaticBitmap1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer2 = new wxFlexGridSizer(2, 2, 0, 0);
    StaticText1 = new wxStaticText(this, ID_STATICTEXT1, _("Domain / IP"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT1"));
    FlexGridSizer2->Add(StaticText1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    cmbDomain = new wxChoice(this, ID_CHOICE1, wxDefaultPosition, wxSize(226,wxDefaultSize.y), 0, 0, 0, wxDefaultValidator, _T("ID_CHOICE1"));
    for (size_t i=0; i<sizeof(BBS_URLS)/sizeof(BBS_URLS[0]); i++)
        cmbDomain->AppendString(BBS_URLS[i]);
    cmbDomain->SetSelection(UploadHelperApp::Configurations(READ, _T("Login"), _T("user_domain"), 0));
    FlexGridSizer2->Add(cmbDomain, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    StaticText2 = new wxStaticText(this, ID_STATICTEXT2, _("Username"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT2"));
    FlexGridSizer2->Add(StaticText2, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    txtUser = new wxTextCtrl(this, ID_TEXTCTRL1, wxEmptyString, wxDefaultPosition, wxSize(200,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL1"));
    txtUser->SetMaxLength(20);
    txtUser->SetFocus();
    FlexGridSizer2->Add(txtUser, 1, wxALL|wxEXPAND|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    StaticText3 = new wxStaticText(this, ID_STATICTEXT3, _("Password"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT3"));
    FlexGridSizer2->Add(StaticText3, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    txtPwd = new wxTextCtrl(this, ID_TEXTCTRL2, wxEmptyString, wxDefaultPosition, wxSize(200,wxDefaultSize.y), wxTE_PASSWORD, wxDefaultValidator, _T("ID_TEXTCTRL2"));
    FlexGridSizer2->Add(txtPwd, 1, wxALL|wxEXPAND|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer1->Add(FlexGridSizer2, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    btnLogin = new wxButton(this, wxID_OK, _("Login"), wxDefaultPosition, wxSize(120,wxDefaultSize.y), 0, wxDefaultValidator, _T("wxID_OK"));
    btnLogin->SetDefault();
    FlexGridSizer1->Add(btnLogin, 1, wxBOTTOM|wxLEFT|wxRIGHT|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 8);
    SetSizer(FlexGridSizer1);
    FlexGridSizer1->SetSizeHints(this);

    Center();
    //*)

}

LoginDialog::~LoginDialog()
{
    //(*Destroy(LoginDialog)
    //*)
}

void LoginDialog::OnInit(wxInitDialogEvent& event)
{
    txtUser->SetValue(UploadHelperApp::Configurations(READ, _T("Login"), _T("user_id"), wxEmptyString));
    txtPwd->SetValue(UploadHelperApp::Configurations(READ, _T("Login"), _T("user_password"), wxEmptyString));
}

void LoginDialog::OnbtnLoginClick(wxCommandEvent& event)
{
    if(!UploadHelperApp::LoginToBBS(txtUser->GetValue(), txtPwd->GetValue(), cmbDomain->GetSelection()))
        return;
    wxMessageBox(OK_LOGIN);
    Close();
}

void LoginDialog::OnClose(wxCloseEvent& event)
{
    Destroy();
}

