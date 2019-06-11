# Define the kmod package name here.
%define	 kmod_name nvidia

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 2.6.32-754.el6.%{_target_cpu}}

Name:	 %{kmod_name}-kmod
Version: 430.26
Release: 1%{?dist}
Group:	 System Environment/Kernel
License: Proprietary
Summary: NVIDIA OpenGL kernel driver module
URL:	 http://www.nvidia.com/

BuildRequires:	redhat-rpm-config
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-build-%(%{__id_u} -n)
ExclusiveArch:	i686 x86_64

# Sources.
Source0:  ftp://download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
Source1:  ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source10: kmodtool-%{kmod_name}-el6.sh

NoSource: 0
NoSource: 1

# Magic hidden here.
%define kmodtool sh %{SOURCE10}
%{expand:%(%{kmodtool} rpmtemplate %{kmod_name} %{kversion} "" 2>/dev/null)}

# Disable building of the debug package(s).
%define	debug_package %{nil}

%description
This package provides the proprietary NVIDIA OpenGL kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -c -T
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf
#echo "override %{kmod_name}-drm * weak-updates/%{kmod_name}" >> kmod-%{kmod_name}.conf
#echo "override %{kmod_name}-modeset * weak-updates/%{kmod_name}" >> kmod-%{kmod_name}.conf
%ifarch x86_64
echo "override %{kmod_name}-uvm * weak-updates/%{kmod_name}" >> kmod-%{kmod_name}.conf
%endif

%ifarch i686
sh %{SOURCE0} --extract-only --target nvidiapkg
%endif

%ifarch x86_64
sh %{SOURCE1} --extract-only --target nvidiapkg
%endif

%{__cp} -a nvidiapkg _kmod_build_

%build
export SYSSRC=%{_usrsrc}/kernels/%{kversion}
pushd _kmod_build_/kernel
%{__make} module
popd

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
ksrc=%{_usrsrc}/kernels/%{kversion}
pushd _kmod_build_/kernel
%{__make} -C "${ksrc}" modules_install M=$PWD
popd
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/modules.*
# Remove the unwanted files
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/extra/nvidia/nvidia-drm.ko
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/extra/nvidia/nvidia-modeset.ko

%clean
%{__rm} -rf %{buildroot}

%changelog
* Wed Jun 12 2019 Michael Lampe <mlampe0@googlemail.com> - 430.26-1
- Updated to version 430.26

* Tue May 14 2019 Michael Lampe <mlampe0@googlemail.com> - 430.14-1
- Updated to version 430.14

* Thu May  9 2019 Michael Lampe <mlampe0@googlemail.com> - 418.74-1
- Updated to version 418.74

* Fri Feb 22 2019 Michael Lampe <mlampe0@googlemail.com> - 418.43-1
- Updated to version 418.43

* Thu Jan  3 2019 Michael Lampe <mlampe0@googlemail.com> - 410.93-1
- Updated to version 410.93

* Thu Nov 15 2018 Michael Lampe <mlampe0@googlemail.com> - 410.78-1
- Updated to version 410.78

* Fri Oct 26 2018 Michael Lampe <mlampe0@googlemail.com> - 410.73-1
- Updated to version 410.73

* Wed Oct 17 2018 Michael Lampe <mlampe0@googlemail.com> - 410.66-1
- Updated to version 410.66
