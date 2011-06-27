%define octave_api api-v37

Name:		octave
Version:	3.4.2
Release:	%mkrel 1
Epoch:		0
Summary:	High-level language for numerical computations
License:	GPLv3+
Group:		Sciences/Mathematics
Source0:	ftp://ftp.gnu.org/gnu/octave/%{name}-%{version}.tar.bz2
Patch0:		octave-3.4.1-pthread-fix.patch
URL:		http://www.octave.org/
Obsoletes:	octave3 < %{epoch}:%{version}-%{release}
Provides:	octave3 = %{epoch}:%{version}-%{release}
Provides:	octave(api) = %{octave_api}
Requires:	gnuplot
Requires(post):	desktop-file-utils
Requires(postun): desktop-file-utils
Requires(post):	rpm-helper
Requires(post): info-install
Requires(preun): info-install
BuildRequires:	bison
BuildRequires:	blas-devel
BuildRequires:	dejagnu
BuildRequires:	desktop-file-utils
BuildRequires:	emacs
BuildRequires:	emacs-bin
BuildRequires:	fftw-devel >= 0:3.0.1
BuildRequires:	flex
BuildRequires:	gcc-gfortran
BuildRequires:	glpk-devel
BuildRequires:	gnuplot
# (Abel) not strictly needed, but play safe
BuildRequires:	gperf
BuildRequires:	hdf5-devel
BuildRequires:	fontconfig-devel
BuildRequires:	lapack-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	pcre-devel
BuildRequires:	curl-devel
# (Lev) needed to support sparse matrix functionality
BuildRequires:	amd-devel
BuildRequires:	camd-devel
BuildRequires:	ccolamd-devel
BuildRequires:	cholmod-devel
BuildRequires:	colamd-devel
BuildRequires:	cxsparse-devel
BuildRequires:	umfpack-devel
# (Lev) other useful libraries
BuildRequires:	qhull-devel
BuildRequires:	qrupdate-devel
# (Lev) for new experimental plotting
BuildRequires:	fltk-devel
BuildRequires:	MesaGL-devel, MesaGLU-devel
# to make imread more functional
BuildRequires:	GraphicsMagick-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

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

%package devel
Summary:	Development headers and files for Octave
Group:		Development/C
Obsoletes:	octave3-devel < %{epoch}:%{version}-%{release}
Provides:	octave3-devel = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	blas-devel
Requires:	fftw-devel
Requires:	gcc-c++
Requires:	gcc-gfortran
Requires:	hdf5-devel
Requires:	lapack-devel
Requires:	readline-devel
Requires:zlib-devel

%description devel
The octave-devel package contains files needed for developing
applications which use GNU Octave.

%package doc
Summary:	Documentation for Octave, a numerical computational language
Group:		Sciences/Mathematics
Requires(post):	info-install
Requires(preun): info-install

%description doc
GNU Octave is a high-level language, primarily intended for numerical
computations. It provides a convenient command line interface for
solving linear and nonlinear problems numerically, and for performing
other numerical experiments using a language that is mostly compatible
with Matlab. It may also be used as a batch-oriented language.

This package contains documentation of Octave in various formats.

%prep
%setup -q
%patch0 -p0 


%build
%define enable64 no
export CPPFLAGS="%{optflags} -DH5_USE_16_API"
%{configure2_5x} --enable-dl --enable-shared --disable-static --enable-lite-kernel --enable-picky-flags --enable-64=%{enable64} --with-f77=gfortran 
%{make} OCTAVE_RELEASE="%{distribution} %{version}-%{release}"

# emacs mode

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

# Make library links
%{__mkdir_p} %{buildroot}/etc/ld.so.conf.d
/bin/echo "%{_libdir}/octave-%{version}" > %{buildroot}/etc/ld.so.conf.d/octave-%{_arch}.conf

# Remove RPM_BUILD_ROOT from ls-R files
%{__perl} -pi -e "s,%{buildroot},," %{buildroot}%{_libexecdir}/octave/ls-R
%{__perl} -pi -e "s,%{buildroot},," %{buildroot}%{_datadir}/octave/ls-R

%{_bindir}/find %{buildroot} -name "*.oct" -print0 | %{_bindir}/xargs -t -0 -r strip --strip-unneeded

# prepare documentation
%{__rm} -rf package-doc
%{__mkdir_p} package-doc

# Create desktop file
%{__rm} %{buildroot}%{_datadir}/applications/www.octave.org-octave.desktop
%{_bindir}/desktop-file-install --add-category Education --remove-category Development \
	--dir %{buildroot}%{_datadir}/applications doc/icons/octave.desktop

# Create directories for add-on packages
HOST_TYPE=`%{buildroot}%{_bindir}/octave-config -p CANONICAL_HOST_TYPE`
%{__mkdir_p} %{buildroot}%{_libexecdir}/octave/site/oct/%{octave_api}/$HOST_TYPE
%{__mkdir_p} %{buildroot}%{_libexecdir}/octave/site/oct/$HOST_TYPE
%{__mkdir_p} %{buildroot}%{_datadir}/octave/packages
/bin/touch %{buildroot}%{_datadir}/octave/octave_packages

%multiarch_includes %{buildroot}%{_includedir}/octave-%{version}/octave/*.h

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc NEWS* AUTHORS BUGS README
%doc examples INSTALL.OCTAVE
%defattr(-,root,root,0755)
%{_bindir}/octave*
%config(noreplace) /etc/ld.so.conf.d/*
%{_libdir}/octave*
%{_datadir}/octave
%exclude %{_datadir}/octave/octave_packages
%ghost %{_datadir}/octave/octave_packages
%if "%{_libdir}" != "%{_libexecdir}"
%{_libexecdir}/octave
%endif
%{_mandir}/man*/octave*
%{_infodir}/octave.info*
%{_datadir}/applications/*

%files devel
%defattr(0644,root,root,0755)
#%%doc doc/liboctave
%defattr(-,root,root)
%{_bindir}/mkoctfile*
%{_includedir}/octave-%{version}
%dir %{multiarch_includedir}/octave-*
%multiarch %{multiarch_includedir}/octave-*/*
%{_mandir}/man*/mkoctfile*

%files doc
%defattr(0644,root,root,0755)
%doc doc/refcard/refcard-a4.pdf
%{_infodir}/liboctave.*
%{_infodir}/OctaveFAQ.*
