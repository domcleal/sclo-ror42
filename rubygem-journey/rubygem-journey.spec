%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from journey-1.0.1.gem by gem2rpm -*- rpm-spec -*-

# TODO: It seems that this gem carries 3D JS library. Although JS libraries
# have exeption ATM, I asked upstream if they could remove it.
#
# https://github.com/rails/journey/issues/15

%global gem_name journey

Summary: Journey is a router
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.4
Release: 9%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/rails/journey
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fixes "TypeError: no implicit conversion of Journey::Path::Pattern into String"
# https://github.com/rails/journey/commit/d836e960d9a20c4c5bc986630d2ba34a340959ea
Patch0: rubygem-journey-2.0.0-fix-assertion-calls.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix_ruby}rubygem(json)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Journey is a router. It routes requests.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd ./%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.rdoc
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/journey.gemspec
%{gem_instdir}/test

%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 1.0.4-9
- Rebuild for sclo-ror42 SCL

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 13 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.4-7
- Fix FTBFS in Rawhide (rhbz#1107148).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.4-4
- Fixed license, the Public Domain file was removed.

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.4-1
- Update to Journey 1.0.4, as this version is needed by ActionPack 3.2.6.
- Remove unneded Requires: ruby.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.1-2
- Move README.rdoc containing license into main package.

* Fri Jan 27 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.1-1
- Initial package
