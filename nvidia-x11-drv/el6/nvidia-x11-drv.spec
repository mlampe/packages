# Define the Max Xorg version (ABI) that this driver release supports
# See README.txt, Chapter 2. Minimum Software Requirements or
# ftp://download.nvidia.com/XFree86/Linux-x86_64/375.26/README/minimumrequirements.html
%define		max_xorg_ver	1.20.99

%define		nvidialibdir	%{_libdir}/nvidia

%define		debug_package	%{nil}
%define		_use_internal_dependency_generator	0

Name:		nvidia-x11-drv
Version:	390.59
Release:	1%{?dist}
Group:		User Interface/X Hardware Support
License:	Distributable
Summary:	NVIDIA OpenGL X11 display driver files
URL:		http://www.nvidia.com/

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-build-%(%{__id_u} -n)
ExclusiveArch:	i686 x86_64

# Sources.
Source0:	ftp://download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
Source1:	ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run

NoSource: 0
NoSource: 1

Source2:	nvidia-config-display
Source3:	blacklist-nouveau.conf
Source4:	nvidia.nodes
Source5:	alternate-install-present
Source6:	nvidia.modprobe
Source7:	02nvidia
Source8:	nvidia_ck.tar.gz

# buildrequires for nvidia.ck
BuildRequires:  glib-devel
BuildRequires:  libacl-devel

# provides desktop-file-install
BuildRequires:	desktop-file-utils
BuildRequires:	perl

Requires:	xorg-x11-server-Xorg <= %{max_xorg_ver}
Requires:	nvidia-kmod = %{?epoch:%{epoch}:}%{version}
Requires(post):	nvidia-kmod = %{?epoch:%{epoch}:}%{version}

Requires(post):	/sbin/ldconfig

# for nvidia-config-display
Requires(post):	 pyxf86config
Requires(preun): pyxf86config

Requires(post):	 grubby
Requires(preun): grubby

%description
This package provides the proprietary NVIDIA OpenGL X11 display driver files.

%prep
%setup -a8 -q -c -T

%ifarch i686
sh %{SOURCE0} --extract-only --target nvidiapkg
%endif

%ifarch x86_64
sh %{SOURCE1} --extract-only --target nvidiapkg
%endif

# Lets just take care of all the docs here rather than during install
pushd nvidiapkg
%{__mv} LICENSE NVIDIA_Changelog pkg-history.txt README.txt html/
%{__mv} nvidia-persistenced-init.tar.bz2 html/
popd
find nvidiapkg/html/ -type f | xargs chmod 0644

%build
%{__make}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

pushd nvidiapkg

# Install nvidia tools
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-bug-report.sh $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-cuda-mps-control $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-cuda-mps-server $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-debugdump $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-persistenced $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-settings $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-smi $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-xconfig $RPM_BUILD_ROOT%{_bindir}/

# Install OpenCL Vendor file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/
%{__install} -p -m 0644 nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/nvidia.icd
# Install vulkan and EGL loaders
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/
%{__install} -p -m 0644 nvidia_icd.json.template $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/nvidia_icd.json
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d/
%{__install} -p -m 0644 10_nvidia.json $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
#%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/egl/egl_external_platform.d/
#%{__install} -p -m 0644 10_nvidia_wayland.json $RPM_BUILD_ROOT%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json

# Install GL, tls and vdpau libs
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/vdpau/
%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialibdir}/
#%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialibdir}/tls/
%{__install} -p -m 0755 libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libEGL_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libEGL.so.1.1.0 $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLdispatch.so.0 $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv1_CM_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv1_CM.so.1.2.0 $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv2_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv2.so.2.1.0 $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGL.so.1.7.0 $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLX.so.0 $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvcuvid.so in 260.xx series driver
%{__install} -p -m 0755 libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-compiler.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-eglcore.so in 340.24 driver
%{__install} -p -m 0755 libnvidia-eglcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-egl-wayland.so in 367.27 driver. Not supported on RHEL
# %{__install} -p -m 0755 libnvidia-egl-wayland.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-encode.so in 310.19 driver
%{__install} -p -m 0755 libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-fatbinaryloader.so in 361.28 driver
%{__install} -p -m 0755 libnvidia-fatbinaryloader.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-fbc.so in 331.20 driver
%{__install} -p -m 0755 libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-glcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-glsi.so in 340.24 driver
%{__install} -p -m 0755 libnvidia-glsi.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added in 346.35 driver
%{__install} -p -m 0755 libnvidia-gtk2.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ifr.so in 325.15 driver
%{__install} -p -m 0755 libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ml.so in 270.xx series driver
%{__install} -p -m 0755 libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-vgxcfg.so in 325.15 driver and removed in 331.20 driver
# %{__install} -p -m 0755 libnvidia-vgxcfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-opencl.so in 304.xx series driver
%{__install} -p -m 0755 libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ptxjitcompiler.so in 361.28 driver
%{__install} -p -m 0755 libnvidia-ptxjitcompiler.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
#%{__install} -p -m 0755 libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
#%{__install} -p -m 0755 tls/*.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/tls/
%{__install} -p -m 0755 tls/*.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
#%{__install} -p -m 0755 libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libOpenGL.so in 361.28 driver
%{__install} -p -m 0755 libOpenGL.so.0 $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/

# Install X driver and extension 
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/
%{__install} -p -m 0755 nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__install} -p -m 0755 libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/

# Create the symlinks
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libcuda.so
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libcuda.so.1
%{__ln_s} libEGL_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libEGL_nvidia.so.0
%{__ln_s} libEGL.so.1.1.0 $RPM_BUILD_ROOT%{nvidialibdir}/libEGL.so.1
%{__ln_s} libGLESv1_CM_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv1_CM_nvidia.so.1
%{__ln_s} libGLESv1_CM.so.1.2.0 $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv1_CM.so.1
%{__ln_s} libGLESv2_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv2_nvidia.so.2
%{__ln_s} libGLESv2.so.2.1.0 $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv2.so.2
%{__ln_s} libGL.so.1.7.0 $RPM_BUILD_ROOT%{nvidialibdir}/libGL.so.1
%{__ln_s} libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLX_nvidia.so.0
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
# Added libnvidia-vgxcfg.so in 325.15 driver and removed in 331.20 driver
# %{__ln_s} libnvidia-vgxcfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-vgxcfg.so
# %{__ln_s} libnvidia-vgxcfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-vgxcfg.so.1
# Added libnvidia-opencl.so in 304.xx series driver
%{__ln_s} libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-opencl.so.1
#%{__ln_s} libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{nvidialibdir}/libOpenCL.so
#%{__ln_s} libOpenCL.so.1.0.0 $RPM_BUILD_ROOT%{nvidialibdir}/libOpenCL.so.1
%{__ln_s} libOpenGL.so.0 $RPM_BUILD_ROOT%{nvidialibdir}/libOpenGL.so
%{__ln_s} libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglx.so
%{__ln_s} libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_nvidia.so.1

# Install man pages
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1/
%{__install} -p -m 0644 nvidia-{cuda-mps-control,persistenced,settings,smi,xconfig}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/

# Install pixmap for the desktop entry
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/pixmaps/
%{__install} -p -m 0644 nvidia-settings.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/

# Desktop entry for nvidia-settings
# GNOME: System > Administration
# KDE: Applications > Administration
# Remove "__UTILS_PATH__/" before the Exec command name
# Replace "__PIXMAP_PATH__/" with the proper pixmaps path
%{__perl} -pi -e 's|(Exec=).*/(.*)|$1$2|g;
                  s|(Icon=).*/(.*)|$1%{_datadir}/pixmaps/$2|g' \
    nvidia-settings.desktop

# GNOME requires category=System on RHEL6
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
    --add-category System \
    nvidia-settings.desktop

# Set vulkan icd file name
%{__perl} -pi -e 's|__NV_VK_ICD__|libGLX_nvidia.so.0|' \
    $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/nvidia_icd.json

# Install application profiles
# added in 319.17
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/nvidia/
%{__install} -p -m 0644 nvidia-application-profiles-%{version}-rc $RPM_BUILD_ROOT%{_datadir}/nvidia/
# added in 340.24
%{__install} -p -m 0644 nvidia-application-profiles-%{version}-key-documentation $RPM_BUILD_ROOT%{_datadir}/nvidia/

# Install X configuration script
%{__mkdir_p} $RPM_BUILD_ROOT%{_sbindir}/
%{__install} -p -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/nvidia-config-display

# Blacklist the nouveau driver
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
%{__install} -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/blacklist-nouveau.conf
# Install nvidia.modprobe
%{__install} -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/nvidia.conf

# Install udev configuration file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/
%{__install} -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/60-nvidia.nodes

# Override makedev rule
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/makedev.d/
%{__install} -p -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/makedev.d/

# Install alternate-install-present file
# This file tells the NVIDIA installer that a packaged version of the driver is already present on the system
%{__install} -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{nvidialibdir}/alternate-install-present

# Install ld.so.conf.d file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo %{nvidialibdir} > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
#echo %{_libdir}/vdpau >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf

# Install scriptlets to set GLX vendor name
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
echo "export __GLX_VENDOR_LIBRARY_NAME=nvidia" > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/nvidia.sh
echo "setenv __GLX_VENDOR_LIBRARY_NAME nvidia" > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/nvidia.csh

popd

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
if [ "$1" -eq "1" ]; then
    # Check if xorg.conf exists, if it does, backup and remove [BugID # 0000127]
    [ -f %{_sysconfdir}/X11/xorg.conf ] && \
      mv %{_sysconfdir}/X11/xorg.conf %{_sysconfdir}/X11/xorg.conf.elreposave &>/dev/null
    # xorg.conf now shouldn't exist so create it
    [ ! -f %{_sysconfdir}/X11/xorg.conf ] && %{_bindir}/nvidia-xconfig &>/dev/null
    # Make sure we have a Files section in xorg.conf, otherwise create an empty one
    XORGCONF=/etc/X11/xorg.conf
    [ -w ${XORGCONF} ] && ! grep -q 'Section "Files"' ${XORGCONF} && \
      echo -e 'Section "Files"\nEndSection' >> ${XORGCONF}
    # Enable nvidia driver when installing
    %{_sbindir}/nvidia-config-display enable &>/dev/null
    # Disable the nouveau driver
    if [[ -x /sbin/grubby && -e /boot/grub/grub.conf ]]; then
      # get installed kernels
      for KERNEL in $(rpm -q --qf '%{v}-%{r}.%{arch}\n' kernel); do
      VMLINUZ="/boot/vmlinuz-"$KERNEL
      # Check kABI compatibility
        for KABI in $(find /lib/modules -name nvidia.ko | cut -d / -f 4); do
          if [[ "$KERNEL" == "$KABI" && -e "$VMLINUZ" ]]; then
            /sbin/grubby --update-kernel="$VMLINUZ" \
              --args='nouveau.modeset=0 rdblacklist=nouveau' &>/dev/null
          fi
        done
      done
    fi
fi || :

/sbin/ldconfig

%preun
if [ "$1" -eq "0" ]; then
    # Clear grub option to disable nouveau for all RHEL6 kernels
    if [[ -x /sbin/grubby && -e /boot/grub/grub.conf ]]; then
      # get installed kernels
      for KERNEL in $(rpm -q --qf '%{v}-%{r}.%{arch}\n' kernel); do
        VMLINUZ="/boot/vmlinuz-"$KERNEL
        if [[ -e "$VMLINUZ" ]]; then
          /sbin/grubby --update-kernel="$VMLINUZ" \
            --remove-args='nouveau.modeset=0 rdblacklist=nouveau nomodeset' &>/dev/null
        fi
      done
    fi
    # Backup and remove xorg.conf
    [ -f %{_sysconfdir}/X11/xorg.conf ] && \
      mv %{_sysconfdir}/X11/xorg.conf %{_sysconfdir}/X11/xorg.conf.uninstalled-nvidia &>/dev/null
fi ||:

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc nvidiapkg/html/*
%{_mandir}/man1/nvidia*.*
%{_datadir}/pixmaps/nvidia-settings.png
%{_datadir}/applications/*nvidia-settings.desktop
#%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-application-profiles-*
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-debugdump
%{_bindir}/nvidia-persistenced
%{_bindir}/nvidia-settings
%{_bindir}/nvidia-smi
%{_bindir}/nvidia-xconfig
%{_sbindir}/nvidia-config-display
%{_prefix}/lib/ConsoleKit/run-seat.d/nvidia.ck
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist-nouveau.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/nvidia.conf
%config(noreplace) %{_sysconfdir}/makedev.d/02nvidia
%config %{_sysconfdir}/ld.so.conf.d/nvidia.conf
%config %{_sysconfdir}/udev/makedev.d/60-nvidia.nodes
%config %{_sysconfdir}/profile.d/nvidia.*sh
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%{_sysconfdir}/vulkan/icd.d/nvidia_icd.json

# now the libs
%dir %{nvidialibdir}
%{nvidialibdir}/lib*
%{nvidialibdir}/alternate-install*
#%dir %{nvidialibdir}/tls
#%{nvidialibdir}/tls/lib*
%{_libdir}/vdpau/libvdpau_nvidia.*
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%dir %{_libdir}/xorg/modules/extensions/nvidia
%{_libdir}/xorg/modules/extensions/nvidia/libglx.*

%changelog
* Thu May 17 2018 Michael Lampe <mlampe0@googlemail.com> - 390.59-1.el6.ml
- Updated to version 390.59

* Fri Mar 30 2018 Michael Lampe <mlampe0@googlemail.com> - 390.48-1.el6.ml
- Updated to version 390.48

* Tue Mar 13 2018 Michael Lampe <mlampe0@googlemail.com> - 390.42-1.el6.ml
- Updated to version 390.42

* Sat Feb  3 2018 Michael Lampe <mlampe0@googlemail.com> - 390.25-2.el6.ml
- add /dev/nvidia-uvm-tools

* Mon Jan 29 2018 Michael Lampe <mlampe0@googlemail.com> - 390.25-1.el6.ml
- Updated to version 390.25

* Sat Jan  6 2018 Michael Lampe <mlampe0@googlemail.com> - 384.111-1.el6.ml
- Updated to version 384.111

* Sat Nov  4 2017 Michael Lampe <mlampe0@googlemail.com> - 384.98-1.el6.ml
- Updated to version 384.98

* Wed Sep 27 2017 Michael Lampe <mlampe0@googlemail.com> - 384.90-1.el6.ml
- Updated to version 384.90

* Mon Aug 28 2017 Michael Lampe <mlampe0@googlemail.com> - 384.69-2.el6.ml
- Install only one libnvidia-tls.so

* Wed Aug 23 2017 Michael Lampe <mlampe0@googlemail.com> - 384.69-1.el6.ml
- Updated to version 384.69

* Thu Aug 17 2017 Michael Lampe <mlampe0@googlemail.com> - 384.59-3.el6.ml 
- Set vulkan icd file name

* Mon Aug 14 2017 Michael Lampe <mlampe0@googlemail.com> - 384.59-2.el6.ml
- Added scriptlets to set GLX vendor name
- Removed all links to libGLX_indirect.so.0

* Sun Aug 13 2017 Michael Lampe <mlampe0@googlemail.com> - 384.59-1.el6.ml
- Updated to version 384.59

* Sun Aug 13 2017 Michael Lampe <mlampe0@googlemail.com> - 375.82-1.el6.ml
- Updated to version 375.82

* Fri May  5 2017 Michael Lampe <mlampe0@googlemail.com> - 375.66-1.el6.ml
- Updated to version 375.66

* Thu Mar 23 2017 Michael Lampe <mlampe0@googlemail.com> - 375.39-1.el6.ml
- Resync with elrepo

* Wed Feb 22 2017 Philip J Perry <phil@elrepo.org> - 375.39-1
- Updated to version 375.39

* Thu Dec 15 2016 Philip J Perry <phil@elrepo.org> - 375.26-1
- Updated to version 375.26

* Sat Nov 19 2016 Philip J Perry <phil@elrepo.org> - 375.20-1
- Updated to version 375.20
- Adds support for Xorg 1.19 (Video Driver ABI 23)
- Enable GLVND
- Install nvidia-persistenced

* Tue Oct 11 2016 Philip J Perry <phil@elrepo.org> - 367.57-1
- Updated to version 367.57

* Sat Aug 27 2016 Philip J Perry <phil@elrepo.org> - 367.44-1
- Updated to version 367.44

* Sat Jul 16 2016 Philip J Perry <phil@elrepo.org> - 367.35-1
- Updated to version 367.35

* Tue Jun 14 2016 Philip J Perry <phil@elrepo.org> - 367.27-1
- Updated to version 367.27

* Wed May 25 2016 Philip J Perry <phil@elrepo.org> - 361.45.11-1
- Updated to version 361.45.11

* Thu Mar 31 2016 Philip J Perry <phil@elrepo.org> - 361.42-1
- Updated to version 361.42

* Tue Mar 01 2016 Philip J Perry <phil@elrepo.org> - 361.28-1
- Updated to version 361.28
- Adds GLVND support
- This package ships the legacy non-GLVND enabled LibGL.so by default

* Sun Jan 31 2016 Philip J Perry <phil@elrepo.org> - 352.79-1
- Updated to version 352.79

* Fri Nov 20 2015 Philip J Perry <phil@elrepo.org> - 352.63-1
- Updated to version 352.63
- Adds support for Xorg 1.18 (Video Driver ABI 20)

* Sat Oct 17 2015 Philip J Perry <phil@elrepo.org> - 352.55-1
- Updated to version 352.55

* Sat Aug 29 2015 Philip J Perry <phil@elrepo.org> - 352.41-1
- Updated to version 352.41
- Add CUDA provides

* Sat Aug 01 2015 Philip J Perry <phil@elrepo.org> - 352.30-1
- Updated to version 352.30
- Add requires for yum-plugin-nvidia

* Fri Jul 03 2015 Philip J Perry <phil@elrepo.org> - 352.21-3
- Add blacklist() provides.
- Revert modalias() provides.

* Wed Jul 01 2015 Philip J Perry <phil@elrepo.org> - 352.21-2
- Add modalias() provides.

* Wed Jun 17 2015 Philip J Perry <phil@elrepo.org> - 352.21-1
- Updated to version 352.21

* Wed Apr 08 2015 Philip J Perry <phil@elrepo.org> - 346.59-1
- Updated to version 346.59

* Wed Feb 25 2015 Philip J Perry <phil@elrepo.org> - 346.47-1
- Updated to version 346.47

* Sat Jan 17 2015 Philip J Perry <phil@elrepo.org> - 346.35-1
- Updated to version 346.35
- Drops support of older G8x, G9x, and GT2xx GPUs

* Fri Dec 12 2014 Philip J Perry <phil@elrepo.org> - 340.65-1.el6.elrepo
- Updated to version 340.65
- Adds support for Xorg 1.17 (Video Driver ABI 19)

* Thu Nov 06 2014 Philip J Perry <phil@elrepo.org> - 340.58-1.el6.elrepo
- Updated to version 340.58

* Sat Oct 04 2014 Philip J Perry <phil@elrepo.org> - 340.46-1.el6.elrepo
- Updated to version 340.46

* Sat Aug 16 2014 Philip J Perry <phil@elrepo.org> - 340.32-1.el6.elrepo
- Updated to version 340.32

* Wed Jul 09 2014 Philip J Perry <phil@elrepo.org> - 340.24-1.el6.elrepo
- Updated to version 340.24
- Adds support for Xorg 1.16

* Sat Jul 05 2014 Philip J Perry <phil@elrepo.org> - 331.89-1.el6.elrepo
- Updated to version 331.89

* Wed May 21 2014 Philip J Perry <phil@elrepo.org> - 331.79-1.el6.elrepo
- Updated to version 331.79

* Sat May 03 2014 Philip J Perry <phil@elrepo.org> - 331.67-3.el6.elrepo
- Add nvidia-modprobe
- Comment out options in /etc/modprobe.d/nvidia.conf

* Fri May 02 2014 Philip J Perry <phil@elrepo.org> - 331.67-2.el6.elrepo
- Add support for the nvidia-uvm module required for CUDA

* Wed Apr 09 2014 Philip J Perry <phil@elrepo.org> - 331.67-1.el6.elrepo
- Updated to version 331.67
- Added missing libnvidia-fbc.so to the 32-bit compat package

* Wed Feb 19 2014 Philip J Perry <phil@elrepo.org> - 331.49-1.el6.elrepo
- Updated to version 331.49

* Sat Jan 18 2014 Philip J Perry <phil@elrepo.org> - 331.38-1.el6.elrepo
- Updated to version 331.38
- Adds support for Xorg 1.15

* Fri Nov 08 2013 Philip J Perry <phil@elrepo.org> - 331.20-1.el6.elrepo
- Updated to version 331.20
- Added libnvidia-fbc.so
- Removes libnvidia-vgxcfg.so
- Added libs specific to the 32-bit package
- Add requires for max Xorg version

* Mon Aug 05 2013 Philip J Perry <phil@elrepo.org> - 325.15-1.el6.elrepo
- Updated to version 325.15
- Added libnvidia-ifr.so and libnvidia-vgxcfg.so
- Fix broken SONAME dependency chain on libGL.so
- Add conflicts with nvidia-x11-drv-304xx
- Added /usr/lib/nvidia/alternate-install-present
  [http://elrepo.org/bugs/view.php?id=398]

* Sun Jun 30 2013 Philip J Perry <phil@elrepo.org> - 319.32-1.el6.elrepo
- Updated to version 319.32

* Fri May 24 2013 Philip J Perry <phil@elrepo.org> - 319.23-1.el6.elrepo
- Updated to version 319.23

* Thu May 09 2013 Philip J Perry <phil@elrepo.org> - 319.17-1.el6.elrepo
- Updated to version 319.17
- Adds application profiles

* Thu Apr 04 2013 Philip J Perry <phil@elrepo.org> - 310.44-1.el6.elrepo
- Updated to version 310.44

* Sat Mar 09 2013 Philip J Perry <phil@elrepo.org> - 310.40-1.el6.elrepo
- Updated to version 310.40

* Wed Jan 23 2013 Philip J Perry <phil@elrepo.org> - 310.32-1.el6.elrepo
- Updated to version 310.32

* Tue Nov 20 2012 Philip J Perry <phil@elrepo.org> - 310.19-2.el6.elrepo
- Fix broken SONAME dependency chain

* Mon Nov 19 2012 Philip J Perry <phil@elrepo.org> - 310.19-1.el6.elrepo
- Updated to version 310.19
- Drops support for older 6xxx and 7xxx series cards
- Drops support for older AGP interface
- Drops support for XVideo Motion Compensation (XvMC)

* Sat Nov 10 2012 Philip J Perry <phil@elrepo.org> - 304.64-1.el6.elrepo
- Updated to version 304.64
- Replace missing libnvidia-tls.so removed in 260.19.21
  [http://elrepo.org/bugs/view.php?id=299]
- Install missing 32-bit libs

* Fri Oct 19 2012 Philip J Perry <phil@elrepo.org> - 304.60-1.el6.elrepo
- Updated to version 304.60

* Fri Sep 28 2012 Philip J Perry <phil@elrepo.org> - 304.51-1.el6.elrepo
- Updated to version 304.51
- Add missing lib and symlink for OpenCL [http://elrepo.org/bugs/view.php?id=304]

* Tue Aug 28 2012 Philip J Perry <phil@elrepo.org> - 304.43-1.el6.elrepo
- Updated to version 304.43

* Tue Aug 14 2012 Philip J Perry <phil@elrepo.org> - 304.37-1.el6.elrepo
- Updated to version 304.37
- Add nvidia-cuda-proxy-control, nvidia-cuda-proxy-server and associated manpage

* Wed Aug 08 2012 Philip J Perry <phil@elrepo.org> - 295.71-1.el5.elrepo
- Updated to version 295.71
- Fixes http://permalink.gmane.org/gmane.comp.security.full-disclosure/86747

* Tue Jun 19 2012 Philip J Perry <phil@elrepo.org> - 302.17-1.el6.elrepo
- Updated to version 302.17

* Sat Jun 16 2012 Philip J Perry <phil@elrepo.org> - 295.59-1.el6.elrepo
- Updated to version 295.59

* Thu May 17 2012 Philip J Perry <phil@elrepo.org> - 295.53-1.el6.elrepo
- Updated to version 295.53

* Fri May 04 2012 Philip J Perry <phil@elrepo.org> - 295.49-1.el6.elrepo
- Updated to version 295.49

* Wed Apr 11 2012 Philip J Perry <phil@elrepo.org> - 295.40-1.el6.elrepo
- Updated to version 295.40
- Fixes CVE-2012-0946

* Fri Mar 23 2012 Philip J Perry <phil@elrepo.org> - 295.33-1.el6.elrepo
- Updated to version 295.33

* Mon Feb 13 2012 Philip J Perry <phil@elrepo.org> - 295.20-1.el6.elrepo
- Updated to version 295.20

* Wed Nov 23 2011 Philip J Perry <phil@elrepo.org> - 290.10-1.el6.elrepo
- Updated to version 290.10

* Fri Oct 07 2011 Philip J Perry <phil@elrepo.org> - 285.05.09-1.el6.elrepo
- Updated to version 285.05.09
- Fix script to disable the nouveau driver
- Adds nvidia-debugdump

* Sun Aug 28 2011 Philip J Perry <phil@elrepo.org>
- Update script to disable the nouveau driver
  [http://elrepo.org/bugs/view.php?id=176]

* Tue Aug 02 2011 Philip J Perry <phil@elrepo.org> - 280.13-1.el6.elrepo
- Updated to version 280.13

* Fri Jul 22 2011 Philip J Perry <phil@elrepo.org> - 275.21-1.el6.elrepo
- Updated to version 275.21

* Fri Jul 15 2011 Philip J Perry <phil@elrepo.org> - 275.19-1.el6.elrepo
- Updated to version 275.19

* Fri Jun 17 2011 Philip J Perry <phil@elrepo.org> - 275.09.07-1.el6.elrepo
- Updated to version 275.09.07

* Sat Apr 16 2011 Philip J Perry <phil@elrepo.org> - 270.41.03-1.el6.elrepo
- Updated to version 270.41.03 for release
- Don't bother running 'nvidia-config-display disable' on uninstall
- Remove existing /etc/x11/xorg.conf during first install
  [http://elrepo.org/bugs/view.php?id=127]

* Fri Mar 25 2011 Philip J Perry <phil@elrepo.org>
- Updated to version 270.30 beta
- Adds libnvidia-ml library.
- Remove vdpau wrapper libs from package (libvdpau from EPEL provides these).
  Move vendor-specific libvdpau_nvidia.so libs to /usr/lib/vdpau.
  Update ldconf path to include /usr/lib/vdpau.
  [http://elrepo.org/bugs/view.php?id=123]

* Wed Mar 09 2011 Philip J Perry <phil@elrepo.org> - 260.19.44-1.el6.elrepo
- Updated to version 260.19.44

* Fri Jan 21 2011 Philip J Perry <phil@elrepo.org> - 260.19.36-1.el6.elrepo
- Updated to version 260.19.36

* Fri Dec 17 2010 Philip J Perry <phil@elrepo.org> - 260.19.29-1.el6.elrepo
- Updated to version 260.19.29

* Sun Nov 28 2010 Philip J Perry <phil@elrepo.org> - 260.19.21-1.el6.elrepo
- Rebuilt for release.

* Sun Nov 28 2010 Philip J Perry <phil@elrepo.org> - 260.19.21-0.4.el6.elrepo
- Remove libnvidia-wfb.so
- Remove additional libnvidia-tls.so
- Tidy up desktop entry for nvidia-settings
  GNOME: System > Administration
  KDE: Applications > Administration

* Sun Nov 21 2010 Philip J Perry <phil@elrepo.org> - 260.19.21-0.3.el6.elrepo
- Rebuilt for testing release.

* Sun Nov 21 2010 Philip J Perry <phil@elrepo.org> - 260.19.21-0.2.el6.elrepo
- Fix udev device creation.

* Sat Nov 20 2010 Philip J Perry <phil@elrepo.org> - 260.19.21-0.1.el6.elrepo
- Initial build for RHEL6 GA release.

* Fri Apr 30 2010 Philip J Perry <phil@elrepo.org> - - 195.36.24-0.1.el6.elrepo
- Initial build for RHEL6beta1
