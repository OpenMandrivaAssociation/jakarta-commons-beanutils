%define debug_package   %{nil}
%define gcj_support	1
%define base_name	beanutils
%define short_name	commons-%{base_name}
%define name		jakarta-%{short_name}
%define version		1.7.0
%define	section		free

Name:		%{name}
Version:	%{version}
Release:	%mkrel 4.4
Epoch:		0
Summary:	Jakarta Commons BeanUtils Package
License:	Apache License
Group:		Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:	http://www.apache.org/dist/jakarta/commons/beanutils/source/commons-beanutils-1.7.0-src.tar.bz2
Url:		http://jakarta.apache.org/commons/%{base_name}/
BuildRequires:	ant
BuildRequires:	jakarta-commons-collections >= 0:2.0
BuildRequires:	jakarta-commons-logging >= 0:1.0
BuildRequires:	jpackage-utils > 0:1.5
Requires:	jakarta-commons-collections >= 0:2.0
Requires:	jakarta-commons-logging >= 0:1.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Provides:	%{short_name}
Obsoletes:	%{short_name}
# libgcj aot-compiled native libraries
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
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
#cp LICENSE.txt LICENSE
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
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
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc PROPOSAL.html STATUS.html RELEASE-NOTES.txt LICENSE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}


