%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name bacon

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.2.0
Release: 2%{?dist}
Summary: A small RSpec clone
Group: Development/Languages
License: MIT
URL: http://github.com/chneukirchen/bacon
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Bacon is a small RSpec clone weighing less than 350 LoC but
nevertheless providing all essential features.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

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
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x


# Derop weird non-utf8 characters in e-mail framework
LANG=C sed 's/\xc2//g' -i %{buildroot}%{gem_instdir}/ChangeLog

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
bin/bacon -Ilib:. --automatic --quiet
%{?scl:EOF}
popd

%files
%{_bindir}/bacon
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%dir %{gem_instdir}/bin
%{gem_instdir}/bin/bacon
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/Rakefile
%{gem_instdir}/bacon.gemspec
%{gem_instdir}/test
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/RDOX
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/ChangeLog
%doc %{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Vít Ondruch <vondruch@redhat.com> - 1.2.0-1
- Update to Bacon 1.2.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.0-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.0-6
- Rebuilt for Ruby 1.9.3.
- Removed unneeded %%defattr and %%clean section.
- Introduced -doc subpackage.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.0-2
- Run tests
- Drop useless macro

* Thu Jun 25 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.0-1
- Package generated by gem2rpm
- Fix up plist
- Make rpmlint happy
