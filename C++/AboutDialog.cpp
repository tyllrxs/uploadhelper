#include "UploadHelperApp.h"

//(*IdInit(AboutDialog)
const long AboutDialog::ID_STATICBITMAP1 = wxNewId();
const long AboutDialog::ID_STATICTEXT2 = wxNewId();
const long AboutDialog::ID_STATICTEXT3 = wxNewId();
const long AboutDialog::ID_STATICTEXT4 = wxNewId();
const long AboutDialog::ID_STATICLINE1 = wxNewId();
const long AboutDialog::ID_STATICTEXT5 = wxNewId();
const long AboutDialog::ID_STATICTEXT6 = wxNewId();
const long AboutDialog::ID_TEXTCTRL1 = wxNewId();
//*)

BEGIN_EVENT_TABLE(AboutDialog,wxDialog)
    //(*EventTable(AboutDialog)
    EVT_CLOSE(AboutDialog::OnClose)
    //*)
END_EVENT_TABLE()

AboutDialog::AboutDialog(wxWindow* parent,wxWindowID id,const wxPoint& pos,const wxSize& size)
{
    //(*Initialize(AboutDialog)
    wxFlexGridSizer* FlexGridSizer4;
    wxFlexGridSizer* FlexGridSizer3;
    wxFlexGridSizer* FlexGridSizer2;
    wxFlexGridSizer* FlexGridSizer1;

    Create(parent, wxID_ANY, _("About"), wxDefaultPosition, wxDefaultSize, wxDEFAULT_DIALOG_STYLE, _T("wxID_ANY"));
    SetClientSize(wxSize(526,344));
    FlexGridSizer1 = new wxFlexGridSizer(3, 1, 0, 0);
    FlexGridSizer2 = new wxFlexGridSizer(1, 2, 0, 0);
    StaticBitmap1 = new wxStaticBitmap(this, ID_STATICBITMAP1, wxBitmap(wxIcon(logo_xpm)), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICBITMAP1"));
    FlexGridSizer2->Add(StaticBitmap1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer3 = new wxFlexGridSizer(5, 1, 0, 0);
    StaticText2 = new wxStaticText(this, ID_STATICTEXT2, APP_NAME + SPACE_STRING + APP_VERSION, wxDefaultPosition, wxSize(356,29), 0, _T("ID_STATICTEXT2"));
    wxFont StaticText2Font = wxSystemSettings::GetFont(wxSYS_DEFAULT_GUI_FONT);
    if ( !StaticText2Font.Ok() ) StaticText2Font = wxSystemSettings::GetFont(wxSYS_DEFAULT_GUI_FONT);
    StaticText2Font.SetPointSize(14);
    StaticText2Font.SetWeight(wxBOLD);
    StaticText2->SetFont(StaticText2Font);
    FlexGridSizer3->Add(StaticText2, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
    StaticText3 = new wxStaticText(this, ID_STATICTEXT3, _("Author:") + SPACE_STRING + APP_AUTHOR + _T(" (") + APP_EMAIL + _T(")"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT3"));
    FlexGridSizer3->Add(StaticText3, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
    HypLink1 = new wxHyperlinkCtrl(this, ID_STATICTEXT4, _("Homepage:") + SPACE_STRING + APP_HOMEPAGE, APP_HOMEPAGE, wxDefaultPosition, wxDefaultSize, wxNO_BORDER, _T("ID_STATICTEXT4"));
    FlexGridSizer3->Add(HypLink1, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
    StaticLine1 = new wxStaticLine(this, ID_STATICLINE1, wxDefaultPosition, wxSize(10,-1), wxLI_HORIZONTAL, _T("ID_STATICLINE1"));
    FlexGridSizer3->Add(StaticLine1, 1, wxALL|wxEXPAND|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    StaticText5 = new wxStaticText(this, ID_STATICTEXT5, _("Licensed under GPL v2"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT5"));
    FlexGridSizer3->Add(StaticText5, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer2->Add(FlexGridSizer3, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer1->Add(FlexGridSizer2, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer4 = new wxFlexGridSizer(2, 1, 0, 0);
    StaticText6 = new wxStaticText(this, ID_STATICTEXT6, _("Thanks to following contributors:"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT6"));
    FlexGridSizer4->Add(StaticText6, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
    TextCtrl1 = new wxTextCtrl(this, ID_TEXTCTRL1, ACKNOWLEDGE_LIST, wxDefaultPosition, wxSize(506,77), wxTE_MULTILINE|wxTE_READONLY, wxDefaultValidator, _T("ID_TEXTCTRL1"));
    FlexGridSizer4->Add(TextCtrl1, 1, wxLEFT|wxRIGHT|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer1->Add(FlexGridSizer4, 1, wxALL|wxEXPAND|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    btnQuit = new wxButton(this, wxID_OK, _("I\'ve known"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("wxID_OK"));
    btnQuit->SetDefault();
    FlexGridSizer1->Add(btnQuit, 1, wxALL|wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL, 5);
    SetSizer(FlexGridSizer1);
    FlexGridSizer1->SetSizeHints(this);

    Center();
    //*)
}

AboutDialog::~AboutDialog()
{
    //(*Destroy(AboutDialog)
    //*)
}


void AboutDialog::OnClose(wxCloseEvent& event)
{
    Destroy();
}
