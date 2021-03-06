%global service vitrage

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             openstack-vitrage
Version:          XXX
Release:          XXX
Summary:          OpenStack Root Cause Analysis
License:          ASL 2.0
URL:              https://github.com/openstack/vitrage
BuildArch:        noarch
Source0:          http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source2:          %{service}.logrotate
Source10:         %{name}-api.service
Source11:         %{name}-graph.service
Source12:         %{name}-notifier.service
Source13:         %{name}-collector.service


BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    systemd
BuildRequires:    python-pbr
BuildRequires:    python-sphinx
BuildRequires:    python-oslo-messaging
BuildRequires:    python-oslo-config
BuildRequires:    python-keystoneauth1
BuildRequires:    python-keystoneclient
BuildRequires:    python-keystonemiddleware
BuildRequires:    python-oslo-db
BuildRequires:    python-oslo-policy



%description
Vitrage is the OpenStack RCA (Root Cause Analysis) Engine
for organizing, analyzing and expanding OpenStack alarms & events,


%package -n       python-vitrage
Summary:          OpenStack vitrage python libraries


Requires:         python-lxml

Requires:         python-oslo-config >= 2:3.14.0,
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-log >= 3.11.0
Requires:         python-oslo-policy >= 1.17.0
Requires:         python-oslo-messaging >= 5.14.0
Requires:         python-oslo-service >= 1.10.0
Requires:         python-oslo-utils >= 1.6.0
Requires:         python-keystonemiddleware >= 4.12.0
Requires:         python-pbr >= 1.8
Requires:         python-pecan >= 1.0.0
Requires:         python-stevedore >= 1.17.1
Requires:         python-werkzeug >= 0.7
Requires:         python-paste-deploy >= 1.5.0
Requires:         python-ceilometerclient >= 2.5.0
Requires:         python-keystoneclient >= 1:3.8.0
Requires:         python-cinderclient >= 1.6.0
Requires:         python-neutronclient >= 5.1.0
Requires:         python-novaclient >= 1:2.29.0
Requires:         python-networkx >= 1.10
Requires:         python-voluptuous >= 0.8.9
Requires:         sympy >= 0.7.6
Requires:         python-dateutil >= 2.4.2
Requires:         python-keystoneauth1 >= 2.12.1
Requires:         python-heatclient >= 1.6.1

%description -n   python-vitrage
OpenStack vitrage provides API and services for RCA (Root Cause Analysis)

This package contains the vitrage python library.

%package        common
Summary:        Components common to all OpenStack vitrage services

Requires:       python-vitrage = %{version}-%{release}

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(pre):    shadow-utils


%description    common
OpenStack vitrage provides API and services for RCA (Root Cause Analysis).


%package        api

Summary:        OpenStack vitrage api

Requires:       %{name}-common = %{version}-%{release}

%description api
OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

This package contains the vitrage API service.


%package        graph

Summary:        OpenStack vitrage graph

Requires:       %{name}-common = %{version}-%{release}

%description graph
OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

This package contains the vitrage graph service.

%package        notifier

Summary:        OpenStack vitrage notifier

Requires:       %{name}-common = %{version}-%{release}

%description notifier
OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

This package contains the vitrage notifier service.


%package        collector
Summary:        OpenStack vitrage collector
Requires:       %{name}-common = %{version}-%{release}

%description collector
OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

This package contains the vitrage collector service.


%package -n python-vitrage-tests
Summary:        Vitrage tests
Requires:       python-vitrage = %{version}-%{release}
Requires:       python-tempest >= 12.0.0

%description -n python-vitrage-tests
OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

This package contains the Vitrage test files.

%package doc
Summary:    Documentation for OpenStack vitrage

BuildRequires: python-oslo-sphinx

%description doc
OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

This package contains documentation files for vitrage.

%prep
%setup -q -n %{service}-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find vitrage -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build
# generate html docs
%{__python2} setup.py build_sphinx

# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=etc/vitrage/vitrage-config-generator.conf
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Create fake egg-info for the tempest plugin
%py2_entrypoint %{service} %{service}

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/vitrage/datasources_values
install -p -D -m 640 etc/vitrage/vitrage.conf %{buildroot}%{_sysconfdir}/vitrage/vitrage.conf
install -p -D -m 640 etc/vitrage/policy.json %{buildroot}%{_sysconfdir}/vitrage/policy.json
install -p -D -m 640 etc/vitrage/api-paste.ini %{buildroot}%{_sysconfdir}/vitrage/api-paste.ini
install -p -D -m 640 etc/vitrage/datasources_values/*.yaml %{buildroot}%{_sysconfdir}/vitrage/datasources_values/

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/vitrage
install -d -m 755 %{buildroot}%{_sharedstatedir}/vitrage/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/vitrage
install -d -m 755 %{buildroot}%{_sysconfdir}/vitrage/static_datasources
install -d -m 755 %{buildroot}%{_sysconfdir}/vitrage/templates

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install systemd unit services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-graph.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-notifier.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-collector.service

# Remove unused files
rm -f %{buildroot}/usr/etc/vitrage/*

%pre common
getent group vitrage >/dev/null || groupadd -r vitrage
if ! getent passwd vitrage >/dev/null; then
  useradd -r -g vitrage -G vitrage -d %{_sharedstatedir}/vitrage -s /sbin/nologin -c "OpenStack vitrage Daemons" vitrage
fi
exit 0

%post -n %{name}-api
%systemd_post %{name}-api.service

%preun -n %{name}-api
%systemd_preun %{name}-api.service

%post -n %{name}-graph
%systemd_post %{name}-graph.service

%preun -n %{name}-graph
%systemd_preun %{name}-graph.service

%post -n %{name}-notifier
%systemd_post %{name}-notifier.service

%preun -n %{name}-notifier
%systemd_preun %{name}-notifier.service

%post -n %{name}-collector
%systemd_post %{name}-collector.service

%preun -n %{name}-collector
%systemd_preun %{name}-collector.service

%files -n python-vitrage
%license LICENSE
%{python2_sitelib}/vitrage
%{python2_sitelib}/vitrage-*.egg-info
%exclude %{python2_sitelib}/vitrage_tempest_tests
%exclude %{python2_sitelib}/vitrage/tests

%files -n python-vitrage-tests
%license LICENSE
%{python2_sitelib}/vitrage_tempest_tests
%{python2_sitelib}/vitrage/tests
%{python2_sitelib}/%{service}_tests.egg-info

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/vitrage
%dir %{_sysconfdir}/vitrage/datasources_values
%config(noreplace) %attr(-, root, vitrage) %{_sysconfdir}/vitrage/vitrage.conf
%config(noreplace) %attr(-, root, vitrage) %{_sysconfdir}/vitrage/policy.json
%config(noreplace) %attr(-, root, vitrage) %{_sysconfdir}/vitrage/api-paste.ini
%config(noreplace) %attr(-, root, vitrage) %{_sysconfdir}/vitrage/datasources_values/*.yaml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0755, vitrage, root)  %{_localstatedir}/log/vitrage
%dir %attr(0755, vitrage, root)  %{_sysconfdir}/vitrage/static_datasources
%dir %attr(0755, vitrage, root)  %{_sysconfdir}/vitrage/templates

%defattr(-, vitrage, vitrage, -)
%dir %{_sharedstatedir}/vitrage
%dir %{_sharedstatedir}/vitrage/tmp

%files api
%{_bindir}/vitrage-api
%{_unitdir}/%{name}-api.service

%files collector
%{_bindir}/vitrage-collector
%{_unitdir}/%{name}-collector.service

%files graph
%{_bindir}/vitrage-graph
%{_unitdir}/%{name}-graph.service

%files notifier
%{_bindir}/vitrage-notifier
%{_unitdir}/%{name}-notifier.service

%files doc
%license LICENSE
%doc doc/build/html

%changelog
