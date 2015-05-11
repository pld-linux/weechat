# TODO:
# - consider doing subpackages for all those plugins (which one should be in main package ?)
# - desktop file (icon exists, but no desktop file?)
#
# Conditional build:
# Features
%bcond_without	aspell	# don't build aspell support
%bcond_without	gnutls	# don't build gnutls support
%bcond_without	doc	# don't build docs
# Bindings
%bcond_without	guile	# don't enable Scheme (guile) scripting language
%bcond_without	lua	# don't enable Lua scripting language
%bcond_without	perl	# don't enable Perl scripting language
%bcond_without	python	# don't enable Python scripting language
%bcond_without	ruby	# don't enable Ruby scripting language
%bcond_without	tcl	# don't enable Tcl scripting language
%bcond_without	js	# don't enable JavaScript scripting language (V8 engine)

Summary:	WeeChat - fast and light chat environment
Summary(pl.UTF-8):	WeeChat - szybkie i lekkie środowisko do rozmów
Name:		weechat
Version:	1.2
Release:	1
License:	GPL v3+
Group:		Applications/Communications
Source0:	http://www.weechat.org/files/src/%{name}-%{version}.tar.gz
# Source0-md5:	7e561d9093af164c2ab32634ece0e0ef
Patch2:		%{name}-curses.patch
URL:		http://www.weechat.org/
%{?with_doc:BuildRequires:	asciidoc}
%{?with_aspell:BuildRequires:	aspell-devel}
BuildRequires:	cmake
BuildRequires:	curl-devel
BuildRequires:	gettext-tools
%{?with_gnutls:BuildRequires:	gnutls-devel}
%{?with_guile:BuildRequires:	guile-devel}
BuildRequires:	libgcrypt-devel
%{?with_lua:BuildRequires:	lua51-devel}
BuildRequires:	ncurses-devel
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%{?with_doc:BuildRequires:	source-highlight}
%{?with_js:BuildRequires:	v8-devel}
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
%endif
BuildRequires:	rpmbuild(macros) >= 1.129
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	tcl-devel
Obsoletes:	weechat-common
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

%package doc
Summary:	Manual for weechat
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
HTML documentation for weechat.

%prep
%setup -q
%patch2 -p0

%{__sed} -i -e 's#PYTHON_LIB=.*#PYTHON_LIB=%{_libdir}#g' configure.ac
%{__sed} -i -e 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/' configure.ac

%build
install -d build
cd build
%cmake \
	-DPREFIX=%{_prefix} \
	-DLIBDIR=%{_libdir} \
	-DENABLE_NCURSES=ON \
	-DENABLE_ASPELL=%{?with_aspell:ON}%{!?with_aspell:OFF} \
	-DENABLE_GNUTLS=%{?with_gnutls:ON}%{!?with_gnutls:OFF} \
	-DENABLE_DOC=%{?with_doc:ON}%{!?with_doc:OFF} \
	-DENABLE_PERL=%{?with_perl:ON}%{!?with_perl:OFF} \
	-DENABLE_PYTHON=%{?with_python:ON}%{!?with_python:OFF} \
	-DENABLE_RUBY=%{?with_ruby:ON}%{!?with_ruby:OFF} \
	-DENABLE_LUA=%{?with_lua:ON}%{!?with_lua:OFF} \
	-DENABLE_GUILE=%{?with_guile:ON}%{!?with_guile:OFF} \
	-DENABLE_TCL=%{?with_tcl:ON}%{!?with_tcl:OFF} \
	-DENABLE_MAN=ON \
	..

%{__make} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# symlink to "weechat"
%{__rm} $RPM_BUILD_ROOT%{_bindir}/weechat-curses

# no -devel, drop
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/%{name}.pc

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.asciidoc ChangeLog.asciidoc README.asciidoc ReleaseNotes.asciidoc
%attr(755,root,root) %{_bindir}/weechat
%{_mandir}/man1/weechat.1*
%lang(de) %{_mandir}/de/man1/weechat.1*
%lang(fr) %{_mandir}/fr/man1/weechat.1*
%lang(it) %{_mandir}/it/man1/weechat.1*
%lang(ja) %{_mandir}/ja/man1/weechat.1*
%lang(pl) %{_mandir}/pl/man1/weechat.1*
%lang(ru) %{_mandir}/ru/man1/weechat.1*
%{_iconsdir}/hicolor/*/apps/weechat.png

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/alias.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/charset.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/exec.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/fifo.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/irc.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/logger.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/relay.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/script.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/trigger.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/xfer.so

# addons
%{?with_aspell:%attr(755,root,root) %{_libdir}/%{name}/plugins/aspell.so}

# language bindings
%{?with_guile:%attr(755,root,root) %{_libdir}/%{name}/plugins/guile.so}
%{?with_lua:%attr(755,root,root) %{_libdir}/%{name}/plugins/lua.so}
%{?with_perl:%attr(755,root,root) %{_libdir}/%{name}/plugins/perl.so}
%{?with_python:%attr(755,root,root) %{_libdir}/%{name}/plugins/python.so}
%{?with_ruby:%attr(755,root,root) %{_libdir}/%{name}/plugins/ruby.so}
%{?with_tcl:%attr(755,root,root) %{_libdir}/%{name}/plugins/tcl.so}
%{?with_js:%attr(755,root,root) %{_libdir}/%{name}/plugins/javascript.so}

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
