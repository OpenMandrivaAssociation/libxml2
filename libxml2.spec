%define build_python 1

%define major		2
%define libname		%mklibname xml2_ %{major}
%define develname	%mklibname xml2 -d

Summary:	Library providing XML and HTML support
Name:		libxml2
Version:	2.7.8
Release:	10
License:	MIT
Group: 		System/Libraries
URL:		http://www.xmlsoft.org/
Source0:	ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
Patch0:		libxml2-2.7.8-reenable-version-script.patch
Patch1:		libxml2-2.7.8-CVE-2010-4494.diff
Patch2:		libxml2-2.7.8-CVE-2011-1944.diff
Patch3:		libxml2-2.7.8-CVE-2011-2821,2834.diff
BuildRequires:	gtk-doc
%if %build_python
BuildRequires:	python-devel
%endif 
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

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

#--------------------------------------------------------------------
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

#--------------------------------------------------------------------
%package utils
Summary: Utilities to manipulate XML files
Group: System/Libraries
Requires: %{libname} >= %{version}-%{release}

%description utils
This packages contains utils to manipulate XML files.

#--------------------------------------------------------------------
%if %build_python
%package python
Summary: Python bindings for the libxml2 library
Group: Development/Python
Requires: %{libname} >= %{version}-%{release}
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
%endif

#--------------------------------------------------------------------
%package -n %{develname}
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
Libraries, include files, etc you can use to develop XML applications.
This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified. 

#--------------------------------------------------------------------
%prep
%setup -q
%patch0 -p1
%patch1 -p0 -b .CVE-2010-4494
%patch2 -p0 -b .CVE-2011-1944
%patch3 -p1 -b .CVE-2011-2821,2834

%build
autoreconf -fi
%configure2_5x \
	--disable-static

%make

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name \*.la|xargs rm -f

#only do it here if check aren't done
if [ %{_with check} -eq 0 ]; then 
  # clean before packaging documentation
  (cd doc/examples ; make clean ; rm -rf .deps Makefile)
  gzip -9 doc/libxml2-api.xml
fi

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/xml2-config

# remove unpackaged files
rm -rf	%{buildroot}%{_prefix}/doc \
 	%{buildroot}%{_datadir}/doc

%check
# all tests must pass
# use TARBALLURL_2="" TARBALLURL="" TESTDIRS="" to disable xstc test which are using remote tarball
make TARBALLURL_2="" TARBALLURL="" TESTDIRS="" check

#need to do that after check otherwise it will fail
# clean before packaging documentation
(cd doc/examples ; make clean ; rm -rf .deps Makefile)
gzip -9 doc/libxml2-api.xml

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files utils
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
%{_mandir}/man1/xmlcatalog*
%{_mandir}/man1/xmllint*

%if %build_python
%files python
%doc doc/*.py doc/python.html
%doc python/TODO
%doc python/libxml2class.txt
%doc python/tests/*.py
%{_libdir}/python%{pyver}/site-packages/*.so
%{_libdir}/python%{pyver}/site-packages/*.py
%endif

%files -n %{develname}
%doc AUTHORS ChangeLog README Copyright TODO 
%doc doc/*.html doc/*.gif doc/*.png doc/html doc/examples doc/tutorial
%doc doc/libxml2-api.xml.gz
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/xml2-config
%{multiarch_bindir}/xml2-config
%{_libdir}/*.so
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_mandir}/man1/xml2-config*
%{_mandir}/man3/*
%{_includedir}/*
%{_datadir}/aclocal/*
