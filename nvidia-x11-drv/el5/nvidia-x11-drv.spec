%define		nvidialibdir	%{_libdir}/nvidia
%define		nvidialib32dir	%{_prefix}/lib/nvidia

%define		debug_package	%{nil}

Name:		nvidia-x11-drv
Version:	340.65
Release:	1%{?dist}
Group:		User Interface/X Hardware Support
License:	Distributable
Summary:	NVIDIA OpenGL X11 display driver files
URL:		http://www.nvidia.com/

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-build-%(%{__id_u} -n)
ExclusiveArch:	i386 x86_64

# Sources.
Source0:  ftp://download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
Source1:  ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
# Source0: http://us.download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
# Source1: http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run

NoSource: 0
NoSource: 1

Source4:	nvidia-config-display
Source5:	nvidia.modprobe
Source6:	nvidia.nodes
Source7:	alternate-install-present

# provides desktop-file-install
BuildRequires:	desktop-file-utils
BuildRequires:	perl

Requires:	nvidia-kmod = %{?epoch:%{epoch}:}%{version}
Requires(post):	nvidia-kmod = %{?epoch:%{epoch}:}%{version}

Requires(post):	/sbin/ldconfig

# for nvidia-config-display
Requires(post):	 pyxf86config
Requires(preun): pyxf86config

# elrepo
Conflicts:	nvidia-x11-drv-304xx
Conflicts:	nvidia-x11-drv-304xx-32bit
Conflicts:	nvidia-x11-drv-173xx
Conflicts:	nvidia-x11-drv-173xx-32bit
Conflicts:	nvidia-x11-drv-96xx
Conflicts:	nvidia-x11-drv-96xx-32bit

# rpmforge
Conflicts:	dkms-nvidia
Conflicts:	dkms-nvidia-x11-drv
Conflicts:	dkms-nvidia-x11-drv-32bit

Conflicts:	xorg-x11-drv-nvidia
Conflicts:	xorg-x11-drv-nvidia-beta
Conflicts:	xorg-x11-drv-nvidia-legacy
Conflicts:	xorg-x11-drv-nvidia-71xx
Conflicts:	xorg-x11-drv-nvidia-96xx
Conflicts:	xorg-x11-drv-nvidia-173xx

%description
This package provides the proprietary NVIDIA OpenGL X11 display driver files.

%package 32bit
Summary:	Compatibility 32-bit files for the 64-bit Proprietary NVIDIA driver
Group:		User Interface/X Hardware Support
Requires:	%{name} = %{version}-%{release}
Requires(post):	/sbin/ldconfig

%description 32bit
Compatibility 32-bit files for the 64-bit Proprietary NVIDIA driver.

%prep
%setup -q -c -T

%ifarch i386
sh %{SOURCE0} --extract-only --target nvidiapkg
%endif

%ifarch x86_64
sh %{SOURCE1} --extract-only --target nvidiapkg
%endif

# Lets just take care of all the docs here rather than in install
pushd nvidiapkg
%{__mv} LICENSE NVIDIA_Changelog pkg-history.txt README.txt html/
popd
find nvidiapkg/html/ -type f | xargs chmod 0644

%build
# Nothing to build

%install
%{__rm} -rf $RPM_BUILD_ROOT

pushd nvidiapkg

# Install nvidia tools
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-bug-report.sh $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-cuda-mps-control $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-cuda-mps-server $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-debugdump $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-settings $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-smi $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-xconfig $RPM_BUILD_ROOT%{_bindir}/

# Install OpenCL Vendor file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/
%{__install} -p -m 0644 nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/nvidia.icd

# Install GL, tls and vdpau libs
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/vdpau/
%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialibdir}/tls/
%{__install} -p -m 0755 libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/
%{__install} -p -m 0755 libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvcuvid.so in 260.xx series driver
%{__install} -p -m 0755 libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-compiler.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-encode.so in 310.19 driver
%{__install} -p -m 0755 libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-fbc.so in 331.20 driver
%{__install} -p -m 0755 libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-glcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ifr.so in 325.15 driver
%{__install} -p -m 0755 libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ml.so in 270.xx series driver
%{__install} -p -m 0755 libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-opencl.so in 304.xx series driver
%{__install} -p -m 0755 libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libOpenCL.so.* $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 tls/*.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/tls/
# Added 64 bit libEGL and libGLES libs in 340.24 driver
%{__install} -p -m 0755 libEGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv1_CM.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv2.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-eglcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-glsi.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/

%ifarch x86_64
# Install 32bit compat GL, tls and vdpau libs
%{__mkdir_p} $RPM_BUILD_ROOT%{_prefix}/lib/vdpau/
%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialib32dir}/tls/
%{__install} -p -m 0755 32/libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_prefix}/lib/vdpau/
%{__install} -p -m 0755 32/libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
# Added libEGL and libGLES libs in 331.20 driver
%{__install} -p -m 0755 32/libEGL.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libGLESv1_CM.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libGLESv2.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvidia-compiler.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
# Added libnvidia-eglcore in 331.20 driver
%{__install} -p -m 0755 32/libnvidia-eglcore.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
# Added missing 32-bit libnvidia-fbc.so in 331.67 driver
%{__install} -p -m 0755 32/libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvidia-glcore.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
# Added libnvidia-glsi in 331.20 driver
%{__install} -p -m 0755 32/libnvidia-glsi.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/libOpenCL.so.* $RPM_BUILD_ROOT%{nvidialib32dir}/
%{__install} -p -m 0755 32/tls/*.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/tls/
%endif

# Install X driver and extension 
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/
%{__install} -p -m 0755 nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__install} -p -m 0755 libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/
%{__install} -p -m 0755 libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/

# Create the symlinks
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libcuda.so
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libcuda.so.1
%{__ln_s} libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGL.so.1
# Added libnvcuvid.so in 260.xx series driver
%{__ln_s} libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvcuvid.so
%{__ln_s} libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvcuvid.so.1
%{__ln_s} libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-cfg.so.1
# Added libnvidia-encode.so in 310.19 driver
%{__ln_s} libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-encode.so
%{__ln_s} libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-encode.so.1
# Added libnvidia-fbc.so in 331.20 driver
%{__ln_s} libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-fbc.so
%{__ln_s} libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-fbc.so.1
# Added libnvidia-ifr.so in 325.15 driver
%{__ln_s} libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-ifr.so
%{__ln_s} libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-ifr.so.1
# Added libnvidia-ml.so in 270.xx series driver
%{__ln_s} libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-ml.so
%{__ln_s} libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-ml.so.1
# Added libnvidia-opencl.so in 304.xx series driver
%{__ln_s} libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-opencl.so.1
%{__ln_s} libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{nvidialibdir}/libOpenCL.so
%{__ln_s} libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{nvidialibdir}/libOpenCL.so.1
%{__ln_s} libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglx.so
%{__ln_s} libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/libwfb.so
%{__ln_s} libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/libnvidia-wfb.so.1
%{__ln_s} libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_nvidia.so.1
# Added 64 bit libEGL and libGLES libs in 340.24 driver
%{__ln_s} libEGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libEGL.so.1
%{__ln_s} libGLESv1_CM.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv1_CM.so.1
%{__ln_s} libGLESv2.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv2.so.2

%ifarch x86_64
# Create the 32-bit symlinks
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libcuda.so
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libcuda.so.1
%{__ln_s} libEGL.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libEGL.so.1
%{__ln_s} libGLESv1_CM.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libGLESv1_CM.so.1
%{__ln_s} libGLESv2.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libGLESv2.so.2
%{__ln_s} libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libGL.so.1
%{__ln_s} libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvcuvid.so
%{__ln_s} libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvcuvid.so.1
%{__ln_s} libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-encode.so
%{__ln_s} libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-encode.so.1
%{__ln_s} libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-fbc.so
%{__ln_s} libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-fbc.so.1
%{__ln_s} libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-ifr.so
%{__ln_s} libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-ifr.so.1
%{__ln_s} libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-ml.so
%{__ln_s} libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-ml.so.1
%{__ln_s} libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialib32dir}/libnvidia-opencl.so.1
%{__ln_s} libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{nvidialib32dir}/libOpenCL.so
%{__ln_s} libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{nvidialib32dir}/libOpenCL.so.1
%{__ln_s} libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_prefix}/lib/vdpau/libvdpau_nvidia.so.1
%endif

# Install man pages
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1/
%{__install} -p -m 0644 nvidia-{cuda-mps-control,settings,smi,xconfig}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/

# Install pixmap for the desktop entry
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/pixmaps/
%{__install} -p -m 0644 nvidia-settings.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/

# Desktop entry for nvidia-settings
# Remove "__UTILS_PATH__/" before the Exec command name
# Replace "__PIXMAP_PATH__/" with the proper pixmaps path
%{__perl} -pi -e 's|(Exec=).*/(.*)|$1$2|g;
                  s|(Icon=).*/(.*)|$1%{_datadir}/pixmaps/$2|g' \
    nvidia-settings.desktop

%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install --vendor elrepo \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
    --add-category System \
    --add-category Application \
    --add-category GNOME \
    nvidia-settings.desktop

# Install application profiles
# added in 319.17
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/nvidia/
%{__install} -p -m 0644 nvidia-application-profiles-%{version}-rc $RPM_BUILD_ROOT%{_datadir}/nvidia/
# added in 340.24
%{__install} -p -m 0644 nvidia-application-profiles-%{version}-key-documentation $RPM_BUILD_ROOT%{_datadir}/nvidia/

# Install X configuration script
%{__mkdir_p} $RPM_BUILD_ROOT%{_sbindir}/
%{__install} -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/nvidia-config-display

# Install modprobe.d file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
%{__install} -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/nvidia.conf

# Install udev configuration file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/
%{__install} -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/60-nvidia.nodes

# Install alternate-install-present file
# This file tells the NVIDIA installer that a packaged version of the driver is already present on the system
%{__install} -p -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{nvidialibdir}/alternate-install-present

# Install ld.so.conf.d file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo %{nvidialibdir} > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%ifarch x86_64
echo %{nvidialib32dir} >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%endif

popd

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
if [ "$1" -eq "1" ]; then
    # If xorg.conf doesn't exist, create it
    [ ! -f %{_sysconfdir}/X11/xorg.conf ] && %{_bindir}/nvidia-xconfig &>/dev/null
    # Make sure we have a Files section in xorg.conf, otherwise create an empty one
    XORGCONF=/etc/X11/xorg.conf
    [ -w ${XORGCONF} ] && ! grep -q 'Section "Files"' ${XORGCONF} && \
      echo -e 'Section "Files"\nEndSection' >> ${XORGCONF}
    # Enable the proprietary nvidia driver
    %{_sbindir}/nvidia-config-display enable &>/dev/null
fi || :

/sbin/ldconfig

%post 32bit
/sbin/ldconfig

%preun
# Disable proprietary nvidia driver on uninstall
if [ "$1" -eq "0" ]; then
    test -f %{_sbindir}/nvidia-config-display && %{_sbindir}/nvidia-config-display disable &>/dev/null || :
fi

%postun
/sbin/ldconfig

%postun 32bit
/sbin/ldconfig

%triggerin -- xorg-x11-server-Xorg
# Enable the proprietary nvidia driver
# Required since xorg-x11-server-Xorg empties the "Files" section
test -f %{_sbindir}/nvidia-config-display && %{_sbindir}/nvidia-config-display enable &>/dev/null || :

%files
%defattr(-,root,root,-)
%doc nvidiapkg/html/*
%{_mandir}/man1/nvidia*.*
%{_datadir}/pixmaps/nvidia-settings.png
%{_datadir}/applications/*nvidia-settings.desktop
%{_datadir}/nvidia/nvidia-application-profiles-*
%{_bindir}/nvidia*
%{_sbindir}/nvidia-config-display
%config(noreplace) %{_sysconfdir}/modprobe.d/nvidia.conf
%config %{_sysconfdir}/ld.so.conf.d/nvidia.conf
%config %{_sysconfdir}/udev/makedev.d/60-nvidia.nodes
%{_sysconfdir}/OpenCL/vendors/nvidia.icd

# now the libs
%dir %{nvidialibdir}
%{nvidialibdir}/lib*
%{nvidialibdir}/alternate-install*
%dir %{nvidialibdir}/tls
%{nvidialibdir}/tls/lib*
%{_libdir}/vdpau/libvdpau_nvidia.*
%{_libdir}/xorg/modules/libwfb.so
%{_libdir}/xorg/modules/libnvidia-wfb.so.*
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%dir %{_libdir}/xorg/modules/extensions/nvidia
%{_libdir}/xorg/modules/extensions/nvidia/libglx.*

# 32-bit compatibility libs
%ifarch x86_64
%files 32bit
%defattr(-,root,root,-)
%dir %{nvidialib32dir}
%{nvidialib32dir}/lib*
%dir %{nvidialib32dir}/tls
%{nvidialib32dir}/tls/lib*
%{_prefix}/lib/vdpau/libvdpau_nvidia.*
%endif

%changelog
* Tue Dec 16 2014 Michael Lampe <mlampe0@googlemail.com> - 340.65-1.el5.ml
- Updated to version 340.65

* Fri Nov 07 2014 Michael Lampe <mlampe0@googlemail.com> - 340.58-1.el5.ml
- Updated to version 340.58

* Thu Oct 02 2014 Michael Lampe <mlampe0@googlemail.com> - 340.46-1.el5.ml
- Updated to version 340.46

* Wed Aug 13 2014 Michael Lampe <mlampe0@googlemail.com> - 340.32-1.el5.ml
- Updated to version 340.32

* Tue Jul 08 2014 Michael Lampe <mlampe0@googlemail.com> - 340.24-1.el5.ml
- Updated to version 340.24

* Mon Jul 07 2014 Michael Lampe <mlampe0@googlemail.com> - 331.89-1.el5.ml
- Updated to version 331.89

* Tue May 20 2014 Michael Lampe <mlampe0@googlemail.com> - 331.79-1.el5.ml
- Updated to version 331.79

* Tue May 06 2014 Michael Lampe <mlampe0@googlemail.com> - 331.67-2.el5.ml
- remove profile.d scriptlets
- remove libtool archives
- prune so links: only keep those needed/intended for linking a program
- remove vdpau from ldconfig file

* Mon May 05 2014 Michael Lampe <mlampe0@googlemail.com> - 331.67-1.el5.ml
- Forked off from elrepo
- Create all devices root:root 600
- Build nvidia-uvm.ko and piggy-back loading and device creation to nvidia.ko
- Use pam_console to hand over device to logged-in users

* Wed Apr 09 2014 Philip J Perry <phil@elrepo.org> - 331.67-1.el5.elrepo
- Updated to version 331.67
- Added missing libnvidia-fbc.so to the 32-bit compat package

* Wed Feb 19 2014 Philip J Perry <phil@elrepo.org> - 331.49-1.el5.elrepo
- Updated to version 331.49

* Sat Jan 18 2014 Philip J Perry <phil@elrepo.org> - 331.38-1.el5.elrepo
- Updated to version 331.38
- Adds support for Xorg 1.15

* Fri Nov 08 2013 Philip J Perry <phil@elrepo.org> - 331.20-1.el5.elrepo
- Updated to version 331.20
- Added libnvidia-fbc.so
- Removes libnvidia-vgxcfg.so
- Added libs specific to the 32-bit package

* Mon Aug 05 2013 Philip J Perry <phil@elrepo.org> - 325.15-1.el5.elrepo
- Updated to version 325.15
- Added libnvidia-ifr.so and libnvidia-vgxcfg.so
- Fix broken SONAME dependency chain on libGL.so
- Add conflicts with nvidia-x11-drv-304xx
- Added /usr/lib/nvidia/alternate-install-present
  [http://elrepo.org/bugs/view.php?id=398]

* Sun Jun 30 2013 Philip J Perry <phil@elrepo.org> - 319.32-1.el5.elrepo
- Updated to version 319.32

* Fri May 24 2013 Philip J Perry <phil@elrepo.org> - 319.23-1.el5.elrepo
- Updated to version 319.23

* Thu May 09 2013 Philip J Perry <phil@elrepo.org> - 319.17-1.el5.elrepo
- Updated to version 319.17
- Adds application profiles

* Thu Apr 04 2013 Philip J Perry <phil@elrepo.org> - 310.44-1.el5.elrepo
- Updated to version 310.44

* Sat Mar 09 2013 Philip J Perry <phil@elrepo.org> - 310.40-1.el5.elrepo
- Updated to version 310.40

* Wed Jan 23 2013 Philip J Perry <phil@elrepo.org> - 310.32-1.el5.elrepo
- Updated to version 310.32

* Tue Nov 20 2012 Philip J Perry <phil@elrepo.org> - 310.19-2.el5.elrepo
- Fix broken SONAME dependency chain

* Mon Nov 19 2012 Philip J Perry <phil@elrepo.org> - 310.19-1.el5.elrepo
- Updated to version 310.19
- Drops support for older 6xxx and 7xxx series cards
- Drops support for older AGP interface
- Drops support for XVideo Motion Compensation (XvMC)

* Sat Nov 10 2012 Philip J Perry <phil@elrepo.org> - 304.64-1.el5.elrepo
- Updated to version 304.64
- Install missing 32-bit libs

* Fri Oct 19 2012 Philip J Perry <phil@elrepo.org> - 304.60-1.el5.elrepo
- Updated to version 304.60

* Fri Sep 28 2012 Philip J Perry <phil@elrepo.org> - 304.51-1.el5.elrepo
- Updated to version 304.51
- Add missing lib and symlink for OpenCL [http://elrepo.org/bugs/view.php?id=304]

* Tue Aug 28 2012 Philip J Perry <phil@elrepo.org> - 304.43-1.el5.elrepo
- Updated to version 304.43

* Tue Aug 14 2012 Philip J Perry <phil@elrepo.org> - 304.37-1.el5.elrepo
- Updated to version 304.37
- Add nvidia-cuda-proxy-control, nvidia-cuda-proxy-server and associated manpage

* Wed Aug 08 2012 Philip J Perry <phil@elrepo.org> - 295.71-1.el5.elrepo
- Updated to version 295.71
- Fixes http://permalink.gmane.org/gmane.comp.security.full-disclosure/86747

* Tue Jun 19 2012 Philip J Perry <phil@elrepo.org> - 302.17-1.el5.elrepo
- Updated to version 302.17

* Sat Jun 16 2012 Philip J Perry <phil@elrepo.org> - 295.59-1.el5.elrepo
- Updated to version 295.59

* Thu May 17 2012 Philip J Perry <phil@elrepo.org> - 295.53-1.el5.elrepo
- Updated to version 295.53

* Fri May 04 2012 Philip J Perry <phil@elrepo.org> - 295.49-1.el5.elrepo
- Updated to version 295.49

* Wed Apr 11 2012 Philip J Perry <phil@elrepo.org> - 295.40-1.el5.elrepo
- Updated to version 295.40
- Fixes CVE-2012-0946

* Fri Mar 23 2012 Philip J Perry <phil@elrepo.org> - 295.33-1.el5.elrepo
- Updated to version 295.33

* Mon Feb 13 2012 Philip J Perry <phil@elrepo.org> - 295.20-1.el5.elrepo
- Updated to version 295.20
- Fix permissions on device file(s)

* Wed Nov 23 2011 Philip J Perry <phil@elrepo.org> - 290.10-1.el5.elrepo
- Updated to version 290.10

* Fri Oct 07 2011 Philip J Perry <phil@elrepo.org> - 285.05.09-1.el5.elrepo
- Updated to version 285.05.09
- Adds nvidia-debugdump

* Tue Aug 02 2011 Philip J Perry <phil@elrepo.org> - 280.13-1.el5.elrepo
- Updated to version 280.13

* Fri Jul 22 2011 Philip J Perry <phil@elrepo.org> - 275.21-1.el5.elrepo
- Updated to version 275.21

* Fri Jul 15 2011 Philip J Perry <phil@elrepo.org> - 275.19-1.el5.elrepo
- Updated to version 275.19

* Fri Jun 17 2011 Philip J Perry <phil@elrepo.org> - 275.09.07-1.el5.elrepo
- Updated to version 275.09.07

* Sat Apr 16 2011 Philip J Perry <phil@elrepo.org> - 270.41.03-1.el5.elrepo
- Updated to version 270.41.03 for release

* Fri Mar 25 2011 Philip J Perry <phil@elrepo.org>
- Updated to version 270.30 beta
- Adds libnvidia-ml library.
- Remove vdpau wrapper libs from package (libvdpau from EPEL provides these).
  Move vendor-specific libvdpau_nvidia.so libs to /usr/lib/vdpau.
  Update ldconf path to include /usr/lib/vdpau.
  [http://elrepo.org/bugs/view.php?id=123]

* Fri Jan 21 2011 Philip J Perry <phil@elrepo.org> - 260.19.36-1.el5.elrepo
- Updated to version 260.19.36
- Test for xorg.conf and create one if missing.

* Thu Dec 16 2010 Philip J Perry <phil@elrepo.org> - 260.19.29-1.el5.elrepo
- Updated to version 260.19.29

* Wed Nov 10 2010 Philip J Perry <phil@elrepo.org> - 260.19.21-1.el5.elrepo
- Updated to version 260.19.21

* Fri Oct 15 2010 Philip J Perry <phil@elrepo.org> - 260.19.12-1.el5.elrepo
- Updated to version 260.19.12

* Fri Sep 10 2010 Philip J Perry <phil@elrepo.org> - 260.19.04-1.el5.elrepo
- Updated to version 260.19.04, internal beta build.
- Adds libnvcuvid library.

* Tue Aug 31 2010 Philip J Perry <phil@elrepo.org> - 256.53-1.el5.elrepo
- Updated to version 256.53

* Sat Jul 30 2010 Philip J Perry <phil@elrepo.org> - 256.44-1.el5.elrepo
- Updated to version 256.44

* Sat Jun 19 2010 Philip J Perry <phil@elrepo.org> - 256.35-1.el5.elrepo
- Updated to version 256.35

* Sat Jun 12 2010 Philip J Perry <phil@elrepo.org> - 195.36.31-1.el5.elrepo
- Updated to version 195.36.31.

* Fri Apr 23 2010 Philip J Perry <phil@elrepo.org> - 195.36.24-1.el5.elrepo
- Updated to version 195.36.24.
- Run ldconfig on 32bit subpackages
  [http://elrepo.org/bugs/view.php?id=58]

* Sat Mar 20 2010 Philip J Perry <phil@elrepo.org> - 195.36.15-1.el5.elrepo
- Updated to version 195.36.15.
- Added OpenCL libraries.
- Added libnvidia-compiler runtime libs.

* Sun Feb 21 2010 Philip J Perry <phil@elrepo.org> - 190.53-1.el5.elrepo
- Updated to version 190.53.
- Fixed vdpau symlinks.
- Split 32-bit compatibility files into a sub-package on x86_64.

* Sun Nov 01 2009 Philip J Perry <phil@elrepo.org> - 190.42-1.el5.elrepo
- Updated to version 190.42.

* Sat Sep 12 2009 Akemi Yagi <toracat@elrepo.org> - 185.18.36-2.el5.elrepo
- To match the version of kmod-nvidia 185.18.36-2

* Sat Sep 12 2009 Akemi Yagi <toracat@elrepo.org> - 185.18.36-1.el5.elrepo
- Update to version 185.18.36.

* Mon Aug 10 2009 Philip J Perry <phil@elrepo.org> - 185.18.31-1.el5.elrepo
- Update to version 185.18.31.

* Tue Jul 14 2009 Philip J Perry <phil@elrepo.org> - 185.18.14-1.el5.elrepo
- Rebuilt for release.

* Mon Jul 13 2009 Akemi Yagi <toracat@elrepo.org>, Dag Wieers <dag@wieers.com>
- Fix udev device creation.

* Fri Jul 10 2009 Dag Wieers <dag@wieers.com>
- Fix Requires to nvidia-kmod.

* Fri Jul 10 2009 Philip J Perry <phil@elrepo.org>
- Fixed permissions on nvidia.(c)sh that cause Xorg to fail.
- Don't create debug or strip the package (NVIDIA doesn't).

* Mon Jul 06 2009 Philip J Perry <phil@elrepo.org>
- Complete rewrite of SPEC file
- Added nvidia.(c)sh, nvidia.modprobe
- Added nvidia-config-display to enable/disable driver
- Added Requires (pyxf86config) and BuildRequires (desktop-file-utils, perl)

* Wed Jun 10 2009 Alan Bartlett <ajb@elrepo.org>
- Updated the package to 185.18.14 version.

* Wed Jun 10 2009 Phil Perry <phil@elrepo.org>
- Added the Requires: /sbin/ldconfig line.
- Added the lines to create the /etc/ld.so.conf.d/nvidia.conf file.

* Wed May 27 2009 Philip J Perry <phil@elrepo.org>, Steve Tindall <s10dal@elrepo.org>
- Corrected the symlinks and their removal.

* Wed May 27 2009 Alan Bartlett <ajb@elrepo.org>
- Corrected typos in the pre & postun sections.

* Thu May 21 2009 Dag Wieers <dag@wieers.com>
- Adjusted the package name.

* Fri May 15 2009 Akemi Yagi <toracat@elrepo.org>
- Corrected the Requires: kmod-nvidia = %{?epoch:%{epoch}:}%{version}-%{release}

* Thu May 14 2009 Alan Bartlett <ajb@elrepo.org>
- Initial build of the x11-drv package.
