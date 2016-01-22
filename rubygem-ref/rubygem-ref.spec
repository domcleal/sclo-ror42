%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from ref-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ref

Summary: Library that implements weak, soft, and strong references in Ruby
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.5
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/bdurand/ref
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Library that implements weak, soft, and strong references in Ruby that work
across multiple runtimes (MRI, REE, YARV, Jruby, Rubinius, and IronRuby). Also
includes implementation of maps/hashes that use references and a reference
queue.


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

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
# To run the tests using minitest 5
ruby -rminitest/autorun - << \RUBY
 module Kernel
   alias orig_require require
   remove_method :require

   def require path
     orig_require path unless path == 'test/unit'
   end
 end

 Test = Minitest

 Dir.glob "./test/**/*_test.rb", &method(:require)
RUBY
%{?scl:EOF}
popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/ext
%doc %{gem_instdir}/MIT_LICENSE
%{gem_libdir}
%exclude %{gem_libdir}/org
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/VERSION
%{gem_instdir}/test
%exclude %{gem_instdir}/test/*.rbc

%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 1.0.5-2
- Rebuild for sclo-ror42 SCL

* Mon Jan 26 2015 Josef Stribny <jstribny@redhat.com> - 1.0.5-1
- Update to 1.0.5

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.0-5
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Mon May 25 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.0-3
- Rebuilt for SCL.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Initial package
