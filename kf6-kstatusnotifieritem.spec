%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

%define libname %mklibname KF6StatusNotifierItem
%define devname %mklibname KF6StatusNotifierItem -d
#define git 20231103

Name: kf6-kstatusnotifieritem
Version: 5.246.0
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/frameworks/kstatusnotifieritem/-/archive/master/kstatusnotifieritem-master.tar.bz2#/kstatusnotifieritem-%{git}.tar.bz2
%else
Source0: https://download.kde.org/%{stable}/frameworks/%{version}/kstatusnotifieritem-%{version}.tar.xz
%endif
Summary: Implementation of Status Notifier Items
URL: https://invent.kde.org/frameworks/kstatusnotifieritem
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(Phonon4Qt6)
BuildRequires: cmake(Qt6Quick)
BuildRequires: pkgconfig(dbusmenu-qt6)
BuildRequires: pkgconfig(libcanberra)
Requires: %{libname} = %{EVRD}

%description
Implementation of Status Notifier Items

%package -n %{libname}
Summary: KNotification is used to notify the user of an event
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
KNotification is used to notify the user of an event.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

KNotification is used to notify the user of an event.

%prep
%autosetup -p1 -n kstatusnotifieritem-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# FIXME for some reason, find_lang misidentifies the language
# for locale files as LC_MESSAGES, so let's
# do it manually for now
for i in %{buildroot}%{_datadir}/locale/*/*/*.qm; do
	echo "%lang($(echo $i |rev |cut -d/ -f3 |rev)) /$(echo $i |rev |cut -d/ -f1-6 |rev)" >>%{name}.lang
done

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/kstatusnotifieritem.*
%{_datadir}/dbus-1/interfaces/*.xml

%files -n %{devname}
%{_includedir}/KF6/KStatusNotifierItem
%{_libdir}/cmake/KF6StatusNotifierItem
%{_qtdir}/doc/KF6StatusNotifierItem.*

%files -n %{libname}
%{_libdir}/libKF6StatusNotifierItem.so*
