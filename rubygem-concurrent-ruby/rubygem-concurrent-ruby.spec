%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name concurrent-ruby

Summary: Modern concurrency tools for Ruby
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.0
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/ruby-concurrency/concurrent-ruby
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Modern concurrency tools including agents, futures,
promises, thread pools, actors, supervisors, and more. Inspired by
Erlang, Clojure, Go, JavaScript, actors, and classic concurrency
patterns.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}


%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_docdir}

%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 1.0.0-1
- New package
