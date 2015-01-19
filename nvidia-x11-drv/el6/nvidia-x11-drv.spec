# Define the Max Xorg version (ABI) that this driver release supports
# See README.txt, Chapter 2. Minimum Software Requirements or
# ftp://download.nvidia.com/XFree86/Linux-x86_64/325.15/README/minimumrequirements.html
%define		max_xorg_ver	1.16.99

%define		nvidialibdir	%{_libdir}/nvidia
%define		nvidialib32dir	%{_prefix}/lib/nvidia

%define		debug_package	%{nil}

Name:		nvidia-x11-drv
Version:	346.35
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
BuildRequires:	glib-devel
BuildRequires:	libacl-devel

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
# Added libnvidia-gtk2.so in 346.35 driver
%{__install} -p -m 0755 libnvidia-gtk2.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/

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

# Install alternate-install-present file
# This file tells the NVIDIA installer that a packaged version of the driver is already present on the system
%{__install} -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{nvidialibdir}/alternate-install-present

# Install ld.so.conf.d file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo %{nvidialibdir} > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%ifarch x86_64
echo %{nvidialib32dir} >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%endif

popd

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
# Warn on libglamoregl
if [ -e /usr/share/X11/xorg.conf.d/glamor.conf ]; then
    echo "WARNING: libglamoregl conflicts with NVIDIA drivers"
    echo "         Disable glamoregl or uninstall xorg-x11-glamor"
    echo "         See: http://elrepo.org/tiki/kmod-nvidia (Known Issues) for more information"
fi

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

%post 32bit
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

%postun 32bit
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc nvidiapkg/html/*
%{_mandir}/man1/nvidia*.*
%{_datadir}/pixmaps/nvidia-settings.png
%{_datadir}/applications/*nvidia-settings.desktop
%{_datadir}/nvidia/nvidia-application-profiles-*
%{_bindir}/nvidia*
%{_sbindir}/nvidia-config-display
%{_prefix}/lib/ConsoleKit/run-seat.d/nvidia.ck
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist-nouveau.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/nvidia.conf
%config(noreplace) %{_sysconfdir}/makedev.d/02nvidia
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
* Mon Jan 19 2015 Michael Lampe <mlampe0@googlemail.com> - 346.35-1.el6.ml
- Update to 346.35

* Tue Dec 16 2014 Michael Lampe <mlampe0@googlemail.com> - 340.65-1.el6.ml
- Updated to 340.65

* Fri Nov 07 2014 Michael Lampe <mlampe0@googlemail.com> - 340.58-1.el6.ml
- Updated to 340.58

* Thu Oct 02 2014 Michael Lampe <mlampe0@googlemail.com> - 340.46-1.el6.ml
- Updated to 340.46

* Thu Aug 14 2014 Michael Lampe <mlampe0@googlemail.com> - 340.32-1.el6.ml
- Updated to 340.32

* Wed Jul 09 2014 Michael Lampe <mlampe0@googlemail.com> - 340.24-1.el6.ml
- Updated to 340.24

* Tue Jul 08 2014 Michael Lampe <mlampe0@googlemail.com> - 331.89-1.el6.ml
- Updated to 331.89

* Tue May 20 2014 Michael Lampe <mlampe0@googlemail.com> - 331.79-1.el6.ml
- Updated to 331.79

* Tue May 06 2014 Michael Lampe <mlampe0@googlemail.com> - 331.67-2.el6.ml
- remove libtool archives
- prune so links: only keep those needed/intended for linking a program
- remove vdpau from ldconfig file

* Mon May 05 2014 Michael Lampe <mlampe0@googlemail.com> - 331.67-1.el6.ml
- Forked off from elrepo
- Create all devices root:video 660
- Build nvidia-uvm.ko and piggy-back loading and device creation to nvidia.ko
- Use a ConsoleKit helper to add ACLs for logged-in users

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
