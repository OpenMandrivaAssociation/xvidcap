#####################
# Hardcode PLF build
%define build_plf 0
#####################

%{?_with_plf: %{expand: %%global build_plf 1}}

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
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
Release:	5%{?extrarelsuffix}
License:	GPLv2+
Group:		Video
URL:		http://xvidcap.sourceforge.net/
Source0:	http://downloads.sourceforge.net/xvidcap/%{name}-%{version}.tar.gz
Source1:	xvidcap_ru.po
Patch0:		xvidcap-1.1.5-docbook.patch
Patch1:		xvidcap-1.1.7-fix-headers.patch
Patch2:		xvidcap-1.1.5-nawk.patch
Patch3:		xvidcap-1.1.7-desktop-entry.patch
Patch4:		xvidcap-1.1.7-ffmpeg-options.patch
Patch5:		xvidcap-1.1.7-shmstr.patch
Patch6:		xvidcap-1.1.7-glib.patch
Patch7:		xvidcap-1.1.7-add-ru-localization.patch
Patch8:		xvidcap-1.1.7-automake-1.13.patch

BuildRequires:	docbook-utils
BuildRequires:	intltool
BuildRequires:	scrollkeeper
BuildRequires:	xmlto
BuildRequires:	jpeg-devel
BuildRequires:  gettext
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(zlib)
%if %{build_plf}
BuildRequires:	libfaac-devel
BuildRequires:	libfaad2-devel
BuildRequires:	liblame-devel
BuildRequires:	pkgconfig(x264)
%endif
BuildConflicts:	ffmpeg-devel
Requires(post):	scrollkeeper
Requires(postun): scrollkeeper
Requires:	mplayer
Requires:	mencoder
Requires:	ffmpeg
Requires:	imagemagick

%description
xvidcap is a screen capture enabling you to capture videos off your X-Window
desktop for illustration or documentation purposes. It is intended to be a
standards-based alternative to tools like Lotus ScreenCam.

%if %{build_plf}
This package is in Restricted reporitory as it is linked with patented codecs.
%endif

%prep
%setup -q
cp -p %{SOURCE1} po/ru.po
%patch0 -p0 -b .docbook
%patch1 -p1
%patch2 -p0 -b .fixawk
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p1 -b .ru_po
%patch8 -p0

aclocal
autoheader
autoconf
automake --add-missing
cp configure.ac configure.in
# NOCONFIGURE=yes sh ./autogen.sh
intltoolize --copy --force

%build
%configure2_5x --disable-dependency-tracking --enable-libtheora LIBS="-lX11 -lz -lXext"
%make CPPFLAGS=-I`pwd`/ffmpeg

%install
%makeinstall_std

chmod 755 %{buildroot}%{_datadir}/%{name}/ppm2mpeg.sh
ln -s %{_datadir}/%{name}/ppm2mpeg.sh %{buildroot}%{_bindir}/ppm2mpeg.sh

rm -fr %{buildroot}/%{_docdir}

%find_lang %{name} --with-gnome --with-man --all-name

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}
%{_bindir}/xvidcap-dbus-client
%{_bindir}/ppm2mpeg.sh
%{_datadir}/dbus-1/services/net.jarre_de_the.Xvidcap.service
%{_mandir}/man1/*
%{_datadir}/applications/xvidcap.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png

