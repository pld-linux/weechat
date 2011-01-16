#
# TODO:
# - consider doing subpackages for all those plugins (which one should be in main package ?)
#
# Conditional build:
%bcond_without	aspell	# don't build aspell support
%bcond_without	gtk	# build gtk support
%bcond_with	qt	# don't build qt support
%bcond_without	ruby	# don't build ruby plugin support
%bcond_without	lua	# don't build lua plugin support
%bcond_without	perl	# don't build perl plugin support
%bcond_without	python	# don't build python plugin support
%bcond_without	gnutls	# don't build gnutls support

%define		skip_post_check_so	ruby.so.0.0.0

Summary:	WeeChat - fast and light chat environment
Summary(pl.UTF-8):	WeeChat - szybkie i lekkie środowisko do rozmów
Name:		weechat
Version:	0.3.4
Release:	1
License:	GPL v3+
Group:		Applications/Communications
Source0:	http://www.weechat.org/files/src/%{name}-%{version}.tar.gz
# Source0-md5:	a36a89b6012994dc67c4c0ea36784d1d
Patch0:		%{name}-ac.patch
Patch1:		%{name}-plugins_header.patch
Patch2:		%{name}-curses.patch
URL:		http://www.weechat.org/
%{?with_aspell:BuildRequires:	aspell-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
%{?with_gnutls:BuildRequires:	gnutls-devel}
%{?with_gtk:BuildRequires:	gtk+2-devel}
BuildRequires:	libtool
%{?with_lua:BuildRequires:	lua-devel >= 5.0}
BuildRequires:	ncurses-devel
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
%endif
%{?with_qt:BuildRequires:	qt-devel}
BuildRequires:	rpmbuild(macros) >= 1.129
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	tcl-devel
Requires:	%{name}-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WeeChat (Wee Enhanced Environment for Chat) is a fast and light chat
environment for many operating systems. Everything can be done with a
keyboard. It is customizable and extensible with scripts.

%description -l pl.UTF-8
WeeChat (Wee Ehanced Environment for Chat) to szybkie i lekkie
środowisko do rozmów dla wielu systemów operacyjnych. Pozwala wszystko
zrobić przy pomocy klawiatury. Jest konfigurowalne i rozszerzalne za
pomocą skryptów.

%package gtk
Summary:	GTK WeeChat UI
Group:		Applications/Communications
Requires:	%{name}-common = %{version}-%{release}

%description gtk
GTK WeeChat UI.

%package common
Summary:	WeeChat common files
Group:		Applications/Communications

%description common
WeeChat common files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
sed -i -e 's#PYTHON_LIB=.*#PYTHON_LIB=%{_libdir}#g' configure.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--enable-threads=posix \
	--disable-doc \
	--disable-static \
	--%{?with_qt:en}%{!?with_qt:dis}able-qt \
	--enable-ncurses \
	--%{?with_aspell:en}%{!?with_aspell:dis}able-aspell \
	--%{?with_gtk:en}%{!?with_gtk:dis}able-gtk \
	--%{?with_perl:en}%{!?with_perl:dis}able-perl \
	--%{?with_python:en}%{!?with_python:dis}able-python \
	--%{?with_ruby:en}%{!?with_ruby:dis}able-ruby \
	--%{?with_lua:en}%{!?with_lua:dis}able-lua \
	--%{?with_gnutls:en}%{!?with_gnutls:dis}able-gnutls
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/weechat/plugins/*.la
cp doc/weechat-curses.1 $RPM_BUILD_ROOT%{_mandir}/man1

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/weechat-curses
%{_mandir}/man1/weechat-curses.1*

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/weechat-gtk
%endif

%files common -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README UPGRADE_0.3
%dir %{_includedir}/weechat
%dir %{_libdir}/weechat
%dir %{_libdir}/weechat/plugins
%{_includedir}/weechat/weechat-plugin.h
%attr(755,root,root) %{_libdir}/weechat/plugins/alias.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/aspell.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/charset.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/fifo.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/irc.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/logger.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/lua.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/perl.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/python.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/relay.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/rmodifier.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/ruby.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/tcl.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/xfer.so*
%{_pkgconfigdir}/weechat.pc
