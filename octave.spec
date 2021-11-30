%global octave_api api-v56

%bcond_without	atlas
%bcond_without	docs
%bcond_without	java
%bcond_with	jit
%bcond_without	64bit_support

Summary:	High-level language for numerical computations
Name:		octave
Version:	6.3.0
Release:	2
License:	GPLv3+
Group:		Sciences/Mathematics
Url:		https://www.octave.org/
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source10:	%{name}.macros
Source20:	octave-2.1.36-emac.lisp
# fix usage of bsdtar with unpack
#Patch1:		octave-4.2.0-bsdtar.patch
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
Patch3:		octave-3.6.3-detect-i586-as-little-endian-ieee754.patch
%endif

BuildRequires:	bison
BuildRequires:	emacs-nox
BuildRequires:	flex
BuildRequires:	fltk-devel
BuildRequires:	gcc-gfortran
BuildRequires:	ghostscript-devel
BuildRequires:	gl2ps-devel
BuildRequires:	glpk-devel
BuildRequires:	gnuplot
BuildRequires:	gperf
BuildRequires:	hdf5-devel
%if %{with java}
BuildRequires:	java-devel
#BuildRequires:	javapackages-local
%endif
BuildRequires:	icoutils
BuildRequires:	less
BuildRequires:	librsvg
%if %{with jit}
BuildRequires:	llvm-devel
%endif
BuildRequires:	pkgconfig(arpack)
%if %{with atlas}
BuildRequires:	pkgconfig(atlas)
%endif
BuildRequires:	pkgconfig(blas)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(lapack)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(ncurses)
#BuildRequires:	pkgconfig(osmesa)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qhull-devel
BuildRequires:	qrupdate-devel
BuildRequires:	qtchooser
BuildRequires:	qt5-assistant
BuildRequires:	qt5-linguist
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-qtchooser
BuildRequires:	qt5-qttools
BuildRequires:	qscintilla-qt5-devel
BuildRequires:	suitesparse-devel
BuildRequires:	sundials-devel
BuildRequires:	texinfo
#BuildRequires:	texlive

Requires:	gnuplot
Requires:	graphicsmagick
Requires:	hdf5
Requires:	java-headless
Requires:	texinfo

Provides:	octave(api) = %{octave_api}

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
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}.el*
%{_bindir}/%{name}*
%{_libdir}/%{name}/site
%{_libdir}/%{name}/%{version}/oct
%{_libdir}/%{name}/%{version}/site
%{_libdir}/%{name}/%{version}/*.so.*
%{_libexecdir}/%{name}/
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/org.octave.Octave.appdata.xml
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{version}%{?rctag}/
%{_datadir}/%{name}/ls-R
%ghost %{_datadir}/%{name}/octave_packages
%{_datadir}/%{name}/packages/
%{_datadir}/%{name}/site/
%if %{with docs}
%{_mandir}/man*/%{name}.1.*
%{_infodir}/%{name}.info*
%{_infodir}/lib%{name}.info*
%endif

#---------------------------------------------------------------------------

%package devel
Summary:	Development headers and files for Octave
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	clang
Requires:	gcc-c++
Requires:	gcc-gfortran
Requires:	gl2ps-devel
Requires:	gnuplot
Requires:	hdf5-devel
Requires:	pkgconfig(arpack)
Requires:	pkgconfig(blas)
Requires:	pkgconfig(fontconfig)
Requires:	pkgconfig(fftw3)
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
Requires:	pkgconfig(GraphicsMagick)
Requires:	pkgconfig(lapack)
Requires:	pkgconfig(libpcre)
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
%doc doc/refcard/*.pdf
%doc doc/interpreter/*.pdf
%doc doc/liboctave/*.pdf
%doc package-doc/*
%{_infodir}/liboctave.*
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1
# emacs mode
cp -a %{SOURCE20} %{name}.el

%build
%configure \
	--enable-shared \
	--disable-static \
	--%{?with_64bit_support:en}%{?!with_64bit_support:dis}able-64=yes \
	--%{?with_docs:en}%{?!with_docs:dis}able-docs \
%if %{with atlas}
	--with-blas="-L%{_libdir}/atlas -ltatlas" \
	--with-lapack="-L%{_libdir}/atlas -ltatlas" \
%endif
	--%{?with_jit:en}%{?!with_jit:dis}able-jit \
	--enable-link-all-dependencies \
	%{nil}

%make_build OCTAVE_RELEASE="%{distribution} %{version}-%{release}"

# emacs mode
%{_bindir}/emacs -batch -q -no-site-file -f batch-byte-compile %{name}.el

%install
%make_install

# docs
%if %{with docs}
	%make install-data install-html install-info install-pdf DESTDIR=%{buildroot}
	rm -rf package-doc
	install -dm 0744 package-doc
%endif

# Make library links
install -dm 0755 %{buildroot}/etc/ld.so.conf.d
/bin/echo "%{_libdir}/octave-%{version}" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# Remove RPM_BUILD_ROOT from ls-R files
perl -pi -e "s,%{buildroot},," %{buildroot}%{_libexecdir}/%{name}/ls-R
perl -pi -e "s,%{buildroot},," %{buildroot}%{_datadir}/%{name}/ls-R
touch %{buildroot}%{_datadir}/%{name}/ls-R

%{_bindir}/find %{buildroot} -name "*.oct" -print0 | %{_bindir}/xargs -t -0 -r strip --strip-unneeded

# .desktop
desktop-file-install \
	--add-category Education \
	--remove-category Development \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/org.octave.Octave.desktop

# packages
install -dm 0755 %{buildroot}%{_datadir}/octave/packages/
/bin/touch %{buildroot}%{_datadir}/octave/octave_packages

# rpm
install -dm 0755 %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -pm 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

# emacs mode
install -dm 0755 %{buildroot}%{_sysconfdir}/emacs/site-start.d
install -pm 0644 %{name}.elc %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.elc
install -pm 0644 %{name}.el %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el

