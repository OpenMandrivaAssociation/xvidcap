%define name	xvidcap
%define version	1.1.4
%define release %mkrel 3

Name: 	 	%{name}
Summary: 	Screen capture video recorder
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
Patch0:		xvidcap-1.1.4-docbook.patch
Patch1:		xvidcap-1.1.4-asneeded.patch
Patch2:		xvidcap-1.1.4-nawk.patch
URL:		http://xvidcap.sourceforge.net/
License:	GPL
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	docbook2x
BuildRequires:	gtk2-devel jpeg-devel png-devel zlib-devel 
BuildRequires:	libglade2.0-devel
BuildRequires:	libxmu-devel
BuildRequires:	desktop-file-utils
BuildRequires:	scrollkeeper
BuildRequires:	perl-XML-Parser
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Requires: mplayer
Requires: mencoder
Requires: ffmpeg
Requires: ImageMagick

%description
xvidcap is a screen capture enabling you to capture videos off your X-Window
desktop for illustration or documentation purposes. It is intended to be a
standards-based alternative to tools like Lotus ScreenCam.

%prep
%setup -q
%patch0 -p1 -b .docbook
%patch1 -p1 -b .asneeded
%patch2 -p1 -b .fixawk

aclocal && autoconf && automake -a -c

%build
%configure2_5x --with-forced-embedded-ffmpeg
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall

chmod 755 %buildroot/%{_datadir}/%{name}/ppm2mpeg.sh
ln -s %{_datadir}/%{name}/ppm2mpeg.sh $RPM_BUILD_ROOT%{_bindir}/ppm2mpeg.sh

rm -fr $RPM_BUILD_ROOT/%_docdir
%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/*/*-??.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name.lang
done

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="xvidcap" icon="video_section.png" needs="x11" title="XVidCap" longtitle="Screen Capture Video Recorder" section="Multimedia/Video" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_scrollkeeper	
	
%postun
%clean_menus
%clean_scrollkeeper

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%name
%{_bindir}/ppm2mpeg.sh
%{_mandir}/man1/*
%lang(de) %{_mandir}/de/man1/*
%lang(es) %{_mandir}/es/man1/*
%lang(it) %{_mandir}/it/man1/*
%_datadir/applications/xvidcap.desktop
%_datadir/%name
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/pixmaps/%name.png
%{_menudir}/%name


