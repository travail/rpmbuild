Name: peco
Summary: Simplistic interactive filtering tool
Version: 0.3.6
Release: 1%{?dist}

License: MIT
Group: Development/Tools
URL: https://github.com/peco/peco
Source0: peco-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

%description
peco (pronounced peh-koh) is based on a python tool, percol. percol was darn useful, but I wanted a tool that was a single binary, and forget about python. peco is written in Go, and therefore you can just grab the binary releases and drop it in your $PATH.

peco can be a great tool to filter stuff like logs, process stats, find files, because unlike grep, you can type as you think and look through the current results.

%prep

%setup

%build

%install
mkdir -p %{buildroot}%{_bindir}
%{__install} peco %{buildroot}%{_bindir}/peco

%files
%attr(755,-,-) %{_bindir}/peco

%changelog
* Thu Jul 14 2016 travail 0.3.6
- Initial build 0.3.6.
