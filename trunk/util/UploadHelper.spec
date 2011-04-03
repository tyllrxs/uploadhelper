Name:    UploadHelper
Version: 4.0
Release: 0
Summary: An open-source, cross-platform program to simplify the uploading work
Vendor:  tyllrxs@gmail.com
Packager:tyllrxs@gmail.com
Group:   Applications/Internet
License: GPL
Icon:    uploadhelper.xpm
URL:     http://homepage.fudan.edu.cn/~tyllr/uh/
Requires:  /bin/sh,/usr/bin/python,python>=2.5,pygtk2
BuildArch: noarch

%description
UploadHelper shares the joy of uploading:)
*) Multiple files uploading simutaneously;
*) Drag&drop operation style;
*) Reship webpage fraction just by one-click. 

%clean
exit 0

%files
/

%post
ln -sf /usr/share/uploadhelper/uploadhelper /usr/bin/uploadhelper
