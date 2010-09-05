//
// C++ Implementation: UtilFunctions
//
// Description: This file contain the implementation of some usefull conversion
//              functions.
//

#include "UploadHelperApp.h"

wxString MyUtilFunc::TrimHTML(wxString strHTML)
{
    wxString tmp=strHTML;
    wxRegEx re(_T("<[^>]*>|\n"));
    re.ReplaceAll(&tmp, wxEmptyString);
    return tmp;
}

int MyUtilFunc::writer(char *data, size_t size, size_t nmemb, std::string *writerData)
{
    if (writerData == NULL)
        return 0;
    writerData->append(data, size*nmemb);
    return size * nmemb;
}

wxString MyUtilFunc::GetBoard(const wxString strBoard)
{
    wxRegEx re(_T("([^ ]+)"));
    if (re.Matches(strBoard))
    {
        return re.GetMatch(strBoard,1);
    }
    else
        return wxEmptyString;
}

char* MyUtilFunc::WX2pChar(const wxString s, const wxString conv)
{
    if(s.IsEmpty())
        return NULL;
    char *p = new char[s.Len()];
    if(conv.IsEmpty())
        strcpy(p, s.mb_str());
    else
        strcpy(p, s.mb_str(wxCSConv(conv)));
    return p;
}

wxString MyUtilFunc::NewURL(const wxString url)
{
    int i=UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("display_host"), 0);
    int j=UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("blank_lines"), 1);
    wxString tmp=url;
    tmp=tmp.Append('\n', j);
    tmp.Replace(_T("bbs.fudan.edu.cn"), BBS_URLS[i]);
    return tmp;
}

wxString MyUtilFunc::ProcessImage(const wxString img)
{
    if(!IS_IMAGE_FILE(img))
        return img;

    wxImage myimg(img);
    bool dirty=false;

    if(UploadHelperApp::Configurations(READ, _T("Image"), _T("scale"), true))
    {
        long w, h;
        UploadHelperApp::Configurations(READ, _T("Image"), _T("scale_w"), _T("1024")).ToLong(&w);
        UploadHelperApp::Configurations(READ, _T("Image"), _T("scale_h"), _T("768")).ToLong(&h);
        if(myimg.GetWidth()>w)
        {
            myimg=myimg.Scale(w, (float)myimg.GetHeight()/(float)myimg.GetWidth()*w);
            dirty=true;
        }
        if(myimg.GetHeight()>h)
        {
            myimg=myimg.Scale((float)myimg.GetWidth()/(float)myimg.GetHeight()*h, h);
            dirty=true;
        }
    }

    if(UploadHelperApp::Configurations(READ, _T("Image"), _T("quality"), true))
    {
        int q=UploadHelperApp::Configurations(READ, _T("Image"), _T("quality_value"), 80);
        long sz;
        UploadHelperApp::Configurations(READ, _T("Image"), _T("quality_size"), _T("1024")).ToLong(&sz);
        if(wxFileName(img).GetSize()>sz*1024 && myimg.HasOption(_T("quality")))
        {
            myimg.SetOption(_T("quality"), q);
            dirty=true;
        }
    }

    if(UploadHelperApp::Configurations(READ, _T("Image"), _T("hue"), false))
    {
        double h=UploadHelperApp::Configurations(READ, _T("Image"), _T("hue_value"), 0);
        myimg.RotateHue(h);
        dirty=true;
    }

    if(UploadHelperApp::Configurations(READ, _T("Image"), _T("blur"), false))
    {
        int b=UploadHelperApp::Configurations(READ, _T("Image"), _T("blur_value"), 0);
        myimg=myimg.Blur(b);
        dirty=true;
    }

    if(UploadHelperApp::Configurations(READ, _T("Image"), _T("rotate"), false))
    {
        double r=UploadHelperApp::Configurations(READ, _T("Image"), _T("rotate_value"), 0);
        myimg=myimg.Rotate(r, wxPoint(myimg.GetWidth()/2, myimg.GetHeight()/2));
        dirty=true;
    }

    if(!wxFileName::DirExists(TEMP_DIR))
        if(!wxFileName::Mkdir(TEMP_DIR))
        {
            wxMessageBox(_("Failed to create temporary folder."));
            return wxEmptyString;
        }

    if(dirty)
    {
        wxString svfile=TEMP_DIR+wxFILE_SEP_PATH+wxFileName(img).GetName()+_T("_tmp.")+wxFileName(img).GetExt();
        //wxMessageBox(svfile);
        if(myimg.SaveFile(svfile))
        {
            return svfile;
        }
        else
        {
            wxMessageBox(_("Failed to save image file."));
            return wxEmptyString;
        };
    }
    else
        return img;
}
