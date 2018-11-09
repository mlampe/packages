# Define the Max Xorg version (ABI) that this driver release supports
%define		max_xorg_ver	1.20.99

%define		nvidialibdir	%{_libdir}/nvidia

%define		debug_package	%{nil}
%define		_use_internal_dependency_generator	0

Name:		nvidia-x11-drv
Version:	410.73
Release:	2%{?dist}
Group:		User Interface/X Hardware Support
License:	Distributable
Summary:	NVIDIA OpenGL X11 display driver files
URL:		http://www.nvidia.com/

ExclusiveArch:	x86_64

# Sources.
Source1:	ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run

NoSource: 1

Source2:	nvidia-config-display
Source3:	blacklist-nouveau.conf
Source4:	nvidia.nodes
Source6:	nvidia.modprobe
Source7:	02nvidia
Source8:	nvidia_ck.tar.gz

# buildrequires for nvidia.ck
BuildRequires:  glib-devel
BuildRequires:  libacl-devel

# for desktop-file-install
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

sh %{SOURCE1} --extract-only --target nvidiapkg

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
# Install EGL Vendor file
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d/
%{__install} -p -m 0644 10_nvidia.json $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json

# Install GL, tls and vdpau libs
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/vdpau/
%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialibdir}/
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
%{__install} -p -m 0755 libOpenGL.so.0 $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvcuvid.so in 260.xx series driver
%{__install} -p -m 0755 libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-cbl.so in 410.57 beta driver
%{__install} -p -m 0755 libnvidia-cbl.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-compiler.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-eglcore.so in 340.24 driver
%{__install} -p -m 0755 libnvidia-eglcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
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
# Added libnvidia-opencl.so in 304.xx series driver
%{__install} -p -m 0755 libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ptxjitcompiler.so in 361.28 driver
%{__install} -p -m 0755 libnvidia-ptxjitcompiler.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-rtcore.so in 410.57 beta drivers
%{__install} -p -m 0755 libnvidia-rtcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvoptix.so in 410.57 beta drivers
%{__install} -p -m 0755 libnvoptix.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 tls/*.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/

# Install X driver and extension 
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/
%{__install} -p -m 0755 nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__install} -p -m 0755 libglxserver_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so

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
%{__ln_s} libGLX.so.0 $RPM_BUILD_ROOT%{nvidialibdir}/libGLX.so
%{__ln_s} libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLX_nvidia.so.0
%{__ln_s} libOpenGL.so.0 $RPM_BUILD_ROOT%{nvidialibdir}/libOpenGL.so
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
%{__ln_s} libnvidia-ptxjitcompiler.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-ptxjitcompiler.so.1
# Added libnvoptix.so in 410.57 beta drivers
%{__ln_s} libnvoptix.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvoptix.so.1
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

# Install ld.so.conf.d file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo %{nvidialibdir} > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf

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
      mv %{_sysconfdir}/X11/xorg.conf %{_sysconfdir}/X11/xorg.conf.before-nvidia &>/dev/null
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
%{_datadir}/applications/nvidia-settings.desktop
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

# now the libs
%dir %{nvidialibdir}
%{nvidialibdir}/lib*
%{_libdir}/vdpau/libvdpau_nvidia.*
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so

%changelog
* Fri Nov  9 2018 Michael Lampe <mlampe0@googlemail.com> - 410.73-2.el6.ml
- Package new libs from 410 series

* Fri Oct 26 2018 Michael Lampe <mlampe0@googlemail.com> - 410.73-1.el6.ml
- Updated to 410.73

* Wed Oct 17 2018 Michael Lampe <mlampe0@googlemail.com> - 410.66-1.el6.ml
- Updated to 410.66

* Tue Aug 21 2018 Michael Lampe <mlampe0@googlemail.com> - 396.54-1.el6.ml
- Updated to version 396.54

* Sat Aug  4 2018 Michael Lampe <mlampe0@googlemail.com> - 396.51-1.el6.ml
- Updated to version 396.51

* Thu Jul 19 2018 Michael Lampe <mlampe0@googlemail.com> - 396.45-1.el6.ml
- Updated to version 396.45

* Tue Jul 17 2018 Michael Lampe <mlampe0@googlemail.com> - 390.77-1.el6.ml
- Updated to version 390.77

* Wed Jun  6 2018 Michael Lampe <mlampe0@googlemail.com> - 390.67-1.el6.ml
- Updated to version 390.67

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
- Resynced with elrepo
