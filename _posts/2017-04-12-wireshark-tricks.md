---
title: Wireshark Tricks
layout: post
---

This is mostly for my own reference, but maybe others will find it interesting
as well.

## Remote Monitoring

You can use `tcpdump` or `tshark` within a ssh session, but the Wireshark GUI is
much more powerful than either of those tools.  Here is a useful command that
will let you pipe traffic back to your computer for Wireshark monitoring.

```bash
ssh HOST tcpdump -U -s0 -n -w - -i INTERFACE "FILTER" | wireshark -k -i -
```

`tcpdump` options:

- `-U` : this option instructs tcpdump to write each packet immediately, rather
  than buffering them
- `-s0` : this option instructs tcpdump to capture as much of the packet's data
  as possible
- `-n` : disables address to name resolution
- `-w -` : instructs tcpdump to write packet data to stdout in PCAP format,
  rather than in some sort of human readable format
- `-i INTERFACE` : which network interface?  You may be able to omit this if
  there is only one obvious one
- `"FILTER"` : a PCAP filter expression. Could be something like `not port 22`

`wireshark` options:

- `-k` : immediately begin capturing
- `-i -` : capture from stdin

Of course, you'll want to make sure that your filter excludes your own SSH
connection!

## Monitor Within a Network Namespace

I've been using [mininet][] to create entire networks consisting of hosts,
routers, switches, etc. All of this is on one Linux computer, simply using the
power of the "network namespace". In particular, each host is a network
namespace, with its own set of virtual NICs and associated addresses. The Linux
kernel networking stack handles all of the protocols as if it were putting the
traffic onto the wire, but instead it simply passes it through the virtual
interfaces and into the next host or switch. In this way, very large networks
can be created, and real programs can be run on these hosts.

Unfortunately, the complexity of network namespaces can make it difficult to
monitor such networks. Depending on the network topology you create, there may
not be any Mininet NICs visible from your default network namespace.  In version
2.23 of `util-linux`, the `nsenter` command was created, allowing you to execute
a command within any other process's namespace. So, you could invoke `tcpdump`
like this:

```bash
nsenter -t PID --net tcpdump [ARGS...]
```

All you need to do is specify the PID of the process whose namespace you want to
use (you get this in Mininet using the `dump` command). The `--net` option tells
`nsenter` that you want to use that process's network namespace.

This is great, if your distribution has `util-linux` version 2.23. However,
despite this version being released in April 2013, and Ubuntu 14.04 being
initially released in April 2014, the [trusty `util-linux` package][ul] is still
on version 2.20.  Classic Ubuntu! So, if you use the current (2017) Mininet VM,
you'll find yourself without this tool. Thankfully, it's actually quite simple
to create your own minimal version of it in just a few lines of C. So simple, in
fact, that it is included in the manual page for the `setns` system call! Here
is my own version of this program:

```c
/**
 * nsdo: run a command within a namespace
 */
#define _GNU_SOURCE

#include <sys/stat.h>
#include <fcntl.h>
#include <sched.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
        if (argc < 3) {
                fprintf(stderr, "usage: %s NSFILE cmd [args...]", argv[0]);
                return EXIT_FAILURE;
        }

        int fd = open(argv[1], O_RDONLY);
        if (fd < 0) {
                perror("open");
                return EXIT_FAILURE;
        }

        if (setns(fd, 0) == -1) {
                perror("setns");
                return EXIT_FAILURE;
        }

        execvp(argv[2], &argv[2]);
        // If exec*() returns, it's an error
        perror("execvp");
        return EXIT_FAILURE;
}
```

I name this program `nsdo`. With it, you can do nearly the same thing you could
do with `nsenter`.

```bash
sudo ./nsdo /proc/PID/ns/net tcpdump [ARGS...]
# if this is all local, you can skip the tcpdump shenanigans:
sudo ./nsdo /proc/PID/ns/net wireshark &
```

This looks a bit different than the `nsenter` program because the underlying
`setns` system call actually takes a file descriptor pointing to a file in the
`/proc/` filesystem. Each process has a directory in `/proc`, and its `ns`
directory contains special files (actually, symlinks that _seem_ broken but
aren't) that correspond to namespaces.

Incidentally, these namespaces underly containerization tools like Docker, so
this little tool could likely even be useful for peering into the
[upside-down][] that is a Docker container.

[mininet]: https://github.com/mininet/mininet
[ul]: http://packages.ubuntu.com/trusty/util-linux
[upside-down]: /images/upside-down.png
