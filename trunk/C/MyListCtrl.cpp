//
// C++ Implementation: ListCtrl
//
// Description: Implements the class ListCtrl, with extra functions added.
//

#include "UploadHelperApp.h"

BEGIN_EVENT_TABLE(mListCtrl, wxListView)
    //EVT_MOTION(mListCtrl::OnMouseMove)
    //EVT_TIMER(TIP_TIMER, mListCtrl::OnTimer)
    EVT_MENU(REVSEL, mListCtrl::RemoveSelected)
    EVT_MENU(REVALL, mListCtrl::RemoveAll)
    EVT_MENU(REVDUP, mListCtrl::RemoveDup)
    EVT_MENU(REVINV, mListCtrl::RemoveInvalid)
    EVT_LIST_ITEM_RIGHT_CLICK(LISTCTRL_UPFILE, mListCtrl::OnRClick)
    EVT_LIST_KEY_DOWN(LISTCTRL_UPFILE, mListCtrl::OnKeyDown)
    EVT_LIST_BEGIN_DRAG(LISTCTRL_UPFILE, mListCtrl::OnBeginDrag)
    EVT_LIST_COL_CLICK(LISTCTRL_UPFILE, mListCtrl::OnColumnClick)
END_EVENT_TABLE()

// struct used as user-data for columns
struct customListEntry
{
  customListEntry(long i, const wxString& col1, const wxString& col2, const wxString& col3, const wxString& col4, const wxString& col5, const wxString& col6, const wxString& col7)
  {
    index = i;
    column_texts[0] = col1;
    column_texts[1] = col2;
    column_texts[2] = col3;
    column_texts[3] = col4;
    column_texts[4] = col5;
    column_texts[5] = col6;
    column_texts[6] = col7;
  }

  // the entry's index
  long index;
  // keeps the text for each column after 0
  wxString column_texts[7];
}; // customListEntry

void mListCtrl::AddFileItem(const wxArrayString& paths, long index)
{
    long base;
    if(index<0 || index>=GetItemCount())
        base=GetItemCount();
    else
        base=index;
    for (long i=0; i<paths.GetCount(); i++)
    {
        long idx=InsertItem(base+i,wxString::Format(_T("%d"),base+i+1),-1);
        SetItem(idx,1,paths[i]);
        wxFileName myfile(paths[i]);
        SetItem(idx,2,myfile.GetHumanReadableSize());
        if(myfile.GetSize()>1024*1024 && UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("file_unsupport_warning"), true))
            SetItemTextColour(idx, *wxRED);
        wxDateTime dtA, dtM, dtC;
        if(!myfile.GetTimes(&dtA, &dtM, &dtC))
            return;
        SetItem(idx,3,dtM.Format());
        SetItem(idx,4,dtC.Format());
        SetItem(idx,5,dtA.Format());
        SetItemData(idx,(long)new customListEntry(idx,
                                                                                    wxString::Format(_T("%d"),base+i+1),
                                                                                    paths[i],
                                                                                    myfile.GetSize().ToString(),
                                                                                    wxString::Format(_T("%ld"),dtM.GetTicks()),
                                                                                    wxString::Format(_T("%ld"),dtC.GetTicks()),
                                                                                    wxString::Format(_T("%ld"),dtA.GetTicks()),
                                                                                    wxEmptyString));
    }
    AutoListNumber();
}

void mListCtrl::OnMouseMove(wxMouseEvent& event)
{
    tipTimer.Stop();
    int flags;
    if(wxNOT_FOUND == HitTest(event.GetPosition(), flags) || !(flags & wxLIST_HITTEST_ONITEM))
        return;
    imgfile=GetCellText(HitTest(event.GetPosition(), flags));
    tipTimer.Start(100, wxTIMER_ONE_SHOT);
}

void mListCtrl::OnTimer(wxTimerEvent& event)
{
    if(imgfile.IsEmpty())
        return;
    wxMenu *focusemenu = new wxMenu;
    wxMenuItem *mnuThumbnail=new wxMenuItem(focusemenu,MENU_THUMBNAIL, wxEmptyString);
    mnuThumbnail->SetBitmap(wxBitmap(wxImage(imgfile).Scale(128, 128)));
    focusemenu->Append(mnuThumbnail);
    PopupMenu(focusemenu, 8, 8);
}

void mListCtrl::RemoveSelected(wxCommandEvent& event)
{
    for(long i=GetItemCount()-1; i>=0; i--)
    {
        if(IsSelected(i))
            DeleteItem(i);
    }
    AutoListNumber();
}

void mListCtrl::RemoveAll(wxCommandEvent& event)
{
    DeleteAllItems();
}

void mListCtrl::RemoveDup(wxCommandEvent& event)
{
    for(long i=GetItemCount()-1; i>=0; i--)
    {
        for(long j=i-1; j>=0; j--)
        {
            #ifdef __WXMSW__
            if(0 == GetCellText(i).CmpNoCase(GetCellText(j)))
            #else
            if(0 == GetCellText(i).Cmp(GetCellText(j)))
            #endif
            {
                DeleteItem(i);
                break;
            }
        }
    }
    AutoListNumber();
}

void mListCtrl::RemoveInvalid(wxCommandEvent& event)
{
    for(long i=GetItemCount()-1; i>=0; i--)
    {
        if(!wxFile::Exists(GetCellText(i)))
            DeleteItem(i);
    }
    AutoListNumber();
}

void mListCtrl::DeselectAll()
{
    for(long i=GetItemCount()-1; i>=0; i--)
        Select(i, false);
}

void mListCtrl::AutoListNumber()
{
    for(long i=0; i<GetItemCount(); i++)
    {
        SetItemText(i, wxString::Format(_T("%d"),i+1));
    }
}

void mListCtrl::OnRClick(wxListEvent& event)
{
    wxMenu *upfilemenu = new wxMenu;
    if(GetFirstSelected() >= 0)
    {
        int flags;
        wxString fname=GetCellText(HitTest(event.GetPoint(), flags));
        wxMenuItem *mnuRemoveSelected=new wxMenuItem(upfilemenu,REVSEL, _("Selected\tDel"));
        if(!UploadHelperApp::Configurations(READ, _T("Miscellaneous"), _T("context_menu_thumbnail"), true)
            || fname.IsEmpty() || !IS_IMAGE_FILE(fname))
            mnuRemoveSelected->SetBitmap(wxBitmap(delete_xpm));
        else
        {
            int w=wxImage(fname).GetWidth();
            int h=wxImage(fname).GetHeight();
            if(w>=h && w>128)
            {
                h=h*128/w;
                w=128;
            }
            else
            {
                if(w<h && h>128)
                {
                    w=w*128/h;
                    h=128;
                }
            }
            mnuRemoveSelected->SetBitmap(wxBitmap(wxImage(fname).Scale(w, h)));
        }
        upfilemenu->Append(mnuRemoveSelected);
    }
    if(GetItemCount() > 0)
    {
        wxMenuItem *mnuRemoveAll=new wxMenuItem(upfilemenu,REVALL, _("All\tShift+Del"));
        mnuRemoveAll->SetBitmap(wxBitmap(delete_xpm));
        upfilemenu->Append(mnuRemoveAll);
    }
    if(upfilemenu->GetMenuItemCount() > 0)
        PopupMenu(upfilemenu);
}

void mListCtrl::OnKeyDown(wxListEvent& event)
{
    wxCommandEvent evt;
    if(WXK_DELETE == event.GetKeyCode())
    {
        if(wxGetKeyState(WXK_SHIFT))
            RemoveAll(evt);
        else
            RemoveSelected(evt);
    }
}

void mListCtrl::OnBeginDrag(wxListEvent& event)
{
    const wxPoint& pt = event.m_pointDrag;
    int flags;
    long itm=HitTest(pt, flags);
    if(itm<0)
        return;
    wxFileDataObject my_data;
    wxString ori_fname=GetCellText(itm, 1);
    my_data.AddFile(ori_fname);
    wxDropSource dragSource(this);
	dragSource.SetData(my_data);
	wxDragResult result = dragSource.DoDragDrop(wxDragCopy);
	if(result==wxDragCopy)
        if(0==ori_fname.CmpNoCase(GetCellText(itm, 1)))
            DeleteItem(itm);
        else
            DeleteItem(itm+1);
    AutoListNumber();
}

int wxCALLBACK CompareItems(long item1, long item2, long data)
{
    mListCtrl* mylist = (mListCtrl*) data;
    customListEntry* list1 = (customListEntry*) item1;
    customListEntry* list2 = (customListEntry*) item2;
    if(!list1)
        return -1;
    if(!list2)
        return 1;

    long col  = mylist->GetSortColumn();
    bool ascending = mylist->GetSortAscending();

    int ret;
    switch(col)
    {
        case 1:
        case 6:
            ret = list1->column_texts[col].CmpNoCase(list2->column_texts[col]);
            break;
        case 2:
        case 3:
        case 4:
        case 5:
            unsigned long sz1, sz2;
            list1->column_texts[col].ToULong(&sz1);
            list2->column_texts[col].ToULong(&sz2);
            ret = (sz1>sz2) ? 1 : -1;
            break;
        default:
            ret = 0;
    }

    if(ascending)
        return ret;
    else
        return -ret;
}

void mListCtrl::OnColumnClick(wxListEvent& event)
{
    if (event.GetColumn() != iSortColumn)
        bSortAscending = true;
    else
        bSortAscending = !bSortAscending;

    iSortColumn = event.GetColumn();
    if(iSortColumn<=0)
        return;

    wxBusyInfo wait(_("Please wait, sorting..."));
    SortItems(CompareItems, (long)this);
    AutoListNumber();
}

wxString mListCtrl::GetCellText(const long row, const long col)
{
    if(row<0 || col<0)
        return wxEmptyString;
    wxListItem lst;
    lst.m_itemId=row;
    lst.m_col=col;
    lst.m_mask=wxLIST_MASK_TEXT;
    GetItem(lst);
    return lst.m_text;
}

wxString mListCtrl::UploadFiles(const wxString strBoard)
{
    if(strBoard.IsEmpty())
    {
        wxMessageBox(ERR_BOARD);
        return wxEmptyString;
    }

    wxGetApp().ReadUserInfo();
    wxString rslt;
    for (long i=0; i<GetItemCount(); i++)
    {
        SetItem(i,6, STATUS_PREPARE);
        Update();

        std::string buffer;
        wxString strFile=GetCellText(i);

        strFile=MyUtilFunc::ProcessImage(strFile);
        if(strFile.IsEmpty())
        {
            SetItem(i,6, STATUS_UPLOAD_FAIL);
            Update();
            continue;
        }

        if(wxFileName(strFile).GetSize()>1024*1024)
        {
            SetItem(i,6, STATUS_SKIP);
            Update();
            continue;
        }
        else
        {
            SetItemTextColour(i, *wxBLACK);
        }

        struct curl_httppost *formpost=NULL, *lastptr=NULL;
        /* Fill in the file upload field */
        curl_formadd(&formpost, &lastptr,
                     CURLFORM_COPYNAME, "up",
                     CURLFORM_FILE, MyUtilFunc::WX2pChar(strFile),
                     CURLFORM_FILENAME, MyUtilFunc::WX2pChar(strFile),
                     CURLFORM_END);

        curl_formadd(&formpost, &lastptr,
                     CURLFORM_COPYNAME, "board",
                     CURLFORM_COPYCONTENTS, MyUtilFunc::WX2pChar(strBoard),
                     CURLFORM_END);

        SetItem(i,6, STATUS_UPLOAD);
        SetItemColumnImage(i,6,4);
        Update();

        CURL* curl;
        CURLcode res;
        curl = curl_easy_init();
        if (curl)
        {
            curl_easy_setopt(curl, CURLOPT_URL, MyUtilFunc::WX2pChar(wxGetApp().progOptions.bbs_url+_T("bbsupload")));
            //curl_easy_setopt(curl, CURLOPT_VERBOSE, 1);
            curl_easy_setopt(curl, CURLOPT_COOKIE, MyUtilFunc::WX2pChar(wxGetApp().progOptions.user_cookie));
            curl_easy_setopt(curl, CURLOPT_HTTPPOST, formpost);
            if(UploadHelperApp::Configurations(READ, _T("General"), _T("proxy"), false))
            {
                wxString proxyAddr, proxyUser;
                proxyAddr=UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_addr"), wxEmptyString);
                proxyUser=UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_user"), wxEmptyString);
                if(!proxyAddr.IsEmpty())
                {
                    proxyAddr+=_T(":")+UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_port"), wxEmptyString);
                    curl_easy_setopt(curl, CURLOPT_PROXY, MyUtilFunc::WX2pChar(proxyAddr));
                    if(!proxyUser.IsEmpty())
                    {
                        proxyUser+=_T(":")+UploadHelperApp::Configurations(READ, _T("General"), _T("proxy_pwd"), wxEmptyString);
                        curl_easy_setopt(curl, CURLOPT_PROXYUSERPWD, MyUtilFunc::WX2pChar(proxyUser));
                    }
                }
            }
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, MyUtilFunc::writer);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);
            res = curl_easy_perform(curl);
            /* always cleanup */
            curl_easy_cleanup(curl);
            /* then cleanup the formpost chain */
            curl_formfree(formpost);

            //Failed to connect to server
            if (CURLE_OK != res)
            {
                wxMessageBox(ERR_NETWORK);
                return wxEmptyString;
            }

            wxString resHTML(buffer.c_str(),wxCSConv(BBS_CODEPAGE));
            //Server tells error in response info
            if (wxNOT_FOUND != resHTML.Find(_T("错误")) || wxNOT_FOUND != resHTML.Find(_T("Nothing Here")))
            {
                wxMessageBox(MyUtilFunc::TrimHTML(resHTML));
                SetItem(i,6, STATUS_UPLOAD_FAIL);
                SetItemColumnImage(i,6,3);
                Update();
                continue;
            }

            //Upload successfully.
            //wxMessageBox(resHTML);
            //Now begin to parse HTML for PIC URL, using "Regular Expression"
            wxRegEx re(_T("n(http:[^\\]+)"));
            if (re.Matches(resHTML))
            {
                rslt += _T("\n") + MyUtilFunc::NewURL(re.GetMatch(resHTML,1));
            }

            SetItem(i,6, STATUS_UPLOADED);
            SetItemColumnImage(i,6,2);
            Update();
        }
    }
    return rslt;
}
