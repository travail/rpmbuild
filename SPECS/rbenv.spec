%define rbenvroot /usr/local/rbenv
%define ruby_build_version v20160602
%define ruby_version 2.3.1

Name: rbenv
Summary: An interpreter of object-oriented scripting language
Version: v1.0.0
Release: 1

License: MIT
Group: Development/Languages
URL: http://ruby-lang.org/
Source0: %{name}.tar.gz
Source1: ruby-build.tar.gz
Source2: ruby-%{ruby_version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
# Prevent to detect dependencies such as ruby(Devel::PatchRuby) >= 0.88
AutoReqProv: no

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Ruby).  It is simple,
straight-forward, and extensible.

%prep

%setup -a 1 -a 2 -n %{name}
mkdir plugins
mv ruby-build plugins/ruby-build

%build
# Check out specific versions.
git checkout -b %{version} refs/tags/%{version}
cd plugins/ruby-build
git checkout -b %{ruby_build_version} refs/tags/%{ruby_build_version}
cd %{_builddir}/%{name}
# Build and install Ruby.
# Emulate installation by "rbenv install X.X.X" with default configuration options.
mkdir -p %{buildroot}%{rbenvroot}/versions/%{ruby_version}
cd ruby-%{ruby_version}
sh configure '--prefix=%{rbenvroot}/versions/%{ruby_version}' 'LDFLAGS=-L%{rbenvroot}/versions/%{ruby_version}/lib ' 'CPPFLAGS=-I%{rbenvroot}/versions/%{ruby_version}/include '
cd %{_builddir}/%{name}

%install
cd ruby-%{ruby_version}
make install DESTDIR=%{buildroot}
cd %{_builddir}/%{name}
rm -rf shims ruby-%{ruby_version} %{_builddir}/%{name}%{rbenvroot}
cp -r * %{buildroot}%{rbenvroot}
cp -r .git %{buildroot}%{rbenvroot}
cp .agignore %{buildroot}%{rbenvroot}
cp .gitignore %{buildroot}%{rbenvroot}
cp .travis.yml %{buildroot}%{rbenvroot}
cp .vimrc %{buildroot}%{rbenvroot}

%files
%defattr(664,travail,travail,775)
%dir %{rbenvroot}
%dir %{rbenvroot}/.git
%{rbenvroot}/.git/*
%{rbenvroot}/.agignore
%{rbenvroot}/.gitignore
%{rbenvroot}/.travis.yml
%{rbenvroot}/.vimrc
%{rbenvroot}/LICENSE
%{rbenvroot}/README.md
%dir %{rbenvroot}/bin
%attr(775,travail,travail) %{rbenvroot}/bin/*
%dir %{rbenvroot}/completions
%{rbenvroot}/completions/*
%dir %{rbenvroot}/libexec
%attr(775,travail,travail) %{rbenvroot}/libexec/*
%dir %{rbenvroot}/rbenv.d
%{rbenvroot}/rbenv.d/*
%dir %{rbenvroot}/src
%{rbenvroot}/src/*
%dir %{rbenvroot}/test/
%{rbenvroot}/test/*

%dir %{rbenvroot}/plugins
%dir %{rbenvroot}/plugins/ruby-build
%dir %{rbenvroot}/plugins/ruby-build/.git
%{rbenvroot}/plugins/ruby-build/.git/*
%{rbenvroot}/plugins/ruby-build/.travis.yml
%{rbenvroot}/plugins/ruby-build/CONDUCT.md
%{rbenvroot}/plugins/ruby-build/LICENSE
%{rbenvroot}/plugins/ruby-build/README.md
%dir %{rbenvroot}/plugins/ruby-build/bin
%attr(775,travail,travail) %{rbenvroot}/plugins/ruby-build/bin/*
%attr(755,travail,travail) %{rbenvroot}/plugins/ruby-build/install.sh
%dir %{rbenvroot}/plugins/ruby-build/script
%attr(755,travail,travail) %{rbenvroot}/plugins/ruby-build/script/*
%dir %{rbenvroot}/plugins/ruby-build/share
%{rbenvroot}/plugins/ruby-build/share/*
%dir %{rbenvroot}/plugins/ruby-build/test
%{rbenvroot}/plugins/ruby-build/test/*

%attr(775,travail,travail) %dir %{rbenvroot}/versions
%dir %{rbenvroot}/versions/%{ruby_version}
%dir %{rbenvroot}/versions/%{ruby_version}/bin
%attr(775,travail,travail) %{rbenvroot}/versions/%{ruby_version}/bin/*
%dir %{rbenvroot}/versions/%{ruby_version}/include
%{rbenvroot}/versions/%{ruby_version}/include/*
%dir %{rbenvroot}/versions/%{ruby_version}/lib
%{rbenvroot}/versions/%{ruby_version}/lib/*
%dir %{rbenvroot}/versions/%{ruby_version}/share
%{rbenvroot}/versions/%{ruby_version}/share/*

%clean

%changelog
* Thu Jul 11 2016 travail v1.0.0
- Initial build with ruby-build v20160602 and ruby-2.3.1.
