#include "UploadHelperApp.h"

//(*IdInit(MainFrame)
#define ID_COMBOBOX_ZONE    1000
#define ID_COMBOBOX_BOARD   1001
#define ID_CHECKBOX_LOCK    1002
#define ID_BUTTON_BROWSE    1003
#define ID_BUTTON_REMOVE    1004
#define ID_BUTTON_UPLOAD    1005
#define ID_BUTTON_SEND    1006
#define ID_MENU_LOGIN    1007
#define ID_MENU_LOGOFF    1008
#define ID_MENU_ALWAYS_TOP    1009
#define ID_MENU_FAQ    1010
#define ID_MENU_HOMEPAGE    1011
#define ID_MENU_UPDATE    1012
#define ID_MENU_SIZE 1013
#define ID_MENU_MODIFIED 1014
#define ID_MENU_CREATED 1015
#define ID_MENU_ACCESSED 1016
#define ID_MENU_FTERM   1017
#define ID_MENU_CTERM   1018

const long MainFrame::ID_STATICTEXT1 = wxNewId();
const long MainFrame::ID_COMBOBOX1 = wxNewId();
const long MainFrame::ID_COMBOBOX2 = wxNewId();
const long MainFrame::ID_CHECKBOX1 = wxNewId();
const long MainFrame::ID_STATICTEXT2 = wxNewId();
const long MainFrame::ID_BUTTON1 = wxNewId();
const long MainFrame::ID_BUTTON3 = wxNewId();
const long MainFrame::ID_BUTTON4 = wxNewId();
const long MainFrame::ID_PANEL1 = wxNewId();
const long MainFrame::ID_STATICTEXT3 = wxNewId();
const long MainFrame::ID_TEXTCTRL1 = wxNewId();
const long MainFrame::ID_STATICTEXT4 = wxNewId();
const long MainFrame::ID_STATICTEXT5 = wxNewId();
const long MainFrame::ID_CHOICE3 = wxNewId();
const long MainFrame::ID_TEXTCTRL2 = wxNewId();
const long MainFrame::ID_TEXTCTRL3 = wxNewId();
const long MainFrame::ID_BUTTON2 = wxNewId();
const long MainFrame::ID_PANEL2 = wxNewId();
const long MainFrame::ID_NOTEBOOK1 = wxNewId();
const long MainFrame::ID_MENUITEM1 = wxNewId();
const long MainFrame::ID_MENUITEM2 = wxNewId();
const long MainFrame::ID_MENUITEM9 = wxNewId();
const long MainFrame::ID_MENUITEM10 = wxNewId();
const long MainFrame::ID_MENUITEM12 = wxNewId();
const long MainFrame::ID_MENUITEM13 = wxNewId();
const long MainFrame::ID_MENUITEM14 = wxNewId();
const long MainFrame::ID_MENUITEM15 = wxNewId();
const long MainFrame::ID_MENUITEM11 = wxNewId();
const long MainFrame::ID_MENUITEM3 = wxNewId();
const long MainFrame::ID_MENUITEM4 = wxNewId();
const long MainFrame::ID_MENUITEM5 = wxNewId();
const long MainFrame::ID_MENUITEM6 = wxNewId();
const long MainFrame::ID_MENUITEM7 = wxNewId();
//*)

const wxEventType wxEVT_NEW_RELEASE = wxNewEventType();
#define wxEVT_NEW_RELEASE(id, fn) \
    DECLARE_EVENT_TABLE_ENTRY( \
        wxEVT_NEW_RELEASE, id, wxID_ANY, \
        (wxObjectEventFunction)(wxEventFunction) wxStaticCastEvent( wxCommandEventFunction, &fn ), \
        (wxObject *) NULL \
    ),

BEGIN_EVENT_TABLE(MainFrame,wxFrame)
    //(*EventTable(MainFrame)
    EVT_COMBOBOX(ID_COMBOBOX_ZONE, MainFrame::OncmbZoneSelect)
    EVT_COMBOBOX(ID_COMBOBOX_BOARD, MainFrame::OncmbBoardSelect)
    EVT_CHECKBOX(ID_CHECKBOX_LOCK, MainFrame::OnchkLockClick)
    EVT_BUTTON(ID_BUTTON_BROWSE, MainFrame::OnbtnBrowseClick)
    EVT_BUTTON(ID_BUTTON_REMOVE, MainFrame::OnbtnRemoveClick)
    EVT_BUTTON(ID_BUTTON_UPLOAD, MainFrame::OnbtnUploadClick)
    EVT_BUTTON(ID_BUTTON_SEND, MainFrame::OnbtnSendClick)
    EVT_MENU(ID_MENU_LOGIN, MainFrame::OnmnuLoginSelected)
    EVT_MENU(ID_MENU_LOGOFF, MainFrame::OnmnuLogoffSelected)
    EVT_MENU(wxID_PREFERENCES, MainFrame::OnmnuPreferenceSelected)
    EVT_MENU(ID_MENU_ALWAYS_TOP, MainFrame::OnmnuAlwaysTopSelected)
    EVT_MENU(ID_MENU_FAQ, MainFrame::OnmnuFAQSelected)
    EVT_MENU(ID_MENU_HOMEPAGE, MainFrame::OnmnuHomepageSelected)
    EVT_MENU(ID_MENU_UPDATE, MainFrame::OnmnuUpdateSelected)
    EVT_MENU(wxID_ABOUT, MainFrame::OnmnuAboutSelected)
    EVT_MENU(ID_MENU_SIZE, MainFrame::OnmnuSizeSelected)
    EVT_MENU(ID_MENU_MODIFIED, MainFrame::OnmnuModifiedSelected)
    EVT_MENU(ID_MENU_CREATED, MainFrame::OnmnuCreatedSelected)
    EVT_MENU(ID_MENU_ACCESSED, MainFrame::OnmnuAccessedSelected)
    EVT_MENU(ID_MENU_FTERM, MainFrame::OnmnuFtermSelected)
    EVT_MENU(ID_MENU_CTERM, MainFrame::OnmnuCtermSelected)
    EVT_MENU(REVSEL, MainFrame::OnmnuRemoveSelectedSelected)
    EVT_MENU(REVALL, MainFrame::OnmnuRemoveAllSelected)
    EVT_MENU(REVDUP, MainFrame::OnmnuRemoveDupSelected)
    EVT_MENU(REVINV, MainFrame::OnmnuRemoveInvalidSelected)
    wxEVT_NEW_RELEASE(wxID_ANY, MainFrame::OnNewRelease)
    //*)
END_EVENT_TABLE()

MainFrame::MainFrame(wxWindow* parent,wxWindowID id)
{
    //(*Initialize(MainFrame)
    wxFlexGridSizer* FlexGridSizer4;
    wxFlexGridSizer* FlexGridSizer3;
    wxFlexGridSizer* FlexGridSizer5;
    wxFlexGridSizer* FlexGridSizer2;
    wxFlexGridSizer* FlexGridSizer6;
    wxFlexGridSizer* FlexGridSizer7;
    wxFlexGridSizer* FlexGridSizer1;

    Create(parent, wxID_ANY, APP_NAME + SPACE_STRING + APP_VERSION, wxDefaultPosition, wxDefaultSize, wxCAPTION|wxSYSTEM_MENU|wxCLOSE_BOX|wxMINIMIZE_BOX|wxTAB_TRAVERSAL|wxWANTS_CHARS);
    SetClientSize(wxSize(603,500));
    SetIcon(wxICON(logo));

    tbMain = new wxNotebook(this, ID_NOTEBOOK1, wxDefaultPosition, wxDefaultSize, 0, _T("ID_NOTEBOOK1"));
    Panel1 = new wxPanel(tbMain, ID_PANEL1, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL, _T("ID_PANEL1"));
    FlexGridSizer1 = new wxFlexGridSizer(3, 1, 0, 0);
    FlexGridSizer2 = new wxFlexGridSizer(1, 4, 0, 0);
    StaticText1 = new wxStaticText(Panel1, ID_STATICTEXT1, _("Destination"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT1"));
    FlexGridSizer2->Add(StaticText1, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    cmbZone = new wxComboBox(Panel1, ID_COMBOBOX_ZONE, wxEmptyString, wxDefaultPosition, wxSize(138,wxDefaultSize.y), 0, 0, wxCB_READONLY|wxCB_DROPDOWN, wxDefaultValidator, _T("ID_COMBOBOX1"));
    FlexGridSizer2->Add(cmbZone, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    cmbBoard = new wxComboBox(Panel1, ID_COMBOBOX_BOARD, wxEmptyString, wxDefaultPosition, wxSize(257,wxDefaultSize.y), 0, 0, wxCB_READONLY|wxCB_DROPDOWN, wxDefaultValidator, _T("ID_COMBOBOX2"));
    FlexGridSizer2->Add(cmbBoard, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    chkLock = new wxCheckBox(Panel1, ID_CHECKBOX_LOCK, _("Loc&k"), wxDefaultPosition, wxDefaultSize, 0, wxDefaultValidator, _T("ID_CHECKBOX1"));
    FlexGridSizer2->Add(chkLock, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer1->Add(FlexGridSizer2, 1, wxLEFT|wxRIGHT|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 2);
    FlexGridSizer3 = new wxFlexGridSizer(1, 4, 0, 0);
    StaticText2 = new wxStaticText(Panel1, wxNewId(), _("Select File(s) to Upload"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT2"));
    FlexGridSizer3->Add(StaticText2, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    btnBrowse = new wxButton(Panel1, ID_BUTTON_BROWSE, _("&Browse..."), wxDefaultPosition, wxSize(160,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_BUTTON1"));
    FlexGridSizer3->Add(btnBrowse, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer3->Add(44,20,1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	btnRemove = new wxButton(Panel1, ID_BUTTON_REMOVE, _("&Remove..."), wxDefaultPosition, wxSize(160,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_BUTTON4"));
	FlexGridSizer3->Add(btnRemove, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer1->Add(FlexGridSizer3, 1, wxBOTTOM|wxLEFT|wxRIGHT|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 2);
    FlexGridSizer4 = new wxFlexGridSizer(0, 3, 0, 0);
    lstUpFile = new mListCtrl(Panel1, LISTCTRL_UPFILE, wxDefaultPosition, wxSize(584,290), wxLC_REPORT, wxDefaultValidator, _T("ID_LISTCTRL1"));
    FlexGridSizer4->Add(lstUpFile, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer1->Add(FlexGridSizer4, 1, wxLEFT|wxRIGHT|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 2);
    btnUpload = new wxButton(Panel1, ID_BUTTON_UPLOAD, _("&Upload Now"), wxDefaultPosition, wxSize(180,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_BUTTON3"));
    FlexGridSizer1->Add(btnUpload, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    Panel1->SetSizer(FlexGridSizer1);
    FlexGridSizer1->Fit(Panel1);
    FlexGridSizer1->SetSizeHints(Panel1);
    Panel2 = new wxPanel(tbMain, wxNewId(), wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL, _T("ID_PANEL2"));
    FlexGridSizer5 = new wxFlexGridSizer(3, 1, 0, 0);
    FlexGridSizer6 = new wxFlexGridSizer(1, 4, 0, 0);
    StaticText3 = new wxStaticText(Panel2, wxNewId(), _("Title"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT3"));
    FlexGridSizer6->Add(StaticText3, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    txtTitle = new wxTextCtrl(Panel2, wxNewId(), wxEmptyString, wxDefaultPosition, wxSize(330,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL1"));
    FlexGridSizer6->Add(txtTitle, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    StaticText4 = new wxStaticText(Panel2, wxNewId(), _("Signature"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT4"));
    FlexGridSizer6->Add(StaticText4, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    cmbSign = new wxChoice(Panel2, wxNewId(), wxDefaultPosition, wxSize(71,wxDefaultSize.y), 0, 0, 0, wxDefaultValidator, _T("ID_CHOICE3"));
    for(int i=0; i<=9; i++)
    {
        cmbSign->Append(wxString::Format(_T("%d"), i));
    }
    cmbSign->SetSelection(1);
    FlexGridSizer6->Add(cmbSign, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer5->Add(FlexGridSizer6, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
    txtContent = new wxTextCtrl(Panel2, wxNewId(), wxEmptyString, wxDefaultPosition, wxSize(588,270), wxTE_MULTILINE|wxVSCROLL, wxDefaultValidator, _T("ID_TEXTCTRL2"));
    FlexGridSizer5->Add(txtContent, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
    FlexGridSizer7 = new wxFlexGridSizer(0, 3, 0, 0);
	StaticText5 = new wxStaticText(Panel2, wxNewId(), _("Target board (English name)"), wxDefaultPosition, wxDefaultSize, 0, _T("ID_STATICTEXT5"));
	FlexGridSizer7->Add(StaticText5, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	txtSendBoard = new wxTextCtrl(Panel2, wxNewId(), wxEmptyString, wxDefaultPosition, wxSize(183,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_TEXTCTRL3"));
	FlexGridSizer7->Add(txtSendBoard, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
	FlexGridSizer5->Add(FlexGridSizer7, 1, wxALL|wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL, 5);
    btnSend = new wxButton(Panel2, ID_BUTTON_SEND, _("S&end"), wxDefaultPosition, wxSize(180,wxDefaultSize.y), 0, wxDefaultValidator, _T("ID_BUTTON2"));
    FlexGridSizer5->Add(btnSend, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5);
    Panel2->SetSizer(FlexGridSizer5);
    FlexGridSizer5->Fit(Panel2);
    FlexGridSizer5->SetSizeHints(Panel2);
    tbMain->AddPage(Panel1, _("Upload Files"), true);
    tbMain->AddPage(Panel2, _("Post Article"), false);

    MenuBar1 = new wxMenuBar();
    Menu1 = new wxMenu();
    mnuLogin = new wxMenuItem(Menu1, ID_MENU_LOGIN, _("S&witch User...\tF12"), wxEmptyString, wxITEM_NORMAL);
    mnuLogin->SetBitmap(wxBitmap(login16));
    Menu1->Append(mnuLogin);
    Menu1->AppendSeparator();
    mnuLogoff = new wxMenuItem(Menu1, ID_MENU_LOGOFF, _("Lo&g Off...\tShift-F12"), wxEmptyString, wxITEM_NORMAL);
    mnuLogoff->SetBitmap(wxBitmap(logoff16));
    Menu1->Append(mnuLogoff);
    MenuBar1->Append(Menu1, _("&Login"));
    Menu2 = new wxMenu();
    MenuItem3 = new wxMenuItem(Menu2, wxID_PREFERENCES, _("&Preferences...\tF8"), wxEmptyString, wxITEM_NORMAL);
    MenuItem3->SetBitmap(wxBitmap(wxImage(set16)));
    Menu2->Append(MenuItem3);
    Menu2->AppendSeparator();
    mnuFileInfo = new wxMenu();
	mnuSize = new wxMenuItem(mnuFileInfo, ID_MENU_SIZE, _("Size"), wxEmptyString, wxITEM_CHECK);
	mnuFileInfo->Append(mnuSize);
	mnuMod = new wxMenuItem(mnuFileInfo, ID_MENU_MODIFIED, _("Modified"), wxEmptyString, wxITEM_CHECK);
	mnuFileInfo->Append(mnuMod);
	mnuCre = new wxMenuItem(mnuFileInfo, ID_MENU_CREATED, _("Created"), wxEmptyString, wxITEM_CHECK);
	mnuFileInfo->Append(mnuCre);
    mnuAcc = new wxMenuItem(mnuFileInfo, ID_MENU_ACCESSED, _("Accessed"), wxEmptyString, wxITEM_CHECK);
	mnuFileInfo->Append(mnuAcc);
	Menu2->Append(wxNewId(), _("F&ile Attributes"), mnuFileInfo, wxEmptyString);
    #ifdef __WXMSW__
        mnuTerm = new wxMenu();
        mnuFterm = new wxMenuItem(mnuTerm, ID_MENU_FTERM, _T("FTerm"), wxEmptyString);
        mnuFterm->SetBitmap(wxBitmap(star_xpm));
        mnuTerm->Append(mnuFterm);
        mnuCterm = new wxMenuItem(mnuTerm, ID_MENU_CTERM, _T("CTerm"), wxEmptyString);
        mnuCterm->SetBitmap(wxBitmap(star2_xpm));
        mnuTerm->Append(mnuCterm);
        Menu2->Append(wxNewId(), _("Integrate to &Term"), mnuTerm, wxEmptyString);
	#endif
    #ifndef __WXMAC__
        Menu2->AppendSeparator();
        mnuAlwaysTop = new wxMenuItem(Menu2, ID_MENU_ALWAYS_TOP, _("Alwa&ys on Top"), wxEmptyString, wxITEM_CHECK);
        Menu2->Append(mnuAlwaysTop);
    #endif
    MenuBar1->Append(Menu2, _("&Settings"));
    Menu3 = new wxMenu();
    mnuFAQ = new wxMenuItem(Menu3, ID_MENU_FAQ, _("&Frequently Asked Questions\tF1"), wxEmptyString, wxITEM_NORMAL);
    mnuFAQ->SetBitmap(wxBitmap(help16));
    Menu3->Append(mnuFAQ);
    Menu3->AppendSeparator();
    mnuHomepage = new wxMenuItem(Menu3, ID_MENU_HOMEPAGE, _("&Homepage"), wxEmptyString, wxITEM_NORMAL);
    mnuHomepage->SetBitmap(wxBitmap(home16));
    Menu3->Append(mnuHomepage);
    mnuUpdate = new wxMenuItem(Menu3, ID_MENU_UPDATE, _("&Check for Updates..."), wxEmptyString, wxITEM_NORMAL);
    mnuUpdate->SetBitmap(wxBitmap(update16));
    Menu3->Append(mnuUpdate);
    #ifndef __WXMAC__
        Menu3->AppendSeparator();
    #endif
    mnuAbout = new wxMenuItem(Menu3, wxID_ABOUT, _("&About..."), wxEmptyString, wxITEM_NORMAL);
    mnuAbout->SetBitmap(wxIcon(logo16_xpm));
    Menu3->Append(mnuAbout);
    MenuBar1->Append(Menu3, _("&Help"));
    SetMenuBar(MenuBar1);

    SetSize(wxSize(GetSize().x, btnUpload->GetPosition().y + 120));
    Center();

    wxImageList *imgs=new wxImageList(16,16);
    tbMain->SetImageList(imgs);
    tbMain->SetPageImage(0,imgs->Add(wxBitmap(upload_xpm)));
    tbMain->SetPageImage(1,imgs->Add(wxBitmap(post_xpm)));
    imgs->Add(wxBitmap(status_ok_xpm));
    imgs->Add(wxBitmap(status_fail_xpm));
    imgs->Add(wxBitmap(status_uploading_xpm));
    lstUpFile->SetImageList(imgs, wxIMAGE_LIST_SMALL);
    lstUpFile->SetDropTarget(new DnDFile(lstUpFile));
    //*)

    //Read configuration
    wxGetApp().ReadUserInfo();

    //CREATE TASKBARICON
    //this->active = TRUE;
    taskbaricon = new mTaskBarIcon(this);
    //if (!(wxGetApp().parameters->Found(_T("notray"))))
    #ifndef __WXMAC__
        taskbaricon->SetIcon(wxIcon(logo16_xpm), APP_NAME);
    #endif
    taskbaricon->restoring = FALSE;

    //Set the header line of FileList
    const wxString UPFILE_LIST_LABEL[] = {
        wxEmptyString,
        _("Filename"),
        _("Size"),
        _("Modified"),
        _("Created"),
        _("Accessed"),
        _("Status")
    };
    int UPFILE_LIST_WIDTH[7];
    wxString tmp=UploadHelperApp::Configurations(READ, _T("General"), _T("listctrl_width"), _T("40, 310, 80, 0, 0, 0, 130"));
    if(!tmp.IsEmpty())
    {
        wxStringTokenizer tkz(tmp, _T(","));
        int num = 0;
        long token;
        while ( tkz.HasMoreTokens() )
        {
            if(!tkz.GetNextToken().ToLong(&token))
                token = 0;
            if(num>=2 && num<6 && token > 0)
            {
                wxMenuItemList list = mnuFileInfo->GetMenuItems();
                wxwxMenuItemListNode *node = list.Item(num-2);
                wxMenuItem *item = (wxMenuItem *)node->GetData();
                item->Check();
            }
            UPFILE_LIST_WIDTH[num] = token;
            num++;
        }
    }
    lstUpFile->InsertColumn(0,
                            UPFILE_LIST_LABEL[0],
                            wxLIST_FORMAT_CENTER,
                            UPFILE_LIST_WIDTH[0]);
    for (int i=1; i<sizeof(UPFILE_LIST_LABEL)/sizeof(UPFILE_LIST_LABEL[0]); i++)
        lstUpFile->InsertColumn(i,
                                UPFILE_LIST_LABEL[i],
                                wxLIST_FORMAT_LEFT,
                                UPFILE_LIST_WIDTH[i]);

    //lstUpFile->SetColumnWidth(3, 50);

    //Read Zones and Boards
    wxXmlDocument doc;
    int num=0;
    if (!doc.Load(PATH_BOARD_LIST))
    {
        wxMessageBox(ERR_READ_BOARD_LIST);
        return;
    }
    wxXmlNode *child = doc.GetRoot()->GetChildren();
    while (child)
    {
        if (child->GetName() == _T("Zone"))
        {
            if(num<10)
                cmbZone->AppendString(wxString::Format(_T("%d) "),num) + child->GetPropVal(_T("name"),_T("default")));
            else
                cmbZone->AppendString(wxString::Format(_T("%c) "),num+55) + child->GetPropVal(_T("name"),_T("default")));
        }
        num++;
        child = child->GetNext();
    }
    cmbZone->SetSelection(UploadHelperApp::Configurations(READ, _T("General"), _T("zone"), DEFAULT_ZONE));
    wxCommandEvent evt;
    OncmbZoneSelect(evt);
    cmbBoard->SetSelection(UploadHelperApp::Configurations(READ, _T("General"), _T("board"), DEFAULT_BOARD));
    OncmbBoardSelect(evt);
    chkLock->SetValue(UploadHelperApp::Configurations(READ, _T("General"), _T("lock"), false));
    OnchkLockClick(evt);
    wxString send_board=UploadHelperApp::Configurations(READ, _T("General"), _T("post_board"), wxEmptyString);
    if(!send_board.IsEmpty())
        txtSendBoard->SetValue(send_board);

    //If no user info found(e.g. uninitialized), show login dialog
    if (wxGetApp().progOptions.user_id.IsEmpty())
    {
        LoginDialog* dlg = new LoginDialog(this);
        dlg->ShowModal();
    }
}

MainFrame::~MainFrame()
{
    //(*Destroy(MainFrame)
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("zone"), cmbZone->GetSelection());
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("board"), cmbBoard->GetSelection());
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("lock"), chkLock->GetValue());
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("post_board"), txtSendBoard->GetValue());
    wxString tmp;
    for(int i=0; i<7; i++)
        tmp+=_T(",")+wxString::Format(_T("%d"), lstUpFile->GetColumnWidth(i));
    UploadHelperApp::Configurations(WRITE, _T("General"), _T("listctrl_width"), tmp.AfterFirst(','));
    delete taskbaricon;
    //*)
}

void MainFrame::OnmnuAboutSelected(wxCommandEvent& event)
{
    AboutDialog* dlg = new AboutDialog(this);
    dlg->ShowModal();
}

void MainFrame::OnmnuLoginSelected(wxCommandEvent& event)
{
    LoginDialog* dlg = new LoginDialog(this);
    dlg->ShowModal();
}

void MainFrame::OnmnuPreferenceSelected(wxCommandEvent& event)
{
    ConfigDialog* dlg = new ConfigDialog(this);
    dlg->ShowModal();
}

void MainFrame::OnmnuSizeSelected(wxCommandEvent& event)
{
    int w=mnuSize->IsChecked() ? 80 : 0;
    lstUpFile->SetColumnWidth(2, w);
}

void MainFrame::OnmnuModifiedSelected(wxCommandEvent& event)
{
    int w=mnuMod->IsChecked() ? 80 : 0;
    lstUpFile->SetColumnWidth(3, w);
}

void MainFrame::OnmnuCreatedSelected(wxCommandEvent& event)
{
    int w=mnuCre->IsChecked() ? 80 : 0;
    lstUpFile->SetColumnWidth(4, w);
}

void MainFrame::OnmnuAccessedSelected(wxCommandEvent& event)
{
    int w=mnuAcc->IsChecked() ? 80 : 0;
    lstUpFile->SetColumnWidth(5, w);
}

void MainFrame::OnchkLockClick(wxCommandEvent& event)
{
    cmbZone->Enable(!chkLock->GetValue());
    cmbBoard->Enable(!chkLock->GetValue());
}

void MainFrame::OnmnuAlwaysTopSelected(wxCommandEvent& event)
{
    if(mnuAlwaysTop->IsChecked())
        SetWindowStyleFlag(GetWindowStyleFlag() | wxSTAY_ON_TOP);
    else
        SetWindowStyleFlag(GetWindowStyleFlag() & ~wxSTAY_ON_TOP);
}

void MainFrame::OnmnuLogoffSelected(wxCommandEvent& event)
{
    wxGetApp().ReadUserInfo();
    if(UploadHelperApp::PerfectConnect(wxGetApp().progOptions.bbs_url+_T("bbslogout")))
    {
        UploadHelperApp::Configurations(WRITE, _T("Login"), _T("user_id"), wxEmptyString);
        UploadHelperApp::Configurations(WRITE, _T("Login"), _T("user_password"), wxEmptyString);
        UploadHelperApp::Configurations(WRITE, _T("Login"), _T("user_cookie"), wxEmptyString);
        wxMessageBox(_("Logged off successfully."));
    }
    else
        return;
}

void MainFrame::OncmbZoneSelect(wxCommandEvent& event)
{
    wxXmlDocument doc;
    if (!doc.Load(PATH_BOARD_LIST))
    {
        wxMessageBox(ERR_READ_BOARD_LIST);
        return;
    }
    int idx=cmbBoard->GetSelection();
    cmbBoard->Clear();
    cmbBoard->SetValue(wxEmptyString);
    wxXmlNode *child = doc.GetRoot()->GetChildren();
    while (child)
    {
        if ((child->GetName() == _T("Zone")) && cmbZone->GetValue().find(child->GetPropVal(_T("name"),_T("default")))<8 )
        {
            wxXmlNode *subChild = child->GetChildren();
            while (subChild)
            {
                if (1)
                {
                    cmbBoard->AppendString(
                        subChild->GetName()
                        + _T(" (")
                        + subChild->GetPropVal(_T("name"),_T("default"))
                        + _T(")")
                    );
                }
                subChild = subChild->GetNext();
            }
            break;
        }
        child = child->GetNext();
    }
    if (idx>=cmbBoard->GetCount())
        idx=cmbBoard->GetCount()-1;
    if(idx>=0){
        cmbBoard->SetSelection(idx);
        OncmbBoardSelect(event);
    }
}

void MainFrame::OncmbBoardSelect(wxCommandEvent& event)
{
    txtSendBoard->SetValue(MyUtilFunc::GetBoard(cmbBoard->GetValue()));
}

void MainFrame::OnbtnBrowseClick(wxCommandEvent& event)
{
    wxFileDialog* fileDlg = new wxFileDialog(this, _("Select File(s) to Upload"), wxEmptyString, wxEmptyString, OPEN_DIALOG_FILTER, wxFD_DEFAULT_STYLE|wxFD_OPEN|wxFD_FILE_MUST_EXIST|wxFD_MULTIPLE|wxFD_CHANGE_DIR|wxFD_PREVIEW|wxTAB_TRAVERSAL|wxWANTS_CHARS, wxDefaultPosition, wxDefaultSize, _T("wxFileDialog"));
    if (fileDlg->ShowModal() != wxID_OK)
        return;
    wxArrayString paths;
    fileDlg->GetPaths(paths);
    lstUpFile->AddFileItem(paths);
    delete fileDlg;
}

void MainFrame::OnbtnRemoveClick(wxCommandEvent& event)
{
    wxMenu *removemenu = new wxMenu;
    wxMenuItem *mnuRemoveSelected=new wxMenuItem(removemenu,REVSEL, _("Selected\tDel"));
    mnuRemoveSelected->SetBitmap(wxBitmap(delete_xpm));
    removemenu->Append(mnuRemoveSelected);
    wxMenuItem *mnuRemoveAll=new wxMenuItem(removemenu,REVALL, _("All\tShift+Del"));
    mnuRemoveAll->SetBitmap(wxBitmap(delete_xpm));
    removemenu->Append(mnuRemoveAll);
    removemenu->AppendSeparator();
    wxMenuItem *mnuRemoveDup=new wxMenuItem(removemenu,REVDUP, _("Duplicates"));
    mnuRemoveDup->SetBitmap(wxBitmap(delete_xpm));
    removemenu->Append(mnuRemoveDup);
    wxMenuItem *mnuRemoveInvalid=new wxMenuItem(removemenu,REVINV, _("Invalid"));
    mnuRemoveInvalid->SetBitmap(wxBitmap(delete_xpm));
    removemenu->Append(mnuRemoveInvalid);
    #ifdef __WXMAC__
        int coorY=btnRemove->GetPosition().y+btnRemove->GetSize().y+Panel1->GetPosition().y+20;
    #else
        int coorY=btnRemove->GetPosition().y+btnRemove->GetSize().y+Panel1->GetPosition().y;
    #endif
    PopupMenu(removemenu, btnRemove->GetPosition().x, coorY);
}

void MainFrame::OnbtnSendClick(wxCommandEvent& event)
{
    //Post Article
    if(txtTitle->GetValue().IsEmpty() || txtContent->GetValue().IsEmpty() || txtSendBoard->GetValue().IsEmpty())
    {
        wxMessageBox(ERR_NO_BLANKS);
        return;
    }
    wxGetApp().ReadUserInfo();

    wxString strTitle=txtTitle->GetValue();
    //For MacOSX 10.4u.SDK compatibility issues, use "curl_escape" instead of the newer form "curl_easy_escape"
    wxString strTitleEsc(curl_escape(MyUtilFunc::WX2pChar(strTitle, BBS_CODEPAGE), 0), wxCSConv(BBS_CODEPAGE));

    wxString strContent=txtContent->GetValue();
    wxString strContentEsc(curl_escape(MyUtilFunc::WX2pChar(strContent, BBS_CODEPAGE), 0), wxCSConv(BBS_CODEPAGE));

    wxString strPost=_T("board=")+txtSendBoard->GetValue()
                     +_T("&replymode=2")
                     +_T("&title=")+strTitleEsc
                     +_T("&signature=")+cmbSign->GetString(cmbSign->GetSelection())
                     +_T("&text=")+strContentEsc;

    if(UploadHelperApp::PerfectConnect(wxGetApp().progOptions.bbs_url+_T("bbssnd"), strPost))
    {
        txtContent->Clear();
        wxMessageBox(OK_POST);
        OnmnuRemoveAllSelected(event);
    }
}

void MainFrame::OnbtnUploadClick(wxCommandEvent& event)
{
    if(lstUpFile->GetItemCount()<=0)
        return;
    if(UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("clear_previous"), false))
        txtContent->Clear();

    //Start to upload files
    wxGetApp().ReadUserInfo();
    if(!UploadHelperApp::PerfectConnect(wxGetApp().progOptions.bbs_url+_T("bbspreupload"), _T("board=PIC")))
        return;

    wxString strBoard = MyUtilFunc::GetBoard(cmbBoard->GetValue());
    txtContent->SetValue(txtContent->GetValue() + lstUpFile->UploadFiles(strBoard));

    tbMain->SetSelection(1);
    if(wxFileName::DirExists(TEMP_DIR))
        try
        {
            wxFileName::Rmdir(TEMP_DIR);
        }
        catch(...)
        {
            ;
        }
}

void MainFrame::OnmnuFAQSelected(wxCommandEvent& event)
{
    wxLaunchDefaultBrowser(APP_HOMEPAGE + _T("/faq.htm"), wxBROWSER_NEW_WINDOW);
}

void MainFrame::OnmnuHomepageSelected(wxCommandEvent& event)
{
    wxLaunchDefaultBrowser(APP_HOMEPAGE, wxBROWSER_NEW_WINDOW);
}

void MainFrame::OnmnuFtermSelected(wxCommandEvent& event)
{
    if(wxNO == wxMessageBox(wxString::Format(_("Please make sure %s is not running, continue?"), _T("FTerm")), _("Confirm"), wxYES_NO|wxNO_DEFAULT|wxICON_QUESTION))
        return;
    wxFileDialog* fileDlg = new wxFileDialog(this, wxString::Format(_("Select the location of %s"), _T("FTerm")), wxEmptyString, wxEmptyString,
                                                wxString::Format(_("%s program"), _T("FTerm"))+_T("|FTerm.exe"),
                                                wxFD_DEFAULT_STYLE|wxFD_OPEN|wxFD_FILE_MUST_EXIST|wxFD_CHANGE_DIR|wxFD_PREVIEW|wxTAB_TRAVERSAL|wxWANTS_CHARS,
                                                wxDefaultPosition, wxDefaultSize, _T("wxFileDialog"));
    if (fileDlg->ShowModal() != wxID_OK)
        return;
    wxString path = fileDlg->GetPath();
    delete fileDlg;
    path = path.BeforeLast(_T('\\'))+_T("\\fterm.ini");
    wxTextFile txt(path);
    if(txt.Exists() && txt.Open(CODE_GB))
    {
        long num;
        for(size_t i=0; i<txt.GetLineCount(); i++)
        {
            wxString token = txt[i];
			if (token.Trim() == wxEmptyString || token.StartsWith(_T(";")))
				continue;
			if (token.StartsWith(_T("TotalNumber=")))
			{
				if(!token.AfterFirst('=').Trim().ToLong(&num))
                {
                    wxMessageBox(ERR_READ_CONFIG);
                    return;
                }
                txt[i] = _T("TotalNumber=") + wxString::Format(_T("%ld"), ++num);
                break;
			}
		}
        txt.AddLine(wxString::Format(_T("[SCRIPT%ld]"), num));
        txt.AddLine(_T("DESC=") + GetTitle());
        txt.AddLine(_T("CMDTYPE=1"));
        txt.AddLine(_T("CATEGORY=") + GetTitle().BeforeFirst(_T(' ')));
        txt.AddLine(_T("COMMAND=") + wxStandardPaths::Get().GetExecutablePath());
		txt.Write(wxTextFileType_None, CODE_GB);
		wxMessageBox(OK_INTEGRATE_TO_TERM);
	}
	else
        wxMessageBox(ERR_READ_CONFIG);
}

void MainFrame::OnmnuCtermSelected(wxCommandEvent& event)
{
    if(wxNO == wxMessageBox(wxString::Format(_("Please make sure %s is not running, continue?"), _T("CTerm")), _("Confirm"), wxYES_NO|wxNO_DEFAULT|wxICON_QUESTION))
        return;
    wxFileDialog* fileDlg = new wxFileDialog(this, wxString::Format(_("Select the location of %s"), _T("CTerm")), wxEmptyString, wxEmptyString,
                                                wxString::Format(_("%s program"), _T("CTerm"))+_T("|CTerm.exe"),
                                                wxFD_DEFAULT_STYLE|wxFD_OPEN|wxFD_FILE_MUST_EXIST|wxFD_CHANGE_DIR|wxFD_PREVIEW|wxTAB_TRAVERSAL|wxWANTS_CHARS,
                                                wxDefaultPosition, wxDefaultSize, _T("wxFileDialog"));
    if (fileDlg->ShowModal() != wxID_OK)
        return;
    wxString path = fileDlg->GetPath();
    delete fileDlg;
    path = path.BeforeLast(_T('\\'))+_T("\\user\\mycmds.txt");
    wxTextFile txt(path);
    if((!txt.Exists() && txt.Create()) || txt.Open(CODE_GB))
    {
        wxString exepath = wxStandardPaths::Get().GetExecutablePath();
        exepath.Replace(_T("\\"), _T("\\\\"));
        txt.AddLine(_T("99; ; ")+APP_REG+_T("; true; py:import os\\\\nos.startfile(r\\\"")+exepath+_T("\\\");"));
		txt.Write(wxTextFileType_None, CODE_GB);
		wxMessageBox(OK_INTEGRATE_TO_TERM);
    }
    else
        wxMessageBox(ERR_READ_CONFIG);
}

void MainFrame::OnmnuUpdateSelected(wxCommandEvent& event)
{
    mCheckNewReleaseThread *thread = new mCheckNewReleaseThread();
    if ( thread->Create() != wxTHREAD_NO_ERROR )
    {
        wxMessageBox(ERR_CREATE_THREAD);
    }
    else
    {
        if ( thread->Run() != wxTHREAD_NO_ERROR )
        {
            wxMessageBox(ERR_RUN_THREAD);
        }
    }
}

void MainFrame::OnNewRelease(wxCommandEvent& event)
{
    wxGetApp().progOptions.new_version = event.GetString();
    if(wxGetApp().progOptions.new_version.CmpNoCase(APP_VERSION)>0)
    {
        if(wxYES == wxMessageBox(APP_NAME + SPACE_STRING + wxGetApp().progOptions.new_version + SPACE_STRING + _("is available.")
                                    + _T("\n") + _("Would you like to update now?"), _("New version found"), wxYES_NO|wxICON_INFORMATION))
            OnmnuHomepageSelected(event);
    }
    else
        wxMessageBox(_("You are using the latest version."));
}

void MainFrame::OnmnuRemoveSelectedSelected(wxCommandEvent& event)
{
    lstUpFile->RemoveSelected(event);
}

void MainFrame::OnmnuRemoveAllSelected(wxCommandEvent& event)
{
    lstUpFile->RemoveAll(event);
}

void MainFrame::OnmnuRemoveDupSelected(wxCommandEvent& event)
{
    lstUpFile->RemoveDup(event);
}

void MainFrame::OnmnuRemoveInvalidSelected(wxCommandEvent& event)
{
    lstUpFile->RemoveInvalid(event);
}


