# Define the kmod package name here.
%define kmod_name nvidia

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 3.10.0-1127.el7.%{_target_cpu}}

Name:    %{kmod_name}-kmod
Version: 450.57
Release: 1%{?dist}
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
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf
echo "override %{kmod_name}-modeset * weak-updates/%{kmod_name}" >> kmod-%{kmod_name}.conf
echo "override %{kmod_name}-uvm * weak-updates/%{kmod_name}" >> kmod-%{kmod_name}.conf
sh %{SOURCE0} --extract-only --target nvidiapkg
%{__cp} -a nvidiapkg _kmod_build_

%build
export SYSSRC=%{_usrsrc}/kernels/%{kversion}
pushd _kmod_build_/kernel
%{__make} %{?_smp_mflags} module
popd

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
pushd _kmod_build_/kernel
%{__install} %{kmod_name}.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} %{kmod_name}-modeset.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} %{kmod_name}-uvm.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
popd
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_prefix}/lib/modprobe.d/
%{__install} %{SOURCE1} %{buildroot}%{_prefix}/lib/modprobe.d/blacklist-nouveau.conf

%clean
%{__rm} -rf %{buildroot}

%changelog
* Wed Jul 15 2020 Michael Lampe <mlampe0@googlemail.com> - 450.57-1.el7.ml
- Updated to version 450.57

* Thu Jun 25 2020 Michael Lampe <mlampe0@googlemail.com> - 440.100-1.el7.ml
- Updated to version 440.100

* Thu Apr  9 2020 Michael Lampe <mlampe0@googlemail.com> - 440.82-1.el7.ml
- Updated to version 440.82

* Tue Mar  3 2020 Michael Lampe <mlampe0@googlemail.com> - 440.64-1.el7.ml
- Updated to version 440.64

* Mon Feb  3 2020 Michael Lampe <mlampe0@googlemail.com> - 440.59-1.el7.ml
- Updated to version 440.59

* Fri Dec 13 2019 Michael Lampe <mlampe0@googlemail.com> - 440.44-1.el7.ml
- Updated to version 440.44

* Sat Nov 23 2019 Michael Lampe <mlampe0@googlemail.com> - 440.36-1.el7.ml
- Updated to version 440.36

* Mon Nov  4 2019 Michael Lampe <mlampe0@googlemail.com> - 440.31-1.el7.ml
- Updated to version 440.31

* Thu Sep 12 2019 Michael Lampe <mlampe0@googlemail.com> - 430.50-1.el7.ml
- Updated to version 430.50

* Fri Aug 30 2019 Michael Lampe <mlampe0@googlemail.com> - 430.40-2.el7.ml
- Rebuilt for 7.7 kernel

* Wed Jul 31 2019 Michael Lampe <mlampe0@googlemail.com> - 430.40-1.el7.ml
- Updated to version 430.40

* Thu Jul 11 2019 Michael Lampe <mlampe0@googlemail.com> - 430.34-1.el7.ml
- Updated to version 430.34

* Tue Jun 11 2019 Michael Lampe <mlampe0@googlemail.com> - 430.26-1.el7.ml
- Updated to version 430.26

* Tue May 14 2019 Michael Lampe <mlampe0@googlemail.com> - 430.14-1.el7.ml
- Updated to version 430.14

* Wed May  8 2019 Michael Lampe <mlampe0@googlemail.com> - 418.74-1.el7.ml
- Updated to version 418.74

* Fri Feb 22 2019 Michael Lampe <mlampe0@googlemail.com> - 418.43-1.el7.ml
- Updated to version 418.43

* Thu Jan  3 2019 Michael Lampe <mlampe0@googlemail.com> - 410.93-1.el7.ml
- Updated to version 410.93

* Fri Nov 16 2018 Michael Lampe <mlampe0@googlemail.com> - 410.78-2.el7.ml
- Rebuilt for 7.6 kernel

* Thu Nov 15 2018 Michael Lampe <mlampe0@googlemail.com> - 410.78-1.el7.ml
- Updated to version 410.78

* Fri Oct 26 2018 Michael Lampe <mlampe0@googlemail.com> - 410.73-1.el7.ml
- Updated to version 410.73

* Wed Oct 17 2018 Michael Lampe <mlampe0@googlemail.com> - 410.66-1.el7.ml
- Resynced with elrepo
