%bcond_without	python

%define	major	2
%define	libname	%mklibname xml2_ %{major}
%define	devname	%mklibname xml2 -d

Summary:	Library providing XML and HTML support
Name:		libxml2
Version:	2.9.0
Release:	3
License:	MIT
Group:		System/Libraries
URL:		http://www.xmlsoft.org/
Source0:	ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
Patch0:		libxml2-rand_seed.patch
BuildRequires:	gtk-doc
%if %{with python}
BuildRequires:	pkgconfig(python2)
%endif
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(liblzma)

%description
This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified. The
output can be a simple SAX stream or and in-memory DOM-like 
representations. In this case one can use the built-in XPath and 
XPointer implementation to select subnodes or ranges. A flexible 
Input/Output mechanism is available, with existing HTTP and FTP modules
and combined to a URI library.

%package -n	%{libname}
Summary:	Shared libraries providing XML and HTML support
Group:		System/Libraries
Obsoletes:	%{mklibname xml 2} < 2.8.0
Provides:	%{name} = %{EVRD}

%description -n	%{libname}
This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified.

%package	utils
Summary:	Utilities to manipulate XML files
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description	utils
This packages contains utils to manipulate XML files.

%if %{with python}
%package -n	python-%{name}
Summary:	Python bindings for the libxml2 library
Group:		Development/Python
%rename		%{name}-python

%description -n	python-%{name}
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified.
%endif

%package -n	%{devname}
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
Libraries, include files, etc you can use to develop XML applications.
This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified. 

%prep
%setup -q
%patch0 -p1

%build
%configure2_5x \
	--disable-static

%make

xz --text -c doc/libxml2-api.xml > doc/libxml2-api.xml.xz

%install
%makeinstall_std
mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libxml2.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libxml2.so.%{major}.*.* %{buildroot}%{_libdir}/libxml2.so

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/xml2-config

# remove unpackaged files
rm -rf	%{buildroot}%{_prefix}/doc %{buildroot}%{_datadir}/doc

%check
# all tests must pass
# use TARBALLURL_2="" TARBALLURL="" TESTDIRS="" to disable xstc test which are using remote tarball
make TARBALLURL_2="" TARBALLURL="" TESTDIRS="" check

%files -n %{libname}
/%{_lib}/libxml2.so.%{major}*

%files utils
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
%{_mandir}/man1/xmlcatalog*
%{_mandir}/man1/xmllint*

%if %{with python}
%files -n python-%{name}
%doc doc/*.py doc/python.html
%doc python/TODO
%doc python/libxml2class.txt
%doc python/tests/*.py
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py
%endif

%files -n %{devname}
%doc AUTHORS ChangeLog README Copyright TODO 
%doc doc/*.html doc/*.gif doc/*.png doc/html doc/tutorial
%doc doc/libxml2-api.xml.xz
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/xml2-config
%{multiarch_bindir}/xml2-config
%{_libdir}/libxml2.so
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_mandir}/man1/xml2-config*
%{_mandir}/man3/*
%{_includedir}/*
%{_datadir}/aclocal/*

%changelog
* Thu Jan 17 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.9.0-3
- move library under /%%{_lib} as it's required by /bin/rpm

* Thu Jan 17 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.9.0-2
- use pkgconfig() deps for buildrequires

* Thu Jun 21 2012 Oden Eriksson <oeriksson@mandriva.com> 2.8.0-1
+ Revision: 806574
- 2.8.0
- drop all patches as they are applied in the 2.8.0 version
- enable lzma support

* Wed Mar 07 2012 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2.7.8-14
+ Revision: 782657
- rename libxml2-python to python-libxml2
- drop explicit python & library package dependencies for python package
- drop ancient obsoletes on %%{_lib}xml2-python
- don't bother packaging doc/examples
- compress libxml2-api.xml in %%build with xz
- use %%{EVRD} macro
- cleanups
- do autoreconf in %%prep

* Wed Feb 22 2012 Oden Eriksson <oeriksson@mandriva.com> 2.7.8-13
+ Revision: 779188
- sync with MDVSA-2012:023

* Mon Jan 16 2012 Oden Eriksson <oeriksson@mandriva.com> 2.7.8-12
+ Revision: 761750
- sync with MDVSA-2012:005

* Thu Dec 15 2011 Oden Eriksson <oeriksson@mandriva.com> 2.7.8-11
+ Revision: 741591
- sync with MDVSA-2011:188

* Mon Dec 05 2011 ZÃ© <ze@mandriva.org> 2.7.8-10
+ Revision: 737977
- fix python file list
- clean all .la files

* Thu Nov 24 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2.7.8-9
+ Revision: 733228
- add back .la files

* Thu Nov 24 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.7.8-8
+ Revision: 733099
- rebuild
- removed defattr
- removed clean section
- removed all .la files
- disabled static build
- removed dup docs across sub pkgs
- cleaned up spec
- remove reqs in devel pkg
- removed mkrel & BuildRoot

* Sun Oct 09 2011 Oden Eriksson <oeriksson@mandriva.com> 2.7.8-7
+ Revision: 703913
- sync with MDVSA-2011:131, MDVSA-2011:145

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added build option for python

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.7.8-6
+ Revision: 661450
- multiarch fixes

* Wed Dec 29 2010 Oden Eriksson <oeriksson@mandriva.com> 2.7.8-5mdv2011.0
+ Revision: 626025
- P1: security fix for CVE-2010-4494 (upstream)

* Tue Dec 28 2010 Funda Wang <fwang@mandriva.org> 2.7.8-4mdv2011.0
+ Revision: 625595
- more specific requires

* Tue Dec 28 2010 Funda Wang <fwang@mandriva.org> 2.7.8-3mdv2011.0
+ Revision: 625494
- revert version script per upstream

* Mon Dec 27 2010 Funda Wang <fwang@mandriva.org> 2.7.8-2mdv2011.0
+ Revision: 625370
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - 2.7.8

* Wed Mar 17 2010 Frederic Crozat <fcrozat@mandriva.com> 2.7.7-1mdv2011.0
+ Revision: 524077
- Release 2.7.7

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.7.6-2mdv2010.1
+ Revision: 519031
- rebuild

* Mon Oct 12 2009 Frederic Crozat <fcrozat@mandriva.com> 2.7.6-1mdv2010.0
+ Revision: 456837
- Release 2.7.6
- Remove patches 3 & 4 (merged upstream)

* Tue Sep 15 2009 Frederic Crozat <fcrozat@mandriva.com> 2.7.4-2mdv2010.0
+ Revision: 443121
- Patch4 (GIT): fix inkscape crash (GNOME bug #566012)

* Fri Sep 11 2009 Frederic Crozat <fcrozat@mandriva.com> 2.7.4-1mdv2010.0
+ Revision: 438471
- Remove the old trick of generating optimisation at build time
- Release 2.7.4
- Remove patches 2, 4 (merged upstream)
- Regenerate patch3
- Change the way examples are cleaned to be nice with check pass

* Wed Aug 12 2009 Oden Eriksson <oeriksson@mandriva.com> 2.7.3-3mdv2010.0
+ Revision: 415502
- P4: security fix for CVE-2009-2414 and CVE-2009-2416

* Mon Jan 26 2009 Funda Wang <fwang@mandriva.org> 2.7.3-2mdv2009.1
+ Revision: 333661
- fix linkage of python module

* Tue Jan 20 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.7.3-1mdv2009.1
+ Revision: 331728
- update the patch again
- update patch 2
- new version
- drop patches 0,1

* Thu Dec 25 2008 Funda Wang <fwang@mandriva.org> 2.7.2-4mdv2009.1
+ Revision: 318621
- rebuild for new python

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2.7.2-3mdv2009.1
+ Revision: 315644
- added P2 to fix build with -Werror=format-security

* Thu Nov 27 2008 Frederic Crozat <fcrozat@mandriva.com> 2.7.2-2mdv2009.1
+ Revision: 307285
- Patches 0, 1 (SVN) : security fixes CVE-2008-4225, CVE-2008-4226

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 2.7.2-1mdv2009.1
+ Revision: 292782
- New version 2.7.2

* Mon Sep 01 2008 Frederic Crozat <fcrozat@mandriva.com> 2.7.1-1mdv2009.0
+ Revision: 278458
- Release 2.7.1
- Remove patch0 (merged upstream)

* Tue Aug 26 2008 Frederic Crozat <fcrozat@mandriva.com> 2.6.32-3mdv2009.0
+ Revision: 276261
- Patch0 (SVN): fix CVE-2008-3281

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 2.6.32-2mdv2009.0
+ Revision: 265004
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Apr 10 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.32-1mdv2009.0
+ Revision: 192542
- new version

* Mon Jan 28 2008 Adam Williamson <awilliamson@mandriva.org> 2.6.31-1mdv2008.1
+ Revision: 158960
- drop patch (merged upstream)
- new release 2.6.31

* Fri Jan 04 2008 Stefan van der Eijk <stefan@mandriva.org> 2.6.30-3mdv2008.1
+ Revision: 144924
- rebuild to fix error: unpacking of archive failed on file /usr/share/doc/lib64xml2-devel/libxml2-api.xml.gz;477e5e00: cpio: read

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Nov 15 2007 Frederic Crozat <fcrozat@mandriva.com> 2.6.30-2mdv2008.1
+ Revision: 108908
- Update tarball with official version
- Update patch0 with improved version for upstream integration (GNOME bug #497012)
- Fix url for source0

* Tue Sep 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.30-1mdv2008.0
+ Revision: 89538
- new version

* Wed Aug 15 2007 Anssi Hannula <anssi@mandriva.org> 2.6.29-4mdv2008.0
+ Revision: 63684
- obsolete renamed python bindings on lib64 archs

* Wed Aug 15 2007 Adam Williamson <awilliamson@mandriva.org> 2.6.29-3mdv2008.0
+ Revision: 63593
- lib package provides libxml2 for now, think about it later
- drop docs from library package
- use autoreconf instead of calling bits of it manually
- clean up descriptions
- python package should follow %%name, not %%libname
- new devel policy
- correct libification (libxml2_2 is the correct name for the lib package)
- clean up a bunch of conditionals for really old versions, no longer needed

* Fri Jul 06 2007 Frederic Crozat <fcrozat@mandriva.com> 2.6.29-1mdv2008.0
+ Revision: 49147
- Release 2.6.29

* Mon Apr 23 2007 Olivier Blin <blino@mandriva.org> 2.6.28-1mdv2008.0
+ Revision: 17345
- 2.6.28 (and rebuild for missing devel package on x86_64)


* Mon Mar 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.6.27-3mdv2007.1
+ Revision: 146578
- do not package big ChangeLog in -python

  + Helio Chissini de Castro <helio@mandriva.com>
    - Remove old source

* Tue Nov 28 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.27-2mdv2007.1
+ Revision: 88048
- rebuild

* Sat Oct 28 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.27-1mdv2007.1
+ Revision: 73543
- new version
- fix source URL

  + Oden Eriksson <oeriksson@mandriva.com>
    - bzip2 cleanup
    - rebuild
    - bunzip patches
    - Import libxml2

* Wed Jun 21 2006 Frederic Crozat <fcrozat@mandriva.com> 2.6.26-2mdv2007.0
- Fix doc (Mdv bug #19007)

* Thu Jun 08 2006 Frederic Crozat <fcrozat@mandriva.com> 2.6.26-1mdv2007.0
- Release 2.6.26

* Wed Jun 07 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.25-1mdv2007.0
- New release 2.6.25

* Sat Apr 29 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.24-1mdk
- New release 2.6.24

* Thu Jan 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.23-1mdk
- New release 2.6.23
- use mkrel

* Wed Nov 16 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.22-2mdk
- Rebuild to get debug package

* Wed Oct 05 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.22-1mdk
- Release 2.6.22
- Remove patch2 (merged upstream)

* Wed Sep 14 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.21-3mdk 
- Update patch2 to fix clash with expat headers

* Tue Sep 13 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.21-2mdk 
- Patch2 (CVS): various fixes

* Tue Sep 06 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.21-1mdk 
- Release 2.6.21

* Thu Aug 25 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.20-3mdk 
- Remove changelog from main package to reduce its size

* Thu Aug 25 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.20-2mdk 
- Move api documentation to devel package

* Wed Jul 20 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.20-1mdk 
- New release 2.6.20
- Disable profiling, it doesn't work with gcc 4

* Tue Apr 19 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.19-1mdk 
- Release 2.6.19

* Thu Feb 24 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.17-2mdk
- multiarch for xml2-config --libtool-libs

* Tue Jan 18 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.17-1mdk
- New release 2.6.17

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 2.6.16-2mdk
- Rebuild for new python

* Wed Nov 10 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.6.16-1mdk
- New release 2.6.16

* Tue Oct 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.14-1mdk
- New release 2.6.14
- Drop support for Mdk version < 9.2
- Remove patch 2 (no longer needed)

* Wed Sep 01 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.13-1mdk
- New release 2.6.13

* Tue Aug 24 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.12-1mdk
- patch 2 fixes the build
- New release 2.6.12

* Fri Jul 09 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.11-2mdk
- Integrate profiling stuff from Fedora (please report any problem)

* Wed Jul 07 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.6.11-1mdk
- New release 2.6.11

* Wed Jun 02 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.6.10-1mdk
- new version

* Tue Apr 20 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.9-1mdk
- drop patch 2 (merged)
- new version

* Sat Apr 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.8-1mdk
- Release 2.6.8
- Patch2 (CVS): fix python tests

