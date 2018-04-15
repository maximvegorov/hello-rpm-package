Name:           %%%PACKAGE%%%
Version:        0.0.1
Release:        1%{?dist}
Summary:        Hello RPM Package

License:        Proprietary
URL:            https://github.com/maximvegorov/%{name}
Source:         %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  systemd
%{?systemd_requires}

Requires(pre):  shadow-utils
Requires:       bash
Requires:       java-1.8.0-openjdk-headless

%description
Hello RPM Package

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{%_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_datadir}/java/%{name}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

install -m 0755 %{name} %{buildroot}%{_bindir}/
install -m 0744 log4j2.xml %{_sysconfdir}/%{name}/
install -m 0744 %{name}-LATEST.jar %{buildroot}%{_datadir}/java/%{name}/
install -m 0744 %{name}.service %{buildroot}%{_unitdir}/

%files
%dir %attr(0755, -, -) %{_sysconfdir}/%{name}/
%dir %attr(0755, -, -) %{_datadir}/java/%{name}/
%dir %attr(0775, %{name}, %{name}) %{_localstatedir}/log/%{name}
%{_bindir}/%{name}
%{_sysconfdir}/%{name}/*
%{_datadir}/java/%{name}/*
%{_unitdir}/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || useradd -r -g %{name} %{name} -s /sbin/nologin

%post
if [ $1 -eq 1 ]; then
    # Initial installation
    systemctl enable %{name} &> /dev/null && systemctl start %{name} &> /dev/null
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
