Name:           %%%PACKAGE%%%
Version:        0.0.1
Release:        1%{?dist}
Summary:        Hello RPM Package

License:        Proprietary
URL:            https://github.com/maximvegorov/%{name}

BuildArch:      noarch

BuildRequires:  systemd
%{?systemd_requires}

Requires(pre):  shadow-utils
Requires:       bash
Requires:       java-1.8.0-openjdk-headless

%description
Hello RPM Package

%prep

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/java/%{name}
mkdir -p %{buildroot}%{_datadir}/java/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

install -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -m 0644 target/%{name}-LATEST.jar %{buildroot}%{_datadir}/java/%{name}/
install -m 0644 %{name}.log4j2.xml %{buildroot}%{_datadir}/java/%{name}/
install -m 0644 %{name}.service %{buildroot}%{_unitdir}/

%files
%dir %{_datadir}/java/%{name}/
%dir %attr(0770, %{name}, %{name}) %{_localstatedir}/log/%{name}
%{_bindir}/%{name}
%{_datadir}/java/%{name}/*
%{_unitdir}/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || useradd -r -g %{name} %{name} -s /sbin/nologin

%post
if [ $1 -eq 1 ]; then
    # Initial installation
    systemctl enabled %{name} &> /dev/null && systemctl start %{name} &> /dev/null
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
