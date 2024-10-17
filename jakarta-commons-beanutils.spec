%define debug_package   %{nil}
%define gcj_support	1
%define base_name	beanutils
%define short_name	commons-%{base_name}

Name:		jakarta-%{short_name}
Version:	1.7.0
Release:	6.0.9
Epoch:		0
Summary:	Jakarta Commons BeanUtils Package
License:	Apache License
Group:		Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:	http://www.apache.org/dist/jakarta/commons/beanutils/source/commons-beanutils-1.7.0-src.tar.bz2
Source1:        pom-maven2jpp-depcat.xsl
Source2:        pom-maven2jpp-newdepmap.xsl
Source3:        pom-maven2jpp-mapdeps.xsl
Source4:        commons-beanutils-1.7.0-jpp-depmap.xml
Source5:        commons-beanutils-1.7.0.pom
Source6:        commons-beanutils-bean-collections-1.7.0.pom
Source7:        commons-beanutils-core-1.7.0.pom
Source8:        commons-build.tar.gz
Source9:        commons-beanutils-maven.xml
Source10:       commons-beanutils-build-other-jars.xml

Patch0:         commons-beanutils-1.7.0-project_xml.patch
Patch1:         commons-beanutils-1.7.0-BeanificationTestCase.patch
Patch2:         commons-beanutils-1.7.0-LocaleBeanificationTestCase.patch
Patch3:         commons-beanutils-1.7.0-navigation_xml.patch
Patch4:         commons-beanutils-1.7.0-project_properties.patch
Url:		https://jakarta.apache.org/commons/%{base_name}/
BuildRequires:	ant
BuildRequires:	locales-en
BuildRequires:	jakarta-commons-collections >= 0:2.0
BuildRequires:	jakarta-commons-logging >= 0:1.0
BuildRequires:	java-rpmbuild > 0:1.5
Requires:	jakarta-commons-collections >= 0:2.0
Requires:	jakarta-commons-logging >= 0:1.0
Provides:	%{short_name}
Obsoletes:	%{short_name}
# libgcj aot-compiled native libraries
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%else
BuildArch:	noarch
%endif

%description
The scope of this package is to create a package of Java utility methods
for accessing and modifying the properties of arbitrary JavaBeans.  No
dependencies outside of the JDK are required, so the use of this package
is very lightweight.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
gzip -dc %{SOURCE8} | tar xf -
cp %{SOURCE9} maven.xml
cp %{SOURCE10} build-other-jars.xml
%remove_java_binaries
%patch0 -b .sav
%patch1 -p0 -b .sav
%patch2 -p0 -b .sav
%patch3 -p0 -b .sav
%patch4 -b .sav


%build
export LC_ALL=ISO-8859-1
export CLASSPATH=$(build-classpath commons-collections commons-logging)
%ant -Dbuild.sysclasspath=first dist

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 dist/%{short_name}-core.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-core-%{version}.jar
install -m 644 dist/%{short_name}-bean-collections.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-bean-collections-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}
%add_to_maven_depmap %{short_name} %{short_name}-core %{version} JPP %{short_name}-core
%add_to_maven_depmap %{short_name} %{short_name}-bean-collections %{version} JPP %{short_name}-bean-collections

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{short_name}.pom
install -pm 644 %{SOURCE6} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{short_name}-bean-collections.pom
install -pm 644 %{SOURCE7} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{short_name}-core.pom


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc PROPOSAL.html STATUS.html RELEASE-NOTES.txt LICENSE.txt
%{_javadir}/*
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}




%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7.0-6.0.6mdv2011.0
+ Revision: 606046
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7.0-6.0.5mdv2010.1
+ Revision: 522926
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.7.0-6.0.4mdv2010.0
+ Revision: 425394
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.7.0-6.0.3mdv2009.1
+ Revision: 351266
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.7.0-6.0.2mdv2009.0
+ Revision: 167932
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.0-6.0.2mdv2008.1
+ Revision: 120900
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Mon Dec 10 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.7.0-6.0.1mdv2008.1
+ Revision: 116860
- add maven poms (jpp sync)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.0-4.5mdv2008.0
+ Revision: 87398
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.7.0-4.4mdv2008.0
+ Revision: 82887
- rebuild


* Wed Mar 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.7.0-4.3mdv2007.1
+ Revision: 143901
- rebuild for 2007.1
- Import jakarta-commons-beanutils

* Fri Aug 04 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-4.2mdv2007.0
- bump release to allow upload

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-4.1mdv2007.0
- bump release

* Sun Jun 11 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-3.0.1mdv2007.0
- bump release to supercede jpp, even though we don't use maven
- don't always build as noarch

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-2.2.3mdv2006.0
- rebuild for libgcj.so.7

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-2.2.2mdk
- quiet %%setup

* Wed Oct 26 2005 David Walluck <walluck@mandriva.org> 0:1.7.0-2.2.1mdk
- natify

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.7.0-2.1mdk
- release

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.7.0-2.1mdk
- release

* Sat Jan 29 2005 Ralph Apel <r.apel@r-apel.de> - 0:1.7.0-2jpp
- Use the "dist" target to get a full build, including bean-collections

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.7.0-1jpp
- Upgrade to 1.7.0

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.6.1-5jpp
- Rebuild with ant-1.6.2

