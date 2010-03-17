%define debug_package   %{nil}
%define gcj_support	1
%define base_name	beanutils
%define short_name	commons-%{base_name}
%define name		jakarta-%{short_name}
%define version		1.7.0
%define	section		free

Name:		%{name}
Version:	%{version}
Release:	%mkrel 6.0.5
Epoch:		0
Summary:	Jakarta Commons BeanUtils Package
License:	Apache License
Group:		Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
Url:		http://jakarta.apache.org/commons/%{base_name}/
BuildRequires:	ant
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
%patch1 -b .sav
%patch2 -b .sav
%patch3 -b .sav
%patch4 -b .sav


%build
export CLASSPATH=$(build-classpath commons-collections commons-logging)
%ant -Dbuild.sysclasspath=first dist

%install
rm -rf $RPM_BUILD_ROOT
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

%clean
rm -rf $RPM_BUILD_ROOT


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


