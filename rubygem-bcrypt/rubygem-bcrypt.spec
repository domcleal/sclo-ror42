%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name bcrypt

Summary: Wrapper around bcrypt() password hashing algorithm
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 3.1.10
Release: 1%{?dist}
Group: Development/Languages
# ext/* - Public Domain
# spec/TestBCrypt.java - ISC
License: MIT and Public Domain and ISC
URL: https://github.com/codahale/bcrypt-ruby
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems) 
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby-devel
BuildRequires: %{?scl_prefix}rubygem(rspec)
Provides: %{?scl_prefix}rubygem(bcrypt) = %{version}

%description
bcrypt() is a sophisticated and secure hash algorithm designed by The
OpenBSD project for hashing passwords. bcrypt-ruby provides a simple,
humane wrapper for safely handling passwords.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description doc
Documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -pa .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

%check
%{?scl:scl enable %{scl} - << \EOF}
pushd .%{gem_instdir}
# 2 failutes due to old RSpec
# https://github.com/rspec/rspec-expectations/pull/284
rspec -I$(dirs +1)%{gem_extdir_mri} spec |grep '34 examples, 2 failures' || exit 1
popd
%{?scl:EOF}

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/COPYING

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile*
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec

%changelog
* Thu Dec 17 2015 Dominic Cleal <dcleal@redhat.com> 3.1.10-1
- Update to 3.1.10

* Thu Jan 22 2015 Josef Stribny <jstribny@redhat.com> - 3.1.9-2
- Convert to SCL

* Thu Jan 15 2015 Vít Ondruch <vondruch@redhat.com> - 3.1.9-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Update to BCrypt 3.1.9.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Josef Stribny <jstribny@redhat.com> - 3.1.7-5
- Fix provides to reflect rubygem(brypt-ruby) as well

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 3.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Mon Apr 07 2014 Josef Stribny <jstribny@redhat.com> - 3.1.7-3
- Fix typo, obsoletes, upstream URL

* Thu Mar 20 2014 Josef Stribny <jstribny@redhat.com> - 3.1.7-2
- Create -doc subpackage
- Fix obsoletes

* Tue Mar 18 2014 Josef Stribny <jstribny@redhat.com> - 3.1.7-1
- Rename package to rubygem-bcrypt (this obsoletes bcrypt-ruby)
- Update to bcrypt 3.1.7

* Wed Nov 27 2013 Vít Ondruch <vondruch@redhat.com> - 3.1.2-2
- Prevent dangling symlink in -debuginfo.

* Mon Nov 11 2013 Josef Stribny <jstribny@redhat.com> - 3.1.2-1
- Update to brypt-ruby 3.1.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Vít Ondruch <vondruch@redhat.com> - 3.0.1-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.1-4
- Fixed wrong provide.

* Mon Jan 23 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.1-1
- Update to bcrypt-ruby 3.0.1.

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 2.1.2-4
- Replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 24 2010 Mohammed Morsi <mmorsi@redhat.com> - 2.1.2-2
- Updates / fixes based on review feedback
- Fixed bcrypt_ext.so install location

* Tue Aug 10 2010 Mohammed Morsi <mmorsi@redhat.com> - 2.1.2-1
- Initial package
