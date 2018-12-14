# Define the Max Xorg version (ABI) that this driver release supports
%global		max_xorg_ver	1.20.99

%global		nvidialibdir	%{_libdir}/nvidia

%global		debug_package	%{nil}

%filter_from_provides /lib.*GL\..*/d; /.*_nvidia.*/d; /libnvidia-[a-c].*/d; /libnvidia-egl.*/d; /libnvidia-fat.*/d; /libnvidia-g.*/d; /libnvidia-[o-z].*/d; /nvidia_drv.*/d; /libglx.*/d
%filter_from_requires /lib.*GL\..*/d; /.*_nvidia.*/d; /libnvidia-[a-c].*/d; /libnvidia-egl.*/d; /libnvidia-fat.*/d; /libnvidia-g.*/d; /libnvidia-[o-z].*/d; /nvidia_drv.*/d; /libglx.*/d
%filter_setup

Name:		nvidia-x11-drv-340xx
Version:	340.107
Release:	1%{?dist}
Group:		User Interface/X Hardware Support
License:	Distributable
Summary:	NVIDIA OpenGL X11 display driver files
URL:		http://www.nvidia.com/

ExclusiveArch:	x86_64

# Sources.
Source0:	https://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
NoSource: 0

Source1:	nvidia-xorg.conf
Source2:	99-nvidia.conf
Source3:	nvidia.ld.so.conf

# for desktop-file-install
BuildRequires:	desktop-file-utils
BuildRequires:	perl

Requires:	perl
Requires:	mesa-filesystem
Requires:	opencl-filesystem
Requires:	xorg-x11-server-Xorg <= %{max_xorg_ver}
Requires:	nvidia-340xx-kmod = %{?epoch:%{epoch}:}%{version}
Requires(post):	nvidia-340xx-kmod = %{?epoch:%{epoch}:}%{version}

Requires(post):	/sbin/ldconfig

Requires(post):	 dracut

Requires(post):	 grubby
Requires(preun): grubby

%description
This package provides the proprietary NVIDIA OpenGL X11 display driver files.

%prep
%setup -q -c -T
sh %{SOURCE0} --extract-only --target nvidiapkg

# Lets just take care of all the docs here rather than during install
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
%{__install} -p -m 0755 nvidia-modprobe $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-settings $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-smi $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-xconfig $RPM_BUILD_ROOT%{_bindir}/

# Install OpenCL Vendor file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/
%{__install} -p -m 0644 nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/nvidia.icd

# Install GL, tls and vdpau libs
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/vdpau/
%{__mkdir_p} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/
%{__install} -p -m 0755 libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added in 340.24 driver
%{__install} -p -m 0755 libEGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv1_CM.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGLESv2.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvcuvid.so in 260.xx series driver
%{__install} -p -m 0755 libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-compiler.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-eglcore.so in 340.24 driver
%{__install} -p -m 0755 libnvidia-eglcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-encode.so in 310.19 driver
%{__install} -p -m 0755 libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-fbc.so in 331.20 driver
%{__install} -p -m 0755 libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 libnvidia-glcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-glsi.so in 340.24 driver
%{__install} -p -m 0755 libnvidia-glsi.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ifr.so in 325.15 driver
%{__install} -p -m 0755 libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-ml.so in 270.xx series driver
%{__install} -p -m 0755 libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
# Added libnvidia-opencl.so in 304.xx series driver
%{__install} -p -m 0755 libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/
%{__install} -p -m 0755 tls/libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/

# Install X driver and extension 
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/
%{__install} -p -m 0755 nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__install} -p -m 0755 libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglx.so

# Create the symlinks
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libcuda.so
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libcuda.so.1
%{__ln_s} libEGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libEGL.so.1
%{__ln_s} libGLESv1_CM.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv1_CM.so.1
%{__ln_s} libGLESv2.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLESv2.so.2
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
%{__ln_s} libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_nvidia.so.1

# Install man pages
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1/
%{__install} -p -m 0644 nvidia-{cuda-mps-control,modprobe,settings,smi,xconfig}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/

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

# Install the Xorg conf files
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/X11/
%{__install} -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/nvidia-xorg.conf
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/
%{__install} -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/99-nvidia.conf
# Install ld.so.conf.d file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
%{__install} -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf

popd

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
if [ "$1" -eq "1" ]; then # new install
    # Check if xorg.conf exists, if it does, backup and remove [BugID # 0000127]
    [ -f %{_sysconfdir}/X11/xorg.conf ] && \
      mv %{_sysconfdir}/X11/xorg.conf %{_sysconfdir}/X11/pre-nvidia.xorg.conf &>/dev/null
    # xorg.conf now shouldn't exist so copy new one
    [ ! -f %{_sysconfdir}/X11/xorg.conf ] && \
      cp -p %{_sysconfdir}/X11/nvidia-xorg.conf %{_sysconfdir}/X11/xorg.conf &>/dev/null
    # Disable the nouveau driver
    [ -f %{_sysconfdir}/default/grub ] && \
      %{__perl} -pi -e 's|(GRUB_CMDLINE_LINUX=".*)"|$1 nouveau\.modeset=0 rd\.driver\.blacklist=nouveau plymouth\.ignore-udev"|g' \
        %{_sysconfdir}/default/grub
    if [ -x /usr/sbin/grubby ]; then
      # get installed kernels
      for KERNEL in $(rpm -q --qf '%{v}-%{r}.%{arch}\n' kernel); do
      VMLINUZ="/boot/vmlinuz-"$KERNEL
      # Check kABI compatibility
        for KABI in $(find /lib/modules -name nvidia.ko | cut -d / -f 4); do
          if [[ "$KERNEL" == "$KABI" && -e "$VMLINUZ" ]]; then
            /usr/bin/dracut --add-drivers nvidia -f /boot/initramfs-$KERNEL.img $KERNEL
            /usr/sbin/grubby --update-kernel="$VMLINUZ" \
              --args='nouveau.modeset=0 rd.driver.blacklist=nouveau plymouth.ignore-udev' &>/dev/null
          fi
        done
      done
    fi
fi || :

/sbin/ldconfig

%preun
if [ "$1" -eq "0" ]; then # uninstall
    # Backup and remove xorg.conf
    [ -f %{_sysconfdir}/X11/xorg.conf ] && \
      mv %{_sysconfdir}/X11/xorg.conf %{_sysconfdir}/X11/post-nvidia.xorg.conf.elreposave &>/dev/null
    # Clear grub option to disable nouveau for all RHEL7 kernels
    if [ -f %{_sysconfdir}/default/grub ]; then
      %{__perl} -pi -e 's|(GRUB_CMDLINE_LINUX=.*) nouveau\.modeset=0|$1|g' %{_sysconfdir}/default/grub
      %{__perl} -pi -e 's|(GRUB_CMDLINE_LINUX=.*) rd\.driver\.blacklist=nouveau|$1|g' %{_sysconfdir}/default/grub
      %{__perl} -pi -e 's|(GRUB_CMDLINE_LINUX=.*) plymouth\.ignore-udev|$1|g' %{_sysconfdir}/default/grub
    fi
    if [ -x /usr/sbin/grubby ]; then
      # get installed kernels
      for KERNEL in $(rpm -q --qf '%{v}-%{r}.%{arch}\n' kernel); do
        VMLINUZ="/boot/vmlinuz-"$KERNEL
        if [[ -e "$VMLINUZ" ]]; then
          /usr/sbin/grubby --update-kernel="$VMLINUZ" \
            --remove-args='nouveau.modeset=0 rd.driver.blacklist=nouveau plymouth.ignore-udev' &>/dev/null
        fi
      done
    fi
fi ||:

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc nvidiapkg/html/*
%{_mandir}/man1/nvidia*.*
%{_datadir}/pixmaps/nvidia-settings.png
%{_datadir}/applications/nvidia-settings.desktop
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-application-profiles-*
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-debugdump
%attr(4755, root, root) %{_bindir}/nvidia-modprobe
%{_bindir}/nvidia-settings
%{_bindir}/nvidia-smi
%{_bindir}/nvidia-xconfig
%config %{_sysconfdir}/X11/nvidia-xorg.conf
%config %{_sysconfdir}/X11/xorg.conf.d/99-nvidia.conf
%config %{_sysconfdir}/ld.so.conf.d/nvidia.conf
%{_sysconfdir}/OpenCL/vendors/nvidia.icd

# now the libs
%dir %{nvidialibdir}
%{nvidialibdir}/lib*
%{_libdir}/vdpau/libvdpau_nvidia.*
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%dir %{_libdir}/xorg/modules/extensions/nvidia
%{_libdir}/xorg/modules/extensions/nvidia/libglx.so

%changelog
* Thu Jun 07 2018 Michael Lampe <mlampe0@googlemail.com> - 340.107-1
- Updated to version 340.107

* Sun Feb 25 2018 Michael Lampe <mlampe0@googlemail.com> - 340.106-2
- Resynced with elrepo
