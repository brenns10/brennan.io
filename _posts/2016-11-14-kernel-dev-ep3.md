---
layout: post
title: Tutorial - Write a System Call
featured: true
---

A while back, I wrote about writing a [shell in C][shell], a task which lets you
peek under the covers of a tool you use daily. Underneath even a simple shell
are many operating system calls,
like [read][], [fork][], [exec][], [wait][], [write][], and [chdir][] (to name a
few). Now, it's time to continue this journey down another level, and learn just
how these system calls are implemented in Linux.

## What is a system call?

Before we start implementing system calls, we'd better make sure we understand
exactly what they are. A naive programmer---like me not that long ago---might
define a system call as any function provided by the C library. But this isn't
quite true. Although many functions in the C library align nicely with system
calls (like [chdir][]), other ones do quite a bit more than simply ask the
operating system to do something (such as [fork][] or [fprintf][]). Still others
simply provide programming functionality without using the operating system,
such as [qsort][] and [strtok][].

In fact, a system call has a very specific definition. It is a way of requesting
that the operating system kernel do something on your behalf. Operations like
tokenizing a string don't require interacting with the kernel, but anything
involving devices, files, or processes definitely does.

System calls also behave differently under the hood than a normal function.
Rather than simply jumping to some code from your program or a library, your
program has to ask the CPU to switch into kernel mode, and then go to a
predefined location within the kernel to handle your system call. This can be
done in a few different ways, such as a processor interrupt, or special
instructions such as `syscall` or `sysenter`. In fact, the modern way of making
a system call in Linux is to let the kernel provide some code (called the VDSO)
which does the right thing to make a system call. Here's
an [interesting SO question][so] on the topic.

Thankfully, all that complexity is handled for us. No matter how a system call
is made, it all comes down to looking up the particular *system call number* in
a table to find the correct kernel function to call. Since all you need is a
table entry and a function, it's actually very easy to implement your own system
call. So let's give it a shot!

## Set up your VM

Unlike my [previous][km1] [articles][km2] on kernel development, implementing a
system call is not something you can do in a kernel module. Instead, you must
actually get a copy of the Linux source, modify it, compile it, and boot it.
This is something you could do directly on your main computer (if you run
Linux), but it's probably best to try this out on a virtual machine! For this
example, we'll be using VirtualBox, so install it if you don't already have it.

Although you can mess around with setting up a virtual machine manually, it's
more worth your time to simply download a pre-installed virtual machine. You can
download a premade Arch Linux machine [here][osbox]. In this article, I'll be
using the 201608 CLI version for VirtualBox. Download and unzip it. Create a new
virtual machine in VirtualBox, and when it asks about a hard disk file, choose
the `vdi` file you downloaded. Create and run your virtual machine, and you
should be greeted with a CLI login screen. The root password should have been
noted on the download page (mine was `osboxes.org`).

*Note: if you have a multicore machine, it would be a good idea to edit your VM
settings to allow it to use more than one core. This will dramatically improve
your compile times, so long as you substitute* &nbsp;`make -jN` *for*
&nbsp;`make` *in all following commands, where N is the number of cores you give
your VM access to.*

The first preparation step you should take is to install `bc`, a build-time
dependency of Linux that isn't included in the virtual machine. Unfortunately,
this will require that you update the virtual machine first. Note that every
command I give in this article should be run as root, which shouldn't be hard,
because the only user on your VM is, in fact, root.

```bash
$ pacman -Syu
$ pacman -S bc
$ reboot
```

You have to reboot because the kernel will almost certainly be updated, and we
want to make sure we're running the kernel we have installed before continuing
with the rest of this process.

## Acquire Source Code

After you have your development virtual machine, the next step is to download
the kernel source code. Although most developers reflexively reach for Git when
they need to get code, this is probably not the time for that! The Linux Git
repository is *very* large, and so cloning it will almost certainly not be
worthwhile. Instead, you should download the source tarball associated with your
kernel version. You can check your version with `uname -r`, and then **pick a
download at [kernel.org][] that is as close to your kernel version as
possible**. Within your virtual machine, download the source using `curl`, e.g.:

```bash
# -O -J will set the output filename based on the URL
$ curl -O -J https://www.kernel.org/pub/linux/kernel/v4.x/linux-VERSION.tar.xz
```

And then you can decompress your tarball, e.g.:

```bash
$ tar xvf linux-VERSION.tar.xz
$ cd linux-VERSION
```

## Configure Your Kernel

The Linux Kernel is extraordinarily configurable; you can enable and disable
many of its features, as well as set build parameters. If you were to make every
configuration choice manually, you'd be doing it all day. Instead, you can skip
this step by simply copying your kernel's existing configuration, which is
conveniently stored (in most Linux computers) in the compressed file
`/proc/config.gz`. To use this configuration for your new kernel, use the
command:

```bash
$ zcat /proc/config.gz > .config
```

To ensure that you have values for all configuration variables, run `make
oldconfig`. More than likely, this will not ask you any configuration questions.

The only configuration item that you ought to modify is the kernel name, to
ensure that it doesn't conflict with your currently installed one. On Arch
Linux, the kernel is built with the suffix `-ARCH`. You should change this
suffix to something unique to you: I used `-stephen`. To do this, the simplest
way is to open `.config` with a text editor, and modify this line directly.
You'll find it just under the "General setup" heading, not too far down the
file:

```
CONFIG_LOCALVERSION="-ARCH"
```

## Add Your System Call

Now that the kernel is configured, you *could* start compiling it right away.
However, creating a system call requires editing a table that is included by a
truly huge amount of code. Since compiling takes a rather long time, you'll end
up wasting a lot of time if you compile right now. So let's get on to the good
stuff: writing your system call!

Some of Linux's code is architecture-specific, such as the code that initially
handles interrupts and system calls. Thus, the tables of system calls are
actually located in directories specific to your processor. We'll just do this
for x86_64.

### System call table

The file containing the system call table for x86_64 is located in
`arch/x86/entry/syscalls/syscall_64.tbl`. This table is read by scripts and used
to generate some of the boilerplate code, which makes our lives a lot easier! Go
to the bottom of the first group (it ends at syscall 328 in version 4.7.1), and
add the following line:

```
329	common	stephen	sys_stephen
```

Notice that there is a tab between each column (not a space). The first column
is the system call number. I chose the next available number in the table, which
in this case was 329. You should also choose the next available number, which
may not be 329! The second column says that this system call is common to both
32-bit and 64-bit CPUs. The third column is the name of the system call, and the
fourth is the name of the function implementing it. By convention this is simply
the syscall name, prefixed by `sys_`. I used `stephen` for my system call name,
but you can use whatever you'd like.

### System call function

The last step is to write the function for the system call! We haven't really
gone into what the system call should do, but really all we would like is to do
something simple that we can observe. An easy thing to do is write to the kernel
log using `printk()`. So, our system call will take one argument, a string, and
it will write it to the kernel log.

You can implement system calls anywhere, but miscellaneous syscalls tend to go
in the `kernel/sys.c` file. Put this somewhere in the file:

```c
SYSCALL_DEFINE1(stephen, char *, msg)
{
  char buf[256];
  long copied = strncpy_from_user(buf, msg, sizeof(buf));
  if (copied < 0 || copied == sizeof(buf))
    return -EFAULT;
  printk(KERN_INFO "stephen syscall called with \"%s\"\n", buf);
  return 0;
}
```

`SYSCALL_DEFINEN` is a family of macros that make it easy to define a system
call with N arguments. The first argument to the macro is the name of the system
call (without `sys_` prepended to it). The remaining arguments are pairs of type
and name for the parameters. Since our system call has one argument, we use
`SYSCALL_DEFINE1`, and our only parameter is a `char *` which we name `msg`.

An interesting issue that we encounter immediately is that we cannot directly
use the `msg` pointer provided to us. There are several reasons why this is the
case, but none are very obvious!

- The process could try to trick us into printing out data from kernel memory by
  giving us a pointer that maps to kernel space. This should not be allowed.
- The process could try to read another process's memory by giving a pointer
  that maps into another process's address space.
- We also need to respect the read/write/execute permissions of memory.

To handle these issues, we use a handy `strncpy_from_user()` [function][strncpy]
which behaves like normal `strncpy`, but checks the user-space memory address
first. If the string was too long or if there was a problem copying, we return
`EFAULT` (although returning `EINVAL` for a too-long string might be better).

Finally, we use `printk` with the `KERN_INFO` log level. This is actually a
macro that resolves to a string literal. The compiler concatenates that with the
format string and `printk()` uses it to determine the log level. Finally,
`printk` does formatting similar to `printf()`, which is where the `%s` comes
in.

## Compile and boot the kernel

**Note:** the steps here get a bit complicated. Read this section but you don't
need to run the commands yet. At the end I'll give a nice bash script that you
can run to do all of this.

Our first step is to compile the kernel and its modules. The main kernel image
is compiled by running `make`. You can find the result in the file
`arch/x86_64/boot/bzImage`. The kernel modules that go along with this version
are compiled and copied into `/lib/modules/KERNEL_VERSION` when you run `make
modules_install`. For instance, with the configuration I have created thus far
in this article, the modules would be compiled and placed in
`/lib/modules/linux-4.7.1-stephen/`.

After you have compiled the kernel and its modules, you'll need to do a few more
things in order to get it to boot. First, you'll have to copy the compiled
kernel image into your `/boot` directory:

```bash
$ cp arch/x86_64/boot/bzImage /boot/vmlinuz-linux-stephen
```

Next, for reasons that aren't really important to us, you need to create an
"initramfs". We can do this with two steps. First, by creating a preset based on
your old one:

```bash
$ sed s/linux/linux-stephen/g </etc/mknitcpio.d/linux.preset >/etc/mkinitcpio.d/linux-stephen.preset
```

Then generate the actual image:

```bash
$ mkinitcpio -p linux-stephen
```

Finally, you'll need to instruct your bootloader (in the case of our virtual
machine, GRUB) to boot our new kernel. Since GRUB can automatically find kernel
images in the `/boot` directory, all we need to do is regenerate the GRUB
config:

```bash
$ grub-mkconfig -o /boot/grub/grub.cfg
```

**So, the steps in this section can be summarized by this script:**

```bash
#!/usr/bin/bash
# Compile and "deploy" a new custom kernel from source on Arch Linux

# Change this if you'd like. It has no relation
# to the suffix set in the kernel config.
SUFFIX="-stephen"

# This causes the script to exit if an error occurs
set -e

# Compile the kernel
make
# Compile and install modules
make modules_install

# Install kernel image
cp arch/x86_64/boot/bzImage /boot/vmlinuz-linux$SUFFIX

# Create preset and build initramfs
sed s/linux/linux$SUFFIX/g \
    </etc/mkinitcpio.d/linux.preset \
    >/etc/mkinitcpio.d/linux$SUFFIX.preset
mkinitcpio -p linux$SUFFIX

# Update bootloader entries with new kernels.
grub-mkconfig -o /boot/grub/grub.cfg
```

Save this as `deploy.sh` in the main directory of your kernel source, set its
execute permission with `chmod u+x deploy.sh`, and from now on you can build and
deploy your kernel by running that single script and rebooting. The compile may
take a while.

Once the script completes, run `reboot`. When GRUB pops up, select "Advanced
Options for Arch Linux". This should bring you a menu listing the available
kernels. Select your custom one to boot it. You can always go back to the
original if something horrible happens.

If all goes well, you should be greeted with login screen roughly like this:

![syscall_kernel_booted](/images/syscall_kernel_booted.png)
{: max-width="100%"}

The text `4.7.1-stephen` is the kernel version, so it is plain to see that we
are running my modified kernel version. If for some reason you can't see a
kernel version on boot, you can always check `uname -r`.

## Testing Your Syscall

So far, you have compiled and booted a kernel which has your own custom
modifications made to it. Take a moment to congratulate yourself! This is
something that not very many people have done. However, the most exciting part
of the whole affair is getting to run your system call. So how exactly do we do
that?

The C library wraps most system calls for us, so we never have to think of
actually triggering an interrupt. For the system calls we don't have available,
the GNU C library provides the `syscall()` function for us, which can call any
system call by number. Here is a tiny little program that uses this to call our
system call:

```c
/*
 * Test the stephen syscall (#329)
 */
#define _GNU_SOURCE
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>

/*
 * Put your syscall number here.
 */
#define SYS_stephen 329

int main(int argc, char **argv)
{
  if (argc <= 1) {
    printf("Must provide a string to give to system call.\n");
    return -1;
  }
  char *arg = argv[1];
  printf("Making system call with \"%s\".\n", arg);
  long res = syscall(SYS_stephen, arg);
  printf("System call returned %ld.\n", res);
  return res;
}
```

Put this in a file named `test.c`, and compile it with `gcc -o test test.c`.
From there, you can run something like this for your first "hello world" system
call!

```bash
$ ./test 'Hello World!'
# use single quotes if you have an exclamation point :)
```

To see the log entries generated here, just use the `dmesg` command. Since
`dmesg` dumps a ton of information onto your terminal, you may want to use
`dmesg | tail` to get the last few lines of the log. You should see your system
call's text in the log! Here's how it looks on my machine:

![syscall_dmesg_output](/images/syscall_dmesg_output.png)
{: max-width="100%"}


## Wrap Up

Congratulations! You've implemented and tested your own system call! From here,
the whole world of kernel development is open to you. You can change what your
system call does and then rebuild everything with that handy deploy script. Or
you could find another system call and edit what it does, leading to some
(potentially) horrific results! You can always reboot with your old kernel to
save your butt.

I really hope that some people follow this tutorial all the way through and get
their own custom kernels and system calls up and running. Please drop me a line
in the comments if you do!

Please keep in mind that I'm not a kernel expert, and nothing I say here is
guaranteed to be the best way to do something. For instance, you can save a lot
of time if you're doing serious development by using qemu instead of VirtualBox.

Finally, if you liked this article, you may want to check out my previous two
kernel development episodes: [Episode 1][km1], [Episode 2][km2]. They're all
about how to make the kernel fail in interesting ways.

[shell]: {% post_url 2015-01-16-write-a-shell-in-c %}
[km1]: {% post_url 2016-10-13-kernel-dev-ep1 %}
[km2]: {% post_url 2016-11-03-kernel-dev-ep2 %}
[lsh]: https://github.com/brenns10/lsh
[osbox]: http://www.osboxes.org/arch-linux/
[kernel.org]: https://cdn.kernel.org/pub/linux/kernel/v4.x/
[strncpy]: https://www.fsl.cs.sunysb.edu/kernel-api/re252.html
[so]: http://stackoverflow.com/questions/12806584/what-is-better-int-0x80-or-syscall

[read]: https://linux.die.net/man/3/read
[fork]: https://linux.die.net/man/3/fork
[exec]: https://linux.die.net/man/3/exec
[wait]: https://linux.die.net/man/3/wait
[write]: https://linux.die.net/man/3/write
[chdir]: https://linux.die.net/man/3/chdir
[fprintf]: https://linux.die.net/man/3/fprintf
[qsort]: https://linux.die.net/man/3/qsort
[strtok]: https://linux.die.net/man/3/strtok
