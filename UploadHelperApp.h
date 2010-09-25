/***************************************************************
 * Name:      UploadHelperApp.h
 * Purpose:   Defines Application Class
 * Author:    tyllr (tyllrxs@gmail.com)
 * Created:   2008-05-28
 * Copyright: tyllr (R)
 * License:     GPL v2
 **************************************************************/

#ifndef UPLOADHELPERAPP_H
    #define UPLOADHELPERAPP_H

    // For compilers that support precompilation, includes "wx/wx.h".
    #include "wx/wxprec.h"

    #ifdef __BORLANDC__
    #pragma hdrstop
    #endif

    #ifndef WX_PRECOMP
    #include "wx/wx.h"
    #endif

    //(*Internal Headers
    #include <wx/app.h>
    #include <wx/artprov.h>
    #include <wx/bitmap.h>
    #include <wx/busyinfo.h>
    #include <wx/confbase.h>
    #include <wx/config.h>
    #include <wx/dnd.h>
    #include <wx/event.h>
    #include <wx/file.h>
    #include <wx/fileconf.h>
    #include <wx/filename.h>
    #include <wx/font.h>
    #include <wx/hyperlink.h>
    #include <wx/intl.h>
    #include <wx/image.h>
    #include <wx/imaglist.h>
    #ifdef __WXMSW__
        #include <wx/msw/regconf.h>
    #endif
    #include <wx/regex.h>
    #include <wx/settings.h>
    #include <wx/stdpaths.h>
    #include <wx/string.h>
    #include <wx/sysopt.h>
    #include <wx/textfile.h>
    #include <wx/timer.h>
    #include <wx/tokenzr.h>
    #include <wx/url.h>
    #include <wx/wfstream.h>
    #include <wx/window.h>
    #include <wx/xml/xml.h>

    #include <iostream>
    #include <curl/curl.h>
    #include <sys/time.h>
    //*)

    //(*Custom Headers
    #include <wx/button.h>
    #include <wx/checkbox.h>
    #include <wx/choice.h>
    #include <wx/combobox.h>
    #include <wx/dialog.h>
    #include <wx/filedlg.h>
    #include <wx/frame.h>
    #include <wx/listctrl.h>
    #include <wx/menu.h>
    #include <wx/msgdlg.h>
    #include <wx/notebook.h>
    #include <wx/panel.h>
    #include <wx/radiobut.h>
    #include <wx/sizer.h>
    #include <wx/slider.h>
    #include <wx/spinctrl.h>
    #include <wx/statbmp.h>
    #include <wx/statline.h>
    #include <wx/stattext.h>
    #include <wx/taskbar.h>
    #include <wx/textctrl.h>
    #include <wx/toolbar.h>

    //xpm Images
    #include "icon/logo.xpm"
    #include "icon/title.xpm"
    #include "icon/16/01.xpm"
    #include "icon/16/02.xpm"
    #include "icon/16/03.xpm"
    #include "icon/16/04.xpm"
    #include "icon/16/05.xpm"
    #include "icon/16/06.xpm"
    #include "icon/16/logo16.xpm"
    #include "icon/16/upload.xpm"
    #include "icon/16/post.xpm"
    #include "icon/16/ok.xpm"
    #include "icon/16/fail.xpm"
    #include "icon/16/uploading.xpm"
    #include "icon/16/exit.xpm"
    #include "icon/16/del.xpm"
    #include "icon/16/star.xpm"
    #include "icon/16/star2.xpm"
    #include "icon/16/star3.xpm"
    #include "icon/16/star4.xpm"
    #include "icon/32/logo32.xpm"
    //*)

    //CUSTOM EVENTS
    extern const wxEventType wxEVT_NEW_RELEASE;

    //(*Custom Macros
    #define BBS_CODEPAGE _T("GB2312")
    #define CODE_GB wxCSConv(_T("GB2312"))

    //Basic information for this app
    #define APP_NAME  _("UploadHelper")
    const wxString APP_REG = _T("UploadHelper");
    const wxString APP_VERSION = _T("4.0 RC");
    const wxString APP_AUTHOR = _T("tyllr");
    const wxString APP_HOMEPAGE = _T("http://homepage.fudan.edu.cn/~tyllr/uh");
    const wxString APP_EMAIL = _T("tyllrxs@gmail.com");
    #define ACKNOWLEDGE_LIST wxString::Format(_T("%s%s%s%s"), \
                                                        _T("Macintosh, DreamGhost, gw, Placebo, DETconan, SakurabaAoi, Lucian, FallinSnow, "), \
                                                        _T("wpbirch, DragonZhao, iloveac, rat, FedoraCore, qrupdhlcn, ssnake, fisio, SuperColin, "), \
                                                        _T("droople, zhangga, lancyl, andyhqa, CAtom, Odom, GFW, CHGS, gotogoal, feisty, marcus, "), \
                                                        _T("overboming, sixtongtong, dymm, alexjiang, tearring, dashuai, raxodus, BetterLife, eagleonhill"))

    //Information related to RYGH bbs (bbs.fudan.edu.cn)
    const wxString BBS_NAME = _T("RYGH");
    const wxString BBS_URLS[4] =
    {
        _T("bbs.fudan.edu.cn"),
        _T("bbs.fudan.sh.cn"),
        _T("202.120.225.9"),
        _T("61.129.42.9")
    };
    const wxString BBS_PATH = _T("/cgi-bin/bbs/");

    //External Data
    const wxString FILE_BOARD_LIST = _T("board_list.xml");
    #define TEMP_DIR    (wxGetHomeDir() + wxFILE_SEP_PATH + _T("temp"))
    //Messages shown to user
    #define ERR_BOARD   _("Board selected is invalid.")
    #define ERR_NO_BLANKS  _("Please fill in the blanks first.")
    #define ERR_NETWORK  _("Failed to connect with server. Please check your network or proxy settings.")
    #define ERR_LOGIN  _("Login failed. Be sure you've typed correctly.")
    #define OK_LOGIN  _("Login successfully. Ready for uploading.")
    #define OK_POST  _("OK. Sent to destination successfully.")
    #define ERR_READ_CONFIG  _("Failed to read configuration. Check the configuration file.")
    #define ERR_WRITE_CONFIG  _("Failed to save configuration.")
    #define ERR_READ_BOARD_LIST  _("Failed to read BOARD LIST. Make sure that the list file is correctly located.")
    #define ERR_CREATE_THREAD  _("Error creating thread!")
    #define ERR_RUN_THREAD  _("Error starting thread!")
    #define STATUS_NOT_YET  wxEmptyString
    #define STATUS_PREPARE  _("Preparing...")
    #define STATUS_UPLOAD  _("Uploading...")
    #define STATUS_UPLOAD_FAIL  _("Failed")
    #define STATUS_UPLOADED  _("Finished")
    #define STATUS_SKIP _("Skip")
    #define OK_INTEGRATE_TO_TERM    _("Successfully added to the toolbar of Term.")

    //Macro functions
    #define IS_IMAGE_FILE(fn)   wxRegEx(_T("\\.(jpe?g|gif|png|bmp)$"), wxRE_ICASE).Matches(fn)

    //Extra constants
    const wxString SPACE_STRING = _T(" ");
    #define READ        4
    #define WRITE       5

    #define LISTCTRL_UPFILE     1000
    #define REVSEL      2000
    #define REVALL      2001
    #define REVDUP      2002
    #define REVINV      2003
    #define HIDE            2100
    #define NEW             2101
    #define CLOSE       2102
    #define MENU_THUMBNAIL  3000
    #define TIP_TIMER   3001

    //Linux dialog filter requires a special pattern to make it incase-sensitive
    #ifdef __WXGTK__
        #define OPEN_DIALOG_FILTER wxString::Format(_T("%s (*.jpg;*.png;*.gif;*.pdf)|*.[Jj][Pp][Gg];*.[Pp][Nn][Gg];*.[Gg][Ii][Ff];*.[Pp][Dd][Ff]|%s (*.jpg;*.png;*.gif)|*.[Jj][Pp][Gg];*.[Pp][Nn][Gg];*.[Gg][Ii][Ff]|%s (*.pdf)|*.[Pp][Dd][Ff]"), \
                                                                                        _("Supported Files"), _("Image Files"), _("Portable Document Format"))
    #else
        #define OPEN_DIALOG_FILTER wxString::Format(_T("%s (*.jpg;*.png;*.gif;*.pdf)|*.jpg;*.png;*.gif;*.pdf|%s (*.jpg;*.png;*.gif)|*.jpg;*.png;*.gif|%s (*.pdf)|*.pdf"), \
                                                                                        _("Supported Files"), _("Image Files"), _("Portable Document Format"))
    #endif

    //Related files locate different on Mac (i.e. app bundle)
    #ifdef __WXMAC__
        #define PATH_BOARD_LIST wxGetApp().progOptions.exe_dir+_T("/../Resources/")+FILE_BOARD_LIST
        #define PATH_LANGUAGE   wxGetApp().progOptions.exe_dir.BeforeLast(_T('.')).AfterLast(_T('/'))+_T(".app/Contents/Resources/lang")
    #elif __WXGTK__
        #define PATH_BOARD_LIST _T("/usr/share/uploadhelper/")+FILE_BOARD_LIST
        #define PATH_LANGUAGE   _T("../../../../../../../../../../usr/share/uploadhelper/lang")
    #else
        #define PATH_BOARD_LIST wxGetApp().progOptions.exe_dir+wxFILE_SEP_PATH+FILE_BOARD_LIST
        #define PATH_LANGUAGE   _T("lang")
    #endif

    //Fixed Toolbar Error on Mac
    //#define wxMAC_USE_NATIVE_TOOLBAR 0

    //define some platform-dependent parameters
    #ifdef __WXMAC__
        //default zone and board
        #define DEFAULT_ZONE    3
        #define DEFAULT_BOARD   0
    #elif __WXGTK__
        #define DEFAULT_ZONE    3
        #define DEFAULT_BOARD   3
    #else
        #define DEFAULT_ZONE    4
        #define DEFAULT_BOARD   9
    #endif
    //*)

    class UploadHelperApp;
    class MainFrame;
    class LoginDialog;
    class ConfigDialog;
    class AboutDialog;
    class mOptions;
    class MyUtilFunc;
    class mUploadThread;
    class mCheckNewReleaseThread;
    class mTaskBarIcon;
    class mListCtrl;
    class DnDFile;

    class mOptions
    {
    public:
        wxString user_id, user_password, user_cookie;
        int user_domain;
        wxString bbs_url;
        wxString exe_dir, new_version;
    };

    class MainFrame: public wxFrame
    {
        public:

            MainFrame(wxWindow* parent,wxWindowID id=wxID_ANY);
            virtual ~MainFrame();

            //(*Declarations(MainFrame)
            wxButton* btnUpload;
            wxMenu* mnuFileInfo;
            wxMenu* mnuTerm;
            wxMenuItem *mnuSize, *mnuMod, *mnuCre, *mnuAcc;
            wxButton* btnBrowse;
            wxButton* btnRemove;
            wxComboBox* cmbBoard;
            wxMenuItem* MenuItem7;
            wxButton* btnSend;
            wxStaticText* StaticText2;
            wxMenuItem* MenuItem2;
            wxMenuItem* mnuLogoff;
            wxMenu* Menu3;
            wxMenuItem* MenuItem11;
            wxNotebook* tbMain;
            wxMenu* MenuItem4;
            wxPanel* Panel1;
            wxStaticText* StaticText1;
            wxStaticText* StaticText3;
            wxCheckBox* chkLock;
            wxMenu* Menu1;
            wxTextCtrl* txtTitle;
            wxMenuItem* MenuItem10;
            wxMenuItem* mnuAlwaysTop;
            wxMenuItem* MenuItem3;
            wxMenuItem* mnuHomepage;
            wxChoice* cmbSign;
            mListCtrl* lstUpFile;
            wxTextCtrl* txtContent;
            wxTextCtrl* txtSendBoard;
            wxMenuBar* MenuBar1;
            wxPanel* Panel2;
            wxMenuItem* mnuFAQ;
            wxMenuItem* mnuUpdate;
            wxMenuItem* mnuAbout;
            wxMenuItem* mnuLogin;
            wxMenu* Menu2;
            wxMenuItem* MenuItem9;
            wxMenuItem* mnuFterm;
            wxMenuItem* mnuCterm;
            wxStaticText* StaticText4;
            wxStaticText* StaticText5;
            wxComboBox* cmbZone;
            wxMenu* Menu4;
            mTaskBarIcon* taskbaricon;
            //*)

        protected:

            //(*Identifiers(MainFrame)
            static const long ID_STATICTEXT1;
            static const long ID_COMBOBOX1;
            static const long ID_COMBOBOX2;
            static const long ID_CHECKBOX1;
            static const long ID_STATICTEXT2;
            static const long ID_BUTTON1;
            static const long ID_BUTTON3;
            static const long ID_BUTTON4;
            static const long ID_PANEL1;
            static const long ID_STATICTEXT3;
            static const long ID_TEXTCTRL1;
            static const long ID_STATICTEXT4;
            static const long ID_STATICTEXT5;
            static const long ID_CHOICE3;
            static const long ID_TEXTCTRL2;
            static const long ID_TEXTCTRL3;
            static const long ID_BUTTON2;
            static const long ID_PANEL2;
            static const long ID_NOTEBOOK1;
            static const long ID_MENUITEM1;
            static const long ID_MENUITEM2;
            static const long ID_MENUITEM9;
            static const long ID_MENUITEM10;
            static const long ID_MENUITEM12;
            static const long ID_MENUITEM13;
            static const long ID_MENUITEM14;
            static const long ID_MENUITEM15;
            static const long ID_MENUITEM11;
            static const long ID_MENUITEM3;
            static const long ID_MENUITEM4;
            static const long ID_MENUITEM5;
            static const long ID_MENUITEM6;
            static const long ID_MENUITEM7;
            //*)

        private:

            //(*Handlers(MainFrame)

            void OnClose(wxCloseEvent& event);
            void OncmbZoneSelect(wxCommandEvent& event);
            void OncmbBoardSelect(wxCommandEvent& event);
            void OnmnuAboutSelected(wxCommandEvent& event);
            void OnmnuLoginSelected(wxCommandEvent& event);
            void OnmnuPreferenceSelected(wxCommandEvent& event);
            void OnchkLockClick(wxCommandEvent& event);
            void OnmnuAlwaysTopSelected(wxCommandEvent& event);
            void OnmnuLogoffSelected(wxCommandEvent& event);
            void OnbtnBrowseClick(wxCommandEvent& event);
            void OnbtnRemoveClick(wxCommandEvent& event);
            void OnbtnSendClick(wxCommandEvent& event);
            void OnbtnUploadClick(wxCommandEvent& event);
            void OnmnuFAQSelected(wxCommandEvent& event);
            void OnmnuHomepageSelected(wxCommandEvent& event);
            void OnmnuToolbarSelected(wxCommandEvent& event);
            void OnmnuUpdateSelected(wxCommandEvent& event);
            void OnmnuSizeSelected(wxCommandEvent& event);
            void OnmnuModifiedSelected(wxCommandEvent& event);
            void OnmnuCreatedSelected(wxCommandEvent& event);
            void OnmnuAccessedSelected(wxCommandEvent& event);
            void OnmnuFtermSelected(wxCommandEvent& event);
            void OnmnuCtermSelected(wxCommandEvent& event);
            void OnNewRelease(wxCommandEvent& event);
            void OnmnuRemoveSelectedSelected(wxCommandEvent& event);
            void OnmnuRemoveAllSelected(wxCommandEvent& event);
            void OnmnuRemoveDupSelected(wxCommandEvent& event);
            void OnmnuRemoveInvalidSelected(wxCommandEvent& event);

            //*)

            DECLARE_EVENT_TABLE()
    };

    class LoginDialog: public wxDialog
    {
    public:

        LoginDialog(wxWindow* parent,wxWindowID id = -1);
        virtual ~LoginDialog();

    private:

        //(*Handlers(LoginDialog)
        void OnInit(wxInitDialogEvent& event);
        void OnQuit(wxCommandEvent& event);
        void OnAbout(wxCommandEvent& event);
        void OnbtnLoginClick(wxCommandEvent& event);
        void OnClose(wxCloseEvent& event);
        void OnClose1(wxCloseEvent& event);
        void OnKillFocus(wxFocusEvent& event);
        void OnMouseLeave(wxMouseEvent& event);
        void OntxtUserText(wxCommandEvent& event);
        void FileRead(const wxString& filename);
        size_t write_data(char *ptr, size_t sz, size_t nmemb, char *mydata);
        //*)

        //(*Identifiers(LoginDialog)
        static const long ID_STATICBITMAP1;
        static const long ID_STATICTEXT1;
        static const long ID_CHOICE1;
        static const long ID_STATICTEXT2;
        static const long ID_TEXTCTRL1;
        static const long ID_STATICTEXT3;
        static const long ID_TEXTCTRL2;
        //*)

        //(*Declarations(LoginDialog)
        wxButton* btnLogin;
        wxTextCtrl* txtPwd;
        wxStaticText* StaticText2;
        wxStaticBitmap* StaticBitmap1;
        wxTextCtrl* txtUser;
        wxStaticText* StaticText1;
        wxStaticText* StaticText3;
        wxChoice* cmbDomain;
        //*)

        DECLARE_EVENT_TABLE()
    };

    class ConfigDialog: public wxDialog
    {
	public:

		ConfigDialog(wxWindow* parent,wxWindowID id=wxID_ANY);
		virtual ~ConfigDialog();

		//(*Declarations(ConfigDialog)
		wxStaticText* StaticText10;
		wxSlider* sldHue;
		wxStaticText* StaticText9;
		wxTextCtrl* txtProxyPwd;
		wxRadioButton* RadioButton1;
		wxSlider* sldQuality;
		wxNotebook* Notebook1;
		wxSpinCtrl* txtThreads;
		wxStaticText* StaticText2;
		wxPanel* Panel4;
		wxRadioButton* RadioButton2;
		wxStaticText* StaticText6;
		wxStaticText* lblBlur;
		wxSlider* sldRotate;
		wxStaticText* StaticText8;
		wxCheckBox* chkFileUnsupportWarning;
		wxCheckBox* chkQuality;
		wxCheckBox* chkRotate;
		wxPanel* Panel1;
		wxStaticText* StaticText1;
		wxStaticText* StaticText3;
		wxPanel* Panel3;
		wxCheckBox* chkScale;
		wxStaticText* StaticText5;
		wxStaticText* StaticText7;
		wxSlider* sldBlur;
		wxTextCtrl* txtScaleW;
		wxSpinCtrl* txtBlankLines;
		wxCheckBox* chkHue;
		wxTextCtrl* txtProxyPort;
		wxStaticText* lblRotate;
		wxTextCtrl* txtProxyAddr;
		wxCheckBox* chkClearPrevious;
		wxCheckBox* chkThumbnail;
		wxTextCtrl* txtScaleH;
		wxPanel* Panel2;
		wxStaticText* lblHue;
		wxCheckBox* chkBlur;
		wxStaticText* StaticText4;
		wxTextCtrl* txtProxyUser;
		wxTextCtrl* txtQualitySize;
		wxChoice* cmbDisplayHost;
		wxStaticText* lblQuality;
		//*)

	protected:

		//(*Identifiers(ConfigDialog)
		static const long ID_RADIOBUTTON1;
		static const long ID_RADIOBUTTON2;
		static const long ID_STATICTEXT1;
		static const long ID_TEXTCTRL1;
		static const long ID_STATICTEXT2;
		static const long ID_TEXTCTRL2;
		static const long ID_STATICTEXT3;
		static const long ID_TEXTCTRL3;
		static const long ID_STATICTEXT4;
		static const long ID_TEXTCTRL4;
		static const long ID_STATICTEXT5;
		static const long ID_SPINCTRL1;
		static const long ID_PANEL1;
		static const long ID_CHECKBOX1;
		static const long ID_TEXTCTRL8;
		static const long ID_STATICTEXT6;
		static const long ID_TEXTCTRL9;
		static const long ID_CHECKBOX2;
		static const long ID_TEXTCTRL10;
		static const long ID_STATICTEXT7;
		static const long ID_STATICTEXT8;
		static const long ID_SLIDER4;
		static const long ID_TEXTCTRL11;
		static const long ID_PANEL4;
		static const long ID_CHECKBOX4;
		static const long ID_SLIDER1;
		static const long ID_TEXTCTRL5;
		static const long ID_CHECKBOX5;
		static const long ID_SLIDER2;
		static const long ID_TEXTCTRL6;
		static const long ID_CHECKBOX6;
		static const long ID_SLIDER3;
		static const long ID_TEXTCTRL7;
		static const long ID_PANEL2;
		static const long ID_STATICTEXT9;
		static const long ID_cmbDisplayHost;
		static const long ID_STATICTEXT10;
		static const long ID_txtBlankLines;
		static const long ID_CHECKBOX3;
		static const long ID_CHECKBOX7;
		static const long ID_PANEL3;
		static const long ID_NOTEBOOK1;
		static const long ID_CHECKBOX8;
		//*)

	private:

		//(*Handlers(ConfigDialog)
		void OnInit(wxInitDialogEvent& event);
		void OnsldQualityScroll(wxScrollEvent& event);
		void OnsldHueScroll(wxScrollEvent& event);
		void OnsldBlurScroll(wxScrollEvent& event);
		void OnsldRotateScroll(wxScrollEvent& event);
		void OnRadioBtnClick(wxCommandEvent& event);
		void OnchkScaleClick(wxCommandEvent& event);
		void OnchkQualityClick(wxCommandEvent& event);
		void OnchkHueClick(wxCommandEvent& event);
		void OnchkBlurClick(wxCommandEvent& event);
		void OnchkRotateClick(wxCommandEvent& event);
		void SaveConfig(wxCommandEvent& event);
		void OnClose(wxCloseEvent& event);
		//*)

		DECLARE_EVENT_TABLE()
    };

    class AboutDialog: public wxDialog
    {
        public:

            AboutDialog(wxWindow* parent,wxWindowID id=wxID_ANY,const wxPoint& pos=wxDefaultPosition,const wxSize& size=wxDefaultSize);
            virtual ~AboutDialog();

            //(*Declarations(AboutDialog)
            wxStaticText* StaticText2;
            wxStaticText* StaticText6;
            wxStaticBitmap* StaticBitmap1;
            wxButton* btnQuit;
            wxStaticText* StaticText3;
            wxStaticText* StaticText5;
            wxStaticLine* StaticLine1;
            wxTextCtrl* TextCtrl1;
            wxHyperlinkCtrl* HypLink1;
            //*)

        protected:

            //(*Identifiers(AboutDialog)
            static const long ID_STATICBITMAP1;
            static const long ID_STATICTEXT2;
            static const long ID_STATICTEXT3;
            static const long ID_STATICTEXT4;
            static const long ID_STATICLINE1;
            static const long ID_STATICTEXT5;
            static const long ID_STATICTEXT6;
            static const long ID_TEXTCTRL1;
            //*)

        private:

            //(*Handlers(AboutDialog)
            void OnClose(wxCloseEvent& event);
            //*)

            DECLARE_EVENT_TABLE()
    };

    class UploadHelperApp : public wxApp
    {
    public:
        virtual bool OnInit();
        //Select language for this app
        void SelectLanguage(int lang);
        void ReadUserInfo();
        static wxString Configurations(int operation, wxString path, wxString option, wxString value);
        static int Configurations(int operation, wxString path, wxString option, int value);
        static long Configurations(int operation, wxString path, wxString option,long value);
        static bool ConnectToURL(wxString url, wxString post=wxEmptyString, wxString* resp=NULL);
        static bool PerfectConnect(wxString url, wxString post=wxEmptyString);
        static bool LoginToBBS(wxString usrid, wxString usrpwd, int usrdomain);

        MainFrame *mainframe;
        mOptions progOptions;
    private:
        wxLocale *m_locale; // ’our’ locale
    };

    DECLARE_APP(UploadHelperApp);

    class mUploadThread : public wxThread
    {
    public:
        mUploadThread();
        // thread execution starts here
        virtual void *Entry();

        // called when the thread exits - whether it terminates normally or is
        // stopped with Delete() (but not when it is Kill()ed!)
        virtual void OnExit();
    };

    class mCheckNewReleaseThread : public wxThread
    {
    public:
        mCheckNewReleaseThread();
        // thread execution starts here
        virtual void *Entry();

        // called when the thread exits - whether it terminates normally or is
        // stopped with Delete() (but not when it is Kill()ed!)
        virtual void OnExit();
    };

    class mTaskBarIcon : public wxTaskBarIcon
    {
    public:
        mTaskBarIcon(MainFrame *frame);
        void OnLButtonClick(wxTaskBarIconEvent&);
        void OnMouseMove(wxTaskBarIconEvent&);
        void OnClose(wxCommandEvent& event);
        void OnHide(wxCommandEvent& event);
        void OnNew(wxCommandEvent& event);
        virtual wxMenu *CreatePopupMenu();
        bool restoring;
    private:
        MainFrame *mainframe;
        DECLARE_EVENT_TABLE()
    };

    class MyUtilFunc
    {
    public:
        static wxString TrimHTML(wxString strHTML);
        static int writer(char *data, size_t size, size_t nmemb, std::string *writerData);
        static wxString GetBoard(const wxString strBoard);
        static char* WX2pChar(const wxString s, const wxString conv=wxEmptyString);
        static wxString NewURL(const wxString url);
        static wxString ProcessImage(const wxString img);
    };

    class mListCtrl : public wxListView
    {
    public:
        mListCtrl(wxWindow* parent, wxWindowID id, const wxPoint& pt, const wxSize& sz, long style, const wxValidator& validator, const wxString& name): \
                    wxListView(parent, id, pt, sz, style, validator, name), tipTimer(this, TIP_TIMER)
        {
            bSortAscending=false;
            iSortColumn=-1;
        }
        void AddFileItem(const wxArrayString& paths, long index=-1);
        void OnMouseMove(wxMouseEvent& event);
        void OnTimer(wxTimerEvent& event);
        void RemoveSelected(wxCommandEvent& event);
        void RemoveAll(wxCommandEvent& event);
        void RemoveDup(wxCommandEvent& event);
        void RemoveInvalid(wxCommandEvent& event);
        void DeselectAll();
        void AutoListNumber();
        void OnRClick(wxListEvent& event);
        void OnKeyDown(wxListEvent& event);
        void OnBeginDrag(wxListEvent& event);
        void OnColumnClick(wxListEvent& event);
        int GetSortColumn(){ return iSortColumn; }
        int GetSortAscending(){ return bSortAscending; }
        wxString GetCellText(const long row, const long col=1);
        wxString UploadFiles(const wxString strBoard);
    private:
        wxTimer tipTimer;
        wxString imgfile;
        bool bSortAscending;
        int iSortColumn;

        DECLARE_EVENT_TABLE()
    };

    // A drag-and-drop class for dragging files (from explorer, nautilus, Finder, etc.) into listctrl
    class DnDFile : public wxFileDropTarget
    {
    public:
       DnDFile(mListCtrl *owner);
       virtual wxDragResult OnDragOver(wxCoord x, wxCoord y, wxDragResult def);
       virtual bool OnDropFiles(wxCoord x, wxCoord y, const wxArrayString& filenames);
    private:
       mListCtrl *m_owner;
       bool bInside;
    };

#endif // UPLOADHELPERAPP_H
