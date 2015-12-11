%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
# Generated from metaclass-0.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name metaclass

Summary: Adds a metaclass method to all Ruby objects
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.4
Release: 1%{?dist}
Group: Development/Languages
# https://github.com/floehopper/metaclass/issues/1
License: MIT
URL: http://github.com/floehopper/metaclass
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Move test suite to Minitest 5
# https://github.com/floehopper/metaclass/pull/8
Patch0: rubygem-metaclass-minitest5.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Adds a metaclass method to all Ruby objects


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
# test_helper.rb currently references bundler, so it is easier to avoid
# its usage at all.
sed -i '2d' ./test/test_helper.rb
%{?scl:scl enable %scl - << \EOF}
RUBYOPT="-Ilib:test -rmetaclass" ruby -e 'Dir.glob "./test/*_test.rb", &method(:require)'
%{?scl:EOF}
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING.txt
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/metaclass.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%doc %{gem_docdir}


%changelog
* Mon Jan 19 2015 Josef Stribny <jstribny@redhat.com> - 0.0.4-1
- Update to 0.0.4

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.1-9
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Thu May 30 2013 Josef Stribny <jstribny@redhat.com> - 0.0.1-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.1-8
- Specfile cleanup.

* Tue Jun 12 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.1-7
- Test rebuild for SCL

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.1-6
- Rebuilt for scl.

* Wed Jan 18 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.1-5
- Build for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.1-3
- Move README.md into -doc subpackage and properly mark.

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.1-2
- Clarified license.

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.1-1
- Initial package
