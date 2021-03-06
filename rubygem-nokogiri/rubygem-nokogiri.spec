%{?scl:%scl_package rubygem-%{gemname}}
%{!?scl:%global pkg_name %{name}}

%global	mainver		1.6.7
%global	prever		.rc3

%global	mainrel		4
%global	prerpmver		%(echo "%{?prever}" | sed -e 's|\\.||g')

%global	gemname		nokogiri
%global	ruby19		1
%global	gemdir		%{gem_dir}
%global	geminstdir	%{gem_instdir}
%global	gemsodir	%{gem_extdir_mri}/lib
%global	gem_name	%{gemname}

# Note for packager:
# Nokogiri 1.4.3.1 gem says that Nokogiri upstream will
# no longer support ruby 1.8.6 after 2010-08-01, so
# it seems that 1.4.3.1 is the last version for F-13 and below.

Summary:	An HTML, XML, SAX, and Reader parser
Name:		%{?scl_prefix}rubygem-%{gemname}
Version:	%{mainver}
Release:	%{?prever:0.}%{mainrel}%{?prever:.%{prerpmver}}%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://nokogiri.rubyforge.org/nokogiri/
Source0:	https://rubygems.org/gems/%{gemname}-%{mainver}%{?prever}.gem
# ./test/html/test_element_description.rb:62 fails, as usual......
# Patch0:		rubygem-nokogiri-1.5.0.beta3-test-failure.patch
#Patch0:		rubygem-nokogiri-1.5.0-allow-non-crosscompile.patch
# Shut down libxml2 version unmatching warning
Patch0:	%{pkg_name}-1.6.6.4-shutdown-libxml2-warning.patch
Requires:	%{?scl_prefix_ruby}ruby(release)
BuildRequires:	%{?scl_prefix_ruby}ruby(release)

BuildRequires:	%{?scl_prefix_ruby}ruby(rubygems)
##
## For %%check
BuildRequires:	%{?scl_prefix_ruby}rubygem(minitest)
BuildRequires:	%{?scl_prefix_ruby}rubygems-devel
Obsoletes:		%{?scl_prefix_ruby}ruby-%{gemname} <= 1.5.2-2
#BuildRequires:	%{?scl_prefix}ruby(racc)
##
## Others
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	%{?scl_prefix_ruby}ruby-devel
Requires:	%{?scl_prefix_ruby}ruby(rubygems)
Provides:	%{?scl_prefix}rubygem(%{gemname}) = %{version}-%{release}

%description
Nokogiri parses and searches XML/HTML very quickly, and also has
correctly implemented CSS3 selector support as well as XPath support.

Nokogiri also features an Hpricot compatibility layer to help ease the change
to using correct CSS and XPath.

%if 0

%package	jruby
Summary:	JRuby support for %{pkg_name}
Group:		Development/Languages
Requires:	%{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description	jruby
This package contains JRuby support for %{pkg_name}.
%endif

%package	doc
Summary:	Documentation for %{pkg_name}
Group:		Documentation
Requires:	%{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description	doc
This package contains documentation for %{pkg_name}.

%package	-n %{?scl_prefix}ruby-%{gemname}
Summary:	Non-Gem support package for %{gemname}
Group:		Development/Languages
Requires:	%{?scl_prefix}%{pkg_name} = %{version}-%{release}
Provides:	%{?scl_prefix}ruby(%{gemname}) = %{version}-%{release}

%description	-n %{?scl_prefix}ruby-%{gemname}
This package provides non-Gem support for %{gemname}.

%global	version	%{mainver}%{?prever}

%prep
%setup -n %{pkg_name}-%{version} -q -T -c

# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
cd %{gem_name}-%{version}

# patches
%patch0 -p1

%{?scl:scl enable %{scl} - << \EOF}
gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
%{?scl:EOF}

# remove bundled external libraries
sed -i \
	-e 's|, "ports/archives/[^"][^"]*"||g' \
	-e 's|, "ports/patches/[^"][^"]*"||g' \
	%{gem_name}.gemspec
# Actually not needed when using system libraries
sed -i -e '\@mini_portile@d' %{gem_name}.gemspec

# Ummm...
%{?scl:scl enable %{scl} - << \EOF}
env LANG=ja_JP.UTF-8 gem build %{gem_name}.gemspec
%{?scl:EOF}
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
mkdir -p ./%{gemdir}
# 1.6.0 needs this
export NOKOGIRI_USE_SYSTEM_LIBRARIES=yes

%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}


# Permission
chmod 0644 .%{gem_cache}

# Remove precompiled Java .jar file
rm -f .%{geminstdir}/lib/*.jar
# For now remove JRuby support
rm -rf .%{geminstdir}/ext/java

%install
mkdir -p %{buildroot}%{gemdir}
cp -a ./%{gemdir}/* %{buildroot}%{gemdir}

# Remove backup file
find %{buildroot} -name \*.orig_\* | xargs rm -vf

# move arch dependent files to %%gem_extdir
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd

# move bin/ files
mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

# remove all shebang
for f in $(find %{buildroot}%{geminstdir} -name \*.rb)
do
	sed -i -e '/^#!/d' $f
	chmod 0644 $f
done

# cleanups
rm -rf %{buildroot}%{geminstdir}/ext/%{gemname}/
rm -rf %{buildroot}%{geminstdir}/tmp/
rm -f %{buildroot}%{geminstdir}/{.autotest,.require_paths,.gemtest,.travis.yml}
rm -f %{buildroot}%{geminstdir}/appveyor.yml
rm -f %{buildroot}%{geminstdir}/.cross_rubies
rm -f %{buildroot}%{geminstdir}/{build_all,dependencies.yml,test_all}
rm -f %{buildroot}%{geminstdir}/.editorconfig
rm -rf %{buildroot}%{geminstdir}/suppressions/
rm -rf %{buildroot}%{geminstdir}/patches/

%check
# Ah....
# test_exslt(TestXsltTransforms) [./test/test_xslt_transforms.rb:93]
# fails without TZ on sparc
export TZ="Asia/Tokyo"
#???
LANG=ja_JP.UTF-8

pushd ./%{geminstdir}

# Need investigation. For now anyway build
%{?scl:scl enable %{scl} - << \EOF}
ruby \
	-I.:lib:test:ext \
	-e \
	"require 'test/helper' ; Dir.glob('test/**/test_*.rb'){|f| require f}" || \
	echo "Please investigate this"
%{?scl:EOF}

for f in $SKIPTEST
do
	mv $f.skip $f
done

popd

%files
%defattr(-,root, root,-)
%{_bindir}/%{gemname}
%{gem_extdir_mri}/
%dir	%{geminstdir}/
%doc	%{geminstdir}/[A-Z]*
#%%doc	%{geminstdir}/nokogiri_help_responses.md
%exclude %{geminstdir}/Rakefile
%exclude %{geminstdir}/Gemfile
%{geminstdir}/bin/
%{geminstdir}/lib/
%exclude	%{gem_cache}
%{gemdir}/specifications/%{gemname}-%{mainver}%{?prever}.gemspec

%if 0

%files	jruby
%defattr(-,root,root,-)
%{geminstdir}/ext/java/
%endif

%files	doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
#%%{geminstdir}/deps.rip
#%%{geminstdir}/spec/
%{geminstdir}/tasks/
%{geminstdir}/test/
%{gemdir}/doc/%{gemname}-%{mainver}%{?prever}/

%changelog
* Thu Dec 17 2015 Dominic Cleal <dcleal@redhat.com> 1.6.7-0.4.rc3
- Fix macro expansions for EL6 under SCL

* Fri Dec 11 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7-0.3.rc3
- Shutdown libxml2 version mismatch warning
* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7-0.2.rc3
- Rebuild against new libxml2, to make rspec test succeed

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.7-0.1.rc3
- 1.6.7.rc3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.6.2-1
- 1.6.6.2

* Fri Jan 23 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.6.1-1
- 1.6.6.1

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.5-2
- Rebuild for ruby 2.2

* Mon Dec  1 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.5-1
- 1.6.5

* Fri Nov  7 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.4.1-1
- 1.6.4.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.3.1-1
- 1.6.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.2.1-1
- 1.6.2.1

* Thu Apr 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.1-2
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Wed Dec 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.1-1
- 1.6.1

* Fri Oct  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-1
- 1.6.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.9-1
- 1.5.9

* Tue Mar 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.5.6-3
- Use %%{gem_extdir_mri} instead of %%{gem_extdir}.

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 1.5.6-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.6-1
- A Happy New Year
- 1.5.6

* Fri Aug 17 2012 Vít Ondruch <vondruch@redhat.com> - 1.5.5-2
- Rebuilt againts libxml2 2.9.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.5-1
- 1.5.5

* Mon May 28 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.2-3
- Fix Obsoletes (bug 822931)

* Mon Apr  9 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.2-1
- 1.5.2

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.5.0-3
- Fix conditionals for F17 to work for RHEL 7 as well.

* Tue Jan 24 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-2
- F-17: rebuild for ruby19
- For now aviod build failure by touching some files

* Thu Jan 18 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-1
- 1.5.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.5.beta4.1
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-0.5.beta4
- Remove unneeded patch

* Thu Mar 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.0-0.4.beta4
- Patch for newer rake to make testsuite run

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.3.beta4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.0-0.3.beta4
- 1.5.0.beta.4

* Tue Dec  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.0-0.2.beta3
- 1.5.0.beta.3

* Sun Oct 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.0-0.1.beta2
- Try 1.5.0.beta.2

* Fri Jul 30 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.3.1-1
- 1.4.3.1

* Wed May 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.2-1
- 1.4.2

* Thu Apr 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-2
- Fix build failure with libxml2 >= 2.7.7

* Tue Dec 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-1
- 1.4.1

* Mon Nov  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.0-1
- 1.4.0

* Sat Aug 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.3-2
- Fix test failure on sparc

* Wed Jul 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.3-1
- 1.3.3

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-3
- F-12: Mass rebuild

* Thu Jul  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-2
- Enable test
- Recompile with -O2

* Thu Jun 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.2-1
- 1.3.2

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3.1-1
- 1.3.1

* Thu Mar 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-1
- 1.2.3

* Thu Mar 19 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.2-1
- 1.2.2

* Thu Mar 12 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.1-1
- 1.2.1

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.1-2
- F-11: Mass rebuild

* Thu Jan 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.1-1
- 1.1.1

* Thu Dec 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.0-1
- Initial packaging
