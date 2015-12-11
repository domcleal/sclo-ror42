# Generated from atomic-1.1.8.gem by gem2rpm -*- rpm-spec -*-
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}

%global gem_name atomic

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.1.16
Release: 1%{?dist}
Summary: An atomic reference implementation for JRuby, Rubinius, and MRI
Group: Development/Languages
License: ASL 2.0
URL: http://github.com/headius/ruby-atomic
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
An atomic reference implementation for JRuby, Rubinius, and MRI.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

# Remove useless shebangs.
sed -i -e '/^#!\/usr\/bin\/env/d' %{buildroot}%{gem_instdir}/examples/*.rb

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib -e 'Dir.glob "./test/test_*.rb", &method(:require)'
%{?scl:EOF}
popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Wed Jan 14 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.16-1
- Update to atomic 1.1.16.

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.1.14-2
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Mon Oct 21 2013 Josef Stribny <jstribny@redhat.com> - 1.1.14-1
- Update to atomic 1.1.14

* Thu Oct 03 2013 Josef Stribny <jstribny@redhat.com> - 1.1.9-4
- Fix macros for -doc sub-package

* Thu Oct 03 2013 Josef Stribny <jstribny@redhat.com> - 1.1.9-3
- Rebuild for scl

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.9-1
- Update to atomic 1.1.9.

* Mon May 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.8-1
- Initial package
