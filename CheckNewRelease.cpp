//
// C++ Implementation: CheckNewRelease
//
// Description: Implements a routine to access the uploadhelper host, and to check if exists some
//              new release.
//

#include "UploadHelperApp.h"

mCheckNewReleaseThread::mCheckNewReleaseThread()
{

}

void *mCheckNewReleaseThread::Entry()
{
    wxURL url(APP_HOMEPAGE+_T("/version.txt"));
    if (url.GetError() == wxURL_NOERR)
    {
        wxInputStream *in_stream;
        char *data=new char[2049];
        in_stream = url.GetInputStream();
        if (in_stream)
        {
            in_stream->Read(data, 2048);
            int readd = in_stream->LastRead();
            if (readd > 0)
            {
                data[readd] = '\0';
                wxString strnewrelease(data, wxConvUTF8);
                wxRegEx re(_T("version=\"([^\"]*)\""));
                if (re.Matches(strnewrelease))
                {
                    wxString ver=re.GetMatch(strnewrelease,1);
                    wxCommandEvent newversionevent(wxEVT_NEW_RELEASE);
                    newversionevent.SetString(ver);
                    wxGetApp().mainframe->GetEventHandler()->AddPendingEvent(newversionevent);
                }
            }
            delete [] data;
            delete in_stream;
        }
    }
    else
        wxMessageBox(ERR_NETWORK);
    return NULL;
}

void mCheckNewReleaseThread::OnExit()
{

}
