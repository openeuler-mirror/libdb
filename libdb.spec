%define realver 036ebf72

Name: libdb
Version: 18.1.32
Release: 2
Summary: Berkeley DB is a family of embedded key-value database libraries providing scalable high-performance data management services to applications.
License: AGPL-3.0 and Public Domain
URL: http://www.oracle.com/database/berkeley-db/
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: https://www.sqlite.org/cgi/src/zip/%{realver}/SQLite-%{realver}.zip

BuildRequires: gcc gcc-c++ libtool tcl-devel java-devel chrpath gdb libdb libdb-cxx libdb-sql

Provides: %{name}-utils
Obsoletes: %{name}-utils

%description
Berkeley DB is a family of embedded key-value database libraries
providing scalable high-performance data management services to applications.
The Berkeley DB products use simple function-call APIs for data access and management.
Berkeley DB enables the development of custom data management solutions,
without the overhead traditionally associated with such custom projects.
Berkeley DB provides a collection of well-proven building-block technologies
that can be configured to address any application need from the hand-held device to the data center,
from a local storage solution to a world-wide distributed one, from kilobytes to petabytes.

%package devel
Summary: C development files for the Berkeley DB library
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: %{name}-devel-static
Obsoletes: %{name}-devel-static

%description devel
This package contains the header files and libraries
for building programs which use the Berkeley DB in C.

%package help
Summary: C development documentation files for the Berkeley DB library
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Obsoletes:  %{name}-devel-doc
BuildArch: noarch

%description help
This package contains the documentation for building programs which use the Berkeley DB.

%package cxx
Summary: The Berkeley DB database library for C++
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cxx
The Berkeley DB supports C++ APIs. This package contains the libraries for C++.

%package cxx-devel
Summary: C++ development files for the Berkeley DB library
Requires: %{name}-cxx%{?_isa} = %{version}-%{release}

%description cxx-devel
This package contains the header files and libraries
for building programs which use the Berkeley DB in C++.

%package tcl
Summary: The Berkeley DB database library for Tcl
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tcl
The Berkeley DB supports Tcl APIs. This package contains the libraries for Tcl.

%package tcl-devel
Summary: Tcl development files for the Berkeley DB library
Requires: %{name}-tcl%{?_isa} = %{version}-%{release}

%description tcl-devel
This package contains the Tcl files and libraries
for building programs which use the Berkeley DB in Tcl.

%package sql
Summary: The Berkeley DB database library for Sql
Requires: %{name}%{?_isa} = %{version}-%{release}

%description sql
The Berkeley DB supports Sql APIs. This package contains the libraries for Sql.

%package sql-devel
Summary: Sql development files for the Berkeley DB library
Requires: %{name}-sql%{?_isa} = %{version}-%{release}

%description sql-devel
This package contains the Sql files and libraries
for building programs which use the Berkeley DB in Sql.

%package java
Summary: The Berkeley DB database library for Java
Requires: %{name}%{?_isa} = %{version}-%{release}

%description java
The Berkeley DB supports Java APIs. This package contains the libraries for Java.

%package java-devel
Summary: Java development files for the Berkeley DB library
Requires: %{name}-java%{?_isa} = %{version}-%{release}

%description java-devel
This package contains the java files and libraries
for building programs which use the Berkeley DB in java.

%prep
%setup -q -n db-%{version} -a 1
cp -rf SQLite-%{realver}/tool lang/sql/sqlite
for code in db_pragma.c db_sequence.c; do
    sed -i '/$(TOP)\/ext\/misc\/totype.c \\/a\$(TOP)\/..\/adapter\/'$code' \\' lang/sql/sqlite/Makefile.in
done

%build
test -d dist/build_db || mkdir dist/build_db

for dir in dist lang/sql/sqlite; do
    cp /usr/lib/rpm/config.{guess,sub} "$dir"
done

pushd dist/build_db
%define _configure ../configure
%configure -C \
	--enable-compat185 --disable-dump185 --enable-shared --enable-static \
	--enable-tcl --with-tcl=%{_libdir} --enable-cxx --enable-sql \
	--enable-java --enable-test --disable-rpath --with-repmgr-ssl=no

%make_build
popd

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%make_install -C dist/build_db

rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a,libdb_tcl.a,libdb_sql.a}
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

cp -a %{_libdir}/libdb-5.* ${RPM_BUILD_ROOT}%{_libdir}
cp -a %{_libdir}/libdb_cxx-5.* ${RPM_BUILD_ROOT}%{_libdir}
cp -a %{_libdir}/libdb_sql-5.* ${RPM_BUILD_ROOT}%{_libdir}

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*
chrpath -d ${RPM_BUILD_ROOT}%{_libdir}/*.so ${RPM_BUILD_ROOT}%{_bindir}/*

%pre

%preun

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -p /sbin/ldconfig cxx

%postun -p /sbin/ldconfig cxx

%post -p /sbin/ldconfig tcl

%postun -p /sbin/ldconfig tcl

%post -p /sbin/ldconfig sql

%postun -p /sbin/ldconfig sql

%post -p /sbin/ldconfig java

%postun -p /sbin/ldconfig java

%files
%doc README
%license LICENSE
%{_libdir}/libdb-*.so
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%{_bindir}/db*_tuner
%{_bindir}/db*_convert

%files devel
%doc examples/*
%license EXAMPLES-LICENSE
%{_libdir}/libdb.so
%{_includedir}/db.h
%{_includedir}/db_185.h
%{_libdir}/libdb-*.a
%{_libdir}/libdb_cxx-*.a
%{_libdir}/libdb_tcl-*.a
%{_libdir}/libdb_sql-*.a
%{_libdir}/libdb_java-*.a

%files help
%doc	docs/*

%files cxx
%{_libdir}/libdb_cxx-*.so

%files cxx-devel
%{_includedir}/db_cxx.h
%{_libdir}/libdb_cxx.so

%files tcl
%{_libdir}/libdb_tcl-*.so

%files tcl-devel
%{_libdir}/libdb_tcl.so

%files sql
%{_libdir}/libdb_sql-*.so

%files sql-devel
%{_bindir}/dbsql
%{_libdir}/libdb_sql.so
%{_includedir}/dbsql.h

%files java
%{_libdir}/libdb_java-*.so
%{_libdir}/*.jar

%files java-devel
%{_libdir}/libdb_java.so

%changelog
* Thu Oct 10 2019 hanxinke<hanxinke@huawei.com> - 18.1.32-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add EXAMPLES-LICENSE to the devel package

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 18.1.32-1
- Package init

