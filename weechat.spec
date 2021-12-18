# TODO:
# - consider doing subpackages for all those plugins (which one should be in main package ?)
# - desktop file (icon exists, but no desktop file?)
#
# Conditional build:
# Features
%bcond_without	aspell	# don't build aspell support
%bcond_without	doc	# don't build docs
# Bindings
%bcond_without	guile	# don't enable Scheme (guile) scripting language
%bcond_without	lua	# don't enable Lua scripting language
%bcond_without	perl	# don't enable Perl scripting language
%bcond_with	php	# don't enable PHP scripting language
%bcond_without	python	# don't enable Python scripting language
%bcond_without	ruby	# don't enable Ruby scripting language
%bcond_without	tcl	# don't enable Tcl scripting language
%bcond_without	js	# don't enable JavaScript scripting language (V8 engine)

%ifnarch %{ix86} %{x8664} arm mips
%undefine	with_js
%endif

%define		php_name	php%{?php_suffix}

Summary:	WeeChat - fast and light chat environment
Summary(pl.UTF-8):	WeeChat - szybkie i lekkie środowisko do rozmów
Name:		weechat
Version:	3.4
Release:	1
License:	GPL v3+
Group:		Applications/Communications
Source0:	https://www.weechat.org/files/src/%{name}-%{version}.tar.xz
# Source0-md5:	f61bcc8b6ab3b8993f7738950e1a753f
URL:		http://www.weechat.org/
%{?with_aspell:BuildRequires:	aspell-devel}
BuildRequires:	cmake >= 3.0
BuildRequires:	curl-devel
BuildRequires:	gettext-tools
BuildRequires:	gnutls-devel
%{?with_guile:BuildRequires:	guile-devel}
BuildRequires:	libgcrypt-devel
%{?with_lua:BuildRequires:	lua-devel}
BuildRequires:	ncurses-devel
%{?with_perl:BuildRequires:	perl-devel}
%{?with_php:BuildRequires:	%{php_name}-devel >= 4:7}
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
%{?with_doc:BuildRequires:	ruby-asciidoctor}
%{?with_ruby:BuildRequires:	ruby-devel >= 1:1.9}
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
%{?with_tcl:BuildRequires:	tcl-devel}
%{?with_js:BuildRequires:	v8-devel}
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Suggests:	%{name}-icons
Suggests:	%{name}-plugin-irc
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
BuildArch:	noarch

%description doc
HTML documentation for weechat.

%package icons
Summary:	Icon files for weechat
Group:		Applications
BuildArch:	noarch
Requires(post,postun):	gtk-update-icon-cache

%description icons
Icon files for weechat.

%package plugin-guile
Summary:	Guile scripting plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-guile
Guile scripting plugin for weechat.

%package plugin-irc
Summary:	IRC chat protocol plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-irc
IRC chat protocol plugin for weechat.

%package plugin-javascript
Summary:	JavaScript scripting plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-javascript
JavaScript scripting plugin for weechat.

%package plugin-lua
Summary:	Lua scripting plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-lua
Lua scripting plugin for weechat.

%package plugin-perl
Summary:	Perl scripting plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-perl
Perl scripting plugin for weechat.

%package plugin-python
Summary:	Python scripting plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-python
Python scripting plugin for weechat.

%package plugin-relay
Summary:	Relay data via network plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-relay
Relay data via network plugin for weechat used by alternative
frontends.

%package plugin-ruby
Summary:	Ruby scripting plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-ruby
Ruby scripting plugin for weechat.

%package plugin-spell
Summary:	Spell checking plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-spell
Spell checking plugin for weechat.

%package plugin-tcl
Summary:	Tcl scripting plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-tcl
Tcl scripting plugin for weechat.

%package plugin-xfer
Summary:	File transfer and direct chat plugin for weechat
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-xfer
File transfer and direct chat plugin for weechat.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DPREFIX=%{_prefix} \
	-DLIBDIR=%{_libdir} \
	-DENABLE_HEADLESS=OFF \
	-DENABLE_NCURSES=ON \
	%{cmake_on_off aspell ENABLE_SPELL} \
	%{cmake_on_off doc ENABLE_DOC} \
	%{cmake_on_off perl ENABLE_PERL} \
	%{cmake_on_off php ENABLE_PHP} \
	%{cmake_on_off python ENABLE_PYTHON} \
	%{cmake_on_off ruby ENABLE_RUBY} \
	%{cmake_on_off lua ENABLE_LUA} \
	%{cmake_on_off guile ENABLE_GUILE} \
	%{cmake_on_off tcl ENABLE_TCL} \
	%{cmake_on_off doc ENABLE_MAN} \
	%{cmake_on_off js ENABLE_JAVASCRIPT} \
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

%post
%update_desktop_database
%update_mime_database

%post icons
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_mime_database

%postun icons
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.adoc ChangeLog.adoc README.adoc ReleaseNotes.adoc
%attr(755,root,root) %{_bindir}/weechat
%if %{with doc}
%{_mandir}/man1/weechat.1*
%lang(cs) %{_mandir}/cs/man1/weechat.1*
%lang(de) %{_mandir}/de/man1/weechat.1*
%lang(fr) %{_mandir}/fr/man1/weechat.1*
%lang(it) %{_mandir}/it/man1/weechat.1*
%lang(ja) %{_mandir}/ja/man1/weechat.1*
%lang(pl) %{_mandir}/pl/man1/weechat.1*
%lang(ru) %{_mandir}/ru/man1/weechat.1*
%endif
%{_desktopdir}/%{name}.desktop

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/alias.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/buflist.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/charset.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/exec.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/fifo.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/fset.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/logger.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/script.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/trigger.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/typing.so

%files icons
%defattr(644,root,root,755)
%{_iconsdir}/hicolor/*/apps/weechat.png

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/%{name}
%lang(cs) %{_docdir}/%{name}/*.cs.html
%lang(de) %{_docdir}/%{name}/*.de.html
%lang(en) %{_docdir}/%{name}/*.en.html
%lang(es) %{_docdir}/%{name}/*.es.html
%lang(fr) %{_docdir}/%{name}/*.fr.html
%lang(it) %{_docdir}/%{name}/*.it.html
%lang(ja) %{_docdir}/%{name}/*.ja.html
%lang(pl) %{_docdir}/%{name}/*.pl.html
%lang(ru) %{_docdir}/%{name}/*.ru.html
%endif

%if %{with guile}
%files plugin-guile
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/guile.so
%endif

%files plugin-irc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/irc.so

%if %{with js}
%files plugin-javascript
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/javascript.so
%endif

%if %{with lua}
%files plugin-lua
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/lua.so
%endif

%if %{with perl}
%files plugin-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/perl.so
%endif

%if %{with python}
%files plugin-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/python.so
%endif

%files plugin-relay
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/relay.so

%if %{with ruby}
%files plugin-ruby
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/ruby.so
%endif

%if %{with aspell}
%files plugin-spell
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/spell.so
%endif

%if %{with tcl}
%files plugin-tcl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/tcl.so
%endif

%files plugin-xfer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/plugins/xfer.so
