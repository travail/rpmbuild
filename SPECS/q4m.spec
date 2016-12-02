%define _prefix /usr/local/q4m
%define _bindir %{_prefix}/bin
%define _datadir %{_prefix}/share
%define _includedir %{_prefix}/include
%define _libdir %{_prefix}/lib
%define _mandir %{_datadir}/man
%define _sbindir %{_prefix}/sbin
%define mysql_version 5.6.16
%define q4m_version 0.9.14
%define mysql_user mysql
%define mysql_port 13306

%{!?with_systemd: %global systemd 0}

Name: q4m
Summary: foo
Version: %{q4m_version}
Release: 1%{?dist}

License: MIT
Group: Applications/Databases
URL: https://q4m.github.io/
Source0: mysql-%{mysql_version}.tar.gz
Source1: %{name}-%{version}.tar.gz
Source2: %{name}.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: cmake ncurses-devel libaio-devel readline-devel
%if 0%{?systemd}
BuildRequires: systemd-units
%endif

%if 0%{?systemd}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
%else
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
Requires(preun):  /sbin/service
%endif

%description
Q4M (Queue for MySQL) is a message queue licensed under GPL that works as a pluggable storage engine of MySQL, designed to be robust, fast, flexible. It is already in production quality, and is used by several web services (see Users of Q4M).
To start using Q4M, download either a binary or source distribution from the install page, and follow the installation instructions. A small tutorial is also avialable. You may use SQL to access Q4M queues, or there is a wrapper module available for perl (Queue::Q4M).

%prep

%setup -a 1 -n mysql-%{mysql_version}
mv %{name}-%{version} storage/q4m

%build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DINSTALL_LAYOUT=STANDALONE \
      -DINSTALL_MANDIR=%{_mandir} \
      -DINSTALL_SCRIPTDIR=%{_prefix}/scripts \
      -DINSTALL_SUPPORTFILESDIR=%{_prefix}/support-files \
      -DDEFAULT_CHARSET=utf8 \
      -DDEFAULT_COLLATION=utf8_general_ci \
      -DWITH_EXTRA_CHARSETS=all \
      -DWITH_ZLIB=bundled \
      -DWITH_SSL=bundled \
      -DWITH_PIC=ON \
      -DWITH_FAST_MUTEXES=ON \
      -DWITH_DEBUG=OFF \
      -DCOMPILATION_COMMENT="Q4M" \
      -DMYSQL_SERVER_SUFFIX="-q4m" \
      -DMYSQL_USER=%{mysql_user} \
      -DMYSQL_TCP_PORT=%{mysql_port} \
      -DMYSQL_UNIX_ADDR="%{_prefix}/mysql.sock" \
      -DWITH_DEFAULT_FEATURE_SET=xsmall \
      -DWITH_PARTITION_STORAGE_ENGINE=1 \
      -DWITHOUT_DAEMON_EXAMPLE_STORAGE_ENGINE=1 \
      -DWITHOUT_FTEXAMPLE_STORAGE_ENGINE=1 \
      -DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
      -DWITHOUT_ARCHIVE_STORAGE_ENGINE=1 \
      -DWITHOUT_BLACKHOLE_STORAGE_ENGINE=1 \
      -DWITHOUT_FEDERATED_STORAGE_ENGINE=1 \
      -DWITHOUT_PERFSCHEMA_STORAGE_ENGINE=1 \
      -DWITHOUT_NDBCLUSTER_STORAGE_ENGINE=1 \
      -DWITH_INNODB_MEMCACHED=OFF \
      -DWITH_EMBEDDED_SERVER=OFF \
      -DWITH_UNIT_TESTS=OFF
make

%install
BUILD_DIR=$RPM_BUILD_DIR/mysql-%{mysql_version}
make DESTDIR=%{buildroot} install
install -D -m 0644 $BUILD_DIR/support-files/mysql-log-rotate %{buildroot}%{_sysconfdir}/logrotate.d/q4m
%if 0%{?systemd}
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%else
install -D -m 0755 $BUILD_DIR/support-files/mysql.server %{buildroot}%{_sysconfdir}/init.d/%{name}
%endif
install -D -m 0755 $BUILD_DIR/support-files/my-default.cnf %{buildroot}%{_prefix}/my.cnf
install -D -m 0644 $BUILD_DIR/storage/q4m/support-files/install.sql %{buildroot}%{_prefix}/support-files/install-q4m.sql

# Replace strings.
sed -i -e 's/\/etc\/my\.cnf/\/usr\/local\/q4m\/my\.cnf/' %{buildroot}%{_prefix}/my.cnf
sed -i -e 's/^basedir=$/\/usr\/local\/q4m/' %{buildroot}%{_prefix}/my.cnf
sed -i -e 's/^datadir=$/\/usr\/local\/q4m\/data/' %{buildroot}%{_prefix}/my.cnf

# Remove files no need to package.
rm -rf %{buildroot}%{_prefix}/mysql-test
rm -rf %{buildroot}%{_prefix}/sql-bench

%pre

%post
/usr/sbin/groupadd -g 27 -o -r %{mysql_user} >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d %{_prefix} -s /bin/bash -c "Q4M Server" %{mysql_user} >/dev/null 2>&1 || :
chown %{mysql_user}:%{mysql_user} %{_prefix}
chown %{mysql_user}:%{mysql_user} -R %{_prefix}/data
sudo -u %{mysql_user} %{_prefix}/scripts/mysql_install_db --basedir %{_prefix} --datadir %{_prefix}/data

%if 0%{?systemd}
/usr/bin/systemctl start %{name}.service
/usr/bin/systemctl enable %{name}.service
%else
/sbin/service %{name} start
/sbin/chkconfig --add %{name}
%endif

%{_bindir}/mysql -uroot < %{_prefix}/support-files/install-q4m.sql

%preun
%if 0%{?systemd}
/usr/bin/systemctl stop %{name}.service
/usr/bin/systemctl disable %{name}.service
%else
/sbin/service %{name} stop
/sbin/chkconfig --del %{name}
%endif

%files
%defattr(-, root, root, -)
%if 0%{?systemd}
%{_unitdir}/%{name}.service
%else
%{_sysconfdir}/init.d/q4m
%endif
%{_sysconfdir}/logrotate.d/q4m

%{_prefix}/COPYING
%{_prefix}/INSTALL-BINARY
%{_prefix}/README

%{_bindir}/
%{_prefix}/docs/
%{_prefix}/data/
%{_includedir}/
%{_libdir}/
%{_prefix}/my.cnf
%{_prefix}/scripts/

%{_datadir}/aclocal/
%{_datadir}/bulgarian/
%{_datadir}/charsets/
%{_datadir}/czech/
%{_datadir}/danish/
%{_datadir}/dictionary.txt
%{_datadir}/dutch/
%{_datadir}/english/
%{_datadir}/errmsg-utf8.txt
%{_datadir}/estonian/
%{_datadir}/fill_help_tables.sql
%{_datadir}/french/
%{_datadir}/german/
%{_datadir}/greek/
%{_datadir}/hungarian/
%{_datadir}/innodb_memcached_config.sql
%{_datadir}/italian/
%{_datadir}/japanese/
%{_datadir}/korean/
%{_datadir}/man/
%{_datadir}/mysql_security_commands.sql
%{_datadir}/mysql_system_tables_data.sql
%{_datadir}/mysql_system_tables.sql
%{_datadir}/mysql_test_data_timezone.sql
%{_datadir}/norwegian/
%{_datadir}/norwegian-ny/
%{_datadir}/polish/
%{_datadir}/portuguese/
%{_datadir}/romanian/
%{_datadir}/russian/
%{_datadir}/serbian/
%{_datadir}/slovak/
%{_datadir}/spanish/
%{_datadir}/swedish/
%{_datadir}/ukrainian/

%{_prefix}/support-files/
