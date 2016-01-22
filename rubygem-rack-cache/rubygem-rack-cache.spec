%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from rack-cache-1.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rack-cache


Summary: HTTP Caching for Rack
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.2
Release: 8%{?dist}
Group: Development/Languages
License: MIT
# The URL doesn't work.
# https://github.com/rtomayko/rack-cache/issues/65
URL: http://tomayko.com/src/rack-cache/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix}rubygem(rack) >= 0.4
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(rack) >= 0.4
BuildRequires: %{?scl_prefix}rubygem(bacon)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Rack::Cache is suitable as a quick drop-in component to enable HTTP caching for
Rack-based applications that produce freshness (Expires, Cache-Control) and/or
validation (Last-Modified, ETag) information

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
pushd ./%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
bacon -I. -q test/*_test.rb
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%exclude %{gem_instdir}/rack-cache.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile*
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/doc
%doc %{gem_instdir}/example
%{gem_instdir}/test

%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 1.2-8
- Rebuild for sclo-ror42 SCL

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 1.2-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Vít Ondruch <vondruch@redhat.com> - 1.2-1
- Updated to rack-cache 1.2.

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 1.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Vít Ondruch <vondruch@redhat.com> - 1.1-1
- Updated to rack-cache 1.1.

* Fri Jul 08 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.2-1
- Initial package
