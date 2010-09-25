#include "UploadHelperApp.h"

//(*IdInit(ConfigDialog)
const long ConfigDialog::ID_RADIOBUTTON1 = wxNewId();
const long ConfigDialog::ID_RADIOBUTTON2 = wxNewId();
const long ConfigDialog::ID_STATICTEXT1 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL1 = wxNewId();
const long ConfigDialog::ID_STATICTEXT2 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL2 = wxNewId();
const long ConfigDialog::ID_STATICTEXT3 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL3 = wxNewId();
const long ConfigDialog::ID_STATICTEXT4 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL4 = wxNewId();
const long ConfigDialog::ID_STATICTEXT5 = wxNewId();
const long ConfigDialog::ID_SPINCTRL1 = wxNewId();
const long ConfigDialog::ID_PANEL1 = wxNewId();
const long ConfigDialog::ID_CHECKBOX1 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL8 = wxNewId();
const long ConfigDialog::ID_STATICTEXT6 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL9 = wxNewId();
const long ConfigDialog::ID_CHECKBOX2 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL10 = wxNewId();
const long ConfigDialog::ID_STATICTEXT7 = wxNewId();
const long ConfigDialog::ID_STATICTEXT8 = wxNewId();
const long ConfigDialog::ID_SLIDER4 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL11 = wxNewId();
const long ConfigDialog::ID_PANEL4 = wxNewId();
const long ConfigDialog::ID_CHECKBOX4 = wxNewId();
const long ConfigDialog::ID_SLIDER1 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL5 = wxNewId();
const long ConfigDialog::ID_CHECKBOX5 = wxNewId();
const long ConfigDialog::ID_SLIDER2 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL6 = wxNewId();
const long ConfigDialog::ID_CHECKBOX6 = wxNewId();
const long ConfigDialog::ID_SLIDER3 = wxNewId();
const long ConfigDialog::ID_TEXTCTRL7 = wxNewId();
const long ConfigDialog::ID_PANEL2 = wxNewId();
const long ConfigDialog::ID_STATICTEXT9 = wxNewId();
const long ConfigDialog::ID_cmbDisplayHost = wxNewId();
const long ConfigDialog::ID_STATICTEXT10 = wxNewId();
const long ConfigDialog::ID_txtBlankLines = wxNewId();
const long ConfigDialog::ID_CHECKBOX3 = wxNewId();
const long ConfigDialog::ID_CHECKBOX7 = wxNewId();
const long ConfigDialog::ID_PANEL3 = wxNewId();
const long ConfigDialog::ID_NOTEBOOK1 = wxNewId();
const long ConfigDialog::ID_CHECKBOX8 = wxNewId();
//*)

BEGIN_EVENT_TABLE(ConfigDialog,wxDialog)
	//(*EventTable(ConfigDialog)
	EVT_INIT_DIALOG(ConfigDialog::OnInit)
	EVT_COMMAND_SCROLL(ID_SLIDER1, ConfigDialog::OnsldHueScroll)
	EVT_COMMAND_SCROLL(ID_SLIDER2, ConfigDialog::OnsldBlurScroll)
	EVT_COMMAND_SCROLL(ID_SLIDER3, ConfigDialog::OnsldRotateScroll)
	EVT_COMMAND_SCROLL(ID_SLIDER4, ConfigDialog::OnsldQualityScroll)
	EVT_RADIOBUTTON(wxID_ANY, ConfigDialog::OnRadioBtnClick)
	EVT_CHECKBOX(ID_CHECKBOX1, ConfigDialog::OnchkScaleClick)
	EVT_CHECKBOX(ID_CHECKBOX2, ConfigDialog::OnchkQualityClick)
	EVT_CHECKBOX(ID_CHECKBOX4, ConfigDialog::OnchkHueClick)
	EVT_CHECKBOX(ID_CHECKBOX5, ConfigDialog::OnchkBlurClick)
	EVT_CHECKBOX(ID_CHECKBOX6, ConfigDialog::OnchkRotateClick)
	EVT_BUTTON(wxID_OK, ConfigDialog::SaveConfig)
	EVT_CLOSE(ConfigDialog::OnClose)
	//*)
END_EVENT_TABLE()

ConfigDialog::ConfigDialog(wxWindow* parent,wxWindowID id)
{
	//(*Initialize(ConfigDialog)
	wxStaticBoxSizer* StaticBoxSizer2;
	wxFlexGridSizer* FlexGridSizer4;
	wxFlexGridSizer* FlexGridSizer10;
	wxFlexGridSizer* FlexGridSizer3;
	wxFlexGridSizer* FlexGridSizer5;
	wxFlexGridSizer* FlexGridSizer9;
	wxFlexGridSizer* FlexGridSizer2;
	wxFlexGridSizer* FlexGridSizer7;
	wxStaticBoxSizer* StaticBoxSizer3;
	wxFlexGridSizer* FlexGridSizer8;
	wxBoxSizer* BoxSizer1;
	wxFlexGridSizer* FlexGridSizer14;
	wxFlexGridSizer* FlexGridSizer13;
	wxFlexGridSizer* FlexGridSizer12;
	wxFlexGridSizer* FlexGridSizer6;
	wxStaticBoxSizer* StaticBoxSizer1;
	wxFlexGridSizer* FlexGridSizer1;
	wxFlexGridSizer* FlexGridSizer11;
	wxStaticBoxSizer* StaticBoxSizer5;
	wxStdDialogButtonSizer* StdDialogButtonSizer1;

	Create(parent, wxID_ANY, _("Preferences"), wxDefaultPosition, wxDefaultSize, wxDEFAULT_DIALOG_STYLE, _T("wxID_ANY"));
	FlexGridSizer1 = new wxFlexGridSizer(2, 1, 0, 0);
	Notebook1 = new wxNotebook(this, ID_NOTEBOOK1, wxDefaultPosition, wxDefaultSize, 0, _T("ID_NOTEBOOK1"));

	Panel1 = new wxPanel(Notebook1, ID_PANEL1, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL, _T("ID_PANEL1"));
	FlexGridSizer2 = new wxFlexGridSizer(0, 1, 0, 0);
	StaticBoxSizer1 = new wxStaticBoxSizer(wxVERTICAL, Panel1, _("Proxy Settings"));
	BoxSizer1 = new wxBoxSizer(wxHORIZONTAL);
	RadioButton1 = new wxRadioButton(Panel1, ID_RADIOBUTTON1, _("No Proxy"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_RADIOBUTTON1"));
	BoxSizer1->Add(RadioButton1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	RadioButton2 = new wxRadioButton(Panel1, ID_RADIOBUTTON2, _("Use Proxy"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_RADIOBUTTON2"));
	BoxSizer1->Add(RadioButton2, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer1->Add(BoxSizer1, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer3 = new wxFlexGridSizer(0, 4, 0, 0);
	StaticText1 = new wxStaticText(Panel1, ID_STATICTEXT1, _("Address"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT1"));
	FlexGridSizer3->Add(StaticText1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtProxyAddr = new wxTextCtrl(Panel1, ID_TEXTCTRL1, wxEmptyString, wxDefaultPosition, wxSize(210,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL1"));
	FlexGridSizer3->Add(txtProxyAddr, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticText2 = new wxStaticText(Panel1, ID_STATICTEXT2, _("Port"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT2"));
	FlexGridSizer3->Add(StaticText2, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtProxyPort = new wxTextCtrl(Panel1, ID_TEXTCTRL2, wxEmptyString, wxDefaultPosition, wxSize(70,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL2"));
	FlexGridSizer3->Add(txtProxyPort, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer1->Add(FlexGridSizer3, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer4 = new wxFlexGridSizer(0, 4, 0, 0);
	StaticText3 = new wxStaticText(Panel1, ID_STATICTEXT3, _("Username"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT3"));
	FlexGridSizer4->Add(StaticText3, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtProxyUser = new wxTextCtrl(Panel1, ID_TEXTCTRL3, wxEmptyString, wxDefaultPosition, wxSize(141,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL3"));
	FlexGridSizer4->Add(txtProxyUser, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticText4 = new wxStaticText(Panel1, ID_STATICTEXT4, _("Password"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT4"));
	FlexGridSizer4->Add(StaticText4, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtProxyPwd = new wxTextCtrl(Panel1, ID_TEXTCTRL4, wxEmptyString, wxDefaultPosition, wxSize(133,wxDefaultSize.y), wxTE_PASSWORD, wxDefaultValidator, _T("ID_TEXTCTRL4"));
	FlexGridSizer4->Add(txtProxyPwd, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer1->Add(FlexGridSizer4, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer2->Add(StaticBoxSizer1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer3 = new wxStaticBoxSizer(wxVERTICAL, Panel1, _("Thread Settings"));
	FlexGridSizer5 = new wxFlexGridSizer(0, 6, 0, 0);
	StaticText5 = new wxStaticText(Panel1, ID_STATICTEXT5, _("Threads"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT5"));
	FlexGridSizer5->Add(StaticText5, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtThreads = new wxSpinCtrl(Panel1, ID_SPINCTRL1, _T("3"), wxDefaultPosition, wxSize(60, wxDefaultSize.y), 0, 1, 10, 3, _T("ID_SPINCTRL1"));
	FlexGridSizer5->Add(txtThreads, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer3->Add(FlexGridSizer5, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer2->Add(StaticBoxSizer3, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	Panel1->SetSizer(FlexGridSizer2);
	FlexGridSizer2->Fit(Panel1);
	FlexGridSizer2->SetSizeHints(Panel1);

	Panel4 = new wxPanel(Notebook1, ID_PANEL4, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL, _T("ID_PANEL4"));
	FlexGridSizer7 = new wxFlexGridSizer(0, 1, 0, 0);
	StaticBoxSizer2 = new wxStaticBoxSizer(wxVERTICAL, Panel4, _("Image Options"));
	FlexGridSizer8 = new wxFlexGridSizer(0, 4, 0, 0);
	chkScale = new wxCheckBox(Panel4, ID_CHECKBOX1, _("Scale Images with size >"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX1"));
	FlexGridSizer8->Add(chkScale, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtScaleW = new wxTextCtrl(Panel4, ID_TEXTCTRL8, wxEmptyString, wxDefaultPosition, wxSize(61,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL8"));
	FlexGridSizer8->Add(txtScaleW, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticText6 = new wxStaticText(Panel4, ID_STATICTEXT6, _T("X"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT6"));
	FlexGridSizer8->Add(StaticText6, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtScaleH = new wxTextCtrl(Panel4, ID_TEXTCTRL9, wxEmptyString, wxDefaultPosition, wxSize(59,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL9"));
	FlexGridSizer8->Add(txtScaleH, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer2->Add(FlexGridSizer8, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer9 = new wxFlexGridSizer(0, 3, 0, 0);
	chkQuality = new wxCheckBox(Panel4, ID_CHECKBOX2, _("Reduce quality of images >"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX2"));
	FlexGridSizer9->Add(chkQuality, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtQualitySize = new wxTextCtrl(Panel4, ID_TEXTCTRL10, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_TEXTCTRL10"));
	FlexGridSizer9->Add(txtQualitySize, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticText7 = new wxStaticText(Panel4, ID_STATICTEXT7, _T("KB"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT7"));
	FlexGridSizer9->Add(StaticText7, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer2->Add(FlexGridSizer9, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer10 = new wxFlexGridSizer(0, 3, 0, 0);
	StaticText8 = new wxStaticText(Panel4, ID_STATICTEXT8, _("Quality"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT8"));
	FlexGridSizer10->Add(StaticText8, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	sldQuality = new wxSlider(Panel4, ID_SLIDER4, 80, 0, 100, wxDefaultPosition, wxSize(182,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_SLIDER4"));
	FlexGridSizer10->Add(sldQuality, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	lblQuality = new wxStaticText(Panel4, ID_TEXTCTRL11, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0, _T("ID_TEXTCTRL11"));
	FlexGridSizer10->Add(lblQuality, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer2->Add(FlexGridSizer10, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer7->Add(StaticBoxSizer2, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	Panel4->SetSizer(FlexGridSizer7);
	FlexGridSizer7->Fit(Panel4);
	FlexGridSizer7->SetSizeHints(Panel4);

	Panel2 = new wxPanel(Notebook1, ID_PANEL2, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL, _T("ID_PANEL2"));
	FlexGridSizer14 = new wxFlexGridSizer(0, 1, 0, 0);
	StaticBoxSizer5 = new wxStaticBoxSizer(wxHORIZONTAL, Panel2, _("Image Filters"));
	FlexGridSizer6 = new wxFlexGridSizer(0, 3, 0, 0);
	chkHue = new wxCheckBox(Panel2, ID_CHECKBOX4, _("Hue"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX4"));
	FlexGridSizer6->Add(chkHue, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	sldHue = new wxSlider(Panel2, ID_SLIDER1, 0, -360, 360, wxDefaultPosition, wxSize(230,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_SLIDER1"));
	FlexGridSizer6->Add(sldHue, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	lblHue = new wxStaticText(Panel2, ID_TEXTCTRL5, _T("     "), wxDefaultPosition, wxDefaultSize, 0, _T("ID_TEXTCTRL5"));
	FlexGridSizer6->Add(lblHue, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	chkBlur = new wxCheckBox(Panel2, ID_CHECKBOX5, _("Blur"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX5"));
	FlexGridSizer6->Add(chkBlur, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	sldBlur = new wxSlider(Panel2, ID_SLIDER2, 0, 0, 100, wxDefaultPosition, wxSize(230,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_SLIDER2"));
	FlexGridSizer6->Add(sldBlur, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	lblBlur = new wxStaticText(Panel2, ID_TEXTCTRL6, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0, _T("ID_TEXTCTRL6"));
	FlexGridSizer6->Add(lblBlur, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	chkRotate = new wxCheckBox(Panel2, ID_CHECKBOX6, _("Rotate"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX6"));
	FlexGridSizer6->Add(chkRotate, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	sldRotate = new wxSlider(Panel2, ID_SLIDER3, 0, -360, 360, wxDefaultPosition, wxSize(230,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_SLIDER3"));
	FlexGridSizer6->Add(sldRotate, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	lblRotate = new wxStaticText(Panel2, ID_TEXTCTRL7, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0, _T("ID_TEXTCTRL7"));
	FlexGridSizer6->Add(lblRotate, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	StaticBoxSizer5->Add(FlexGridSizer6, 1, wxALL|wxALIGN_LEFT|wxALIGN_TOP, 5);
	FlexGridSizer14->Add(StaticBoxSizer5, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	Panel2->SetSizer(FlexGridSizer14);
	FlexGridSizer14->Fit(Panel2);
	FlexGridSizer14->SetSizeHints(Panel2);

	Panel3 = new wxPanel(Notebook1, ID_PANEL3, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL, _T("ID_PANEL3"));
	FlexGridSizer11 = new wxFlexGridSizer(0, 1, 0, 0);
	FlexGridSizer12 = new wxFlexGridSizer(0, 3, 0, 0);
	StaticText9 = new wxStaticText(Panel3, ID_STATICTEXT9, _("Display host address in URL as"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT9"));
	FlexGridSizer12->Add(StaticText9, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	cmbDisplayHost = new wxChoice(Panel3, ID_cmbDisplayHost, wxDefaultPosition, wxSize(157,wxDefaultSize.y), 0, 0, 0, wxDefaultValidator, _T("ID_cmbDisplayHost"));
	FlexGridSizer12->Add(cmbDisplayHost, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer11->Add(FlexGridSizer12, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer13 = new wxFlexGridSizer(0, 3, 0, 0);
	StaticText10 = new wxStaticText(Panel3, ID_STATICTEXT10, _("Blank Lines between URLs"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT10"));
	FlexGridSizer13->Add(StaticText10, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtBlankLines = new wxSpinCtrl(Panel3, ID_txtBlankLines, _T("1"), wxDefaultPosition, wxSize(60, wxDefaultSize.y), 0, 0, 10, 1, _T("ID_txtBlankLines"));
	FlexGridSizer13->Add(txtBlankLines, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer11->Add(FlexGridSizer13, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	chkFileUnsupportWarning = new wxCheckBox(Panel3, ID_CHECKBOX3, _("Warn me when file is too large or not supported"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX3"));
	FlexGridSizer11->Add(chkFileUnsupportWarning, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	chkClearPrevious = new wxCheckBox(Panel3, ID_CHECKBOX7, _("Clear previous text before uploading"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX7"));
	FlexGridSizer11->Add(chkClearPrevious, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	chkThumbnail = new wxCheckBox(Panel3, ID_CHECKBOX8, _("Show thumbnail in context menu"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX8"));
	FlexGridSizer11->Add(chkThumbnail, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
	Panel3->SetSizer(FlexGridSizer11);
	FlexGridSizer11->Fit(Panel3);
	FlexGridSizer11->SetSizeHints(Panel3);

	Notebook1->AddPage(Panel1, _("General"), false);
	Notebook1->AddPage(Panel4, _("Image Options"), false);
	Notebook1->AddPage(Panel2, _("Image Filters"), false);
	Notebook1->AddPage(Panel3, _("Miscellaneous"), false);
	FlexGridSizer1->Add(Notebook1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);

    #ifndef __WXMAC__
        StdDialogButtonSizer1 = new wxStdDialogButtonSizer();
        StdDialogButtonSizer1->AddButton(new wxButton(this, wxID_OK, _("OK")));
        StdDialogButtonSizer1->AddButton(new wxButton(this, wxID_CANCEL, _("Cancel")));
        StdDialogButtonSizer1->Realize();
        FlexGridSizer1->Add(StdDialogButtonSizer1, 1, wxALL|wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL, 5);
    #endif

	SetSizer(FlexGridSizer1);
	FlexGridSizer1->Fit(this);
	FlexGridSizer1->SetSizeHints(this);

	Center();
	//*)
}

ConfigDialog::~ConfigDialog()
{
	//(*Destroy(ConfigDialog)
	#ifdef __WXMAC__
        wxCommandEvent evt;
        SaveConfig(evt);
	#endif
	//*)
}


void ConfigDialog::OnInit(wxInitDialogEvent& event)
{
    wxCommandEvent ev;
    if(UploadHelperApp::Configurations(READ, _T("General"), _T("proxy"), false))
        RadioButton2->SetValue(true);
    else
        RadioButton1->SetValue(true);
    txtProxyAddr->SetValue(UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_addr"), wxEmptyString));
    txtProxyPort->SetValue(UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_port"), wxEmptyString));
    txtProxyUser->SetValue(UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_user"), wxEmptyString));
    txtProxyPwd->SetValue(UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_pwd"), wxEmptyString));
    OnRadioBtnClick(ev);
    txtThreads->SetValue(UploadHelperApp::Configurations(READ, _T("General"), _T("threads"), 3));

    wxScrollEvent evt;
    chkScale->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("scale"), true));
    txtScaleW->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("scale_w"), _T("1024")));
    txtScaleH->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("scale_h"), _T("768")));
    OnchkScaleClick(ev);
    chkQuality->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("quality"), true));
    txtQualitySize->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("quality_size"), _T("1024")));
    sldQuality->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("quality_value"), 80));
    OnsldQualityScroll(evt);
    OnchkQualityClick(ev);

    chkHue->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("hue"), false));
    sldHue->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("hue_value"), 0));
    OnsldHueScroll(evt);
    OnchkHueClick(ev);
    chkBlur->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("blur"), false));
    sldBlur->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("blur_value"), 0));
    OnsldBlurScroll(evt);
    OnchkBlurClick(ev);
    chkRotate->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("rotate"), false));
    sldRotate->SetValue(UploadHelperApp::Configurations(READ, _T("Image"), _T("rotate_value"), 0));
    OnsldRotateScroll(evt);
    OnchkRotateClick(ev);

    for(int i=0; i<sizeof(BBS_URLS)/sizeof(BBS_URLS[0]); i++)
        cmbDisplayHost->AppendString(BBS_URLS[i]);
    cmbDisplayHost->SetSelection(UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("display_host"), 0));
    txtBlankLines->SetValue(UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("blank_lines"), 1));
    chkFileUnsupportWarning->SetValue(UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("file_unsupport_warning"), true));
    chkClearPrevious->SetValue(UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("clear_previous"), false));
    chkThumbnail->SetValue(UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("context_menu_thumbnail"), true));
}

void ConfigDialog::OnsldHueScroll(wxScrollEvent& event)
{
    lblHue->SetLabel(wxString::Format(_T("%4.2f"), sldHue->GetValue()/360.0));
}

void ConfigDialog::OnsldBlurScroll(wxScrollEvent& event)
{
    lblBlur->SetLabel(wxString::Format(_T("%d"), sldBlur->GetValue()));
}

void ConfigDialog::OnsldRotateScroll(wxScrollEvent& event)
{
    lblRotate->SetLabel(wxString::Format(_T("%d"), sldRotate->GetValue()));
}

void ConfigDialog::OnsldQualityScroll(wxScrollEvent& event)
{
    lblQuality->SetLabel(wxString::Format(_T("%d"), sldQuality->GetValue()));
}

void ConfigDialog::OnRadioBtnClick(wxCommandEvent& event)
{
    bool flag=RadioButton2->GetValue();
    txtProxyAddr->Enable(flag);
    txtProxyPort->Enable(flag);
    txtProxyUser->Enable(flag);
    txtProxyPwd->Enable(flag);
}

void ConfigDialog::OnchkScaleClick(wxCommandEvent& event)
{
    bool flag=chkScale->GetValue();
    txtScaleW->Enable(flag);
    txtScaleH->Enable(flag);
}

void ConfigDialog::OnchkQualityClick(wxCommandEvent& event)
{
    bool flag=chkQuality->GetValue();
    txtQualitySize->Enable(flag);
    sldQuality->Enable(flag);
}

void ConfigDialog::OnchkHueClick(wxCommandEvent& event)
{
    sldHue->Enable(chkHue->GetValue());
}

void ConfigDialog::OnchkBlurClick(wxCommandEvent& event)
{
    sldBlur->Enable(chkBlur->GetValue());
}

void ConfigDialog::OnchkRotateClick(wxCommandEvent& event)
{
    sldRotate->Enable(chkRotate->GetValue());
}

void ConfigDialog::SaveConfig(wxCommandEvent& event)
{
    if(RadioButton1->GetValue())
        UploadHelperApp::Configurations(WRITE, _T("General"), _T("proxy"), false);
    else
        UploadHelperApp::Configurations(WRITE, _T("General"), _T("proxy"), true);
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("proxy_addr"), txtProxyAddr->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("proxy_port"), txtProxyPort->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("proxy_user"), txtProxyUser->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("proxy_pwd"), txtProxyPwd->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("threads"), txtThreads->GetValue());

    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("scale"), chkScale->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("scale_w"), txtScaleW->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("scale_h"), txtScaleH->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("quality"), chkQuality->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("quality_size"), txtQualitySize->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("quality_value"), sldQuality->GetValue());

    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("hue"), chkHue->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("hue_value"), sldHue->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("blur"), chkBlur->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("blur_value"), sldBlur->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("rotate"), chkRotate->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Image"), _T("rotate_value"), sldRotate->GetValue());

    UploadHelperApp::Configurations(WRITE, _T("Miscellaneous"), _T("display_host"), cmbDisplayHost->GetSelection());
    UploadHelperApp::Configurations(WRITE, _T("Miscellaneous"), _T("blank_lines"), txtBlankLines->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Miscellaneous"), _T("file_unsupport_warning"), chkFileUnsupportWarning->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Miscellaneous"), _T("clear_previous"), chkClearPrevious->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("Miscellaneous"), _T("context_menu_thumbnail"), chkThumbnail->GetValue());

    Close();
}

void ConfigDialog::OnClose(wxCloseEvent& event)
{
    Destroy();
}
