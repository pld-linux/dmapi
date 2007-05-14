Summary:	DMAPI library
Summary(pl.UTF-8):	Biblioteka DMAPI
Name:		dmapi
Version:	2.2.8
Release:	1
License:	LGPL/GPL
Group:		Libraries
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.gz
# Source0-md5:	29c5ba7d9a3524fd247be00c3b43e8d9
Patch0:		%{name}-miscfix.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	sed >= 4.0
BuildRequires:	xfsprogs-devel >= 2.6.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}
%define		_libexecdir	/usr/%{_lib}

%description
DMAPI, or XDSM, is an implementation of the X/Open document: Systems
Management: Data Storage Management (XDSM) API dated February 1997.
This interface is made available for the XFS filesystem by means of
the libdm library.

See the XDSM manual at
http://www.opengroup.org/onlinepubs/9657099/toc.htm for a description
of the functions offered by libdm library.

%description -l pl.UTF-8
DMAPI (albo XDSM) to implementacja dokumentu X/Open "Systems
Management: Data Storage Management (XDSM) API) z lutego 1997. Ten
interfejs jest dostępny dla systemu plików XFS poprzez bibliotekę
libdm.

Opis funkcji oferowanych przez bibliotekę libdm jest w podręczniku:
http://www.opengroup.org/onlinepubs/9657099/toc.htm

%package devel
Summary:	Header files for DMAPI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki DMAPI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xfsprogs-devel

%description devel
Header files required to develop software which uses DMAPI.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do tworzenia oprogramowania używającego
DMAPI.

%package static
Summary:	Static DMAPI library
Summary(pl.UTF-8):	Statyczna biblioteka DMAPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of DMAPI library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki DMAPI.

%prep
%setup -q
%patch0 -p1

%build
rm -f aclocal.m4
%{__aclocal} -I m4
%{__autoconf}
%configure \
	DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}" \
	OPTIMIZER="%{rpmcflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT=$RPM_BUILD_ROOT
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV

%{__make} install \
	DIST_MANIFEST=$DIST_INSTALL
%{__make} install-dev \
	DIST_MANIFEST=$DIST_INSTALL_DEV

rm -f $RPM_BUILD_ROOT%{_libexecdir}/libdm.so
ln -sf %{_libdir}/$(cd $RPM_BUILD_ROOT%{_libdir} ; echo libdm.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libexecdir}/libdm.so
%{__sed} -i "s|libdir='%{_libdir}'|libdir='%{_libexecdir}'|" \
	$RPM_BUILD_ROOT%{_libexecdir}/libdm.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING specifies which parts are on LGPL/GPL
%doc doc/{CHANGES,COPYING}
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/lib*.so
%{_libexecdir}/lib*.la
%{_includedir}/xfs/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libexecdir}/lib*.a
