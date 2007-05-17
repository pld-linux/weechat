#
# TODO:
# - consider doing subpackages for all those plugins (which one should be in main package ?)
# - maybe some other BRs ?
#
# Conditional build:
%bcond_without	aspell	# don't build aspell support
%bcond_without	qt	# don't build qt support
%bcond_without	ruby	# don't build ruby plugin support
%bcond_without	lua	# don't build lua plugin support
%bcond_without	perl	# don't build perl plugin support
%bcond_without	python	# don't build python plugin support
%bcond_without	gnutls	# don't build gnutls support
#
Summary:	WeeChat - fast and light chat environment
Summary(pl.UTF-8):	WeeChat - szybkie i lekkie środowisko do rozmów
Name:		weechat
Version:	0.2.3
Release:	0.3
License:	GPL
Group:		X11/Applications
Source0:	http://weechat.flashtux.org/download/%{name}-%{version}.tar.bz2
# Source0-md5:	12c39b30988d78e9544acda6e518476f
URL:		http://weechat.flashtux.org/
%{?with_aspell:BuildRequires:	aspell-devel}
%{?with_lgnutls:BuildRequires:	gnutls-devel}
%{?with_lua:BuildRequires:	lua-devel}
BuildRequires:	ncurses-devel
%{?with_perl:BuildRequires:	perl-devel}
%{?with_python:BuildRequires:	python-devel}
%{?with_qt:BuildRequires:	qt-devel}
BuildRequires:	rpmbuild(macros) >= 1.129
%{?with_ruby:BuildRequires:	ruby-devel}
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

%prep
%setup -q

%build
%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--disable-static \
	--enable-plugins \
	--with-qt-libraries=%{_libdir} \
	--%{?with_qt:en}%{!?with_qt:dis}able-qt \
	--enable-ncurses \
	--%{?with_aspell:en}%{!?with_aspell:dis}able-aspell \
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

rm -f $RPM_BUILD_ROOT%{_libdir}/weechat/plugins/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS FAQ NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/weechat/plugins
%attr(755,root,root) %{_libdir}/weechat/plugins/*.so*
%{_mandir}/man1/*.1*
