---
layout: post
title: "Stephen Tries Kernel Development: Episode I"
description: In which I trap a module in the kernel forever.
---

For the past few weeks I've been dipping my toes into Linux kernel development,
as part of the work I'm doing for my master's thesis. Like most things that stir
up my nerdy interests, it's leaked onto Twitter quite a bit...

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">BTW my Twitter is slowly turning into &quot;Stephen tries kernel development&quot;. I&#39;m not sorry, but I figured I should warn people.</p>&mdash; Stephen Brennan (@brenns10) <a href="https://twitter.com/brenns10/status/780917721022107648">September 27, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

I've already broken things in several interesting ways, and while the results
fit nicely into tweets, they don't get the explanation they deserve. So I
decided to take Andrew's [suggestion][mt] that I blog about this stuff. I'm
intending to post short articles that "follow up" on my silly tweets with a bit
of background and explanation, so that somebody else could (in theory) reproduce
them. This first one will be a bit longer since I'm going to include a little
background on the kernel before anything else.

## What is a kernel?

This is a big question, and one that you can write papers instead of paragraphs
about. To put it simply, computers have lots of devices attached to them, like
keyboards, mice, screens, webcams, hard disks, flash drives, WiFi cards, etc.
Your programs usually aren't that useful unless they do something with those
devices. The problem is, these programs are basically rude little children at
day-care. You have tons of them running at the same time. They all want to play
with the same ~~toys~~ devices. What's worse, they all believe that they're the
only programs in the world, and so they don't know *anything* about how to share
resources like the processor or memory.

The kernel is a critical piece of software that herds the
[~~cats~~](/images/herding-cats.gif) ~~children~~ programs on your computer. It
lets programs use devices without interfering with each other. It also
"schedules" programs so they run for a certain amount of time and then get
"paused", ensuring that each running program gets a fair amount of time to run.
Finally, it even "tricks" the programs into believing that they can...

![Use ALL the memory]

... instead of sharing it with other programs[^fn-allie].

All of that to say, without a kernel you can't use a computer---at least, not in
the modern sense of the term.

Linux kernel development is notoriously hard because it's a rat's nest of
complexity. As a project which had [15 million lines][loc] of code back in 2011,
it's filled with unspoken rules, terrible naming, inconsistent interfaces, and
more. You need to understand lots of the "nitty-gritties" of how modern
computers work in order to be effective. Plus, you must constantly be thinking
about scary "concurrency" related ideas like preemption, interrupts,
synchronization, etc---easily some of the most difficult programming concepts
for humans to reason about. Since performance is important to Linux, sometimes
clarity of code is sacrificed for efficiency. And finally, the cherry on top of
it all is that mistakes made in the kernel tend to have *far* worse consequences
than in a regular program---sometimes as bad as *hold the power button and hope
the computer will turn back on.*

If you're interested in following along with my learning, my main resources are
the [Linux Kernel Module Programming Guide][lkmpg] (to get my feet wet) and
[*Linux Kernel Development, Third Edition*][lkd3e], by Robert Love (this one is
the real resource).

## Episode I

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Current kernel dev scoreboard:<br><br>1 messed up kernel module that can&#39;t be removed<br><br>1 process in an uninterruptable sleep due to my own bug</p>&mdash; Stephen Brennan (@brenns10) <a href="https://twitter.com/brenns10/status/780940425511051264">September 28, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

I started my journey with kernel modules. These are bits of code that can be
dynamically loaded into and unloaded from the kernel. If you have a compiled
module named `hello.ko`, it is really quite simple to use it: `sudo insmod
hello.ko` loads it, and `sudo rmmod hello` unloads it. Where do you get a
compiled module? Well, the [kernel module guide][lkmpg] gives this code as an
example:

```c
/*
 *  hello-3.c - Illustrating the __init, __initdata and __exit macros.
 */
#include <linux/module.h>	/* Needed by all modules */
#include <linux/kernel.h>	/* Needed for KERN_INFO */
#include <linux/init.h>		/* Needed for the macros */

static int hello3_data __initdata = 3;

static int __init hello_3_init(void)
{
	printk(KERN_INFO "Hello, world %d\n", hello3_data);
	return 0;
}

static void __exit hello_3_exit(void)
{
	printk(KERN_INFO "Goodbye, world 3\n");
}

module_init(hello_3_init);
module_exit(hello_3_exit);
```

There's also a [Makefile][modmake] for compiling it. There's plenty to explain
in this code, and I'd encourage you to read about it in the first few chapters
of the guide. But hopefully it shouldn't take too much blank staring to see that
this module contains two functions, one which runs on initialization (when you
`insmod` it), and one which runs on exit (when you `rmmod` it). These functions
print out some log messages (use the `dmesg` command to see kernel logs). The
init function uses a statically declared integer, `hello3_data`, in its
printout.

What I'd like to ~~break~~ focus on in this case is the `__initdata` macro in
the declaration of `hello3_data`. This is a neat optimization that informs the
kernel that you only want that variable when you're initializing your module. So
the kernel will free the memory holding that variable after your init function
runs.

Like any well-intentioned optimization, this makes it *so very easy* to shoot
yourself in the foot. Not surprisingly, the compiler won't really complain at
you if you use the variable outside of the init function[^fn-c]. So, there's no
reason we couldn't use that variable in our exit function...

```c
static void __exit hello_3_exit(void)
{
	printk(KERN_INFO "Goodbye, world %d\n", hello3_data);
}
```

If you compile and load this module, you'll find that everything compiles
fine[^fn-modpost]! The problems start happening when you try to remove the
module.

```bash
$ sudo rmmod hello-3
[1]    14095 killed     sudo rmmod hello-3
```

The rmmod command got killed by the kernel! How odd. What's stranger is if you
try again:

```bash
$ sudo rmmod hello-3
rmmod: ERROR: Module hello_3 is in use
```

This time, the kernel complains that your module is in use.

You see, the first time you run `rmmod`, the exit function runs and causes a
memory error because `hello3_data` was deleted. The kernel experiences an "Oops"
(that's the [technical term][oops] for it) and decides that since your module
crashed while unloading, it's safest to just mark it as "in use" to prevent
further damage.

[You can rmmmod it any time you'd like, but will never leave!][hotelcalifornia]
(until you reboot)

**Score one on the kernel development scorecard!** Read [Episode 2][ep2] to see
how I put a process into an uninterruptible sleep using nothing but a kernel
module. Read [Episode 3][ep3] to learn how to make your own system call.

[Use ALL the memory]: /images/use-all-the-memory.jpg
{: max-width="100%"}
[lkmpg]: http://www.tldp.org/LDP/lkmpg/2.6/html/lkmpg.html
[lkmpgch4]: http://www.tldp.org/LDP/lkmpg/2.6/html/lkmpg.html#AEN567
[lkd3e]: https://www.amazon.com/Linux-Kernel-Development-Robert-Love/dp/0672329468/
[modmake]: http://www.tldp.org/LDP/lkmpg/2.6/html/lkmpg.html#AEN189
[mt]: https://twitter.com/andrew_mason1/status/780946894226731009
[xally]: http://hyperboleandahalf.blogspot.com/2010/06/this-is-why-ill-never-be-adult.html
[mismatch]: http://stackoverflow.com/questions/8563978/what-is-kernel-section-mismatch
[oops]: https://en.wikipedia.org/wiki/Linux_kernel_oops
[loc]: http://arstechnica.com/business/2012/04/linux-kernel-in-2011-15-million-total-lines-of-code-and-microsoft-is-a-top-contributor/
[hotelcalifornia]: https://www.youtube.com/watch?v=G0ATsOXSPBw
[ep2]: {% post_url 2016-11-03-kernel-dev-ep2 %}
[ep3]: {% post_url 2016-11-14-kernel-dev-ep3 %}

---

#### Footnotes

[^fn-allie]:
    *Of course, all credit for the origin of the "use all the memory" image goes
    to Allie Brosh and her classic post
    [This is Why I'll Never be an Adult][xally]. Her whole blog is worth
    reading!*

[^fn-c]:
    Well, it's not surprising if you've spent much time using C. Most of the
    things you think are *rules* for programming C are actually *guidelines*,
    waiting to be broken without so much as a peep from the compiler.

[^fn-modpost]:
    Well, mostly. There is an output line from `make` that cryptically warns of
    a ["section mismatch"][mismatch]. But hey, as long as it compiles,
    everything is fine, amirite??
