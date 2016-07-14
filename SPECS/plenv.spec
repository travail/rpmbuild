%define plenvroot /usr/local/plenv
%define perl_build_version 1.13
%define perl_version 5.22.2

Name: plenv
Summary: Perl binary manager
version: 2.2.0
Release: 1

License: MIT
Group: Development/Languages
URL: http://www.perl.org/
Source0: %{name}.tar.gz
Source1: perl-build.tar.gz
Source2: perl-%{perl_version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
# Prevent to detect dependencies such as perl(Devel::PatchPerl) >= 0.88
AutoReqProv: no

%description
Use plenv to pick a Perl version for your application and guarantee
that your development environment matches production.
Put plenv to work with Carton for painless Perl upgrades and bulletproof deployments.

%prep

%setup -a 1 -a 2 -n %{name}
mkdir plugins
mv perl-build plugins/perl-build

%build
# Check out specific versions.
git checkout -b %{version} refs/tags/%{version}
cd plugins/perl-build
git checkout -b %{perl_build_version} refs/tags/%{perl_build_version}
cd %{_builddir}/%{name}
# Build and install Perl.
# Emulate installation by "plenv install X.X.X" with default configuration options.
mkdir -p %{buildroot}%{plenvroot}/versions/%{perl_version}
cd perl-%{perl_version}
sh Configure -de -Dprefix=%{plenvroot}/versions/%{perl_version} -Dusedevel -A'eval:scriptdir=%{plenvroot}/versions/%{perl_version}/bin'
cd %{_builddir}/%{name}

%install
cd perl-%{perl_version}
make install DESTDIR=%{buildroot}
cd %{_builddir}/%{name}
rm -rf build cache shims perl-%{perl_version} %{_builddir}/%{name}%{plenvroot}
cp -r * %{buildroot}%{plenvroot}
cp -r .git %{buildroot}%{plenvroot}
cp .gitattributes %{buildroot}%{plenvroot}
cp .gitignore %{buildroot}%{plenvroot}
cp .travis.yml %{buildroot}%{plenvroot}

cd %{buildroot}%{plenvroot}/versions/%{perl_version}/bin
for file in `find . -type f`
do
    ln -s $file ${file/%{perl_version}/}
done
cd %{_builddir}/%{name}

%files
%defattr(664,travail,travail,775)
%dir %{plenvroot}
%dir %{plenvroot}/.git
%{plenvroot}/.git/*
%{plenvroot}/.gitattributes
%{plenvroot}/.gitignore
%{plenvroot}/.travis.yml
%{plenvroot}/Changes
%{plenvroot}/LICENSE
%{plenvroot}/Makefile
%{plenvroot}/README.md
%dir %{plenvroot}/author
%attr(775,travail,travail) %{plenvroot}/author/*
%dir %{plenvroot}/bin
%attr(775,travail,travail) %{plenvroot}/bin/*
%dir %{plenvroot}/completions
%{plenvroot}/completions/*
%dir %{plenvroot}/libexec
%attr(775,travail,travail) %{plenvroot}/libexec/*
%dir %{plenvroot}/plenv.d/
%dir %{plenvroot}/plenv.d/rehash
%attr(775,travail,travail) %{plenvroot}/plenv.d/rehash/*
%dir %{plenvroot}/test/
%{plenvroot}/test/*

%dir %{plenvroot}/plugins
%dir %{plenvroot}/plugins/perl-build
%dir %{plenvroot}/plugins/perl-build/.git
%{plenvroot}/plugins/perl-build/.git/*
%{plenvroot}/plugins/perl-build/.gitignore
%{plenvroot}/plugins/perl-build/.travis.yml
%{plenvroot}/plugins/perl-build/Build.PL
%{plenvroot}/plugins/perl-build/Changes
%{plenvroot}/plugins/perl-build/LICENSE
%{plenvroot}/plugins/perl-build/MANIFEST.SKIP
%{plenvroot}/plugins/perl-build/META.json
%{plenvroot}/plugins/perl-build/README.md
%dir %{plenvroot}/plugins/perl-build/author
%{plenvroot}/plugins/perl-build/author/*
%dir %{plenvroot}/plugins/perl-build/bin
%attr(775,travail,travail) %{plenvroot}/plugins/perl-build/bin/*
%{plenvroot}/plugins/perl-build/cpanfile
%dir %{plenvroot}/plugins/perl-build/lib
%dir %{plenvroot}/plugins/perl-build/lib/Perl
%{plenvroot}/plugins/perl-build/lib/Perl/*.pm
%dir %{plenvroot}/plugins/perl-build/lib/Perl/Build
%{plenvroot}/plugins/perl-build/lib/Perl/Build/*
%{plenvroot}/plugins/perl-build/minil.toml
%attr(755,travail,travail) %{plenvroot}/plugins/perl-build/perl-build
%dir %{plenvroot}/plugins/perl-build/script
%attr(755,travail,travail) %{plenvroot}/plugins/perl-build/script/*
%dir %{plenvroot}/plugins/perl-build/t
%{plenvroot}/plugins/perl-build/t/*
%dir %{plenvroot}/plugins/perl-build/xt
%{plenvroot}/plugins/perl-build/xt/*

%attr(775,travail,travail) %dir %{plenvroot}/versions
%dir %{plenvroot}/versions/%{perl_version}
%dir %{plenvroot}/versions/%{perl_version}/bin
%attr(775,travail,travail) %{plenvroot}/versions/%{perl_version}/bin/*
%dir %{plenvroot}/versions/%{perl_version}/lib
%{plenvroot}/versions/%{perl_version}/lib/*
%dir %{plenvroot}/versions/%{perl_version}/man
%{plenvroot}/versions/%{perl_version}/man/*

%clean

%changelog
* Thu Jul 11 2016 travail <travail@gmail.com> 2.2.0
- Initial build with perl-build 1.13 and perl-5.22.2.
