%global vd_rc %{?v_rc:0.%{?v_rc}.}
%global debug_package %{nil}
%global _use_internal_dependency_generator 0
%global __find_provides %{_builddir}/%{srcname}/find-provides %__find_provides


Summary: High-performance HTTP accelerator
Name:    varnish
Version: %{versiontag}
Release: %{?vd_rc}%{releasetag}%{?dist}
License: BSD
Group:   System Environment/Daemons
URL:     https://www.varnish-cache.org/
Source:  %{srcname}.tgz

BuildRequires: jemalloc-devel
BuildRequires: libedit-devel
BuildRequires: ncurses-devel
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: python(abi) >= 2.7
BuildRequires: python-docutils >= 0.6
BuildRequires: python-sphinx
BuildRequires: systemd-units

Requires: gcc
Requires: logrotate

Requires(post):   systemd-units
Requires(post):   systemd-sysv
Requires(preun):  systemd-units
Requires(postun): systemd-units

Provides:  varnish-libs%{?_isa} = %{version}-%{release}
Provides:  varnish-libs = %{version}-%{release}
Obsoletes: varnish-libs

Provides:  varnish-docs = %{version}-%{release}
Obsoletes: varnish-docs

Provides:  varnish-debuginfo%{?_isa} = %{version}-%{release}
Provides:  varnish-debuginfo = %{version}-%{release}
Obsoletes: varnish-debuginfo


%description
This is Varnish Cache, a high-performance HTTP accelerator.

Varnish Cache stores web pages in memory so web servers don't have to
create the same web page over and over again. Varnish Cache serves
pages much faster than any application server; giving the website a
significant speed up.

Documentation wiki and additional information about Varnish Cache is
available on: https://www.varnish-cache.org/


%package devel
Summary:   Development files for %{name}
Group:     System Environment/Libraries
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  pkgconfig
Requires:  python(abi) >= 2.7
Provides:  varnish-libs-devel%{?_isa} = %{version}-%{release}
Provides:  varnish-libs-devel = %{version}-%{release}
Obsoletes: varnish-libs-devel


%description devel
Development files for %{name}
Varnish Cache is a high-performance HTTP accelerator


%prep
%setup -q -n %{srcname}


%build
%configure --localstatedir=/var/lib --without-rst2html
%make_build V=1


%check
%if 0%{?nocheck} == 0
%make_build check VERBOSE=1
%endif


%install
export DONT_STRIP=1
%make_install

find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'

mkdir -p %{buildroot}/var/lib/varnish
mkdir -p %{buildroot}/var/log/varnish
mkdir -p %{buildroot}/var/run/varnish
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
install -D -m 0644 etc/example.vcl %{buildroot}%{_sysconfdir}/varnish/default.vcl
install -D -m 0644 varnish.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/varnish

mkdir -p %{buildroot}%{_unitdir}
install -D -m 0644 varnish.service %{buildroot}%{_unitdir}/varnish.service
install -D -m 0644 varnishncsa.service %{buildroot}%{_unitdir}/varnishncsa.service
install -D -m 0755 varnishreload %{buildroot}%{_sbindir}/varnishreload

echo %{_libdir}/%{name} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%clean
rm -rf %{buildroot}


%files
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{name}
%{_var}/lib/varnish
%{_var}/log/varnish
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
%{_docdir}/%{name}/
%{_datadir}/%{name}
%{_unitdir}/*
%exclude %{_datadir}/%{name}/vmodtool*
%exclude %{_datadir}/%{name}/vsctool*
%doc README*
%doc LICENSE
%doc doc/html
%doc doc/changes*.html
%doc doc/changes*.rst
%dir %{_sysconfdir}/varnish/
%config(noreplace) %{_sysconfdir}/varnish/default.vcl
%config(noreplace) %{_sysconfdir}/logrotate.d/varnish
%config %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files devel
%{_libdir}/lib*.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/varnishapi.pc
%{_datadir}/%{name}/vmodtool*
%{_datadir}/%{name}/vsctool*
%{_datadir}/aclocal/*


%pre
getent group varnish >/dev/null ||
groupadd -r varnish

getent passwd varnishlog >/dev/null ||
useradd -r -g varnish -d /dev/null -s /sbin/nologin \
	-c "varnishlog user" varnishlog

getent passwd varnish >/dev/null ||
useradd -r -g varnish -d /var/lib/varnish -s /sbin/nologin \
	-c "Varnish Cache" varnish

exit 0


%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
chown varnishlog:varnish /var/log/varnish/
/sbin/ldconfig


%preun
if [ $1 -lt 1 ]; then
  # Package removal, not upgrade
  /bin/systemctl --no-reload disable varnish.service > /dev/null 2>&1 || :
  /bin/systemctl stop varnish.service > /dev/null 2>&1 || :
  /bin/systemctl stop varnishncsa.service > /dev/null 2>&1 || :
fi


%postun -p /sbin/ldconfig


%changelog
* Thu Jul 24 2014 Varnish Software <opensource@varnish-software.com> - 3.0.0-1
- This changelog is not in use. See doc/changes.rst for release notes.
