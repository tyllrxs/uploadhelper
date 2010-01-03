AUTOMAKE_OPTIONS=foreign

bin_PROGRAMS=UploadHelper

UploadHelper_SOURCES=AboutDialog.cpp \
CheckNewRelease.cpp \
ConfigDialog.cpp \
DnDFile.cpp \
LoginDialog.cpp \
MainFrame.cpp \
MyListCtrl.cpp \
TaskBarIcon.cpp \
UploadHelperApp.cpp \
UploadHelperApp.h \
UploadThread.cpp \
UtilFunctions.cpp

install-exec-hook:
	mkdir -p /usr/share/uploadhelper/
	cp board_list.xml /usr/share/uploadhelper/ && \
	cp -R lang/ /usr/share/uploadhelper/
