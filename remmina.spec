# Main branch is the "next" branch, not master
%global commit0 55fb3aad40aa487cd3fdd2395633735e006eeafb
%global date 20170923
%global shortcommit0 %%(c=%%{commit0}; echo ${c:0:7})

# RC releases
#%%global snapshot rcgit.19

Name:          remmina
Version:       1.2.0
Release:       0.43%{?snapshot:.%{snapshot}}%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:       Remote Desktop Client
License:       GPLv2+ and MIT
URL:           http://remmina.sourceforge.net
%if %{?snapshot}0
Source0:       https://github.com/FreeRDP/Remmina/archive/v%{version}%{?snapshot:-%{snapshot}}.tar.gz#/Remmina-%{version}%{?snapshot:-%{snapshot}}.tar.gz
%else
Source0:       https://github.com/FreeRDP/Remmina/archive/%{commit0}/Remmina-%{commit0}.tar.gz#/Remmina-%{shortcommit0}.tar.gz
%endif

# Cmake helper file to easy build plugins outside remmina source tree
# See http://www.muflone.com/remmina-plugin-rdesktop/english/install.html which
# use http://www.muflone.com/remmina-plugin-builder/ with remmina bundled source.
# So we can't use it directly only as instructions.
Source1:       pluginBuild-CMakeLists.txt

BuildRequires: cmake >= 2.8
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libappstream-glib
BuildRequires: libgcrypt-devel
BuildRequires: pkgconfig(appindicator3-0.1)
BuildRequires: pkgconfig(avahi-ui) >= 0.6.30
BuildRequires: pkgconfig(avahi-ui-gtk3) >= 0.6.30
BuildRequires: pkgconfig(freerdp2)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libsecret-1)
BuildRequires: pkgconfig(libssh) >= 0.6
BuildRequires: pkgconfig(libvncserver)
BuildRequires: pkgconfig(spice-client-gtk-3.0)
BuildRequires: pkgconfig(vte-2.91)
BuildRequires: pkgconfig(xkbfile)

# We don't ship the remmina-plugins-telepathy package any longer
Provides:      remmina-plugins-telepathy = %{version}
Obsoletes:     remmina-plugins-telepathy < %{version}-%{release}

%if 0%{?fedora} > 23
Recommends:    remmina-plugins-nx remmina-plugins-rdp
Recommends:    remmina-plugins-gnome remmina-plugins-vnc remmina-plugins-xdmcp
%endif

%description
Remmina is a remote desktop client written in GTK+, aiming to be useful for
system administrators and travelers, who need to work with lots of remote
computers in front of either large monitors or tiny net-books.

Remmina supports multiple network protocols in an integrated and consistent
user interface. Currently RDP, VNC, XDMCP and SSH are supported.

Please don't forget to install the plugins for the protocols you want to use.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains header files for developing plugins for
%{name}.


%package        plugins-gnome
Summary:        GNOME keyring integration for Remmina Remote Desktop Client
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    plugins-gnome
Remmina is a remote desktop client written in GTK+, aiming to be useful for
system administrators and travelers, who need to work with lots of remote
computers in front of either large monitors or tiny net-books.

This package contains the plugin with GNOME keyring support for the Remmina
remote desktop client.


%package        plugins-nx
Summary:        NX plugin for Remmina Remote Desktop Client
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       nxproxy

%description    plugins-nx
Remmina is a remote desktop client written in GTK+, aiming to be useful for
system administrators and travelers, who need to work with lots of remote
computers in front of either large monitors or tiny net-books.

This package contains the NX plugin for the Remmina remote desktop client.


%package        plugins-rdp
Summary:        RDP plugin for Remmina Remote Desktop Client
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    plugins-rdp
Remmina is a remote desktop client written in GTK+, aiming to be useful for
system administrators and travelers, who need to work with lots of remote
computers in front of either large monitors or tiny net-books.

This package contains the Remote Desktop Protocol (RDP) plugin for the Remmina
remote desktop client.


%package        plugins-vnc
Summary:        VNC plugin for Remmina Remote Desktop Client
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    plugins-vnc
Remmina is a remote desktop client written in GTK+, aiming to be useful for
system administrators and travelers, who need to work with lots of remote
computers in front of either large monitors or tiny net-books.

This package contains the VNC plugin for the Remmina remote desktop
client.


%package        plugins-xdmcp
Summary:        XDMCP plugin for Remmina Remote Desktop Client
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xorg-x11-server-Xephyr

%description    plugins-xdmcp
Remmina is a remote desktop client written in GTK+, aiming to be useful for
system administrators and travelers, who need to work with lots of remote
computers in front of either large monitors or tiny net-books.

This package contains the XDMCP plugin for the Remmina remote desktop
client.


%package        plugins-spice
Summary:        SPICE plugin for Remmina Remote Desktop Client
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    plugins-spice
Remmina is a remote desktop client written in GTK+, aiming to be useful for
system administrators and travelers, who need to work with lots of remote
computers in front of either large monitors or tiny net-books.

This package contains the SPICE plugin for the Remmina remote desktop
client.


%prep
%setup -qn Remmina-%{?snapshot:%{version}-%{snapshot}}%{?commit0}

%build
mkdir -p build

%cmake --build=build \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_COMPONENT=1 \
    -DWITH_APPINDICATOR=ON \
    -DWITH_AVAHI=ON \
    -DWITH_FREERDP=ON \
    -DWITH_GCRYPT=ON \
    -DWITH_GETTEXT=ON \
    -DWITH_LIBSSH=ON \
    -DWITH_SPICE=ON \
    -DWITH_SURVEY=OFF \
    -DWITH_TELEPATHY=OFF \
    -DWITH_VTE=ON \
    -DWITH_ZLIB=ON \
    -DGIT_REVISION=%{commit0} \
    .

make %{?_smp_mflags}

%install
%make_install

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

mkdir -p %{buildroot}/%{_libdir}/cmake/%{name}/
cp -pr cmake/*.cmake %{buildroot}/%{_libdir}/cmake/%{name}/
cp -pr config.h.in %{buildroot}/%{_includedir}/%{name}/
cp -p %{SOURCE1} %{buildroot}/%{_includedir}/%{name}/

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-nx
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-rdp
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-vnc
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-xdmcp
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-spice
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-nx
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-rdp
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-vnc
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-xdmcp
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-spice
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-nx
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-rdp
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-vnc
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-xdmcp
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-spice
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc AUTHORS ChangeLog README.md
%{_bindir}/%{name}
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/actions/*.*
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/icons/hicolor/*/emblems/remmina-sftp.png
%{_datadir}/%{name}/
%dir %{_libdir}/remmina/
%dir %{_libdir}/remmina/plugins/
%{_mandir}/man1/%{name}.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/*.cmake

%files plugins-gnome
%{_libdir}/remmina/plugins/remmina-plugins-gnome.so

%files plugins-nx
%{_libdir}/remmina/plugins/remmina-plugin-nx.so
%{_datadir}/icons/hicolor/*/emblems/remmina-nx.png

%files plugins-rdp
%{_libdir}/remmina/plugins/remmina-plugin-rdp.so
%{_datadir}/icons/hicolor/*/emblems/remmina-rdp-ssh.png
%{_datadir}/icons/hicolor/*/emblems/remmina-rdp.png

%files plugins-vnc
%{_libdir}/remmina/plugins/remmina-plugin-vnc.so
%{_datadir}/icons/hicolor/*/emblems/remmina-vnc-ssh.png
%{_datadir}/icons/hicolor/*/emblems/remmina-vnc.png

%files plugins-xdmcp
%{_libdir}/remmina/plugins/remmina-plugin-xdmcp.so
%{_datadir}/icons/hicolor/*/emblems/remmina-xdmcp-ssh.png
%{_datadir}/icons/hicolor/*/emblems/remmina-xdmcp.png

%files plugins-spice
%{_libdir}/remmina/plugins/remmina-plugin-spice.so
%{_datadir}/icons/hicolor/*/emblems/remmina-spice.png


%changelog
* Tue Sep 26 2017 David Morgado <dcrmorgado@gmail.com> - 1.2.0-0.43.20170923git55fb3aa
- Update to latest snapshot.

* Mon Sep 11 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.42.20170908git205df66
- Update to latest snapshot.
- Trim changelog.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.41.20170724git0387ee0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.40.20170724git0387ee0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 27 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.39.20170724git0387ee0
- Update to latest snapshot (matching with rcgit 19).

* Wed Jul 12 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.38.20170710git89009c8
- Update to latest snapshot.

* Mon Jun 26 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.37.20170622git7e82138
- Rebuild for FreeRDP update.

* Mon Jun 26 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.36.20170622git7e82138
- Update to latest snapshot.

* Mon May 15 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.35.20170510git41c8de6
- Update to latest snapshot.

* Mon Apr 24 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.34.20170424git2c0a77e
- Update to latest snapshot.

* Wed Mar 22 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.33.20170317git4d8d257
- Update to latest snapshot.

* Thu Mar 09 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.32.20170302git1da1fb6
- Remove non-working telepathy plugin.

* Thu Mar 02 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.31.20170302git1da1fb6
- Update to latest snapshot.

* Wed Feb 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-0.30.20161226gitd1a4a73
- rebuild (libvncserver)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.29.20161226gitd1a4a73
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.28.20161226gitd1a4a73
- Switch to latest snapshot of the next branch.

* Sat Dec 03 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.27.20161126git35604d5
- Update to latest code drop from the libfreerdp_updates branch.

* Fri Nov 04 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.26.20161104git80a77b8
- Update to latest snapshot.
- Still not building properly with FreeRDP:
  https://github.com/FreeRDP/Remmina/issues/1028

* Fri Oct 14 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.25.20161010gitaeaae39
- Update to latest snapshot.

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.24.20161004git88f490d
- Update to latest snapshot.

* Tue Sep 20 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.23.20160914git42f5a87
- Update to latest snapshot, update release to follow packaging guidelines.

* Sat Aug 27 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 1.2.0-0.22.git.679bb8e
- Provide GIT_REVISION to cmake for use in version.

* Tue Aug 16 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 1.2.0-0.21.git.679bb8e
- Update to try solve issues with tray icons - https://github.com/FreeRDP/Remmina/issues/944#issuecomment-239913278
- Drop old issue 292 hack.
- Conditionally allow build by hash or pre-releases.

* Fri Aug 12 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.20.git.cbcb19e
- Update to latest snapshot.

* Thu Jun 23 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.19.rcgit.14
- Rebuild for spice-gtk upgrade.

* Tue Jun 21 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.18.rcgit.14
- Update to version 1.2.0-rcgit.14.

* Tue Jun 07 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.17.rcgit.13
- Use "snapshot" name only once in the SPEC file.

* Tue Jun 07 2016 Simone Caronni <negativo17@gmail.com> - 1.2.0-0.16.rcgit.12
- Update to version 12.0-rcgit.13, enable SPICE plugin, update cmake options.

* Fri May 20 2016 David Woodhouse <dwmw2@infradead.org> - 1.2.0-0.15.rcgit.12
- Disable survey, as it has build problems

* Fri May 20 2016 David Woodhouse <dwmw2@infradead.org> - 1.2.0-0.14.rcgit.12
- Update to version 12.0-rcgit.12.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.13.rcgit.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 02 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 1.2.0-0.12.rcgit.7
- Update to version 1.2.0-rcgit.7.

* Fri Jan 01 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 1.2.0-0.11.git.b43697d
- Recommends all plugins by suggestion bz#1241658.
