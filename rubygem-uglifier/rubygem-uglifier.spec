%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from uglifier-1.2.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name uglifier

Summary: Ruby wrapper for UglifyJS JavaScript compressor
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.4.0
Release: 1%{?dist}
Group: Development/Languages
# Uglifier itself is MIT
# the bundled JavaScript from UglifyJS is BSD
License: MIT and BSD
URL: http://github.com/lautis/uglifier
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(execjs) >= 0.3.0
Requires: %{?scl_prefix_ruby}rubygem(json) => 1.8
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(execjs) >= 0.3.0
BuildRequires: %{?scl_prefix_ruby}rubygem(json) => 1.8
BuildRequires: %{?scl_prefix}rubygem(rspec)
BuildRequires: %{?scl_prefix}rubygem(therubyracer)
BuildRequires: %{?scl_prefix_v8}v8
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Ruby wrapper for UglifyJS JavaScript compressor.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %scl - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}

# source_map is not part of the collection, ged rid of source_map in specs
sed -i "s/require 'source_map'//"  spec/spec_helper.rb
rm spec/source_map_spec.rb

%{?scl:scl enable %scl %scl_v8 - << \EOF}
rspec spec
%{?scl:EOF}
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%exclude %{gem_instdir}/gemfiles
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md

%changelog
* Mon Jan 26 2015 Josef Stribny <jstribny@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Mon Feb 17 2014 Josef Stribny <jstribny@redhat.com> - 2.2.1-4
- Depend on scldevel(v8) virtual provide

* Thu Jan 23 2014 Vít Ondruch <vondruch@redhat.com> - 2.2.1-3
- Fix rubygems dependency.

* Tue Nov 26 2013 Josef Stribny <jstribny@redhat.com> - 2.2.1-2
- Use v8 scl macro

* Mon Oct 21 2013 Josef Stribny <jstribny@redhat.com> - 2.2.1-1
- Update to uglifier 2.2.1

* Wed Jun 12 2013 Josef Stribny <jstribny@redhat.com> - 1.2.6-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Jul 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.6-2
- Imported from Fedora again.

* Mon Jul 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.6-1
- Initial package
