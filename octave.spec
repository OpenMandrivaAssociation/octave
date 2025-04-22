# For now -- since C code (built with clang) and
# Fortran code (built with gfortran) are linked
# together, LTO object files don't work
%global _disable_lto 1

%global octave_api api-v60

%bcond docs		1
%bcond java		1

%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
%global arch64 1
%else
%global arch64 0
%endif

# BLAS lib
%global blaslib flexiblas

# (mandian)
# blas64 is still not compatible with some packages
%if 0%{?arch64}
%bcond use_blas64	0
%else
%bcond use_blas64	0
%endif

Summary:	High-level language for numerical computations
Name:		octave
Version:	10.1.0
Release:	3
License:	GPLv3+
Group:		Sciences/Mathematics
Url:		https://www.octave.org/
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
# from fedora with slight modification
Source10:	%{name}.macros
Source20:	octave-2.1.36-emacs.lisp
BuildRequires:	bison
#BuildRequires:	emacs-nox
BuildRequires:	flex
BuildRequires:	fltk-devel
BuildRequires:	gcc-gfortran
BuildRequires:	ghostscript-devel
BuildRequires:	gl2ps-devel
BuildRequires:	glpk-devel
BuildRequires:	gnuplot
BuildRequires:	gomp-devel
BuildRequires:	gperf
BuildRequires:	hdf5-devel
%if %{with java}
BuildRequires:	jdk-current
#BuildRequires:	javapackages-local
%endif
BuildRequires:	icoutils
BuildRequires:	less
BuildRequires:	librsvg
BuildRequires:	llvm-devel
BuildRequires:	locales-fr
#BuildRequires:	locales-ja
#BuildRequires:	locales-zh
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fftw3)
%if %{with use_blas64}
BuildRequires:	pkgconfig(%{blaslib}64)
BuildRequires:	pkgconfig(arpack64)
%else
BuildRequires:	pkgconfig(%{blaslib})
BuildRequires:	pkgconfig(arpack)
%endif
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(ncurses)
#BuildRequires:	pkgconfig(ompi)
#BuildRequires:	pkgconfig(osmesa)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Core5Compat)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Help)
BuildRequires:	pkgconfig(Qt6Linguist)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6OpenGL)
BuildRequires:	pkgconfig(Qt6OpenGLWidgets)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6Sql)
BuildRequires:	pkgconfig(Qt6Xml)
BuildRequires:	pkgconfig(RapidJSON)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qhull-devel
BuildRequires:	qrupdate-devel
BuildRequires:	qscintilla-qt6-devel
BuildRequires:	qt6-qtbase-tools
BuildRequires:	qt6-qttools-devel
BuildRequires:	suitesparse-devel
BuildRequires:	sundials-devel
BuildRequires:	texinfo
BuildRequires:	texlive

Requires:	gnuplot
Requires:	graphicsmagick
Requires:	hdf5
Requires:	java-headless
Requires:	qt6-qtbase-sql-sqlite
Requires:	texinfo

Provides:	octave(api) = %{octave_api}

%patchlist
# fix java check
octave-java2.patch

# This patch is required when installing all sagemath dependencies,
# otherwise it will fail with a message like:
#
#	$ octave
#	$ fatal: lo_ieee_init: floating point format is not IEEE! Maybe DLAMCH is miscompiled, or you are using some strange system without IEEE floating point math?
#
# and, while the reason is clear (using x87 and 80 bits doubles) the
# proper library/dependency causing it was not detected.
# This is not an issue in x86_64 that uses sse2+
%ifarch %{ix86}
octave-3.6.3-detect-i586-as-little-endian-ieee754.patch
%endif

%description
GNU Octave is a high-level language, primarily intended for numerical
computations. It provides a convenient command line interface for
solving linear and nonlinear problems numerically, and for performing
other numerical experiments using a language that is mostly compatible
with Matlab. It may also be used as a batch-oriented language.

Octave has extensive tools for solving common numerical linear algebra
problems, finding the roots of nonlinear equations, integrating
ordinary functions, manipulating polynomials, and integrating ordinary
differential and differential-algebraic equations. It is easily
extensible and customizable via user-defined functions written in
Octave's own language, or using dynamically loaded modules written in
C++, C, Fortran, or other languages.

%files
%license COPYING
%doc NEWS* AUTHORS BUGS README
%doc examples INSTALL.OCTAVE
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/octave-*.conf
%{_bindir}/%{name}*
%dir %{_libdir}/octave/
%dir %{_libdir}/octave/%{version}
#{_libdir}/%{name}/site
%{_libdir}/%{name}/%{version}/oct
%{_libdir}/%{name}/%{version}/site
%{_libdir}/%{name}/%{version}/mkoctfile-%{version}
%{_libdir}/%{name}/%{version}/octave-config-%{version}
%{_libdir}/%{name}/%{version}/*.so.*
%{_libdir}/%{name}/packages/
%{_libdir}/%{name}/site/
%{_libexecdir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_metainfodir}/org.octave.Octave.metainfo.xml
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{version}/
%{_datadir}/%{name}/ls-R
%ghost %{_datadir}/%{name}/octave_packages
%{_datadir}/%{name}/packages/
%{_datadir}/%{name}/site/
%if %{with docs}
%{_mandir}/man*/%{name}*.1.*
%{_infodir}/%{name}.info*
%{_infodir}/lib%{name}.info*
%endif

#---------------------------------------------------------------------------

%package devel
Summary:	Development headers and files for Octave
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	clang
Requires:	clang
Requires:	gcc-c++
Requires:	gcc-gfortran
Requires:	appstream-util
Requires:	gl2ps-devel
Requires:	gnuplot
Requires:	hdf5-devel
%if %{with use_blas64}
Requires:	pkgconfig(%{blaslib}64)
%else
Requires:	pkgconfig(%{blaslib})
%endif
Requires:	pkgconfig(fontconfig)
Requires:	pkgconfig(fftw3)
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
Requires:	pkgconfig(GraphicsMagick)
Requires:	pkgconfig(appstream-glib)
Requires:	pkgconfig(libpcre2-8)
Requires:	pkgconfig(libcurl)
Requires:	pkgconfig(readline)
Requires:	pkgconfig(zlib)
Requires:	pstoedit
Requires:	qrupdate-devel
Requires:	suitesparse-devel
Requires:	texinfo
Requires:	transfig

%description devel
The octave-devel package contains files needed for developing
applications which use GNU Octave.

%files devel
%{_bindir}/mkoctfile*
%{_includedir}/%{name}-%{version}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}/%{version}/*.so
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%if %{with docs}
%{_mandir}/man1/mkoctfile.1*
%endif

#---------------------------------------------------------------------------

%if %{with docs}
%package doc
Summary:	Documentation for Octave, a numerical computational language
Group:		Sciences/Mathematics

%description doc
GNU Octave is a high-level language, primarily intended for numerical
computations. It provides a convenient command line interface for
solving linear and nonlinear problems numerically, and for performing
other numerical experiments using a language that is mostly compatible
with Matlab. It may also be used as a batch-oriented language.

This package contains documentation of Octave in various formats.

%files doc
%doc examples/
%{_docdir}/%{name}/liboctave.html/
%{_docdir}/%{name}/liboctave.pdf
%{_docdir}/%{name}/octave.html
%{_docdir}/%{name}/octave.pdf
%doc doc/refcard/*.pdf
%doc doc/interpreter/*.pdf
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# check if octave_api macro is updated
octave_api_new=$(sed -nE 's,OCTAVE_API_VERSION="(.*)",\1,p' configure.ac)
if [[ %{octave_api} != "${octave_api_new}" ]]
then
  echo "octave_api in spec is set to %{octave_api} but ${octave_api_new} is detected."
  exit 1
fi

%build
%configure \
	--enable-shared \
	--disable-static \
	--%{?with_docs:en}%{?!with_docs:dis}able-docs \
	--enable-link-all-dependencies \
	--enable-openmp \
	--with-lapack=%{blaslib}%{?with_use_blas64:64} \
	--with-blas=%{blaslib}%{?with_use_blas64:64} \
	--with-suitesparseconfig=suitesparseconfig%{?with_use_blas64:64} \
	--with-amd=amd%{?with_use_blas64:64} \
	--with-camd=camd%{?with_use_blas64:64} \
	--with-colamd=colamd%{?with_use_blas64:64} \
	--with-ccolamd=ccolamd%{?with_use_blas64:64} \
	--with-cholmod=cholmod%{?with_use_blas64:64} \
	--with-cxsparse=cxsparse%{?with_use_blas64:64} \
	--with-klu=klu%{?with_use_blas64:64} \
	--with-spqr=spqr%{?with_use_blas64:64} \
	--with-umfpack=umfpack%{?with_use_blas64:64} \
	%{nil}

# lrelease doesn't require -qt option
sed -i -e 's|LRELEASEFLAGS="-qt=\$qt_version"|LRELEASEFLAGS=""|g' ./configure

%make_build OCTAVE_RELEASE="%{version}-%{release} by %{distribution}"

# docs
%if %{with docs}
	export TEXINFO_XS_PARSER=0
	make html info pdf
%endif

%install
%make_install

# docs
%if %{with docs}
	export TEXINFO_XS_PARSER=0
	make install-data install-html install-info install-pdf DESTDIR=%{buildroot}
%endif

# Make library links
install -dm 0755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
/bin/echo "%{_libdir}/%{name}/%{version}" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# FIXME: octave can't find his libraries when building octave add-on packages
mv %{buildroot}%{_bindir}/octave-config-%{version} %{buildroot}%{_libdir}/%{name}/%{version}/octave-config-%{version}
ln -s %{_libdir}/%{name}/%{version}/octave-config-%{version} %{buildroot}%{_bindir}/octave-config-%{version}
mv %{buildroot}%{_bindir}/mkoctfile-%{version} %{buildroot}%{_libdir}/%{name}/%{version}/mkoctfile-%{version}
cat > %{buildroot}%{_bindir}/mkoctfile-%{version} <<EOF
#!/bin/bash
exec %{_libdir}/%{name}/%{version}/mkoctfile-%{version} -L%{_libdir}/%{name}/%{version} "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/mkoctfile-%{version}

# remove RPM_BUILD_ROOT from ls-R files
#touch %{buildroot}%{_libexecdir}/%{name}/ls-R
#sed -i -e "s|%{buildroot}||g" %{buildroot}%{_libexecdir}/%{name}/ls-R
touch %{buildroot}%{_datadir}/%{name}/ls-R
sed -i -e "s|%{buildroot}||g" %{buildroot}%{_datadir}/%{name}/ls-R

# strip .oct files
%{_bindir}/find %{buildroot} -name "*.oct" -print0 | %{_bindir}/xargs -t -0 -r strip --strip-unneeded

# .desktop
desktop-file-install \
	--add-category Education \
	--remove-category Development \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/org.octave.Octave.desktop

# packages
HOST_TYPE=`%{buildroot}%{_libdir}/%{name}/%{version}/octave-config-%{version} -p CANONICAL_HOST_TYPE`
install -dm 0755 %{buildroot}%{_libdir}/%{name}/site/oct/%{octave_api}/$HOST_TYPE
install -dm 0755 %{buildroot}%{_libdir}/%{name}/site/oct/$HOST_TYPE
install -dm 0755 %{buildroot}%{_libdir}/%{name}/packages
install -dm 0755 %{buildroot}%{_datadir}/%{name}/packages
/bin/touch %{buildroot}%{_datadir}/octave/octave_packages

# rpm macros
install -dm 0755 %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -pm 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

# remove static lib stuff
find %{buildroot}%{_libdir} -name \*.la -delete

