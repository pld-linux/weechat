# TODO:
# - consider doing subpackages for all those plugins (which one should be in main package ?)
#
# Conditional build:
# Features
%bcond_without	aspell	# don't build aspell support
%bcond_without	gtk	# build gtk support
%bcond_without	gnutls	# don't build gnutls support
%bcond_without	doc	# don't build docs
# Bindings
%bcond_without	guile	# don't enable Scheme (guile) scripting language
%bcond_without	lua	# don't enable Lua scripting language
%bcond_without	perl	# don't enable Perl scripting language
%bcond_without	python	# don't enable Python scripting language
%bcond_without	ruby	# don't enable Ruby scripting language
%bcond_without	tcl	# don't enable Tcl scripting language

Summary:	WeeChat - fast and light chat environment
Summary(pl.UTF-8):	WeeChat - szybkie i lekkie środowisko do rozmów
Name:		weechat
Version:	0.4.0
Release:	1
License:	GPL v3+
Group:		Applications/Communications
Source0:	http://www.weechat.org/files/src/%{name}-%{version}.tar.gz
# Source0-md5:	6d3c0f338d4ec3fb3386becd1efa6ae1
Patch0:		%{name}-ac.patch
Patch1:		%{name}-plugins_header.patch
Patch2:		%{name}-curses.patch
URL:		http://www.weechat.org/
%{?with_aspell:BuildRequires:	aspell-devel}
BuildRequires:	cmake
BuildRequires:	curl-devel
BuildRequires:	gettext-devel
%{?with_gnutls:BuildRequires:	gnutls-devel}
%{?with_gtk:BuildRequires:	gtk+2-devel}
%{?with_guile:BuildRequires:	guile-devel}
BuildRequires:	libatomic_ops
BuildRequires:	libgcrypt-devel
%{?with_lua:BuildRequires:	lua51-devel}
BuildRequires:	ncurses-devel
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
%endif
BuildRequires:	rpmbuild(macros) >= 1.129
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	tcl-devel
Requires:	%{name}-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	ruby.so.0.0.0

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
WeeChat common files for Curses and GTK UI.

%package doc
Summary:	Manual for weechat
Group:		Documentation

%description doc
HTML documentation for weechat.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0

%{__sed} -i -e 's#PYTHON_LIB=.*#PYTHON_LIB=%{_libdir}#g' configure.in
%{__sed} -i -e 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/' configure.in

%if %{without gtk}
echo 'AC_DEFUN([AM_PATH_GTK_2_0],[])' >> acinclude.m4
%endif

%build
install -d build
cd build
%cmake \
	-DPREFIX=%{_prefix} \
	-DLIBDIR=%{_libdir} \
	-DENABLE_NCURSES=ON \
	-DENABLE_ASPELL=%{?with_aspell:ON}%{!?with_aspell:OFF} \
	-DENABLE_GTK=%{?with_gtk:ON}%{!?with_gtk:OFF} \
	-DENABLE_GNUTLS=%{?with_gnutls:ON}%{!?with_gnutls:OFF} \
	-DENABLE_DOC=%{?with_doc:ON}%{!?with_doc:OFF} \
	-DENABLE_PERL=%{?with_perl:ON}%{!?with_perl:OFF} \
	-DENABLE_PYTHON=%{?with_python:ON}%{!?with_python:OFF} \
	-DENABLE_RUBY=%{?with_ruby:ON}%{!?with_ruby:OFF} \
	-DENABLE_LUA=%{?with_lua:ON}%{!?with_lua:OFF} \
	-DENABLE_GUILE=%{?with_guile:ON}%{!?with_guile:OFF} \
	-DENABLE_TCL=%{?with_tcl:ON}%{!?with_tcl:OFF} \
	..

%{__make} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# no -devel, drop
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/%{name}.pc

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
%doc AUTHORS ChangeLog NEWS README
%dir %{_libdir}/weechat
%dir %{_libdir}/weechat/plugins
%attr(755,root,root) %{_libdir}/weechat/plugins/alias.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/charset.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/fifo.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/irc.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/logger.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/relay.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/rmodifier.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/script.so*
%attr(755,root,root) %{_libdir}/weechat/plugins/xfer.so*

# addons
%{?with_aspell:%attr(755,root,root) %{_libdir}/weechat/plugins/aspell.so*}

# language bindings
%{?with_guile:%attr(755,root,root) %{_libdir}/weechat/plugins/guile.so*}
%{?with_lua:%attr(755,root,root) %{_libdir}/weechat/plugins/lua.so*}
%{?with_perl:%attr(755,root,root) %{_libdir}/weechat/plugins/perl.so*}
%{?with_python:%attr(755,root,root) %{_libdir}/weechat/plugins/python.so*}
%{?with_ruby:%attr(755,root,root) %{_libdir}/weechat/plugins/ruby.so*}
%{?with_tcl:%attr(755,root,root) %{_libdir}/weechat/plugins/tcl.so*}

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/%{name}
%lang(de) %{_docdir}/%{name}/*.de.html
%lang(en) %{_docdir}/%{name}/*.en.html
%lang(es) %{_docdir}/%{name}/*.es.html
%lang(fr) %{_docdir}/%{name}/*.fr.html
%lang(it) %{_docdir}/%{name}/*.it.html
%lang(ja) %{_docdir}/%{name}/*.ja.html
%lang(pl) %{_docdir}/%{name}/*.pl.html
%lang(ru) %{_docdir}/%{name}/*.ru.html
%endif
