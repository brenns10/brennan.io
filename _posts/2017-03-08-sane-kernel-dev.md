---
layout: post
title: Kernel Development Made Easier
---

A little while ago I wrote a post about creating a Linux [system call][syscall].
In it, I explained how to create a virtual machine, get the Linux source, modify
it, build it, and boot your custom kernel. This is a totally valid way to do
kernel development, but it can be a bit inconvenient. For one, the code was
stored within the VM, so all editing and compiling was done in a VM too. For
another, there was a pretty complex process to build an "initrd" in order for
Arch Linux to boot properly. And finally, the kernel configuration we used was
pretty massive, resulting in longer build times for extra features and device
support to be compiled into the kernel.

For simple development and debugging, we can do better! In this post, I'll
describe the setup that I'm using now - which allows me to compile and boot a
kernel in a matter of seconds, while being able to edit and compile on the host
machine.

## Intro to qemu

If you're like me a few months ago, you may have never heard of qemu. As far as
I was concerned, the only "hypervisor" I would ever need was VirtualBox, which
was open-source and very easy to use. Qemu is like the `curl` of hypervisors. It
runs on the command-line and takes every option under the sun. If you know it
well, you can make great use of it, but the rest of us will just use a web
browser.

Since qemu is so configurable, you're actually able to do some really cool
things, like directly booting a Linux kernel image in a VM. Even more exciting,
you can do that without ever creating a virtual hard drive---in essence, you can
boot a VM with a different kernel, running on your host's filesystem. This is
really, really convenient for development tasks. But it can be a chore to set
this all up. Enter `vido`.

## Intro to vido

[`vido`][vido] is a Python wrapper script around qemu. It's named similar to
sudo (**s**uper **u**ser **do**) because its operation is similar: it runs a
command inside a virtual machine with a custom Linux kernel (**vi**rtual
**do**). A command like the following would boot your kernel and print out
information about it:

```bash
$ vido [options] -- uname -a
# uname output appears here...
```

`vido` is not the only tool for this purpose. One similar tool
is [`eudyptula-boot`][eudyptula], which looks like an excellent choice. However
I wanted to use something I could easily modify, and `vido` is written in Python
which makes it infinitely more hackable for me than the bash script that is
`eudyptula-boot`.

On Arch Linux[^1], you can install qemu through pacman and vido through pip:

```bash
$ sudo pacman -S qemu qemu-arch-extra
$ sudo pip install vido
```

An even better option than pip installing is to clone vido from
its [source][vido] directly. Then, run `sudo python setup.py develop` from
within the directory. This will still install `vido` to your system, but it will
install links that point to your git clone. This allows you to make changes to
`vido`, should the need arise.

## Configuring the Kernel

In order to make `vido` work, we can't just use any old kernel. The kernel needs
to have support for some special file systems and configuration options.
Thankfully, `vido` comes with a list of configuration options that need to be
applied. They will work with any reasonably recent kernel.

If you want to customize the kernel configuration, the most obvious options are
the `make config`, `make menuconfig`, and `make xconfig` tools. These pop open
GUIs that allow you to browse and edit configuration safely. They're definitely
worth using, to explore and familiarize yourself. But there's just nothing worse
than opening up these tools and setting configuration values by hand, one by one
by one.

The most convenient system, when you already know exactly what you want out of
your kernel, is the script `scripts/kconfig/merge_config.sh`, located in your
Linux checkout. You can use this bad boy to take several files with
configuration values set, merge them together, and apply them on top of a
minimal base configuration. This lets you maintain a list of required
configuration values and apply them instantly, without any fussing with a menu.
In our case, `vido` comes with a file named `kvm.config` that contains its
required configuration values. In addition, you may want to create a file named
`debug.config` with some of the options below:

```
CONFIG_DEBUG_KERNEL=y
CONFIG_DEBUG_INFO=y
CONFIG_STACKTRACE=y
CONFIG_DEBUG_LIST=y
CONFIG_DEBUG_KMEMLEAK=y
CONFIG_SLUB_DEBUG=y
CONFIG_KMEMCHECK=y
CONFIG_DEBUG_MUTEXES=y
CONFIG_DEBUG_ATOMIC_SLEEP=y
CONFIG_FRAME_POINTER=y
```

You can grep through the source for documentation on what they do, but many of
them can be helpful for discovering bugs or narrowing down when they occur. Most
incur a performance penalty, but that doesn't matter a ton for us.

If you have these files, you can run a command like this in your Linux checkout:

```bash
$ scripts/kconfig/merge_config.sh -n \
  arch/x86/configs/kvm_guest.config \
  path/to/vido/kvm.config \
  path/to/debug.config
```

And *voila!* your kernel is configured. Now a simple `make -jX` (where X = the
number of CPUs you have) will compile your kernel, depositing the image in
`arch/x86_64/boot/bzImage`.

## Putting it all together

From here, you are ready to boot your kernel and start messing around. Here is
the command I use to run `vido`:

```bash
$ vido --kvm --kernel path/to/arch/x86_64/boot/bzImage -- sh
```

This will run `sh` in your VM, giving you a chance to run commands
interactively. Some good things to do are to check your `dmesg` output and run
`uname`. This is a great time to revisit the [system call tutorial][syscall],
make the same code changes, and then try testing it out in vido instead!

[syscall]: {% post_url 2016-11-14-kernel-dev-ep3 %}
[vido]: https://github.com/g2p/vido
[eudyptula]: https://github.com/vincentbernat/eudyptula-boot

#### Footnotes

[^1]:
     Warning! Python 3.6.0 has a bug that breaks part of vido. Version 3.6.1
     contains a fix for this bug, but it's not scheduled for release until March
     13th. As a result, you need either an old (3.5) version of Python, or a
     patched version of Python 3.6. Arch users can simply use
     my
     [PKGBUILD](https://gist.github.com/brenns10/90aa07d4ca9a985039fb7a3e88d9362f),
     which contains the proper patch. Clone that gist and run:
     ```bash
     $ makepkg -s --skippgpcheck --nocheck
     # -s will install build dependencies
     # --skippgpcheck will not verify pgp signatures
     # --nocheck skips some of the very lengthy test suites
     $ sudo pacman -U python-3.6.0-3.pkg.tar.xz
     ```
     If `python -V` gives something other than 3.6.0, you should be fine.
