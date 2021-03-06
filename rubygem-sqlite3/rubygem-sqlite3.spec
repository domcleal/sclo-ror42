%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}

%global gem_name sqlite3

Summary:        Allows Ruby scripts to interface with a SQLite3 database
Name:           %{?scl_prefix}rubygem-%{gem_name}
Version:        1.3.10
Release:        2%{?dist}
Group:          Development/Languages
License:        BSD
URL:            https://github.com/sparklemotion/sqlite3-ruby
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:       %{?scl_prefix_ruby}ruby(rubygems)
Requires:       %{?scl_prefix_ruby}ruby(release)
BuildRequires:  %{?scl_prefix_ruby}rubygems-devel
BuildRequires:  %{?scl_prefix_ruby}ruby-devel
BuildRequires:  sqlite-devel
BuildRequires:  %{?scl_prefix_ruby}rubygem(rake)
BuildRequires:	%{?scl_prefix_ruby}rubygem(minitest) >= 5.0.0
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}-%{release}

%description
SQLite3/Ruby is a module to allow Ruby scripts to interface with a SQLite3
database.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
# setup.rb shipped in the -doc subpackage has LGPLv2.1 licensing
License: BSD and LGPLv2
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -q -c -T

%{?scl:scl enable %{scl} - << \EOF}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
%gem_install -n %{SOURCE0}
%{?scl:EOF}

# Permission
find . -name \*.rb -or -name \*.gem | xargs chmod 0644

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
mkdir -p %{buildroot}%{gem_extdir_mri}/sqlite3
mv %{buildroot}%{gem_instdir}/ext/sqlite3/sqlite3_native.so %{buildroot}%{gem_extdir_mri}/sqlite3
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/

%check
%{?scl:scl enable %{scl} - << \EOF}
pushd .%{gem_instdir}
ruby -I$(dirs +1)%{gem_extdir_mri}:lib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd
%{?scl:EOF}

%files
%{gem_extdir_mri}
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gemtest
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/ext
%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/API_CHANGES.rdoc
%doc %{gem_instdir}/CHANGELOG.rdoc
%doc %{gem_instdir}/ChangeLog.cvs
%doc %{gem_instdir}/Manifest.txt
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/setup.rb
%doc %{gem_docdir}
%doc %{gem_instdir}/faq/
%{gem_instdir}/tasks/
%{gem_instdir}/test/


%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 1.3.10-2
- Rebuild for sclo-ror42 SCL

* Mon Jan 19 2015 Josef Stribny <jstribny@redhat.com> - 1.3.10-1
- Update to 1.3.10

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.3.6-5
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Wed Nov 20 2013 Josef Stribny <jstribny@redhat.com> - 1.3.6-4
- Fix -doc license
  - Resolves: rhbz#969970

* Fri Oct 04 2013 Josef Stribny <jstribny@redhat.com> - 1.3.6-3
- Rebuild because of fixed rubygems extension path

* Thu May 30 2013 Josef Stribny <jstribny@redhat.com> - 1.3.6-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.6-1
- Update to Sqlite3 1.3.6.
- Specfile cleanup

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.5-1
- Rebuilt for scl.
- Updated to 1.3.5.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.4-3
- Rebuilt for Ruby 1.9.3.
- Drop ruby-sqlite3 subpackage.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.4-1
- Updated to sqlite3 1.3.4.
- Use the upstream big endian fix.

* Wed Jun 22 2011 Dan Horák <dan[at]danny.cz> - 1.3.3-5
- fix build on big endian arches (patch by Vít Ondruch)

* Fri Jun 03 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.3-4
- The subdirectory of ruby_sitearch has to be owned by package.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.3-2
- Updated links.
- Removed obsolete BuildRoot.
- Removed unnecessary cleanup.

* Wed Feb 02 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.3-1
- Package renamed from rubygem-sqlite3-ruby to rubygem-sqlite3.
- Test suite executed upon build.
- Documentation moved into separate package.
- Removed clean section which is not necessary.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-4
- F-12: Rebuild to create valid debuginfo rpm again (ref: #505774)

* Tue Jun 16 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-3
- Create ruby-sqlite3 as subpackage (ref: #472621, #472622)
- Use gem as source

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.2.4-1
- Fix items from review (#459881)
- New upstream version

* Sun Aug 31 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.2.2-2
- Fix items from review (#459881)

* Sun Jul 13 2008 Matt Hicks <mhicks@localhost.localdomain> - 1.2.2-1
- Initial package
