%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from rails-html-sanitizer-1.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails-html-sanitizer

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.2
Release: 2%{?dist}
Summary: This gem is responsible to sanitize HTML fragments in Rails applications
Group: Development/Languages
License: MIT
URL: https://github.com/rails/rails-html-sanitizer
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(loofah) >= 2.0
Requires: %{?scl_prefix}rubygem(loofah) < 3
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(loofah)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(rails-dom-testing)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
HTML sanitization to Rails applications.

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
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)' | grep \
  %if 0%{?el6}
  "295 runs, 308 assertions, 2 failures, 0 errors, 0 skips"
  %else
  "295 runs, 308 assertions, 0 failures, 0 errors, 0 skips"
  %endif
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
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Fri Dec 18 2015 Dominic Cleal <dcleal@redhat.com> 1.0.2-2
- Ignore libxml2 related test failure on EL6

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.1-1
- Initial package
