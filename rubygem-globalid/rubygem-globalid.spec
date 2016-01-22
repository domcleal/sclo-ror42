%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from globalid-0.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name globalid

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.3.3
Release: 3%{?dist}
Summary: Refer to any model with a URI: gid://app/class/id
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/globalid.git && cd globalid
# git checkout v0.3.0
# tar czvf globalid-0.3.3-tests.tar.gz test/
Source1: globalid-0.3.3-tests.tar.gz
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(activesupport) >= 4.1.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel 
BuildRequires: %{?scl_prefix_ruby}ruby >= 1.9.3
BuildRequires: %{?scl_prefix}rubygem(activesupport) >= 4.1
BuildRequires: %{?scl_prefix}rubygem(activemodel) >= 4.1
BuildRequires: %{?scl_prefix}rubygem(railties) >= 4.1
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
URIs for your models makes it easy to pass references around.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar xf %{SOURCE1}
sed -i '1d' ./test/helper.rb
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -rforwardable -e "Dir.glob './test/cases/*test.rb', &method(:require)"
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/lib
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 0.3.3-3
- Rebuild for sclo-ror42 SCL

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Josef Stribny <jstribny@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Tue Jan 06 2015 Josef Stribny <jstribny@redhat.com> - 0.3.0-1
- Initial package
