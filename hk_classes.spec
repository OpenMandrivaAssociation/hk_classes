%define LIBMAJ 15
%define libname %mklibname %name %LIBMAJ
%define develname %mklibname %name -d
%define release 14

Summary:	GUI independent C++ database application libraries	
Name:		hk_classes
Version: 	0.8.3
Release: 	%release
License:	GPL
Group:		Databases
Source0:		http://hk-classes.sourceforge.net/hk_classes-%{version}.tar.bz2
Patch0:		hk_classes-0.8.3-gcc43.patch
Patch1:		hk_classes-0.8.3-fix-str-fmt.patch
patch2:		hk_classes-0.8.3.unistd.patch
Url:		http://hk-classes.sourceforge.net
BuildRequires:	fontconfig-devel
BuildRequires:	mysql-devel 
BuildRequires:  postgresql-devel 
BuildRequires:  unixODBC-devel 
BuildRequires:  libpx-devel 
BuildRequires:  xbsql-devel
BuildRequires:	pkgconfig(python) 
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
%patch0 -p1
%patch1 -p0
%patch2 -p1 -b .unistd

%build
%configure2_5x --with-xbase-libdir=%{_libdir}
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

%postun -n %{libname}
if [ "$1" = "0" ]; then
    rm -f /etc/ld.so.conf.new
    grep -v -e "/usr/lib/%{name}" /etc/ld.so.conf > /etc/ld.so.conf.new
    mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi

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
%{_libdir}/%{name}/libhk_classes.so


%changelog
* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 0.8.3-13mdv2011.0
+ Revision: 627248
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.8.3-12mdv2011.0
+ Revision: 626528
- rebuilt against mysql-5.5.8 libs

* Sun Nov 14 2010 Funda Wang <fwang@mandriva.org> 0.8.3-10mdv2011.0
+ Revision: 597469
- rebuild

* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 0.8.3-9mdv2011.0
+ Revision: 593919
- rebuild for py2.7

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.8.3-8mdv2010.0
+ Revision: 437869
- rebuild

* Sun Dec 28 2008 Funda Wang <fwang@mandriva.org> 0.8.3-7mdv2009.1
+ Revision: 320256
- fix str fmt

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.8.3-6mdv2009.1
+ Revision: 311335
- rebuilt against mysql-5.1.30 libs

* Thu Jul 31 2008 Funda Wang <fwang@mandriva.org> 0.8.3-5mdv2009.0
+ Revision: 257502
- fix underlining
- more gcc4.3 patch
- BR fontconfig
- add gcc 4.3 patch

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix spacing at top of description
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Oct 22 2007 Funda Wang <fwang@mandriva.org> 0.8.3-3mdv2008.1
+ Revision: 101127
- finally fix bug#29974, drivers/*.la should not belongs to devel package

  + Thierry Vignaud <tv@mandriva.org>
    - do not hardcode bz2 extension

* Tue Jun 26 2007 Funda Wang <fwang@mandriva.org> 0.8.3-2mdv2008.0
+ Revision: 44396
- corrected libmajor

* Tue Jun 26 2007 Funda Wang <fwang@mandriva.org> 0.8.3-1mdv2008.0
+ Revision: 44391
- New devel policy

  + Per Ã˜yvind Karlsen <peroyvind@mandriva.org>
    - update to 0.8.3


* Mon Jan 15 2007 Nicolas LÃ©cureuil <neoclust@mandriva.org> 0.8.2-2mdv2007.0
+ Revision: 109105
- Rebuild against new python

* Tue Oct 31 2006 Lenny Cartier <lenny@mandriva.com> 0.8.2-1mdv2007.1
+ Revision: 74154
- Update to 0.8.2

* Mon Jul 10 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 0.8.1-2mdv2007.0
+ Revision: 38596
- Fix File list
- Increase release
- try to fix bug #23156

* Fri Jun 23 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 0.8.1-1mdv2007.0
+ Revision: 37885
- Fix file list
- remove ( for the moment?) Patch0
- fix folder
- 0.8.1
- import hk_classes-0.8-1mdk

* Sun Dec 11 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 0.8-1mdk
- 0.8 final
- patch0: fix python path detection on x86_64
- do not require firebird-devel on x86_64 - the package is not available. Add
  a word about that in description
- xbase seems to be broken on x86_64
- build on x86_64

* Thu Oct 06 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.8-0.test2.2mdk
- BuildRequires Fix

* Wed Oct 05 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.8-0.test2.1mdk
- 0.8-test2
- Fix files list
- Fx BuildRequires

* Wed Jul 13 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.7.4a-1mdk
- 0.7.4a 
	 -  This is mainly a bugfix release
- Drop Patch 0   merged upstream

* Wed Jul 06 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.7.4-2mdk
- fix file section
- fix buildrequires

* Sat Jul 02 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.7.4-1mdk
- 0.7.4
- Patch 0 fix #include

* Sat Apr 30 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.7.4-0test1.1mdk
- New release 0.7.4test1

* Mon Apr 25 2005 Stew Benedict <sbenedict@mandriva.com> 0.7.2-3mdk
- rebuild for new libpq

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 0.7.2-2mdk
- Rebuild for new python

* Tue Nov 30 2004 Stew Benedict <sbenedict@mandrakesoft.com> 0.7.2-1mdk
- 0.7.2, provides

* Fri Sep 24 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.7.1-1mdk
- 0.7.1

* Thu Jun 17 2004 Stew Benedict <sbenedict@mandrakesoft.com> 0.6.3-2mdk
- rebuild

* Thu Apr 22 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6.3-1mdk
- 0.6.3

