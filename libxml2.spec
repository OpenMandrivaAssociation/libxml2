# disable_lto is a workaround for unresolved symbols in the 32bit library.
# 64-bit LTO is added via optflags; cmake32 strips -flto.
%global _disable_lto 1

%bcond_without python

# ICU support is needed in order for libreoffice, chromium, qtwebengine and
# maybe others to use system libxml.
# Please don't disable it without good reason. And if you do, fix the
# packages that rely on it.
%bcond_without icu

# %pgo trains the 64-bit library. --without pgo skips the two-pass build.
%bcond_without pgo

%define major 16
%define oldlibname %mklibname xml2_ 2
%define libname %mklibname xml2
%define devname %mklibname xml2 -d
# libxml2 is used by wine -- needs a 32-bit compat package
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%if %{with compat32}
%define oldlib32name libxml2_2
%define lib32name libxml2
%define dev32name libxml2-devel
%endif

# (tpg) optimize it a bit. -flto is stripped again for cmake32.
%global optflags %{optflags} -O3 -flto

Summary:	Library providing XML and HTML support
Name:		libxml2
Version:	2.15.4
Release:	2
License:	MIT
Group:		System/Libraries
Url:		https://www.xmlsoft.org/
Source0:	https://download.gnome.org/sources/libxml2/%(echo %{version}|cut -d. -f1-2)/libxml2-%{version}.tar.xz
#Source0:	http://xmlsoft.org/sources/%{name}-%{version}.tar.gz
Patch1:		libxml2-2.9.9-no-Lusrlib.patch
Patch2:		https://src.fedoraproject.org/rpms/libxml2/raw/rawhide/f/libxml2-2.9.8-python3-unicode-errors.patch
BuildRequires:	cmake ninja
BuildRequires:	doxygen
BuildRequires:	xsltproc
%if %{with python}
BuildRequires:	pkgconfig(python3)
BuildRequires:	gettext-devel
%endif
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)
%ifarch riscv64
BuildRequires:	atomic-devel
%endif
%if %{with icu}
BuildRequires:	pkgconfig(icu-i18n)
%endif
%if %{with compat32}
# We don't require the same slew of dependencies as the regular version:
# We don't build the command line tools (hence, no need for readline),
# and since wine doesn't use python, we don't need the python bits either.
# Lastly, ICU is enabled in the regular build because of WebKit/Blink and
# LibreOffice - neither of which is relevant to wine.
BuildRequires:	devel(libz)
BuildRequires:	devel(liblzma)
# clang -m32 reads i386-*.cfg. The i686-openmandriva target has
# libclang_rt.builtins.a and the sysroot lld needs.
BuildRequires:	cross-i686-openmandriva-linux-gnu-clang
BuildRequires:	cross-i686-openmandriva-linux-gnu-libc
BuildRequires:	cross-i686-openmandriva-linux-gnu-gcc
BuildRequires:	cross-i686-openmandriva-linux-gnu-binutils
BuildRequires:	cross-i686-openmandriva-linux-gnu-kernel-headers
%endif
%if "%{lib32name}" == "%{name}"
# Renamed 2025-03-07 before 6.0
%rename %{oldlib32name}
%endif

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
Group:		System/Libraries
# Renamed 2025-03-07 before 6.0
%rename %{oldlibname}

%description -n %{libname}
This library allows you to manipulate XML files. It includes support
for reading, modifying and writing XML and HTML files. There is DTDs
support: this includes parsing and validation even with complex DtDs,
either at parse time or later once the document has been modified.

%package -n %{devname}
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
%if %{with icu}
# libxml/encoding.h #includes <unicode/ucnv.h>
Requires:	pkgconfig(icu-i18n)
%endif
# Needed because libxml2.so links to them
Requires:	pkgconfig(liblzma)
Requires:	pkgconfig(zlib)

%description -n %{devname}
Libraries, include files, etc you can use to develop XML applications.
This library allows you to manipulate XML files. It includes support
for reading, modifying and writing XML and HTML files. There is DTDs
support: this includes parsing and validation even with complex DtDs,
either at parse time or later once the document has been modified.

%if %{with compat32}
%if "%{lib32name}" != "%{name}"
%package -n %{lib32name}
Summary:	Shared libraries providing XML and HTML support (32-bit)
Group:		System/Libraries
# Renamed 2025-03-07 before 6.0
%rename %{oldlib32name}

%description -n %{lib32name}
This library allows you to manipulate XML files. It includes support
for reading, modifying and writing XML and HTML files. There is DTDs
support: this includes parsing and validation even with complex DtDs,
either at parse time or later once the document has been modified.
%endif

%package -n %{dev32name}
Summary:	Libraries, includes, etc. to develop XML and HTML applications (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{EVRD}
Requires:	%{devname} = %{EVRD}
# Needed because libxml2.so links to them
Requires:	pkgconfig(liblzma)
Requires:	devel(libz)

%description -n %{dev32name}
Libraries, include files, etc you can use to develop XML applications.
This library allows you to manipulate XML files. It includes support
for reading, modifying and writing XML and HTML files. There is DTDs
support: this includes parsing and validation even with complex DtDs,
either at parse time or later once the document has been modified.
%endif

%package utils
Summary:	Utilities to manipulate XML files
Group:		System/Libraries

%description utils
This packages contains utils to manipulate XML files.

%if %{with python}
%package -n python-%{name}
Summary:	Python bindings for the libxml2 library
Group:		Development/Python
%rename		%{name}-python
Requires:	%{libname} = %{EVRD}

%description -n python-%{name}
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows you to manipulate XML files. It includes support
for reading, modifying and writing XML and HTML files. There is DTDs
support: this includes parsing and validation even with complex DtDs,
either at parse time or later once the document has been modified.
%endif

%prep
%autosetup -p1

# cmake32 stays in %prep so it never sees the PGO CFLAGS rpm injects
# around %build. 64-bit objects go in _OMV_rpm_build so the PGO wipe
# leaves the 32-bit tree alone.
%if %{with compat32}
export CONFIGURE_TOP="$(pwd)"
# clang -m32 uses i386-pc-linux-gnu (builtins only).
# --target=i686-openmandriva-linux-gnu finds libclang_rt.builtins.a
# and the matching sysroot.
CFLAGS32="$(echo "${CFLAGS:-%{optflags}}" | sed -e 's/ -m64//g;s/ -mx32//g;s/ -flto//g;s/ -fprofile-[^ ]*//g;s/ -Wno-missing-profile//g') -m32 --target=i686-openmandriva-linux-gnu"
CXXFLAGS32="$(echo "${CXXFLAGS:-%{optflags}}" | sed -e 's/ -m64//g;s/ -mx32//g;s/ -flto//g;s/ -fprofile-[^ ]*//g;s/ -Wno-missing-profile//g') -m32 --target=i686-openmandriva-linux-gnu"
LDFLAGS32="$(echo "${LDFLAGS:-%{build_ldflags}}" | sed -e 's/ -m64//g;s/ -mx32//g;s/ -flto//g;s/ -fprofile-[^ ]*//g;s/ -Wno-missing-profile//g') -m32 --target=i686-openmandriva-linux-gnu"
export CFLAGS32 CXXFLAGS32 LDFLAGS32
%cmake32 \
	-G Ninja \
	-DLIBXML2_WITH_PYTHON:BOOL=OFF \
	-DLIBXML2_WITH_ICU:BOOL=OFF \
	-DLIBXML2_WITH_TLS:BOOL=ON \
	-DLIBXML2_WITH_THREAD_ALLOC:BOOL=ON
cd ..
%endif

%build
%if %{with compat32}
%ninja_build -C build32
%endif

# Out-of-tree name rpm's %pgo wipe recognizes, so pass 2 does not
# re-extract sources or rebuild the 32-bit library.
export CMAKE_BUILD_DIR=_OMV_rpm_build
%cmake \
	-G Ninja \
%if !%{with python}
	-DLIBXML2_WITH_PYTHON:BOOL=OFF \
%else
	-DLIBXML2_WITH_PYTHON:BOOL=ON \
	-DLIBXML2_PYTHON_INSTALL_DIR=%{py_platsitedir} \
%endif
%if %{with icu}
	-DLIBXML2_WITH_ICU:BOOL=ON \
%else
	-DLIBXML2_WITH_ICU:BOOL=OFF \
%endif
	-DLIBXML2_WITH_TLS:BOOL=ON \
	-DLIBXML2_WITH_THREAD_ALLOC:BOOL=ON
cd ..

%ninja_build -C _OMV_rpm_build

# Typical well-formed traffic (config / appstream / HTML / the XML spec).
# The test suite overweights error paths and is a poor PGO profile.
# --repeat is xmllint's own 100-iteration timing/profiling loop.
%if %{with pgo}
%pgo
export LLVM_PROFILE_FILE="%{_pgo_profile_dir}/libxml2-%%m-%%p.profraw"
export LD_LIBRARY_PATH="$(pwd)/_OMV_rpm_build${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
xml=./_OMV_rpm_build/xmllint
catlg=./_OMV_rpm_build/xmlcatalog
[ -x "$xml" ] || { echo "PGO: instrumented xmllint missing"; exit 1; }

train=pgo-train
mkdir -p "$train"
cat > "$train/config.xml" <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
	<server host="localhost" port="8080" ssl="false">
		<timeout>30</timeout>
		<workers>8</workers>
		<listen address="::" backlog="128"/>
	</server>
	<log level="info" path="/var/log/app.log"/>
	<users>
		<user id="1" name="root" enabled="true"><email>root@example.com</email></user>
		<user id="2" name="alice" enabled="true"><email>alice@example.com</email></user>
		<user id="3" name="café" enabled="false"><email>cafe@example.com</email></user>
	</users>
</configuration>
EOF
cat > "$train/appstream.xml" <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<components version="0.14" origin="openmandriva">
	<component type="desktop-application">
		<id>org.example.App</id>
		<name>Example App</name>
		<summary>A typical desktop application</summary>
		<description><p>Short description with <em>inline</em> markup and UTF-8 café.</p></description>
		<url type="homepage">https://example.com/</url>
		<provides><binary>example</binary></provides>
		<releases>
			<release version="1.2.3" date="2026-08-01"/>
			<release version="1.2.2" date="2026-07-01"/>
		</releases>
	</component>
</components>
EOF
{
	echo '<?xml version="1.0" encoding="UTF-8"?>'
	echo '<catalog>'
	i=0
	while [ $i -lt 4000 ]; do
		echo "<item id=\"$i\" name=\"entry-$i\" enabled=\"true\"><title>Item $i</title><desc>Typical text for item $i (café 日本語)</desc><meta k=\"v$i\"/></item>"
		i=$((i + 1))
	done
	echo '</catalog>'
} > "$train/large.xml"

"$xml" --nonet --repeat --noout "$train/config.xml" "$train/appstream.xml" "$train/large.xml"
"$xml" --nonet --repeat --stream --noout "$train/large.xml" test/valid/REC-xml-19980210.xml
"$xml" --nonet --repeat --memory --noout "$train/large.xml"
"$xml" --nonet --repeat --push --noout "$train/config.xml"
"$xml" --nonet --repeat --valid --noout test/valid/REC-xml-19980210.xml
"$xml" --nonet --repeat --stream --valid --noout test/valid/REC-xml-19980210.xml
"$xml" --nonet --repeat --html --nowarning --noout test/HTML/Down.html test/HTML/attr-ents.html
"$xml" --nonet --html --recover --nowarning --noout test/HTML/wired.html || :
"$xml" --nonet --xpath '//item/@id' "$train/large.xml" >/dev/null
"$xml" --nonet --c14n "$train/config.xml" >/dev/null
"$xml" --nonet --format --encode UTF-8 -o /dev/null "$train/large.xml"
if [ -x "$catlg" ]; then
	"$catlg" --create --noout "$train/catalog.xml"
	"$catlg" --noout --add public "-//Example//DTD Config 1.0//EN" "config.dtd" "$train/catalog.xml"
	"$catlg" "$train/catalog.xml" "-//Example//DTD Config 1.0//EN" >/dev/null
fi
%endif

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C _OMV_rpm_build

# remove unpackaged files
rm -rf %{buildroot}%{_prefix}/doc %{buildroot}%{_datadir}/doc

#check
# all tests must pass
# use TARBALLURL_2="" TARBALLURL="" TESTDIRS="" to disable xstc test which are using remote tarball
# Currently (2.9.4-1) disabled because it freezes some build machines
#make TARBALLURL_2="" TARBALLURL="" TESTDIRS="" check

%files -n %{libname}
%{_libdir}/libxml2.so.%{major}*

%files utils
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
#doc %{_mandir}/man1/xmlcatalog*
#doc %{_mandir}/man1/xmllint*

%if %{with python}
%files -n python-%{name}
%doc python/tests/*.py
%{py_platsitedir}/*.so*
%{py_platsitedir}/*.py
%endif

%files -n %{devname}
%doc README* Copyright
#doc doc/libxml2-api.xml.xz
#{_datadir}/aclocal/*
%{_bindir}/xml2-config
%{_libdir}/cmake/libxml2*
%{_libdir}/libxml2.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
#doc %{_mandir}/man1/xml2-config*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libxml2.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libxml2.so
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/cmake/libxml2*
%endif
