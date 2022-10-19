Name:		libdb
Version:	5.3.28
Release:	40
Summary:	The Berkeley DB database library for C
License:	BSD and LGPLv2 and Sleepycat
URL:		https://www.oracle.com/database/berkeley-db/

Source0:	http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1:        http://download.oracle.com/berkeley-db/db.1.85.tar.gz
Source2:        http://www.gnu.org/licenses/lgpl-2.1.txt
Source3:        libdb-5.3.28-manpages.tar.gz

Patch0:         libdb-multiarch.patch
Patch10:        http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11:        http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12:        http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13:        http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
Patch20:        db-1.85-errno.patch
Patch22:        db-4.6.21-1.85-compat.patch
Patch24:        db-4.5.20-jni-include-dir.patch
Patch25:        007-mt19937db.c_license.patch
Patch26:        java8-fix.patch
Patch27:        db-5.3.21-memp_stat-upstream-fix.patch
Patch28:        db-5.3.21-mutex_leak.patch
Patch29:        db-5.3.28-lemon_hash.patch
Patch30:        db-5.3.28-condition_variable.patch
Patch31:        db-5.3.28-condition-variable-ppc.patch
Patch32:        db-5.3.28-rpm-lock-check.patch
# downstream patch to hotfix rhbz#1464033, sent upstream
Patch33:        db-5.3.28-cwd-db_config.patch
Patch34:        libdb-5.3.21-region-size-check.patch
# Patch sent upstream
Patch35:        checkpoint-opd-deadlock.patch
Patch36:        db-5.3.28-atomic_compare_exchange.patch
Patch37:        backport-CVE-2019-2708-Resolved-data-store-execution-which-led-to-partial-DoS.patch

Patch38:        bugfix-fix-deadlock-on-mempool-file-locks.patch
Patch39:        libdb-limit-cpu.patch
Patch40:        libdb-cbd-race.patch
Patch41:        add-check-for-device-number-in-__check_lock_fn.patch
Patch42:        fix-a-potential-infinite-loop.patch
Patch43:        db-5.3.28-sw.patch

BuildRequires:	gcc gcc-c++ perl-interpreter libtool tcl-devel >= 8.5.2-3 
BuildRequires:  java-devel >= 1:1.6.0 chrpath zlib-devel
Conflicts:      filesystem < 3

Provides:       %{name}-utils = %{version}-%{release}
Obsoletes:      %{name}-utils < %{version}-%{release}
Provides:       %{name}-cxx = %{version}-%{release}
Obsoletes:      %{name}-cxx < %{version}-%{release}
Provides:       %{name}-tcl = %{version}-%{release}
Obsoletes:      %{name}-tcl < %{version}-%{release}
Provides:       %{name}-sql = %{version}-%{release}
Obsoletes:      %{name}-sql < %{version}-%{release}
Provides:       %{name}-java = %{version}-%{release}
Obsoletes:      %{name}-java < %{version}-%{release}

%description
Oracle Berkeley DB provides the best open source embeddable databases 
allowing developers the choice of SQL, Key/Value, XML/XQuery or Java 
Object storage for their data model. At its core is a fast, scalable, 
transactional database engine with proven reliability and availability. 
Berkeley DB comes three versions: Berkeley DB, Berkeley DB Java 
Edition, and Berkeley DB XML.

%package        devel
Summary:        Header files for libdb
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-devel-doc = %{version}-%{release}
Obsoletes:      %{name}-devel-doc < %{version}-%{release}
Provides:       %{name}-devel-static = %{version}-%{release}
Obsoletes:      %{name}-devel-static < %{version}-%{release}
Provides:       %{name}-cxx-devel = %{version}-%{release}
Obsoletes:      %{name}-cxx-devel < %{version}-%{release}
Provides:       %{name}-tcl-devel = %{version}-%{release}
Obsoletes:      %{name}-tcl-devel < %{version}-%{release}
Provides:       %{name}-sql-devel = %{version}-%{release}
Obsoletes:      %{name}-sql-devel < %{version}-%{release}
Provides:       %{name}-java-devel = %{version}-%{release}
Obsoletes:      %{name}-java-devel < %{version}-%{release}

%description    devel
Header files for libdb.

%package_help 

%prep
%setup -q -n db-%{version} -a 1
cp %{SOURCE2} .
tar -xf %{SOURCE3}

%patch0 -p1
pushd db.1.85/PORT/linux
%patch10 -p0
popd
pushd db.1.85
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch20 -p1
popd

%patch22 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%ifarch sw_64
%patch43 -p1
%endif

pushd dist
./s_config
popd

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CFLAGS="$CFLAGS -DSHAREDSTATEDIR='\"%{_sharedstatedir}\"' -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -I../../../lang/sql/sqlite/ext/fts3/"
export CFLAGS

make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

test -d dist/dist-tls || mkdir dist/dist-tls

/bin/sh libtool --tag=CC --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c util/db_dump185.c -o dist/dist-tls/db_dump185.lo
/bin/sh libtool --tag=LD --mode=link %{__cc} -o dist/dist-tls/db_dump185 dist/dist-tls/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

for dir in dist lang/sql/sqlite lang/sql/jdbc lang/sql/odbc; do
  cp /usr/lib/rpm/%{?_vendor}/config.{guess,sub} "$dir"
done

pushd dist/dist-tls
%define _configure ../configure
%configure -C \
           --enable-compat185 --enable-dump185 --enable-shared --enable-tcl --with-tcl=%{_libdir} \
           --enable-cxx --enable-sql --enable-java --enable-test --disable-rpath --with-tcl=%{_libdir}/tcl8.6

%disable_rpath

%make_build

popd

%install
%make_install STRIP=/bin/true -C dist/dist-tls

%delete_la

chmod +x %{buildroot}%{_libdir}/*.so*

install -d -m 0755 %{buildroot}%{_includedir}/libdb
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/libdb/

for i in db.h db_cxx.h db_185.h; do
    ln -s %{name}/$i %{buildroot}%{_includedir}
done 

install -d -m 0755 %{buildroot}%{_datadir}/java
mv %{buildroot}%{_libdir}/*.jar %{buildroot}%{_datadir}/java/

chmod u+w %{buildroot}%{_bindir} %{buildroot}%{_bindir}/*
chrpath -d ${RPM_BUILD_ROOT}%{_libdir}/*.so ${RPM_BUILD_ROOT}%{_bindir}/*

rm -rf docs/{csharp,installation}
rm -rf %{buildroot}%{_prefix}/docs
rm -rf example/csharp
mv examples docs
install -d -m 0755 %{buildroot}%{_mandir}/man1
mv man/* %{buildroot}%{_mandir}/man1/

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc docs/license
%license LICENSE
%{_bindir}/*
%{_libdir}/*.so
%{_datadir}/java/*.jar
%exclude %{_libdir}/libdb.so
%exclude %{_libdir}/libdb_cxx.so
%exclude %{_libdir}/libdb_tcl.so
%exclude %{_libdir}/libdb_sql.so
%exclude %{_libdir}/libdb_java.so

%files          devel
%defattr(-,root,root)
%doc docs/*
%{_libdir}/*.a
%{_libdir}/libdb.so
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_sql.so
%{_libdir}/libdb_java.so
%{_includedir}/*

%files          help
%defattr(-,root,root)
%doc README
%{_mandir}/man1

%changelog
* Wed Oct 19 2022 wuzx<wuzx1226@qq.com> - 5.3.28-40
- add sw64 patch

* Tue Jul 12 2022 Kou Wenqi <kouwenqi@kylinos.cn> - 5.3.28-39
- Fix a potential infinite loop

* Tue Jun 28 2022 panxiaohe <panxh.life@foxmail.com> - 5.3.28-38
- add check for device number in __check_lock_fn

* Mon Apr 19 2021 wangchen <wangchen137@huawei.com> - 5.3.28-37
- Fix CVE-2019-2708

* Tue Sep 8 2020 wangchen <wangchen137@huawei.com> - 5.3.28-36
- Modify the URL of Source0

* Wed Nov 6 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.3.28-35
- Add Package version

* Mon Nov 4 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.3.28-34
- Package init
