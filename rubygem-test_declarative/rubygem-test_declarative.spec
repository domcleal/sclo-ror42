%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}

# Generated from test_declarative-0.0.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name test_declarative

Summary: Simply adds a declarative test method syntax to test/unit
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.5
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/svenfuchs/test_declarative
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Minitest 5 support
# https://github.com/svenfuchs/test_declarative/pull/4
Patch0: rubygem-test_declarative-minitest5.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest) >= 5.0.0
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Simply adds a declarative test method syntax to test/unit.


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

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
ruby -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%exclude %{gem_cache}
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.textile
%{gem_instdir}/test


%changelog
* Mon Jan 19 2015 Josef Stribny <jstribny@redhat.com> - 0.0.5-6
- Use Minitest 5

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.5-5
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Fri Jun 07 2013 Josef Stribny <jstribny@redhat.com> - 0.0.5-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.5-3
- Specfile cleanup

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.5-2
- Rebuilt for scl.

* Fri Jan 20 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.5-1
- Initial package
