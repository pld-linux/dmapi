Summary:	DMAPI library
Summary(pl):	Biblioteka DMAPI
Name:		dmapi
Version:	2.0.0
Release:	2
License:	GPL
Group:		Libraries
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	autoconf
BuildRequires:	xfsprogs-devel >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DMAPI, or XDSM, is an implementation of the X/Open document: Systems
Management: Data Storage Management (XDSM) API dated February 1997.
This interface is made available for the XFS filesystem by means of
the libdm library.

See the XDSM manual at
http://www.opengroup.org/onlinepubs/9657099/toc.htm for a description
of the functions offered by libdm library.

%description -l pl
DMAPI (albo XDSM) to implementacja dokumentu X/Open "Systems
Management: Data Storage Management (XDSM) API) z lutego 1997. Ten
interfejs jest dostêpny dla systemu plików XFS poprzez bibliotekê
libdm.

Opis funkcji oferowanych przez bibliotekê libdm jest w podrêczniku:
http://www.opengroup.org/onlinepubs/9657099/toc.htm

%package devel
Summary:	Header files for DMAPI library
Summary(pl):	Pliki nag³ówkowe biblioteki DMAPI
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	xfsprogs-devel

%description devel
Header files required to develop software which uses DMAPI.

%description devel -l pl
Pliki nag³ówkowe potrzebne do tworzenia oprogramowania u¿ywaj±cego
DMAPI.

%package static
Summary:	Static DMAPI library
Summary(pl):	Statyczna biblioteka DMAPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of DMAPI library.

%description static -l pl
Statyczna wersja biblioteki DMAPI.

%prep
%setup  -q

%build
DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}"; export DEBUG
autoconf
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV

%{__make} install DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"

rm -f $RPM_BUILD_ROOT%{_libdir}/libdm.so
ln -sf /lib/libdm.so.0.0.1 $RPM_BUILD_ROOT%{_libdir}/libdm.so

gzip -9nf doc/CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*.gz
%attr(755,root,root) /lib/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/xfs/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
