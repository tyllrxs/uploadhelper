#include "UploadHelperApp.h"

IMPLEMENT_APP(UploadHelperApp);

bool UploadHelperApp::OnInit()
{
    //(*AppInitialize
    bool wxsOK = true;
    wxInitAllImageHandlers();

    #ifdef __WXMAC__
        /*wxApp::SetExitOnFrameDelete(false);
        wxMenuBar *menubar = new wxMenuBar;
        // add open, new, etc options to your menubar.
        wxMenuBar::MacSetCommonMenuBar(menubar);*/
        wxSystemOptions::SetOption(_T("mac.listctrl.always_use_generic"), 1);
    #endif

    //Get the executing path of application
    wxString exeDir=wxStandardPaths::Get().GetExecutablePath();
    wxFileName fname(exeDir);
    progOptions.exe_dir=fname.GetPath();

    m_locale = NULL;
    SelectLanguage(wxLANGUAGE_DEFAULT);
    //SelectLanguage(wxLANGUAGE_CHINESE_TRADITIONAL);
    SetAppName(APP_NAME);

    if ( wxsOK )
    {
        mainframe = new MainFrame(0);
        mainframe->Show();
        SetTopWindow(mainframe);
    }
    //*)
    return wxsOK;

}

void UploadHelperApp::SelectLanguage(int lang)
{
    delete m_locale;
    m_locale = new wxLocale(lang);
    m_locale->AddCatalogLookupPathPrefix(PATH_LANGUAGE);
    m_locale->AddCatalog(_T("UploadHelper"));
}

void UploadHelperApp::ReadUserInfo()
{
    //Read login configuration
    progOptions.user_domain=Configurations(READ, _T("Login"), _T("user_domain"), 0);
    progOptions.user_id=Configurations(READ, _T("Login"), _T("user_id"), wxEmptyString);
    progOptions.user_password=Configurations(READ, _T("Login"), _T("user_password"), wxEmptyString);
    progOptions.user_cookie=Configurations(READ, _T("Login"), _T("user_cookie"), wxEmptyString);
    progOptions.bbs_url=_T("http://") + BBS_URLS[progOptions.user_domain] + BBS_PATH;
}

wxString UploadHelperApp::Configurations(int operation, wxString path, wxString option,wxString value)
{
    wxString tmpvalue = value;
    wxFileConfig *config = new wxFileConfig(APP_REG);
    config->SetPath(_T("/")+path);
    if (operation == WRITE)
        config->Write(option,tmpvalue);
    else
        config->Read(option,&tmpvalue);
    delete config;
    return tmpvalue;
}

int UploadHelperApp::Configurations(int operation, wxString path, wxString option,int value)
{
    int tmpvalue = value;
    wxFileConfig *config = new wxFileConfig(APP_REG);
    config->SetPath(_T("/")+path);
    if (operation == WRITE)
        config->Write(option,tmpvalue);
    else
        config->Read(option,&tmpvalue);
    delete config;
    return tmpvalue;
}

long UploadHelperApp::Configurations(int operation, wxString path, wxString option,long value)
{
    wxString tmpvalue;
    long returnvalue;
    tmpvalue << value;
    wxFileConfig *config = new wxFileConfig(APP_REG);
    config->SetPath(_T("/")+path);
    if (operation == WRITE)
        config->Write(option,tmpvalue);
    else
        config->Read(option,&tmpvalue);
    delete config;
    tmpvalue.ToLong(&returnvalue);
    return returnvalue;
}

bool UploadHelperApp::ConnectToURL(const wxString url, const wxString pst, wxString* resp)
{
    CURL *myurl;
    CURLcode res;
    std::string buffer;

    if(url.IsEmpty())
        return false;

    wxString cookie=UploadHelperApp::Configurations(READ, _T("Login"), _T("user_cookie"), wxEmptyString);
    myurl = curl_easy_init();
    if (myurl)
    {
        res = curl_easy_setopt(myurl, CURLOPT_URL, MyUtilFunc::WX2pChar(url));
        //res = curl_easy_setopt(myurl, CURLOPT_VERBOSE, 1);
        if(!pst.IsEmpty())
        {
            res = curl_easy_setopt(myurl, CURLOPT_POSTFIELDS, MyUtilFunc::WX2pChar(pst, BBS_CODEPAGE));
        }
        if(!cookie.IsEmpty())
        {
            res = curl_easy_setopt(myurl, CURLOPT_COOKIE, MyUtilFunc::WX2pChar(cookie));
        }
        if(UploadHelperApp::Configurations(READ, _T("General"), _T("proxy"), false))
        {
            wxString proxyAddr, proxyUser;
            proxyAddr=UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_addr"), wxEmptyString);
            proxyUser=UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_user"), wxEmptyString);
            if(!proxyAddr.IsEmpty())
            {
                proxyAddr+=_T(":")+UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_port"), wxEmptyString);
                res = curl_easy_setopt(myurl, CURLOPT_PROXY, MyUtilFunc::WX2pChar(proxyAddr));
                if(!proxyUser.IsEmpty())
                {
                    proxyUser+=_T(":")+UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_pwd"), wxEmptyString);
                    res = curl_easy_setopt(myurl, CURLOPT_PROXYUSERPWD, MyUtilFunc::WX2pChar(proxyUser));
                }
            }
        }
        res = curl_easy_setopt(myurl, CURLOPT_WRITEFUNCTION, MyUtilFunc::writer);
        res = curl_easy_setopt(myurl, CURLOPT_WRITEDATA, &buffer);
        res = curl_easy_perform(myurl);
        curl_easy_cleanup(myurl);
    }

    //Failed to connect to server
    if (CURLE_OK != res)
    {
        wxMessageBox(ERR_NETWORK);
        return false;
    }
    wxString resHTML(buffer.c_str(), wxCSConv(BBS_CODEPAGE));
    //wxMessageBox(resHTML);
    *resp=resHTML;

    //Server tells error in response info
    if (wxNOT_FOUND != resHTML.Find(_T("错误")) || wxNOT_FOUND != resHTML.Find(_T("Nothing Here")))
        return false;
    else    //Connected successfully.
        return true;
}

bool UploadHelperApp::PerfectConnect(wxString url, wxString pst)
{
    for(int cnt=0; cnt<2; cnt++)
    {
        wxString resHTML=wxEmptyString;
        if(ConnectToURL(url, pst, &resHTML))
            return true;
        else
        {
            if(resHTML.IsEmpty())
            {
                //wxMessageBox(ERR_NETWORK);
                return false;
            }
            else
            {
                //Server tells error in response info
                if(cnt>0)
                {
                    wxMessageBox(MyUtilFunc::TrimHTML(resHTML));
                    return false;
                }
                else
                {
                    if(wxNOT_FOUND != resHTML.Find(_T("匆匆过客")))
                    {
                        if(!LoginToBBS(Configurations(READ, _T("Login"), _T("user_id"), wxEmptyString), \
                                                Configurations(READ, _T("Login"), _T("user_password"), wxEmptyString), \
                                                Configurations(READ, _T("Login"), _T("user_domain"), 0)))
                        {
                            LoginDialog* dlg = new LoginDialog(wxGetApp().mainframe);
                            dlg->ShowModal(); //Open "Login" dialog
                            continue;
                        }
                    }
                    else
                    {
                        wxMessageBox(MyUtilFunc::TrimHTML(resHTML));
                        return false;
                    }
                }
            }
        }
    }
}

bool UploadHelperApp::LoginToBBS(wxString usrid, wxString usrpwd, int usrdomain)
{
    wxString strPost = _T("id=") + usrid + _T("&pw=") + usrpwd;
    wxString strURL = _T("http://") + BBS_URLS[usrdomain] + BBS_PATH + _T("bbslogin");

    wxString resHTML;
    if(!ConnectToURL(strURL, strPost, &resHTML))
    {
        if(!resHTML.IsEmpty())
            wxMessageBox(MyUtilFunc::TrimHTML(resHTML));
        return false;
    }
    //Login OK. Now begin to parse HTML for cookie, using "Regular Expression"
    wxRegEx re(_T("cookie='([^']*)'"));
    wxString cookie=_T("");
    size_t num;
    while (wxNOT_FOUND != resHTML.Find(_T("</script>")))
    {
        if (re.Matches(resHTML))
        {
            cookie+=re.GetMatch(resHTML,1)+_T(";");
        }
        num=resHTML.Find(_T("</script>"));
        resHTML=resHTML.substr(num+9);
    }

    //Save all info to configuration file
    Configurations(WRITE, _T("Login"), _T("user_domain"), usrdomain);
    Configurations(WRITE, _T("Login"), _T("user_id"), usrid);
    Configurations(WRITE, _T("Login"), _T("user_password"), usrpwd);
    Configurations(WRITE, _T("Login"), _T("user_cookie"), cookie);

    return true;
}
