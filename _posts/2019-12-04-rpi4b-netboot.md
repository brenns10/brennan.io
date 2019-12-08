---
layout: post
title: Network Booting Raspberry Pi 4B with Upstream Kernel
description: Network Booting Raspberry Pi 4B with Upstream Kernel
---

This is a guide and personal documentation for how I got my Raspberry Pi 4B
booted with an upstream Linux kernel. I use this setup for quickly booting
custom kernels as I do development. As a result, I had the following goals:

1. Quick boot cycles with no fiddling with SD card
2. Reasonably simple to configure (although it still took me several days to get
   everything figured out)
3. Userspace needs minimal functionality, just enough to do simple tests

The resulting setup involves network booting, so that you don't need to copy the
kernel image, config.txt, or cmdline.txt each time you change them. Userspace is
just an initrd with BusyBox, and a custom shell script running as init. The
setup looks something like this:

```
+---------+                +---------------+
|   Pi    |<-- ethernet -->|  Dev Machine  | . . . wifi . . . < Internet >
+---------+                +---------------+
                           | (kernel +     |
                           | userspace     |
                           | images)       |
                           +---------------+
```

The Pi's ethernet port plugs directly into my Linux development machine (a
laptop), which has a wifi internet connection. This ethernet connection allows
the Pi's bootloader to grab boot files from my computer. The Pi is also plugged
into a HDMI monitor, USB keyboard, and USB C power cable. If you want to follow
along, you'll want to have all of those components, as well as a Micro SD card
with Raspbian installed.

A final note before starting this: network booting a Pi 4B is still in **beta**
at the time of writing. You'll need to be prepared to potentially use the
[recovery steps][rpi-download] to reprogram the EEPROM if things go awry. But if
you're following along with this guide, you're probably willing to do that.

Let's get into how to set everything up.

## Step 1: Get a cross compiler

If you happen to already be on an ARM machine, I guess you can skip this. But
for the rest of us, you'll need to install a cross-compiler toolchain which will
let you compile for arm7l. This will be necessary so we can compile the kernel,
as well as the userspace.

On Ubuntu, there is a pre-built package `gcc-arm-linux-gnueabihf`, but for me on
Arch Linux, the best you can find is the AUR package `arm-linux-gnueabihf-gcc`.
This means you'll need to do a lot of compiling to create the cross-compiler, as
the package maintainer [says here][aur-cc]. Thankfully, my AUR helper was able
to pretty much automate all this (run on your Linux dev machine, *not* the Pi):

    yaourt -S arm-linux-gnueabihf-gcc
    # Go through the prompts. It will take a long time. Watch Netflix?
    # I had to add some pgp keys with `gpg --recv-keys KEYID` in a separate
    # terminal when prompted.

## Step 2: Prepare your EEPROM

The Raspberry Pi has firmware and bootloaders that are responsible for loading
the kernel. The most recent beta firmware implements network boot, and it
requires updating and configuring your Pi 4's EEPROM.  While normally I would
spell out all the commands necessary to do this, there's actually really amazing
[documentation][doc-setup-netboot] describing how to do it. Simply boot into
Raspbian and run the commands from the Installation, Configuration, and Update
sections of that page. Once you've rebooted, the firmware should be up-to-date
and you can continue on.

## Step 3: Prepare boot files

The way network boot works, is that the firmware/bootloader will do DHCP
(essentially, ask to connect to a network over Ethernet), and then use "Trivial
File Transfer Protocol", aka TFTP, to request files necessary to boot. Some of
the necessary boot files include firmware files, so the first thing you'll want
to do is download the latest version of the [Raspberry Pi Firmware][firmware].
While git cloning may seem like the right move here...  trust me, just download
the ZIP file, it'll be much faster.

Create a directory to host your boot files, e.g. `$HOME/rpi-boot`, and copy the
files from the `boot` directory of that repository into there. For example:

    wget https://github.com/raspberrypi/firmware/archive/master.zip
    unzip firmware-master.zip
    mkdir $HOME/rpi-boot
    cp -r firmware-master/boot/* $HOME/rpi-boot/

Note that this will contain some kernel images already. These are precompiled,
and built from the *downstream* Raspberry Pi Linux tree. They're great to have
around, but we won't be using them.

## Step 4: Prepare busybox initrd

Once network boot has loaded a kernel, the kernel is going to want a root
filesystem. We have several options here. One is to use "Network File System",
i.e. NFS, to share a root directory which the kernel can read. This is a totally
valid approach, but for me, I found it to be difficult to configure, arcane, and
ultimately really flakey. So, I didn't use NFS.

A drop-dead simple way to have a root file system is to use an "initial
ramdisk", and just include a very small userspace. BusyBox is an excellent set
of core utilities which has a very small footprint. Using our new
cross-compiler, we will compile our userspace and install it into a directory on
our computer. This will later get bundled up into the initial ramdisk, which
will get loaded with the kernel.

To get started, hit up [BusyBox][bb] and find their latest source tarball. From
there:

    # Download and extract it
    wget <BusyBox latest release tarball>
    tar xf <the-tarball>
    cd <the-extracted-directory>

    # Configure and compile, statically linked
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
    LDFLAGS="--static" make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j4

So far, we've downloaded, configured, and compiled busybox. We used `--static`
to statically link the C library. This means that we won't need to build &
install the C library into our initramfs, which cuts down on the work here. Now,
we'll go ahead and create the skeleton of the initramfs, and install BusyBox
into it.

    # Create the root directory of the ramfs
    mkdir ~/rpi-ramfs

    # Install tools & symlinks
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- install CONFIG_PREFIX=~/rpi-ramfs

    # Create important directories
    mkdir -p ~/rpi-ramfs/{proc,sys,dev,etc,usr/lib,bin,sbin}

    # Rather than using busybox's "real" init system, we're going to use some
    # shell scripts. Just delete the symlink:
    rm ~/rpi-ramfs/sbin/init
    vim ~/rpi-ramfs/sbin/init  # see below
    vim ~/rpi-ramfs/sbin/init2  # also see below

For `/sbin/init` (the main init) I ended up using the following:

```
#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
echo /sbin/mdev > /proc/sys/kernel/hotplug
/sbin/mdev -s
exec setsid sh -c 'exec sh </dev/tty1 >/dev/tty1 2>&1 /sbin/init2'
```

The first few lines mount some kernel filesystems and get hotplugging setup. You
may even be able to skip them, but I wanted to have them around.  The last line
I included because I was having trouble seeing any command input or output from
this script. For example, a command like `echo hello world` would not output
onto the screen.

The [BusyBox FAQ][faq] gave me some advice for fixing this issue, which you can
see in the final line. It essentially does some job control magic before
executing the contents of `/sbin/init2`. Any commands you put in that file will
get executed, and you'll be able to see their output too!  Here is what I ended
up putting in `init2`, but you are free to put whatever tests you want:

```
#!/bin/sh
echo 'hello world'

head -c2 /dev/hwrng

# do user commands
exec /bin/sh
```

Once you've created these files in your ramfs, you should be all set. The
following step (compiling the kernel) will automatically build your ramfs for
you!

## Step 5: Compile kernel

Although the boot files in Step 2 include several kernels, we would like to
compile our own kernel directly from the upstream Linux project. Since upstream
support for the Pi 4 is constantly evolving, you'll need to get the latest
possible release. I'd recommend grabbing the latest linux-next tree, which is
[linked][next] on the kernel homepage.

To compile and build the kernel, we'll create a "build directory". This is my
preferred mechanism of compiling the kernel -- it ensures that your source
directory stays clean, and you can have multiple build directories with
completely different settings in parallel. Here's how it will look:

    cd path/to/your/linux/tree

    # Create the directory where build results will be placed
    mkdir ~/rpi-build

    # Configure the kernel
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j4 defconfig O=~/rpi-build defconfig
    scripts/config --file ~/rpi-build/.config --disable CONFIG_LOCALVERSION_AUTO
    scripts/config --file ~/rpi-build/.config --set-str CONFIG_INITRAMFS_SOURCE ~/rpi-ramfs
    scripts/config --file ~/rpi-build/.config --set-val CONFIG_INITRAMFS_ROOT_UID 1000
    scripts/config --file ~/rpi-build/.config --set-val CONFIG_INITRAMFS_ROOT_GID 1000

    # Compile it!
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j4 O=~/rpi-build

In this configuration, we use `INITRAMFS_ROOT_SOURCE` to specify our ramfs
directory location. This handy setting tells the kernel build system to package
up that folder, build a ramfs, and _compile it into the kernel_. This way, we
don't need to tell the bootloader anything about the ramfs, which is really
convenient; I haven't been able to get the Raspberry Pi network bootloader to
work with external initramfs yet.

Now that the kernel is built, we simply need to copy all necessary boot files
into the `~/rpi-boot` directory so the Pi will network boot from it:

```
cp ~/rpi-build/arch/arm/boot/zImage ~/rpi-boot/kernel-upstream.img
cp ~/rpi-build/arch/arm/boot/dts/bcm2711-rpi-4-b.dtb ~/rpi-boot/bcm2711-rpi-4-b-UPSTREAM.dtb
```

The first file, not surprisingly, is the kernel. The second one is a Device
Tree, which contains a complete specification of the devices available on the
board. It is different from the one that is shipped with the Rapsberry Pi
firmware we downloaded before, so we keep it separate and be sure to only use
this one with upstream kernels.

To instruct the Raspberry Pi to use the new kernel and device tree, we'll need
to edit the `config.txt` of the boot directory with the following:

```
# Good for if you have a USB serial cable, but not necessary
enable_uart=1

# Upstream kernel
kernel=kernel-upstream.img
device_tree=bcm2711-rpi-4-b-UPSTREAM.dtb
```

We also want to set some command line arguments for the kernel in `cmdline.txt`
of the boot directory:

```
dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty0 rootfstype=ramfs root=/dev/ram rw rdinit=/sbin/init
```

## Step 6: Setup DHCP & TFTP

Remember back in step 2, where I said that the bootloader would DHCP and then
load boot files over TFTP? Now is the time to set up those things on your Linux
development machine. While this might sound realy daunting, I found it
surprisingly interesting on my Arch Linux machine (with NetworkManager), and it
should be similarly easy on Ubuntu or other distros.

Quite simply, open up your network settings panel (nm-connection-editor is a
popular choice here, although I found the KDE network settings panel worthy as
well), and create a new wired connection which is "shared to other computers".
Click through any wizard and save the connection. Be sure to set its preference
higher than any other Ethernet connections you have, so that it is chosen by
default when your Ethernet cable is plugged in. **You really want to test this
out to make sure it works.** Otherwise later, you'll wonder why your Pi isn't
booting.

To get DHCP and TFTP running, first install `dnsmasq`. Then go ahead and edit
the file `/etc/NetworkManager/dnsmasq-shared.d/tftp.conf` to look like this:

```
# Skip DNS hosting, we're just trying to serve DHCP here.
port=0
# It's really nice to be able to debug what the firmware is doing
log-dhcp
# dnsmasq will be our tftp server
enable-tftp
# you should expand out $HOME below, dnsmasq will not do it for you
tftp-root=$HOME/rpi-boot
pxe-service=0,"Raspberry Pi Boot"
user=root
```

Once that's done, restart NetworkManager so that the changes will take effect.

    sudo systemctl restart NetworkManager

## Step 5: Configure and boot

At this point, everything is ready. We have compiled a kernel, which contains
our homemade initrd with BusyBox all baked in. We have all the necessary
firmware in a boot directory, which we have configured to serve over TFTP.

All we need to do is plug the Pi into our development machine over ethernet, and
turn on the power. It's also nice to have the serial port on, or the HDMI port
plugged in, so you can see console output.

When you power on the Pi, you can watch your system log like this to see the
DHCP requests and TFTP activity as your Pi starts up:

    journalctl -f

For me, I see things like this for DNS:
```
dnsmasq-dhcp[112203]: 3209674060 DHCPREQUEST(enp0s25) 10.42.0.16 MAC-ADDRESS-HERE
```

From there, I see the following for TFTP:

```
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/config.txt to 10.42.0.16
dnsmasq-tftp[3138]: file /home/stephen/rpi-boot/recover4.elf not found
dnsmasq-tftp[3138]: file /home/stephen/rpi-boot/recovery.elf not found
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/start4.elf to 10.42.0.16
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/fixup4.dat to 10.42.0.16
dnsmasq-tftp[3138]: file /home/stephen/rpi-boot/recovery.elf not found
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/config.txt to 10.42.0.16
dnsmasq-tftp[3138]: file /home/stephen/rpi-boot/dt-blob.bin not found
dnsmasq-tftp[3138]: file /home/stephen/rpi-boot/recovery.elf not found
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/config.txt to 10.42.0.16
dnsmasq-tftp[3138]: file /home/stephen/rpi-boot/bootcfg.txt not found
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/bcm2711-rpi-4-b-UPSTREAM.dtb to 10.42.0.16
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/config.txt to 10.42.0.16
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/overlays/pi3-disable-bt.dtbo to 10.42.0.16
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/cmdline.txt to 10.42.0.16
dnsmasq-tftp[3138]: file /home/stephen/rpi-boot/armstub8-32-gic.bin not found
dnsmasq-tftp[3138]: error 0 Early terminate received from 10.42.0.16
dnsmasq-tftp[3138]: failed sending /home/stephen/rpi-boot/kernel-upstream.img to 10.42.0.16
dnsmasq-tftp[3138]: sent /home/stephen/rpi-boot/kernel-upstream.img to 10.42.0.16
```

The TFTP requests will reveal interesting behavior in the bootloader. For
instance, you can see that the bootloader tests for the existence of several
files, including the kernel. It will "even" cancel loading these files, and
request them again once it "decides" on which kernel it wants to really load.

If you're lucky, you'll see the kernel boot up, and you'll see output from the
init script pop up on the monitor or serial port. Congratulations - you've done
a lot of work, but now you have a kernel development setup which gives you
pretty amazing power over the entire system - you can freely modify any part of
the system and experiment as much as possible!

## Resources & Further work

First, this article is heavily based upon several others describing related
setups, from which I've built my own.

- [Eric Anholt][anholt] has a page describing a similar setup (netboot + NFS for
  the Pi 2-3). Large portions of this are wholesale stolen from his setup, but
  updated here and there with my experiences.
- [This article][initramfs] was an easy reference for creating an initramfs.
- Some of the inspiration for using a BusyBox initramfs rather than bothering
  with NFS came from [Ron Munitz's talk][munitz-minimal] at Open Source Summit
  2019: "Understanding, building, and researching minimal (and not so minimal)
  Linux systems". PDF slides are [here][munitz-pdf].
- Another [documentation file][net-tutorial] from Raspberry Pi gives some info
  about how to setup network boot, if you're looking for more resources on that.

[rpi-download]: https://www.raspberrypi.org/documentation/hardware/raspberrypi/booteeprom.md
[aur-cc]: https://aur.archlinux.org/packages/arm-linux-gnueabihf-gcc/
[doc-setup-netboot]: https://github.com/raspberrypi/rpi-eeprom/blob/master/firmware/raspberry_pi4_network_boot_beta.md
[firmware]: https://github.com/raspberrypi/firmware
[bb]: https://www.busybox.net/
[faq]: https://busybox.net/FAQ.html#job_control
[next]: https://www.kernel.org/
[anholt]: https://github.com/anholt/linux/wiki/Raspberry-Pi-development-environment
[initramfs]: https://lyngvaer.no/log/create-linux-initramfs
[munitz-minimal]: https://ossna19.sched.com/event/PURH/understanding-building-and-researching-minimal-and-not-so-minimal-linux-systems-ron-munitz-the-pscg
[munitz-pdf]: https://static.sched.com/hosted_files/ossna19/bb/Ron%20Munitz%20Open%20Source%20Summit%202019%20San%20Diego%20talk.pdf
[net-tutorial]: https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/net_tutorial.md
