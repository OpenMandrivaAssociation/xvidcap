%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

# Note that disabling these does not cause build failures, but
# other output formats than xwd will be disabled
# embedded ffmpeg vhook modules
%define _disable_ld_no_undefined 1
# FIXME: embedded ffmpeg
%define _disable_ld_as_needed 1

Name:		xvidcap
Summary:	Screen capture video recorder
Version:	1.1.7
Release:	3
Source:		http://downloads.sourceforge.net/xvidcap/%{name}-%{version}.tar.gz
Patch0:		xvidcap-1.1.5-docbook.patch
Patch1:		xvidcap-1.1.7-fix-headers.patch
Patch2:		xvidcap-1.1.5-nawk.patch
Patch3:		xvidcap-1.1.7-desktop-entry.patch
Patch4:		xvidcap-1.1.7-ffmpeg-options.patch
Patch5:		xvidcap-1.1.7-shmstr.patch
URL:		http://xvidcap.sourceforge.net/
License:	GPLv2+
Group:		Video

BuildRequires:	docbook-utils xmlto
BuildRequires:	gtk2-devel 
BuildRequires:	jpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libx11-devel 
BuildRequires:	zlib-devel 
BuildRequires:	libglade2.0-devel
BuildRequires:	libtheora-devel
BuildRequires:	libxmu-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	scrollkeeper
BuildRequires:	intltool
%if %build_plf
BuildRequires: libfaac-devel libfaad2-devel
BuildRequires: x264-devel >= 0.65
BuildRequires: liblame-devel
%endif
BuildConflicts: libffmpeg-devel
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
%if %build_plf

This package is in PLF because it is linked with patented codecs.
%endif

%prep
%setup -q
%patch0 -p0 -b .docbook
%patch1 -p1
%patch2 -p0 -b .fixawk
%patch3 -p1
%patch4 -p1
%patch5 -p0

NOCONFIGURE=yes sh ./autogen.sh
intltoolize --copy --force

%build
%configure2_5x --disable-dependency-tracking --enable-libtheora LIBS="-lX11 -lz"
%make CPPFLAGS=-I`pwd`/ffmpeg

%install
rm -rf %{buildroot} %{name}.lang

%makeinstall_std

chmod 755 %{buildroot}%{_datadir}/%{name}/ppm2mpeg.sh
ln -s %{_datadir}/%{name}/ppm2mpeg.sh %{buildroot}%{_bindir}/ppm2mpeg.sh

rm -fr %{buildroot}/%{_docdir}

for omf in %{buildroot}%{_datadir}/omf/*/*-??.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%{buildroot}!!)" >> %{name}.lang
done

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
%{_bindir}/xvidcap-dbus-client
%{_bindir}/ppm2mpeg.sh
%_datadir/dbus-1/services/net.jarre_de_the.Xvidcap.service
%{_mandir}/man1/*
%lang(de) %{_mandir}/de/man1/*
%lang(es) %{_mandir}/es/man1/*
%lang(it) %{_mandir}/it/man1/*
%{_datadir}/applications/xvidcap.desktop
%{_datadir}/%{name}
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*.omf
%{_datadir}/pixmaps/%{name}.png
