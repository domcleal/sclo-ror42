%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from rails-dom-testing-1.0.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails-dom-testing

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.5
Release: 2%{?dist}
Summary: Compares doms and assert certain elements exists in doms using Nokogiri
Group: Development/Languages
License: MIT
URL: https://github.com/kaspth/rails-dom-testing
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(activesupport) >= 4.1.0.beta
Requires: %{?scl_prefix}rubygem(activesupport) < 5.0
Requires: %{?scl_prefix}rubygem(nokogiri) >= 1.6.0
Requires: %{?scl_prefix}rubygem(nokogiri) < 1.7
Requires: %{?scl_prefix}rubygem(rails-deprecated_sanitizer) >= 1.0.1
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel 
BuildRequires: %{?scl_prefix_ruby}ruby 
BuildRequires: %{?scl_prefix}rubygem(activesupport) 
BuildRequires: %{?scl_prefix}rubygem(nokogiri) 
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest) 
BuildRequires: %{?scl_prefix}rubygem(rails-deprecated_sanitizer)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Dom and Selector assertions for Rails applications.

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

# Relax AS dependency.
sed -i '/activesupport/ s/4.2.0/4.1.0/' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




# Run the test suite

%check
pushd .%{gem_instdir}
# ActiveSupport::TestCase.test_order is not available in AS 4.1.
sed -i "/\.test_order/ s/^/#/" test/test_helper.rb

%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%doc %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.5-1
- Initial package
