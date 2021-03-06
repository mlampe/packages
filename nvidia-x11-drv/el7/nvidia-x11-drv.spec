# Define the Max Xorg version (ABI) that this driver release supports
%global		max_xorg_ver	1.20.99

%global		debug_package	%{nil}

%filter_from_provides /.*_nvidia.*/d; /libnvidia-[a-c].*/d; /libnvidia-egl.*/d; /libnvidia-fat.*/d; /libnvidia-g.*/d; /libnvidia-ope.*/d; /libnvidia-[p-z].*/d; /libnvoptix.*/d; /nvidia_drv.*/d
%filter_from_requires /.*_nvidia.*/d; /libnvidia-[a-c].*/d; /libnvidia-egl.*/d; /libnvidia-fat.*/d; /libnvidia-g.*/d; /libnvidia-ope.*/d; /libnvidia-[p-z].*/d; /libnvoptix.*/d; /nvidia_drv.*/d
%filter_setup

Name:		nvidia-x11-drv
Version:	460.84
Release:	1%{?dist}
Group:		User Interface/X Hardware Support
License:	Distributable
Summary:	NVIDIA OpenGL X11 display driver files
URL:		http://www.nvidia.com/

ExclusiveArch:	x86_64

# Sources.
Source0:	http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
NoSource: 0

Source1:	nvidia-xorg.conf

# for desktop-file-install
BuildRequires:	desktop-file-utils
BuildRequires:	perl

Requires:	perl
Requires:	libglvnd-egl
Requires:	mesa-filesystem
Requires:	opencl-filesystem
Requires:	vulkan-filesystem
Requires:	xorg-x11-server-Xorg <= %{max_xorg_ver}
Requires:	nvidia-kmod = %{?epoch:%{epoch}:}%{version}
Requires(post):	nvidia-kmod = %{?epoch:%{epoch}:}%{version}

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
%{__mv} nvidia-persistenced-init.tar.bz2 html/
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
%{__install} -p -m 0755 nvidia-persistenced $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-settings $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-smi $RPM_BUILD_ROOT%{_bindir}/
%{__install} -p -m 0755 nvidia-xconfig $RPM_BUILD_ROOT%{_bindir}/

# Install OpenCL Vendor file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/
%{__install} -p -m 0644 nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors/nvidia.icd
# Install vulkan and EGL loaders
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/vulkan/icd.d/
%{__install} -p -m 0644 nvidia_icd.json $RPM_BUILD_ROOT%{_datadir}/vulkan/icd.d/nvidia_icd.json
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d/
%{__install} -p -m 0644 10_nvidia.json $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json

# Install GL, tls and vdpau libs
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/vdpau/
%{__install} -p -m 0755 libcuda.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libEGL_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libGLESv1_CM_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libGLESv2_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvcuvid.so in 260.xx series driver
%{__install} -p -m 0755 libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-cbl.so in 410.57 beta driver
%{__install} -p -m 0755 libnvidia-cbl.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libnvidia-compiler.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-eglcore.so in 340.24 driver
%{__install} -p -m 0755 libnvidia-eglcore.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-encode.so in 310.19 driver
%{__install} -p -m 0755 libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-fbc.so in 331.20 driver
%{__install} -p -m 0755 libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libnvidia-glcore.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-glsi.so in 340.24 driver
%{__install} -p -m 0755 libnvidia-glsi.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added in 396.18 driver
%{__install} -p -m 0755 libnvidia-glvkspirv.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added in 346.35 driver
%{__install} -p -m 0755 libnvidia-gtk2.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-ifr.so in 325.15 driver
%{__install} -p -m 0755 libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-ml.so in 270.xx series driver
%{__install} -p -m 0755 libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-ngx.so in 450.xx series driver
%{__install} -p -m 0755 libnvidia-ngx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-opencl.so in 304.xx series driver
%{__install} -p -m 0755 libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-opticalflow.so in 418.43 driver
%{__install} -p -m 0755 libnvidia-opticalflow.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-ptxjitcompiler.so in 361.28 driver
%{__install} -p -m 0755 libnvidia-ptxjitcompiler.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvidia-rtcore.so in 410.57 beta drivers
%{__install} -p -m 0755 libnvidia-rtcore.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
# Added libnvoptix.so in 410.57 beta drivers
%{__install} -p -m 0755 libnvoptix.so.%{version} $RPM_BUILD_ROOT%{_libdir}/
%{__install} -p -m 0755 libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/

# Install X driver and extension 
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/
%{__install} -p -m 0755 nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/
%{__install} -p -m 0755 libglxserver_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so

# Create the symlinks
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libcuda.so
%{__ln_s} libcuda.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libcuda.so.1
%{__ln_s} libEGL_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libEGL_nvidia.so.0
%{__ln_s} libGLESv1_CM_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libGLESv1_CM_nvidia.so.1
%{__ln_s} libGLESv2_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libGLESv2_nvidia.so.2
%{__ln_s} libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libGLX_nvidia.so.0
# Workaround buggy mesa
%{__ln_s} libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libGLX_indirect.so.0
# Added libnvcuvid.so in 260.xx series driver
%{__ln_s} libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvcuvid.so
%{__ln_s} libnvcuvid.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvcuvid.so.1
%{__ln_s} libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-cfg.so.1
# Added libnvidia-encode.so in 310.19 driver
%{__ln_s} libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-encode.so
%{__ln_s} libnvidia-encode.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-encode.so.1
# Added libnvidia-fbc.so in 331.20 driver
%{__ln_s} libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-fbc.so
%{__ln_s} libnvidia-fbc.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-fbc.so.1
# Added libnvidia-ifr.so in 325.15 driver
%{__ln_s} libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-ifr.so
%{__ln_s} libnvidia-ifr.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-ifr.so.1
# Added libnvidia-ml.so in 270.xx series driver
%{__ln_s} libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-ml.so
%{__ln_s} libnvidia-ml.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-ml.so.1
# Added libnvidia-ngx.so in 450.xx series driver
%{__ln_s} libnvidia-ngx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-ngx.so
%{__ln_s} libnvidia-ngx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-ngx.so.1
# Added libnvidia-opencl.so in 304.xx series driver
%{__ln_s} libnvidia-opencl.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-opencl.so.1
# Added libnvidia-opticalflow.so in 418.43 driver
%{__ln_s} libnvidia-opticalflow.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-opticalflow.so
%{__ln_s} libnvidia-opticalflow.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-opticalflow.so.1
%{__ln_s} libnvidia-ptxjitcompiler.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvidia-ptxjitcompiler.so.1
# Added libnvoptix.so in 410.57 beta drivers
%{__ln_s} libnvoptix.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libnvoptix.so.1
%{__ln_s} libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_nvidia.so.1

# Install man pages
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1/
%{__install} -p -m 0644 nvidia-{cuda-mps-control,modprobe,persistenced,settings,smi,xconfig}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/

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

# Install the Xorg conf file
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/X11/
%{__install} -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/nvidia-xorg.conf

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
      %{__perl} -pi -e 's|(GRUB_CMDLINE_LINUX=".*)"|$1 nouveau\.modeset=0 rd\.driver\.blacklist=nouveau"|g' \
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
              --args='nouveau.modeset=0 rd.driver.blacklist=nouveau' &>/dev/null
          fi
        done
      done
    fi
fi || :

/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc nvidiapkg/html/*
%{_mandir}/man1/nvidia*.*
%{_datadir}/pixmaps/nvidia-settings.png
%{_datadir}/applications/nvidia-settings.desktop
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%{_datadir}/vulkan/icd.d/nvidia_icd.json
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-application-profiles-*
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-debugdump
%attr(4755, root, root) %{_bindir}/nvidia-modprobe
%{_bindir}/nvidia-persistenced
%{_bindir}/nvidia-settings
%{_bindir}/nvidia-smi
%{_bindir}/nvidia-xconfig
%config %{_sysconfdir}/X11/nvidia-xorg.conf
%{_sysconfdir}/OpenCL/vendors/nvidia.icd

# now the libs
%{_libdir}/lib*
%{_libdir}/vdpau/libvdpau_nvidia.*
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so

%changelog
* Fri Jun  4 2021 Michael Lampe <mlampe0@googlemail.com> - 460.84-1.el7.ml
- Updated to 460.84

* Wed May 12 2021 Michael Lampe <mlampe0@googlemail.com> - 460.80-1.el7.ml
- Updated to 460.80

* Thu Apr 15 2021 Michael Lampe <mlampe0@googlemail.com> - 460.73.01-1.el7.ml
- Updated to 460.73.01

* Mon Mar 22 2021 Michael Lampe <mlampe0@googlemail.com> - 460.67-1.el7.ml
- Updated to 460.67

* Wed Mar  3 2021 Michael Lampe <mlampe0@googlemail.com> - 460.56-1.el7.ml
- Updated to 460.56

* Tue Jan 26 2021 Michael Lampe <mlampe0@googlemail.com> - 460.39-1.el7.ml
- Updated to 460.39

* Thu Jan  7 2021 Michael Lampe <mlampe0@googlemail.com> - 460.32.03-1.el7.ml
- Updated to 460.32.03

* Fri Oct  2 2020 Michael Lampe <mlampe0@googlemail.com> - 450.80.02-1.el7.ml
- Updated to version 450.80.02

* Tue Aug 25 2020 Michael Lampe <mlampe0@googlemail.com> - 450.66-1.el7.ml
- Updated to version 450.66

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

* Thu Nov 15 2018 Michael Lampe <mlampe0@googlemail.com> - 410.78-1.el7.ml
- Updated to version 410.78

* Tue Oct 30 2018 Michael Lampe <mlampe0@googlemail.com> - 410.73-2.el7.ml
- Adapted to libglvnd support in RHEL 7.6

* Fri Oct 26 2018 Michael Lampe <mlampe0@googlemail.com> - 410.73-1.el7.ml
- Updated to version 410.73

* Wed Oct 17 2018 Michael Lampe <mlampe0@googlemail.com> - 410.66-1.el7.ml
- Resynced with elrepo
