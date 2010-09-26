# -*- coding: utf-8 -*-

import cPickle
import wx

	
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# DragList

class DragList(wx.ListCtrl):

    def __init__(self, *arg, **kw):
	wx.ListCtrl.__init__(self, *arg, **kw)
	
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self._startDrag)


    def getItemInfo(self, idx):
        """Collect all relevant data of a listitem, and put it in a list"""
        l = []
        l.append(idx) # We need the original index, so it is easier to eventualy delete it
        l.append(self.GetItemData(idx)) # Itemdata
        l.append(self.GetItemText(idx)) # Text first column
        for i in range(1, self.GetColumnCount()): # Possible extra columns
            l.append(self.GetItem(idx, i).GetText())
        l.append(self.GetItem(idx, 3).GetImage())
        return l

    def _startDrag(self, e):
        """ Put together a data object for drag-and-drop _from_ this list. """
        l = []
        idx = -1
        while True: # find all the selected items and put them in a list
            idx = self.GetNextItem(idx, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if idx == -1:
                break
            l.append(self.getItemInfo(idx))

        # Pickle the items list.
        itemdata = cPickle.dumps(l, 1)
        # create our own data format and use it in a
        # custom data object
        ldata = wx.CustomDataObject("ListCtrlItems")
        ldata.SetData(itemdata)
        # Now make a data object for the  item list.
        data = wx.DataObjectComposite()
        data.Add(ldata)

        # Create drop source and begin drag-and-drop.
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)
        

    def _insert(self, x, y, seq):
        """ Insert text at given x, y coordinates --- used with drag-and-drop. """

        # Find insertion point.
        index, flags = self.HitTest((x, y))

        if index == wx.NOT_FOUND: # not clicked on an item
            if flags & (wx.LIST_HITTEST_NOWHERE|wx.LIST_HITTEST_ABOVE|wx.LIST_HITTEST_BELOW): # empty list or below last item
                index = self.GetItemCount() # append to end of list
            elif self.GetItemCount() > 0:
                if y <= self.GetItemRect(0).y: # clicked just above first item
                    index = 0 # append to top of list
                else:
                    index = self.GetItemCount() + 1 # append to end of list
        else: # clicked on an item
            # Get bounding rectangle for the item the user is dropping over.
            rect = self.GetItemRect(index)

            # If the user is dropping into the lower half of the rect, we want to insert _after_ this item.
            # Correct for the fact that there may be a heading involved
            if y > rect.y - self.GetItemRect(0).y + rect.height/2:
                index += 1

        for i in seq: # insert the item data
            idx = self.InsertStringItem(index, i[2])
            self.SetItemData(idx, i[1])
            for j in range(1, self.GetColumnCount()):
                try: # Target list can have more columns than source
                    if j == 3:
                	img = i[6]
                    else:
                	img = -1
                    self.SetStringItem(idx, j, i[2+j], img)
                except:
                    pass # ignore the extra columns
            index += 1
        
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ListDrop

class ListDrop(wx.FileDropTarget):
    """ Drop target for simple lists. """

    def __init__(self, source):
        """ Arguments:
         - source: source listctrl.
        """
        wx.FileDropTarget.__init__(self)
        self.dv = source
        
	# copy the data from the drag source to our data object
        # specify the type of data we will accept    
	self.data = DropData()
	self.SetDataObject(self.data)         

    # Called when OnDrop returns True.  We need to get the data and
    # do something with it.
    def OnData(self, x, y, d):

        if self.GetData():
		recv = self.data.GetReceivedFormat()
		if recv == wx.DataFormat(wx.DF_FILENAME):
		    d = self.OnDropFiles(x, y, self.data.fileDat.GetFilenames())
		else:
		    #self.data = wx.CustomDataObject("ListCtrlItems")
		    #self.SetDataObject(self.data)  
		    # convert it back to a list and give it to the viewer      
		    ldata = self.data.customDat.GetData()
		    l = cPickle.loads(ldata)
		    self.dv._insert(x, y, l)
		    
		    # If move, we want to remove the item from this list.
		    if d == wx.DragMove:
			    # It's possible we are dragging/dropping from this list to this list.  In which case, the
			    # index we are removing may have changed...

			    # Find correct position.
			    l.reverse() # Delete all the items, starting with the last item
			    for i in l:
				pos = self.dv.FindItem(i[0], i[2])
				self.dv.DeleteItem(pos)	
                
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d
        
        
    def OnDropFiles(self, x, y, paths):
	wx.GetApp().GetTopWindow().append_files(paths)
	
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

class DropData(wx.DataObjectComposite):

    def __init__(self):
    
	wx.DataObjectComposite.__init__(self)
	self.customDat=wx.CustomDataObject("ListCtrlItems")
	self.Add(self.customDat)
	self.fileDat=wx.FileDataObject()
	self.Add(self.fileDat)
