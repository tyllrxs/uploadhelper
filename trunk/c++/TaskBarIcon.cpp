//
// C++ Implementation: TaskBarIcon
//
// Description: Implements the class taskbaricon, with include a icon on the tray.
//

#include "UploadHelperApp.h"

BEGIN_EVENT_TABLE(mTaskBarIcon, wxTaskBarIcon)
    EVT_MENU(CLOSE,  mTaskBarIcon::OnClose)
    EVT_MENU(HIDE,  mTaskBarIcon::OnHide)
    EVT_TASKBAR_LEFT_DOWN(mTaskBarIcon::OnLButtonClick)
    EVT_TASKBAR_MOVE(mTaskBarIcon::OnMouseMove)
END_EVENT_TABLE()

mTaskBarIcon::mTaskBarIcon(MainFrame *frame)
{
    mainframe = frame;
};

void mTaskBarIcon::OnLButtonClick(wxTaskBarIconEvent&)
{
    //wxCommandEvent event;
    //OnHide(event);
}

void mTaskBarIcon::OnMouseMove(wxTaskBarIconEvent&)
{
    /*wxString taskTip = APP_NAME;
    #ifdef __WXMSW__
        SetIcon(wxIcon(logo),taskTip);
    #else
        SetIcon(wxIcon(logo16),taskTip);
    #endif*/
}

wxMenu *mTaskBarIcon::CreatePopupMenu()
{
    wxMenu *traymenu = new wxMenu;
    #ifndef __WXMAC__
        wxMenuItem *mnuhide;
        if (mainframe)
        {
            if (mainframe->IsShown())
                mnuhide = new wxMenuItem(traymenu,HIDE, _("Hide the main window"));
            else
                mnuhide = new wxMenuItem(traymenu,HIDE, _("Show the main window"));
            wxMenuItem *mnuclose = new wxMenuItem(traymenu,CLOSE, _("E&xit"));
            mnuclose->SetBitmap(wxBitmap(exit_xpm));
            traymenu->Append(mnuhide);
            traymenu->AppendSeparator();
            traymenu->Append(mnuclose);
        }
    #endif
    return traymenu;
}

void mTaskBarIcon::OnClose(wxCommandEvent& event)
{
    if (mainframe)
        mainframe->Close();
}

void mTaskBarIcon::OnHide(wxCommandEvent& event)
{
    if (mainframe)
    {
        if (mainframe->IsShown())
        {
            //if (mainframe->IsActive())
            {
                restoring = true;
                mainframe->Hide();
            }
        }
        else
        {
            restoring = true;
            if (mainframe->IsIconized())
                mainframe->Iconize(false);
            mainframe->Show();
            restoring = false;
            //mainframe->RequestUserAttention();
        }
    }
}
