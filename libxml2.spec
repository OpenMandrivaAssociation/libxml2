%define major		2
%define libname		%mklibname xml2_ %{major}
%define develname	%mklibname xml2 -d

Summary:	Library providing XML and HTML support
Name:		libxml2
Version:	2.7.4
Release:	%mkrel 1
License:	MIT
Group: 		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.xmlsoft.org/
Source0:	ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
Patch3:		libxml2-2.7.4-python-linking.patch
BuildRequires:	gtk-doc
BuildRequires:	python-devel >= %{pyver}
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	autoconf

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

%package -n %{libname}
Summary:	Shared libraries providing XML and HTML support
Group: 		System/Libraries
Obsoletes:	%{mklibname xml 2}
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified.

%package utils
Summary: Utilities to manipulate XML files
Group: System/Libraries
Requires: %{libname} >= %{version}

%description utils
This packages contains utils to manipulate XML files.

%package python
Summary: Python bindings for the libxml2 library
Group: Development/Python
Requires: %{libname} >= %{version}
Requires: python >= %{pyver}
Provides: python-%{name} = %{version}-%{release}
%if "%{_lib}" != "lib"
Obsoletes: %{_lib}xml2-python < 2.6.29-4
%endif

%description python
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified.

%package -n %{develname}
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/C
Requires: %{libname} = %{version}
Requires: zlib-devel
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
Libraries, include files, etc you can use to develop XML applications.
This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified. 

%prep
%setup -q
%patch3 -p1 -b .python-linking

#needed by patch3
autoreconf

%build

%configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

#only do it here if check aren't done
if [ %{_with check} -eq 0 ]; then 
  # clean before packaging documentation
  (cd doc/examples ; make clean ; rm -rf .deps Makefile)
  gzip -9 doc/libxml2-api.xml
fi


# multiarch policy
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/xml2-config

# remove unpackaged files
rm -rf	$RPM_BUILD_ROOT%{_prefix}/doc \
 	$RPM_BUILD_ROOT%{_datadir}/doc \
	$RPM_BUILD_ROOT%{_libdir}/python%{pyver}/site-packages/*.{la,a} \

%check
# all tests must pass
# use TARBALLURL_2="" TARBALLURL="" TESTDIRS="" to disable xstc test which are using remote tarball
make TARBALLURL_2="" TARBALLURL="" TESTDIRS="" check

#need to do that after check otherwise it will fail
# clean before packaging documentation
(cd doc/examples ; make clean ; rm -rf .deps Makefile)
gzip -9 doc/libxml2-api.xml

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/lib*.so.*

%files utils
%defattr(-, root, root)
%doc AUTHORS README Copyright TODO 
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
%{_mandir}/man1/xmlcatalog*
%{_mandir}/man1/xmllint*

%files python
%defattr(-, root, root)
%doc AUTHORS README Copyright TODO 
%doc doc/*.py doc/python.html
%doc python/TODO
%doc python/libxml2class.txt
%doc python/tests/*.py
%{_libdir}/python%{pyver}/site-packages/*.so
%{_libdir}/python%{pyver}/site-packages/*.py

%files -n %{develname}
%defattr(-, root, root)
%doc AUTHORS ChangeLog README Copyright TODO 
%doc doc/*.html doc/*.gif doc/*.png doc/html doc/examples doc/tutorial
%doc doc/libxml2-api.xml.gz
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/xml2-config
%multiarch %{multiarch_bindir}/xml2-config
%{_libdir}/*a
%{_libdir}/*.so
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_mandir}/man1/xml2-config*
%{_mandir}/man3/*
%{_includedir}/*
%{_datadir}/aclocal/*
