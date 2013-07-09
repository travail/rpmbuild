%define name fluent-agent-lite
%define version 0.9
%define prefix /usr/local
%define build_perl_path /usr/bin/perl

%define _use_internal_dependency_generator 0

%global debug_package %{nil}

Name:           fluent-agent-lite
Version:        %{version}
Release:        original
Summary:        Log transfer agent service over fluentd protocol

Group:          Applications/System
License:        Apache Software License v2
URL:            https://github.com/tagomoris/fluent-agent-lite
# Source0:        http://tagomoris.github.io/tarballs/fluent-agent-lite.v%{version}.tar.gz
Source0:        fluent-agent-lite.v%{version}.tar.gz
# Source1:        fluent-agent-lite.conf
# Source2:        fluent-agent.servers.primary
# Source3:        fluent-agent.servers.secondary
BuildRoot:      %{_tmppath}/%{name}-root

ExclusiveArch:  x86_64 i386
AutoReq:        no

%description
Log transfer agent service over fluentd protocol.

%prep
%setup -q -n fluent-agent-lite-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
env PREFIX=$RPM_BUILD_ROOT PERL_PATH=%{build_perl_path} bin/install.sh
# install -m 644 $RPM_SOURCE_DIR/fluent-agent-lite.conf $RPM_BUILD_ROOT/etc/fluent-agent-lite.conf
# install -m 644 $RPM_SOURCE_DIR/fluent-agent.servers.primary $RPM_BUILD_ROOT/etc/fluent-agent.servers.primary
# install -m 644 $RPM_SOURCE_DIR/fluent-agent.servers.secondary $RPM_BUILD_ROOT/etc/fluent-agent.servers.secondary

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/fluent-agent-lite.conf
# %config %{_sysconfdir}/fluent-agent.servers.primary
# %config %{_sysconfdir}/fluent-agent.servers.secondary
%{_sysconfdir}/init.d/fluent-agent-lite
%{prefix}/*
# %doc README

%changelog
* Thu Jun 27 2013 TAGOMORI Satoshi <tagomoris@gmail.com>
- add configuration pattern for log files
- fix to check input log files
* Sat Apr 13 2013 TAGOMORI Satoshi <tagomoris@gmail.com>
- fix not to read lines already exists just after start-up
- CPANize
* Tue Mar 19 2013 TAGOMORI Satoshi <tagomoris@gmail.com>
- add i386 support for specs
- add keepalive time option
- fix to remove .pid file when stop
* Wed Aug 29 2012 TAGOMORI Satoshi <tagomoris@gmail.com>
- add ping_message options
* Wed Mar 21 2012 TAGOMORI Satoshi <tagomoris@gmail.com>
- fix to send PackedForward object
- bugfix about installer / init script
- add feature about drain log
* Thu Mar 15 2012 TAGOMORI Satoshi <tagomoris@gmail.com>
- bugfix about path of perl
* Wed Mar 14 2012 TAGOMORI Satoshi <tagomoris@gmail.com>
- initial packaging attempt
