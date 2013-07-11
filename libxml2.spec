%bcond_without	python

%define	major	2
%define	libname	%mklibname xml2_ %{major}
%define	devname	%mklibname xml2 -d

Summary:	Library providing XML and HTML support
Name:		libxml2
Version:	2.9.1
Release:	2
License:	MIT
Group:		System/Libraries
Url:		http://www.xmlsoft.org/
Source0:	ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
BuildRequires:	gtk-doc
%if %{with python}
BuildRequires:	pkgconfig(python2)
%endif
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)

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
%{_datadir}/aclocal/*
%{_bindir}/xml2-config
%{multiarch_bindir}/xml2-config
%{_libdir}/libxml2.so
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/xml2-config*
%{_mandir}/man3/*

