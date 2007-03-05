%bcond_without	qt	# don't build qt support
%bcond_without	ncurses	# don't build ncurses support
%bcond_without	ruby	# don't build ruby plugin support
%bcond_without	lua	# don't build lua plugin support
%bcond_without	perl	# don't build perl plugin support
%bcond_without	python	# don't build python plugin support
%bcond_without	gnutls	# don't build gnutls support

Summary:	WeeChat
Summary(pl.UTF-8):	WeeChat
Name:		weechat
Version:	0.2.3
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	http://weechat.flashtux.org/download/%{name}-%{version}.tar.bz2
# Source0-md5:	12c39b30988d78e9544acda6e518476f
URL:		http://weechat.flashtux.org/
%{?with_lgnutls:BuildRequires:	gnutls-devel}
%{?with_lua:BuildRequires:	lua-devel}
%{?with_ncurses:BuildRequires:	ncurses-devel}
%{?with_perl:BuildRequires:	perl-devel}
%{?with_python:BuildRequires:	python-devel}
%{?with_qt:BuildRequires:	qt-devel}
BuildRequires:	rpmbuild(macros) >= 1.129
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WeeChat (Wee Enhanced Environment for Chat) is a fast and light chat
environment for many operating systems. Everything can be done with a keyboard.
It is customizable and extensible with scripts.

#%description -l pl.UTF-8

%prep
%setup -q

%build
%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--enable-plugins \
	--with-qt-libraries=%{_libdir} \
	--%{?with_qt:en}%{!?with_qt:dis}able-qt \
	--%{?with_ncurses:en}%{!?with_ncurses:dis}able-ncurses \
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

rm -f $RPM_BUILD_ROOT%{_libdir}/weechat/plugins/*.a

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README FAQ AUTHORS BUGS INSTALL NEWS TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/weechat/plugins
%attr(755,root,root) %{_libdir}/weechat/plugins/*.so*
%{_libdir}/weechat/plugins/*.la
%{_mandir}/man1/*.1.gz
