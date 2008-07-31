%define name	xvidcap
%define version	1.1.6
%define release %mkrel 3

Name:		%{name}
Summary:	Screen capture video recorder
Version:	%{version}
Release:	%{release}
Source:		http://downloads.sourceforge.net/xvidcap/%{name}-%{version}.tar.bz2
Patch0:		xvidcap-1.1.5-docbook.patch
Patch2:		xvidcap-1.1.5-nawk.patch
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
Requires:	mplayer
Requires:	mencoder
Requires:	ffmpeg
Requires:	imagemagick

%description
xvidcap is a screen capture enabling you to capture videos off your X-Window
desktop for illustration or documentation purposes. It is intended to be a
standards-based alternative to tools like Lotus ScreenCam.

%prep
%setup -q
%patch0 -p0 -b .docbook
%patch2 -p0 -b .fixawk

sh ./autogen.sh

%build
%configure2_5x \
	--with-forced-embedded-ffmpeg

%make

%install
rm -rf %{buildroot} %{name}.lang

%makeinstall_std

chmod 755 %{buildroot}%{_datadir}/%{name}/ppm2mpeg.sh
ln -s %{_datadir}/%{name}/ppm2mpeg.sh %{buildroot}%{_bindir}/ppm2mpeg.sh

rm -fr %{buildroot}/%{_docdir}

for omf in %{buildroot}%{_datadir}/omf/*/*-??.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%{buildroot}!!)" >> %{name}.lang
done

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %{name} --with-gnome

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_scrollkeeper	
%endif
	
%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}
%{_bindir}/ppm2mpeg.sh
%{_mandir}/man1/*
%lang(de) %{_mandir}/de/man1/*
%lang(es) %{_mandir}/es/man1/*
%lang(it) %{_mandir}/it/man1/*
%{_datadir}/applications/xvidcap.desktop
%{_datadir}/%{name}
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*.omf
%{_datadir}/pixmaps/%{name}.png
