---
layout: post
title: Kernel Segfaults for Fun (but no profit)
description: It's all fun and games until a process is put into an uninterruptible sleep.
---

In "episode 2" of my kernel development series, I'm going to talk about how I
put Python into an uninterruptible sleep. This spooky story involves a rogue
kernel module, segmentation faults, and reference counting (a topic
already [well established][spoop] to be spooky). And only a few days late for
Halloween!

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Update: I did this: <a href="https://t.co/Ay4f2Y31NZ">https://t.co/Ay4f2Y31NZ</a></p>&mdash; Stephen Brennan (@brenns10) <a href="https://twitter.com/brenns10/status/780941169136054272">September 28, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

For developers used to working in user-space---like me---the kernel can be a
difficult adjustment, in lots of ways. One particular difficulty is that the
kernel feels very opaque. There's no GUI to watch, nor is there a simple way to
attach a debugger and step through your code. You can write to the log like a
normal program, but that's pretty much the end of the similarities.

A nice trade-off is that the kernel provides several critical services to your
computer, such as the filesystem and the network stack. So if you want to
interact with the kernel, you can use these services in "special" ways. To go
along with that, Linux has inherited the "everything is a file" mindset from
Unix. As a result, a standard way to exchange information with user-space is via
special files. For example, the entire `/proc` directory contains special kernel
files, such as `/proc/cpuinfo`, which can give you information about your
processor, or `/proc/uptime`, which gives you uptime info.

## Custom Character Devices

There are plenty of ways to hook into the filesystem from the kernel, but the
way described by the [Linux Kernel Module Programming Guide][lkmpg] is to create
a new type of character device. Basically, you create a kernel module
implementing some file operations and register them with the kernel. Then, from
userspace you create a new character device file using `mknod`, and suddenly you
can talk to your kernel module's code very easily!

In the example they present, we create a kernel module which implements a device
file that, when read, reports the number of times it has been opened. The basic
idea is that you create a struct containing pointers to implementations for a
few functions - `read()`, `write()`, `open()`, and `close()` being the most
important. This struct gets registered with the kernel.

```c
static struct file_operations fops = {
  .read = device_read,
  .write = device_write,
  .open = device_open,
  .release = device_release
};
```

The module maintains some static variables, most importantly a buffer for the
actual text of the file, a "read pointer" for keeping track of the location
within the file, as well as a flag for whether the file has been opened.

```c
static int Device_Open = 0;
static char msg[BUF_LEN];
static char *msg_Ptr;
```

When a process tries to open the device, the following function is executed:

```c
static int device_open(struct inode *inode, struct file *filp)
{
  static int counter = 0;

  if (Device_Open)
    return -EBUSY;

  Device_Open++;
  sprintf(msg, "I already told you %d times Hello world!\n", counter++);
  msg_Ptr = msg;
  try_module_get(THIS_MODULE);

  return SUCCESS;
}
```

First, we check to see whether or not the device is currently opened
elsewhere---if so, we return an error[^fn-race]. Then, we fill up the buffer
with a message that we create based on the number of times the file has been
opened. Finally, we use the `try_module_get()` function, which I'll explain a
lot more in just a little bit.

Next, when the process reads from the file, our read function copies the data
into their buffer:

```c
static ssize_t device_read(struct file *filp, /* see include/linux/fs.h   */
                           char *buffer,      /* buffer to fill with data */
                           size_t length,     /* length of the buffer     */
                           loff_t *offset)
{
  int bytes_read = 0;

  if (*msg_Ptr == 0)
    return 0;

  while (length && *msg_Ptr) {
    /*
     * The buffer is in the user data segment, not the kernel segment so "*"
     * assignment won't work. We have to use put_user which copies data from the
     * kernel data segment to the user data segment.
     */
    put_user(*(msg_Ptr++), buffer++);
    length--;
    bytes_read++;
  }

  return bytes_read;
}
```

An interesting thing to note is the use of `put_user()`, which is necessary
because memory addresses are mapped to different places in the kernel versus
user-space, so pointers from user-space don't point to the correct things in
kernel-space!

Finally, when the device is closed we decrement our usage count.

```c
static int device_release(struct inode *inode, struct file *filp)
{
  Device_Open--;
  module_put(THIS_MODULE);
  return SUCCESS;
}
```

Again, we see a strange `module_put()` call, but let's disregard that for a
moment longer.

The remainder of the module contains an init and exit function to register and
de-register the character device. I won't bother to put those here. There is
also a `write()` function that always returns an error, because writing to this
file doesn't make sense. You can see the complete code in this [gist][], which
also contains a Makefile.

To try it all out, follow the steps below:

```bash
$ make
$ sudo insmod chardev.ko
$ dmesg | tail
# Read the message printed, and use the provided command to create a device
# file.
# EG:
$ sudo mknod /dev/chardev c 242 0
$ cat /dev/chardev
I already told you 0 times Hello world!
$ cat /dev/chardev
I already told you 1 times Hello world!

# Don't forget to clean up.
$ sudo rm /dev/chardev
$ sudo rm mod chardev
```

As you can see, the file behaves mostly like a normal file. It can be opened
with your normal Linux utilities. The only noticeable difference here is that
the number in the file increments each time it is opened.

## Module Reference Counts

So what's with `try_module_get()` and this `module_put()` thing? They are
actually module reference counts! Linux's kernel module system is very cool,
allowing code to be loaded *and* unloaded from the kernel! This is nice, but
what happens if the user tries to remove a kernel module while it is in the
middle of some important operation? This fails, because a correctly written
module uses `try_module_get()` to indicate when it is in the middle of an
operation (like when its device file is open).

Of course, this immediately raises an exciting question: what happens if you
disregard these safeguards? What would happen if you opened a device file,
removed the module implementing it, and then tried to use the file? We can try
this very easily by simply removing our get and put calls!

A nice quick way to try this is with a python shell. First, make sure that you
recompile, load the module, and create the device file. Then, in a separate
terminal, pop open a Python shell and open the file:

```bash
$ python
>>> f = open('/dev/chardev', 'r')
```

Now, go back to your original terminal and `rmmod` the character device. Without
the reference counts, the kernel happily removes the module and its data. Of
course, there is still an open file out there containing pointers to our read
and write functions, which are now simply patches of freed memory (or worse,
memory belonging to newly loaded code). So, when we try to use the file, things
go very, very wrong:

```python
>>> f.read()

...

...
```

The process is no longer responsive, even to Control-C or any signal you can
send it! The reason can be quickly discovered by checking your `dmesg` output.
You'll see a whole bunch of debug information, along with a report that says
something like:

```
BUG: unable to handle kernel paging request at ffffffffa15ec008
```

For an example of the entire stack trace produced, check [this][dmesg] out.

During the system call, the kernel had a segfault! When this happens to a
user-space process, the kernel just sends `SIGSEGV` to the offending process,
which typically kills it (unless the process explicitly handles the signal). But
you can't just kill the whole kernel just because some crappy kernel module
developer named Stephen Brennan caused a segfault. So the kernel decides that
the safest way to handle it is to suspend the process. It marks the process with
`TASK_UNINTERRUPTIBLE` and puts it to sleep, so that the process will never be
scheduled to run, and no signals may be delivered to it.

You can even check on the process with `ps` to confirm this:

```bash
$ ps `pgrep python`
  PID TTY      STAT   TIME COMMAND
32580 pts/5    D+     0:00 [python]
```

The `D` tells us that the process is in uninterruptible sleep! This (nearly)
zombie process will be bumbling around your computer until you reboot it.
Thankfully it's fairly harmless (unless you have lots of them [dancing][mash]
around your computer).

*Coming up next in the series: implementing a system call!*
[Read Episode 1 Here][ep1]

[lkmpg]: http://www.tldp.org/LDP/lkmpg/2.6/html/lkmpg.html
[gist]: https://gist.github.com/brenns10/65d1ee6bb8419f96d2ae693eb7a66cc0
[dmesg]: http://hastebin.com/niwawumabo.txt
[spoop]: {% post_url 2015-11-02-spooky-garbage-collection %}
[mash]: https://www.youtube.com/watch?v=l2PoSljk8cE
[ep1]: {% post_url 2016-10-13-kernel-dev-ep1 %}

#### Footnotes:

[^fn-race]:
    Note that this is **spectacularly** poor synchronization. Two processes
    could concurrently open the file, and both make it past the if statement
    before incrementing `Device_Open`. If we truly wanted mutual exclusion, we
    would need to use some sort of locking mechanism, like a spinlock or mutex.
    In this case, it doesn't really matter which (though in general that's not
    true).
