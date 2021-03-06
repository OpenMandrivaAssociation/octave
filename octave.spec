# WARNING missing BR:
# configure: WARNING: SUNDIALS NVECTOR serial library not found.  Solvers ode15i and ode15s will be disabled.
# configure: WARNING: SUNDIALS IDA library not found.  Solvers ode15i and ode15s will be disabled.
# configure: WARNING: JAVA_HOME environment variable not initialized.  Auto-detection will proceed but is unreliable.

%define octave_api api-v51
%define _disable_rebuild_configure 1
%define _disable_lto 1

Name:		octave
Version:	4.4.1
Release:	2
Summary:	High-level language for numerical computations
License:	GPLv3+
Group:		Sciences/Mathematics
Url:		https://www.octave.org/
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source99:       %{name}.macros
Source100:	octave.rpmlintrc

# fix usage of bsdtar with unpack
Patch1:		octave-4.2.0-bsdtar.patch
# This patch is required when installing all sagemath dependencies,
# otherwise it will fail with a message like:
#
#	$ octave
#	$ fatal: lo_ieee_init: floating point format is not IEEE!  Maybe DLAMCH is miscompiled, or you are using some strange system without IEEE floating point math?
#
# and, while the reason is clear (using x87 and 80 bits doubles) the
# proper library/dependency causing it was not detected.
# This is not an issue in x86_64 that uses sse2+
Patch3:		octave-3.6.3-detect-i586-as-little-endian-ieee754.patch
BuildRequires:	bison
BuildRequires:	dejagnu
BuildRequires:	desktop-file-utils
BuildRequires:	emacs-nox
BuildRequires:	flex
BuildRequires:	gcc-gfortran
BuildRequires:	gnuplot
# (Abel) not strictly needed, but play safe
BuildRequires:	gperf
BuildRequires:	texinfo
BuildRequires:	texlive
BuildRequires:	glpk-devel
BuildRequires:	hdf5-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(arpack)
BuildRequires:	pkgconfig(atlas)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(ncurses)
# (Lev) needed to support sparse matrix functionality
BuildRequires:	amd-devel
BuildRequires:	suitesparse-devel
BuildRequires:	ccolamd-devel
BuildRequires:	cholmod-devel
BuildRequires:	colamd-devel
BuildRequires:	cxsparse-devel
BuildRequires:	umfpack-devel
# (Lev) other useful libraries
BuildRequires:	pkgconfig(ompi)
BuildRequires:	qhull-devel
BuildRequires:	qrupdate-devel
# (Lev) for new experimental plotting
BuildRequires:	fltk-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
# to make imread more functional
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(pixman-1)
# gui
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  qscintilla-qt5-devel
BuildRequires:  qtchooser
BuildRequires:	qt5-linguist-tools
BuildRequires:	portaudio-devel
BuildRequires:	sndfile-devel
BuildRequires:	gl2ps-devel
BuildRequires:	pkgconfig(osmesa)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	ghostscript-devel
BuildRequires:	java-1.8.0-openjdk-devel
%rename	octave3
Provides:	octave(api) = %{octave_api}
Requires:	gnuplot
Requires:	java-1.8.0-headless

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
%defattr(0644,root,root,0755)
%doc NEWS* AUTHORS BUGS README
%doc examples INSTALL.OCTAVE
%defattr(-,root,root,0755)
%{_bindir}/octave*
%config(noreplace) /etc/ld.so.conf.d/*
%{_libdir}/octave*
%{_datadir}/octave
%{_datadir}/metainfo/org.octave.Octave.appdata.xml
%{_datadir}/icons/*/*/apps/octave.png
%{_datadir}/icons/*/*/apps/octave.svg
%if "%{_libdir}" != "%{_libexecdir}"
%{_libexecdir}/octave
%endif
%{_mandir}/man*/octave*
%{_infodir}/octave.info*
%{_datadir}/applications/*

#---------------------------------------------------------------------------

%package devel
Summary:	Development headers and files for Octave
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	gcc-c++
Requires:	gcc-gfortran
Requires:	gl2ps-devel
Requires:	suitesparse-devel
Requires:	readline-devel
Requires:	pkgconfig(arpack)
Requires:	pkgconfig(fontconfig)
Requires:	pkgconfig(fftw3)
Requires:	pkgconfig(libpcre)
Requires:	pkgconfig(libcurl)
Requires:	pkgconfig(GraphicsMagick)
Requires:	hdf5-devel
Requires:	qrupdate-devel
Requires:	texinfo
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
%rename	octave3-devel

%description devel
The octave-devel package contains files needed for developing
applications which use GNU Octave.

%files devel
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/mkoctfile*
%{_includedir}/octave-%{version}
#% {multiarch_includedir}/octave-%{version}
%{_mandir}/man1/mkoctfile.1*
%{_sysconfdir}/rpm/macros.d/%{name}.macros

#---------------------------------------------------------------------------

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
%doc doc/refcard/refcard-a4.pdf
%{_infodir}/liboctave.*

#---------------------------------------------------------------------------

%prep
%setup -q
%patch1 -p1
%ifarch %{ix86}
%patch3 -p1
%endif

# fix lrelease syntax
sed -i -e 's!LRELEASEFLAGS="-qt$qt_version"!LRELEASEFLAGS=!' configure

%build
export CC=gcc
export CXX=g++

%define enable64 no
export CPPFLAGS="%{optflags} -DH5_USE_16_API"
# find lrelease
export PATH=%_libdir/qt5/bin:$PATH
export QCOLLECTIONGENERATOR=qhelpgenerator
%configure \
	--enable-dl \
	--enable-shared \
	--disable-static \
	--enable-64=%{enable64} \
	--with-qt=5 \
        --with-amd="-lamd -lsuitesparseconfig" \
        --with-camd="-lcamd -lsuitesparseconfig" \
        --with-colamd="-lcolamd -lsuitesparseconfig" \
        --with-ccolamd="-lccolamd -lsuitesparseconfig" \
        --with-blas="-L%{_libdir}/atlas -ltatlas" \
        --with-lapack="-L%{_libdir}/atlas -ltatlas" \
	%{nil}
make OCTAVE_RELEASE="%{distribution} %{version}-%{release}"

# emacs mode

%install
make install

# Make library links
install -dm 0755 %{buildroot}/etc/ld.so.conf.d
/bin/echo "%{_libdir}/octave-%{version}" > %{buildroot}/etc/ld.so.conf.d/octave-%{_arch}.conf

# Remove RPM_BUILD_ROOT from ls-R files
perl -pi -e "s,%{buildroot},," %{buildroot}%{_libexecdir}/octave/ls-R
perl -pi -e "s,%{buildroot},," %{buildroot}%{_datadir}/octave/ls-R

%{_bindir}/find %{buildroot} -name "*.oct" -print0 | %{_bindir}/xargs -t -0 -r strip --strip-unneeded

# docs
rm -rf package-doc
install -dm 0744 package-doc

# .desktop
mv %{buildroot}%{_datadir}/applications/org.octave.Octave.desktop \
        %{buildroot}%{_datadir}/applications/octave.desktop
desktop-file-install \
	--add-category Education \
	--remove-category Development \
        --dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/octave.desktop

# packages
install -dm 0755 %{buildroot}%{_datadir}/octave/packages/
/bin/touch %{buildroot}%{_datadir}/octave/octave_packages

# rpm
install -dm 0755 %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -pm 0644 %{SOURCE99} %{buildroot}%{_sysconfdir}/rpm/macros.d/
