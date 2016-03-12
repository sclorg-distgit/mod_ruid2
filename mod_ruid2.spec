%if 0%{?scl:1}
%scl_package mod_ruid2
%global sub_prefix sclo-%{scl_prefix}
%endif

%if 0%{?scl:1}
%{!?_httpd24_apxs:       %{expand: %%global _httpd24_apxs       %%{_sbindir}/apxs}}
%{!?_httpd24_mmn:        %{expand: %%global _httpd24_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd24_confdir:    %{expand: %%global _httpd24_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd24_modconfdir: %{expand: %%global _httpd24_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd24_moddir:    %{expand: %%global _httpd24_moddir    %%{_libdir}/httpd/modules}}
%else
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}
%endif

Summary: Run all httpd process under user's access right.
Name: %{?scl:%sub_prefix}mod_ruid2
Version: 0.9.8
Release: 4%{?dist}
Group: System Environment/Daemons
URL: http://sourceforge.net/projects/mod-ruid/
Source0: http://downloads.sourceforge.net/project/mod-ruid/mod_ruid2/mod_ruid2-%{version}.tar.gz
Source1: mod_ruid2.conf
Source2: 10-mod_ruid2.conf
License: ASL 2.0

BuildRequires: %{?scl:%scl_prefix}httpd-devel 
BuildRequires: libcap-devel

Requires(pre): %{?scl:%scl_prefix}httpd

%if 0%{?scl:1}
Requires: %{?scl:%scl_prefix}httpd-mmn = %{_httpd24_mmn}
%else
Requires: httpd-mmn = %{_httpd_mmn}
%endif

%{?scl:Requires:%scl_runtime}

Provides: %{?scl_prefix}mod_ruid2 = %{version}-%{release}
Provides: %{?scl_prefix}mod_ruid2%{_isa} = %{version}-%{release}

# Suppres auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
With this module, all httpd process run under user's access right, not nobody or apache.
mod_ruid2 is similar to mod_suid2, but has better performance than mod_suid2 because it
doesn`t need to kill httpd children after one request. It makes use of kernel capabilites
and after receiving a new request suids again. If you want to run apache modules, i.e.
WebDAV, PHP, and so on under user's right, this module is useful.

%prep
%setup -q -n mod_ruid2-%{version}


%build
%if 0%{?scl:1}
%{_httpd24_apxs} -l cap -c mod_ruid2.c
%else
%{_httpd_apxs} -l cap -c mod_ruid2.c
%endif


%install
# install module

%if 0%{?scl:1}
mkdir -p %{buildroot}%{_httpd24_moddir}
install -m 755 .libs/mod_ruid2.so %{buildroot}%{_httpd24_moddir}
%else
mkdir -p %{buildroot}%{_httpd_moddir}
install -m 755 .libs/mod_ruid2.so %{buildroot}%{_httpd_moddir}
%endif

# install module configuration

%if 0%{?scl:1}
mkdir -p %{buildroot}%{_httpd24_confdir}
install -m 644 %{SOURCE1} %{buildroot}%{_httpd24_confdir}
mkdir -p %{buildroot}%{_httpd24_modconfdir}
install -m 644 %{SOURCE2} %{buildroot}%{_httpd24_modconfdir}
%else
mkdir -p %{buildroot}%{_httpd_confdir}
install -m 644 %{SOURCE1} %{buildroot}%{_httpd_confdir}
mkdir -p %{buildroot}%{_httpd_modconfdir}
install -m 644 %{SOURCE2} %{buildroot}%{_httpd_modconfdir}
%endif


%files
%doc README LICENSE

%if 0%{?scl:1}
%config(noreplace) %{_httpd24_modconfdir}/10-mod_ruid2.conf
%config(noreplace) %{_httpd24_confdir}/mod_ruid2.conf
%{_httpd24_moddir}/mod_ruid2.so
%else
%config(noreplace) %{_httpd_modconfdir}/10-mod_ruid2.conf
%config(noreplace) %{_httpd_confdir}/mod_ruid2.conf
%{_httpd_moddir}/mod_ruid2.so
%endif


%changelog
* Wed Feb 24 2016 Jaroslaw Polok <jaroslaw.polok@cern.ch> 0.9.8-4
- repackage as Software Collection

* Fri Mar 22 2013 Kees Monshouwer <km|monshouwer_com> 0.9.8-1
- Address reported security bug in chroot mode. Thanks to the
  "cPanel Security Team" for the discovery of this bug.
- Improve chroot behavior in drop capability mode.

* Wed Apr 11 2012 Kees Monshouwer <km|monshouwer_com> 0.9.7-1
- Update to 0.9.7
- Reduction of memory usage, especially in large deployments

* Wed Apr 11 2012 Kees Monshouwer <km|monshouwer_com> 0.9.6-1
- Update to 0.9.6
- Fixed: user group exchange in default config

* Wed Mar 07 2012 Kees Monshouwer <km|monshouwer_com> 0.9.5-1
- Update to 0.9.5
- Switch default mode to 'config' !!!
- Apache 2.4 compatibility

* Wed Feb 23 2011 Kees Monshouwer <km|monshouwer.com> 0.9.4-1
- Update to 0.9.4
- Fixed: mod_security incompatibility issue

* Tue Jan 04 2011 Kees Monshouwer <km|monshouwer_com> 0.9.3-1
- Update to 0.9.3
- Fixed: chroot issue with sub-requests caused by mod_rewrite

* Tue Dec 21 2010 Kees Monshouwer <km|monshouwer_com> 0.9.2-1
- Update to 0.9.2
- Fixed: array subscript was above array bounds in ruid_set_perm

* Mon Oct 18 2010 Kees Monshouwer <km|monshouwer_com> 0.9.1-1
- Update to 0.9.1

* Wed Jun 23 2010 Kees Monshouwer <km|monshouwer_com> 0.9-1
- Added chroot functionality
- Update to 0.9

* Mon Jun 21 2010 Kees Monshouwer <km|monshouwer_com> 0.8.2-1
- Added drop capability mode to drop capabilities permanent after set[ug]id
- Update to 0.8.2

* Thu May 27 2010 Kees Monshouwer <km|monshouwer_com> 0.8.1-1
- Changed module name to mod_ruid2
- Update to 0.8.1

* Mon Apr 12 2010 Kees Monshouwer <km|monshouwer_com> 0.8-1
- Update to 0.8

* Wed Oct 21 2009 Kees Monshouwer <km|monshouwer_com> 0.7.1-1
- Fixed security problem in config

* Sun Sep 27 2009 Kees Monshouwer <km|monshouwer_com> 0.7-1
- Added per directory config option

* Wed Aug 29 2007 Kees Monshouwer <km|monshouwer_com> 0.6-3.1
- Build for CentOS 5

* Fri Sep 08 2006 Kees Monshouwer <km|monshouwer_com> 0.6-3
- Fixed first child request groups bug

* Fri Sep 08 2006 Kees Monshouwer <km|monshouwer_com> 0.6-2
- Fixed some uninitalized vars and a typo
- Changed the default user and group to apache

* Wed Mar 08 2006 Kees Monshouwer <km|monshouwer_com> 0.6-1
- Inital build for CentOS 4.2



