---
layout: post
title: Network booting your Raspberry Pi 4B
description: Network booting your Raspberry Pi 4B
---

While the Raspberry Pi is a great platform for dabbling in OS development or
Linux kernel development, the workflow is not very good. A typical cycle
involves first building an operating system image, copying it to a SD card,
popping the card out of your development machine and into the Pi, and then power
cycling the Pi. Not only are SD cards not the most reliable, they're also small
and frustrating to move between computers every few minutes. You can
dramatically improve this workflow with network booting.

This guide will describe the network booting setup I have for my Raspberry Pi 4,
Model B. I use this to boot custom kernels for Linux kernel development, so I'll
go through the process up to the point of booting an upstream Linux kernel with
a minimal BusyBox userspace. However, I'll flag places along the way where you
could diverge and do things differently. The end setup looks something like
this:

```
+---------+                +---------------+
|   Pi    |<-- ethernet -->|  Dev Machine  | . . . wifi . . . < Internet >
+---------+                +---------------+
                           | (kernel +     |
                           | userspace     |
                           | images)       |
                           +---------------+
```

Essentially, you connect your Pi to your computer over Ethernet, and let it
serve your kernel and userspace over the network boot system. Later, your Pi can
even use your computer to connect to the Internet as well, although I won't
cover that.

If you want to follow along, you'll want to have the following:

- A Raspberry Pi 4B, monitor & cable, USB keyboard, power source
- A Linux development machine, preferably connected to the internet via WiFi,
  and with an ethernet port
- An ethernet cable
- A Micro SD card with a recent Raspbian installed on it
- Optionally, a USB TTL serial cable. You'd be surprised how great serial ports
  are for debugging. Get it from Adafruit - make sure it's compatible with the
  3.3V logic levels that the Pi uses.

A final note before starting this: network booting a Pi 4B is still in beta at
the time of writing. You'll need to be prepared to potentially use the [recovery
steps][rpi-download] to reprogram the EEPROM if things go awry. But if you're
here, you're probably willing to do that.

## Step 0: Get a cross compiler

If you happen to already be on an ARM machine, I guess you can skip this. But
for the rest of us, you'll need to install a cross-compiler toolchain which will
let you compile for arm7l. This will be necessary so we can compile the kernel,
as well as the userspace.

On Ubuntu, there is a pre-built package `gcc-arm-linux-gnueabihf`, but on Arch
Linux, the best you can find is the AUR package `arm-linux-gnueabihf-gcc`. This
means you'll need to do a lot of compiling to create the cross-compiler, as the
package maintainer [says here][aur-cc]. Thankfully, my AUR helper was able to
pretty much automate all this (run on your Linux dev machine, *not* the Pi):

    yaourt -S arm-linux-gnueabihf-gcc
    # Go through the prompts.
    # I had to add some pgp keys with `gpg --recv-keys KEYID` in a separate
    # terminal when prompted.

[aur-cc]: https://aur.archlinux.org/packages/arm-linux-gnueabihf-gcc/

## Step 1: Prepare your EEPROM

The Raspberry Pi has firmware and bootloaders that are responsible for loading
the kernel. The most recent beta firmware implements network boot, and it
requires updating and configuring your Pi 4's EEPROM.  While normally I would
spell out all the commands necessary to do this, there's actually really amazing
[documentation][doc-setup-netboot] describing how to do it. Simply boot into
Raspbian and run the commands from the Installation, Configuration, and Update
sections of that page. Once you've rebooted, the firmware should be up-to-date
and you can continue on.

## Step 2: Prepare boot files

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

## Step 3: Prepare busybox initrd

Once network boot has loaded a kernel, the kernel is going to want a root
filesystem. We have several options here. One is to use "Network File System",
i.e. NFS, to share a root directory which the kernel can read. This is a totally
valid approach, but for me, I found it to be difficult to configure, arcane, and
ultimately really flakey.

A drop-dead simple way to have a root file system is to use an "initial
ramdisk", and just include a very small userspace image. BusyBox is an excellent
set of core utilities which has a very small footprint. Using our new
cross-compiler, we will compile our userspace and install it into a directory on
our computer. This will later get bundled up into the initial ramdisk, which
will get loaded with the kernel.

To get started, hit up [BusyBox][bb] and find their latest source tarball. From
there:

    # Download and extract it
    wget <BusyBox latest release tarball>
    tar xf the-tarball

    # Configure and compile, statically linked
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
    LDFLAGS="--static" make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j4

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

For `/sbin/init` (the main init) use the following:

```
#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
echo /sbin/mdev > /proc/sys/kernel/hotplug
/sbin/mdev -s
exec setsid sh -c 'exec sh </dev/tty1 >/dev/tty1 2>&1 /sbin/init2'
```

The first few lines are general housekeeping and could probably even be removed.
The last line I included because I was having trouble seeing any command input
or output from my init script. [BusyBox FAQ][faq] gave me some advice for
getting the job control stuff working, such that I could run the scripts in
`/sbin/init2` and see their output. Here is what I ended up putting in `init2`,
but you are free to put whatever tests you want:

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

[bb]: https://www.busybox.net/
[faq]: https://busybox.net/FAQ.html#job_control

## Step 4: Compile kernel

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
    scripts/config --file ~/rpi-build/.config --set-str INITRAMFS_ROOT_SOURCE ~/rpi-ramfs

    # Compile it!
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j4 O=~/rpi-build

When we configured the kernel, we used `INITRAMFS_ROOT_SOURCE` to specify our
ramfs location. This handy configuration tell the kernel build system to package
up that folder, build a ramfs, and _compile it into the kernel_. This way, we
don't need to tell the bootloader anything about the ramfs, which is really
convenient; I haven't been able to get the Raspberry Pi network bootloader to
work with external initramfs yet.

Now that the kernel is build, we simply need to copy all necessary boot files
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
# Good for if you have the USB serial cable
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

[next]: https://www.kernel.org/

## Step 5: Setup DHCP & TFTP

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
default when your Ethernet cable is plugged in.

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

Once that's done, restart NetworkManager:

    sudo systemctl restart NetworkManager

## Step 5: Configure and boot

At this point, everything is ready. We have compiled a kernel, which contains
our homemade root filesystem with BusyBox. We have all the necessary firmware in
a boot directory, which we have configured to serve over TFTP.

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

## Resources

- Article on setting up a basic initramfs:
  https://lyngvaer.no/log/create-linux-initramfs

[rpi-download]: https://www.raspberrypi.org/documentation/hardware/raspberrypi/booteeprom.md
[doc-setup-netboot]: https://github.com/raspberrypi/rpi-eeprom/blob/master/firmware/raspberry_pi4_network_boot_beta.md
[anholt]: https://github.com/anholt/linux/wiki/Raspberry-Pi-development-environment
[firmware]: https://github.com/raspberrypi/firmware
