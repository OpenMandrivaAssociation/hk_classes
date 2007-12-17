%define LIBMAJ 15
%define libname %mklibname %name %LIBMAJ
%define develname %mklibname %name -d
%define release %mkrel 3

Summary:	GUI independent C++ database application libraries	
Name:		hk_classes
Version: 	0.8.3
Release: 	%release
License:	GPL
Group:		Databases
Source:		http://hk-classes.sourceforge.net/hk_classes-%{version}.tar.bz2
Url:		http://hk-classes.sourceforge.net

BuildRequires:	mysql-devel 
BuildRequires:  postgresql-devel 
BuildRequires:  unixODBC-devel 
BuildRequires:  libpx-devel 
BuildRequires:  xbsql-devel
BuildRequires:	python-devel 
BuildRequires:  sqlite3-devel
%ifarch x86_64
%else
BuildRequires:  firebird-devel
%endif
BuildRequires:  chrpath 
Requires: 	%{libname} = %{version}-%{release}

%description

Hk_classes is a set of GUI independent C++ libraries which allow the rapid 
development of database applications and includes command line tools to use 
hk_classes in scripts.

firebird support is not available for x86_64

%package	-n python-%{name}
Summary:  	Python support for hk_classes
Group: 		Development/Python
%py_requires -d

%description -n python-%{name}

Python scripting support for hk_classes.

%package	-n %{libname}
Summary:  	Libraries for hk_classes applications
Group: 		System/Libraries
Obsoletes:	%mklibname %name 5
Conflicts:	%develname < 0.8.3-3
Conflicts:	%{mklibname -d %name 5}

%description -n %{libname}

Hk_classes libraries for command-line scripts and application development.

%package	-n %{develname}
Summary:  	Development files for hk_classes applications
Group: 		Development/Databases
Requires: 	%{libname} = %{version}-%{release}
Provides:	hk_classes-devel = %{version}
Obsoletes:	%mklibname -d %name 15
Conflicts:	%libname < 0.8.3-3
Conflicts:	%mklibname %name 5

%description -n %{develname}

Hk_classes header files for application development.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --with-xbase-libdir=%{_libdir}
%make

%install
%makeinstall_std

# (sb) create a default config file

install -d $RPM_BUILD_ROOT/%{_sysconfdir}
cat << EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/hk_classes.conf
<?xml version="1.0" ?>

<HK_VERSION>0.8.2</HK_VERSION>
<GENERAL>
  <SHOWPEDANTIC>YES</SHOWPEDANTIC>
  <DRIVERPATH>%{_libdir}/%{name}/drivers</DRIVERPATH>
  <DEFAULTFONT>Courier</DEFAULTFONT>
  <DEFAULTFONTSIZE>12</DEFAULTFONTSIZE>
  <DEFAULTTEXTALIGNMENT>LEFT</DEFAULTTEXTALIGNMENT>
  <DEFAULTNUMBERALIGNMENT>RIGHT</DEFAULTNUMBERALIGNMENT>
  <MAXIMIZEDWINDOWS>NO</MAXIMIZEDWINDOWS>
  <DEFAULTPRECISION>2</DEFAULTPRECISION>
  <DEFAULTTHOUSANDSSEPARATOR>NO</DEFAULTTHOUSANDSSEPARATOR>
  <DEFAULTDRIVER>mysql</DEFAULTDRIVER>
  <DEFAULTSIZETYPE>ABSOLUTE</DEFAULTSIZETYPE>
  <MEASURESYSTEM>CM</MEASURESYSTEM>
</GENERAL>
<HK_REGIONAL>
  <DEFAULTTIMEFORMAT>h:m:s</DEFAULTTIMEFORMAT>
  <DEFAULTDATETIMEFORMAT>D.M.Y h:m:s</DEFAULTDATETIMEFORMAT>
  <DEFAULTDATEFORMAT>D.M.Y</DEFAULTDATEFORMAT>
  <LOCALE/>
</HK_REGIONAL>
<REPORT>
  <PRINTERCOMMAND>lpr</PRINTERCOMMAND>
  <REPORTFONTENCODING>ISO-8859-1</REPORTFONTENCODING>
</REPORT>
EOF

# (sb) get rid of rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*

# (sb) fix the .la files
perl -pi -e "s|-L$RPM_BUILD_DIR/%{name}-%{version}/hk_classes||g" $RPM_BUILD_ROOT%{_libdir}/%{name}/drivers/*.la

# (sb) installed but not packaged
rm -rf $RPM_BUILD_ROOT/usr/local

mkdir -p %buildroot/%_sysconfdir/ld.so.conf.d
echo "%_libdir/%name" >  %buildroot/%_sysconfdir/ld.so.conf.d/%name.conf

%post -n %{libname}
grep -q "^/usr/lib/%{name}$" /etc/ld.so.conf || echo "/usr/lib/%{name}" >> /etc/ld.so.conf
/sbin/ldconfig

%postun -n %{libname}
if [ "$1" = "0" ]; then
    rm -f /etc/ld.so.conf.new
    grep -v -e "/usr/lib/%{name}" /etc/ld.so.conf > /etc/ld.so.conf.new
    mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc ChangeLog COPYING NEWS INSTALL README
%{_bindir}/hk_actionquery
%{_bindir}/hk_exportcsv
%{_bindir}/hk_exporthtml
%{_bindir}/hk_exportxml
%{_bindir}/hk_importcsv
%{_bindir}/hk_report
%{_bindir}/hk_dbcopy
%config(noreplace) %{_sysconfdir}/hk_classes.conf
%{_mandir}/man1/hk_actionquery.1man*
%{_mandir}/man1/hk_exportcsv.1man*
%{_mandir}/man1/hk_exporthtml.1man*
%{_mandir}/man1/hk_exportxml.1man*
%{_mandir}/man1/hk_importcsv.1man*
%{_mandir}/man1/hk_report.1man*
%{_mandir}/man1/hk_dbcopy.1man*

%files -n python-%{name}
%defattr(-,root,root)
%python_sitearch/*

%files -n %{libname}
%defattr(-,root,root)
%{_sysconfdir}/ld.so.conf.d/hk_classes.conf
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libhk_classes.so.%{LIBMAJ}*
%{_libdir}/%{name}/drivers

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}/libhk_classes.la
%{_libdir}/%{name}/libhk_classes.so
