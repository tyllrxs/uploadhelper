//
// C++ Implementation: DnDFile
//
// Description: A drag-and-drop class for dragging files (from explorer, nautilus, Finder, etc.) into listctrl
//

#include "UploadHelperApp.h"

DnDFile::DnDFile(mListCtrl *owner)
{
   m_owner = owner;
   bInside = false;
}

wxDragResult DnDFile::OnDragOver(wxCoord x, wxCoord y, wxDragResult def)
{
    wxPoint pt(x, y);
    int flags;
    long itm=m_owner->HitTest(pt, flags);
    m_owner->DeselectAll();
    //m_owner->Select(itm);
    return def;
}

bool DnDFile::OnDropFiles(wxCoord x, wxCoord y, const wxArrayString& filenames)
{
    wxPoint pt(x, y);
    int flags;
    long itm=m_owner->HitTest(pt, flags);
    //m_owner->DeleteItem(m_owner->GetFocusedItem());
    m_owner->AddFileItem(filenames, itm);
    m_owner->DeselectAll();
    if(itm>=0)
        m_owner->Select(itm);
    else
        m_owner->Select(m_owner->GetItemCount()-1);
    return true;
}
