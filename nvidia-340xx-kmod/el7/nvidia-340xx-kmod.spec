# Define the kmod package name here.
%define kmod_name nvidia-340xx

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 3.10.0-1127.el7.%{_target_cpu}}

Name:    %{kmod_name}-kmod
Version: 340.108
Release: 2%{?dist}
Group:   System Environment/Kernel
License: Proprietary
Summary: NVIDIA OpenGL kernel driver module
URL:	 http://www.nvidia.com/

BuildRequires: perl
BuildRequires: redhat-rpm-config
ExclusiveArch: x86_64

# Sources.
Source0:  ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source1:  blacklist-nouveau.conf
Source10: kmodtool-%{kmod_name}-el7.sh

NoSource: 0

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provides the proprietary NVIDIA OpenGL kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -c -T
echo "override nvidia * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf
echo "override nvidia-uvm * weak-updates/%{kmod_name}" >> kmod-%{kmod_name}.conf
sh %{SOURCE0} --extract-only --target nvidiapkg

%{__cp} -a nvidiapkg _kmod_build_

%build
export SYSSRC=%{_usrsrc}/kernels/%{kversion}
pushd _kmod_build_/kernel
%{__make} module
popd
pushd _kmod_build_/kernel/uvm
%{__make} module
popd

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
pushd _kmod_build_/kernel
%{__install} nvidia.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
popd
pushd _kmod_build_/kernel/uvm
%{__install} nvidia-uvm.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
popd
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_prefix}/lib/modprobe.d/
%{__install} %{SOURCE1} %{buildroot}%{_prefix}/lib/modprobe.d/blacklist-nouveau.conf

%clean
%{__rm} -rf %{buildroot}

%changelog
* Thu Apr 09 2020 Michael Lampe <mlampe0@googlemail.com> - 340.108-2
- Rebuilt for 7.8 kernel

* Thu Dec 26 2019 Michael Lampe <mlampe0@googlemail.com> - 340.108-1
- Updated to version 340.108

* Mon Aug 12 2019 Michael Lampe <mlampe0@googlemail.com> - 340.107-3
- Rebuilt for 7.7 kernel

* Mon Nov 19 2018 Michael Lampe <mlampe0@googlemail.com> - 340.107-2
- Rebuilt for 7.6 kernel

* Thu Jun 07 2018 Michael Lampe <mlampe0@googlemail.com> - 340.107-1
- Updated to version 340.107

* Mon Apr 30 2018 Michael Lampe <mlampe0@googlemail.com> - 340.106-3
- Rebuilt for 7.5 kernel

* Wed Mar 14 2018 Michael Lampe <mlampe0@googlemail.com> - 340.106-2
- Rebuilt for retpoline
