Name:           hello-rpm-package
Version:        0.0.1
Release:        1%{?dist}
Summary:        Hello RPM Package

License:        Proprietary
URL:            https://github.com/maximvegorov/%{name}

BuildRoot:      rpmbuild

BuildArch:      noarch

%{?systemd_requires}
BuildRequires:  systemd
BuildRequires:  java-1.8.0-openjdk-headless
BuildRequires:  maven

Requires:       shadow-utils
Requires:       bash
Requires:       java-1.8.0-openjdk-headless

%description
Hello RPM Package

%prep
if [ -d rpmbuild ]; then
    rm -rf rpmbuild > /dev/null 2>&1
fi
mkdir rpmdir

%build
maven clean package

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{name}
mkdir -p %{buildroot}/%{_datadir}/%{name}
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}

install -m 0755 %{name} %{buildroot}/%{_bindir}/%{name}
install -m 0644 target/%{name}-LATEST.jar %{buildroot}/%{_datadir}/%{name}/
install -m 0644 %{name}.log4j2.xml %{buildroot}/%{_datadir}/%{name}/
install -m 0644 %{name}.service %{buildroot}/%{_unitdir}/

%files
%dir %{_datadir}/%{name}/
%dir %{_localstatedir}/log/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}/*
%{_unitdir}/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || useradd -r -g %{name} %{name} -s /sbin/nologin

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
