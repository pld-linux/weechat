%bcond_without	qt	# don't build qt support
%bcond_without	ncurses	# don't build ncurses support

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
#BuildRequires:	autoconf
#BuildRequires:	automake
%{?with_ncurses:BuildRequires:	ncurses-devel}
BuildRequires:	perl-devel
BuildRequires:	python-devel
%{?with_qt:BuildRequires:	qt-devel}
BuildRequires:	rpmbuild(macros) >= 1.129
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
	--with-qt-libraries=%{_libdir} \
	--%{?with_qt:en}%{!?with_qt:dis}able-qt \
	--%{?with_ncurses:en}%{!?with_ncurses:dis}able-ncurses
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
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/weechat/plugins
%attr(755,root,root) %{_libdir}/weechat/plugins/*.so*
%{_libdir}/weechat/plugins/*.la
%{_mandir}/man1/*.1.gz
