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
#
Summary:	WeeChat - fast and light chat environment
Summary(pl.UTF-8):	WeeChat - szybkie i lekkie środowisko do rozmów
Name:		weechat
Version:	0.2.6.1
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://weechat.flashtux.org/download/%{name}-%{version}.tar.bz2
# Source0-md5:	6cf818482feb6a6ef90b70694d25c7e9
Patch0:		%{name}-ac.patch
URL:		http://weechat.flashtux.org/
%{?with_aspell:BuildRequires:	aspell-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-style-xsl
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
Group:		X11/Applications
Requires:	%{name}-common = %{version}-%{release}

%description gtk
GTK WeeChat UI.

%package common
Summary:	WeeChat common files
Group:		X11/Applications

%description common
WeeChat common files.

%prep
%setup -q
%patch0 -p1
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
	--with-doc-xsl-prefix=%{_datadir}/sgml/docbook/xsl-stylesheets \
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--disable-static \
	--enable-plugins \
	--with-qt-libraries=%{_libdir} \
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf html-doc
mv $RPM_BUILD_ROOT%{_datadir}/doc/weechat html-doc

rm -f $RPM_BUILD_ROOT%{_libdir}/weechat/plugins/*.la

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
%doc AUTHORS BUGS FAQ NEWS README TODO
%doc html-doc/*
%dir %{_libdir}/weechat
%dir %{_libdir}/weechat/plugins
%attr(755,root,root) %{_libdir}/weechat/plugins/aspell.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/charset.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/lua.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/perl.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/python.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/ruby.so*
