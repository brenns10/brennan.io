---
layout: post
title: "Build your own OS: Pre-emptive Multitasking"
description: "Build your own OS: Pre-emptive Multitasking"
---

One of my recent long-running projects has been building my own operating
system. It's called [SOS][sos], for Stephen's OS (real creative, I know). And
beyond all odds, this project has progressed really well! Recently, SOS got the
ability to do _pre-emptive multitasking_ --- and it only took me 116 commits and
1.5 years of on-and-off effort to get there! Throughout that time, I haven't
really posted about SOS because it felt too complicated to write about. But I
don't want to let that prevent me from trying, so starting with this newest
achievement, I'm going to try to post about different features and achievements
with SOS. To start, this post will describe how I got pre-emptive multi-tasking
working.

### What is pre-emptive multitasking?

An OS kernel's primary job is to manage resources, and one of the most basic
resources to manage is the CPU. The OS needs to be able to allow every program
to "have a turn" executing on the CPU. This means that it needs to be able to
run a process for some time, but then pause its execution and allow another
process to continue. Beyond simply allocating CPU time, this also gives the
illusion of several programs running in parallel, even though only one can ever
be running on one CPU at a time.

The challenge is that most programs are not written to be considerate of other
running programs by pausing their own execution. And even if they were, it
would only take one buggy or malicious program to starve the rest of the
programs of CPU time. So the OS needs a way to pause the execution of a program
without its cooperation.  This is where the _timer_ comes in. Timers tick at a
regular interval, and can be configured to trigger an interrupt after a certain
number of ticks. This interrupt will pause whatever the CPU is doing, giving the
OS the opportunity to let another process use the CPU.

### Enabling timer interrupts on ARM

When I began implementing timer interrupts in SOS, the OS already supported
multiple processes. The were able to make system calls, and could "cooperatively
multitask" by calling a `relinquish()` system call which would allow the OS to
schedule another process. I wanted to switch to the pre-emptive multitasking
model by enabling timer interrupts and allowing the OS to schedule new processes
during the interrupt.

SOS targets the ARMv7-A architecture. While it is "optional", the architecture
includes the "ARM Generic Timer". You can read all about it in Chapter B8 of the
[reference manual][armv7-ref]. This timer consists of five registers:

- `CNTFRQ` - a 32-bit read-only register containing the frequency of the timer.
- `CNTPCT` - a 64-bit read-only register containing the current value of the
  timer, incrementing on each tick.
- `CNTP_CVAL` - the CompareValue register, a 64-bit register which is compared
  against `CNTPCT`, triggering an interview when both are equal.
- `CNTP_TVAL` - the TimerValue register, a 32-bit register which counts downward
  and causes an interrupt when it reaches 0.
- `CNTP_CTL` - the Control register, which enables and disables the timer.

With that information, I created this initialization function for the timer:

```c
#define HZ 100

void timer_init(void)
{
	uint32_t dst;

	/* get timer frequency */
	GET_CNTFRQ(dst);

	/* Set timer tval to tick at appx HZ per second, by dividing the
	 * frequency by HZ */
	dst /= HZ;
	SET_CNTP_TVAL(dst);

	/* Enable the timer */
	dst = 1;
	SET_CNTP_CTL(dst); /* enable timer */

	gic_enable_interrupt(30u);
}
```

Each `GET_` and `SET_` macro expands to a special ARM assembly instruction which
loads the value of these registers into (or stores the value from) the variable
given as argument. For example:

```
# Load CNTFRQ register into register v1 (the dst variable).
# Each additional argument beyond "v1" identifies the register CNTFRQ from
# the generic timer -- these values can be found in the architecture
# reference manual.
mrc p15, 0, v1, c14, c0, 0
```

I wanted to have the interrupt trigger 100 times per second, so I defined that
as the constant `HZ`. This value effectively subdivides CPU time into 100
slices per second.  We divide the frequency by this value to determine the
number of timer ticks to wait until the interrupt to fire. We set this into the
TimerValue register, which will count down and fire an interrupt when it hits
zero. Finally, we set the control register to the value 1. This value enables
the timer and ensures that the interrupt will be delivered to the CPU.

The final line, `gic_enable_interrupt(30u)`, enables the timer interrupt in the
"Generic Interrupt Controller." While not the subject of this blog post, the GIC
allows the CPU to enable and manage interrupts from multiple sources. The number
30 is the interrupt identifier which belongs to the timer. In a more mature
operating system, it would likely be detected automatically via the [Device
Tree][dtree], but for the purposes of getting this working, I've hard-coded it.

### Handling the timer interrupt

Once the timer interrupt is configured, we know that an interrupt will fire in
1/100th of a second, so we need to have an interrupt handler configured for it.
For the ARMv7-A architecture, when an interrupt is triggered, the CPU saves a
few pieces of state, and immediately jumps and begins executing instructions
from address 0x18. From there, the SOS interrupt handler does a few critical
steps:

1. Store the CPU's return state onto a stack dedicated for interrupt handling.
   The return state includes the address of the instruction which we will
   continue executing once the interrupt has finished being handled.
2. Push all the registers which the interrupted process could have been using
   onto the stack.
3. Branch into a C function which will continue handling the interrupt.
4. On return, restore all of this state from the stack, and return to the
   interrupted instruction.

Let's take a closer look at the C function which handles the interrupt:

```c
void irq(void)
{
	uint32_t intid = gic_interrupt_acknowledge();

	if (intid == 30) {
		timer_isr(intid);
	} else if (intid == 33) {
		uart_isr(intid);
	} else {
		printf("Unhandled IRQ: ID=%u, not ending\n", intid);
	}
}
```

The `gic_interrupt_acknowledge()` function reads a special register from the
interrupt controller, which tells us which interrupt ID triggered the exception.
Again, if the OS were more mature, we could have dynamically looked up which
interrupt corresponded to which device, but I hard-coded it here as well.

Since many devices other than the timer could interrupt the processor (such as
the UART, which is also handled here), we need to check this interrupt ID and
pass control onto the timer if this was a timer interrupt. Here is the
`timer_isr()` function (here ISR stands for "Interrupt Service Routine"):

```c
void timer_isr(uint32_t intid)
{
	uint32_t reg;

	/* Reset timer to go off in another 1/HZ second */
	GET_CNTFRQ(reg);
	reg /= HZ;
	SET_CNTP_TVAL(reg);

	/* Ensure the timer is still on */
	reg = 1;
	SET_CNTP_CTL(reg);

	/* Interrupt should now be safe to clear */
	gic_end_interrupt(intid);

	get_spsr(reg);
	reg = reg & ARM_MODE_MASK;
	if (reg == ARM_MODE_USER || reg == ARM_MODE_SYS) {
		/* We interrupted sys/user mode. This means we can go ahead and
		 * reschedule safely. */
		schedule();
	}
}
```

Right off the bat, we do the same thing we did when we initialized the timer:
set it to go off in another hundredth of a second, and ensure it is still
enabled. The next thing we do is use `gic_end_interrupt()`, which writes the
interrupt ID to another special register in the interrupt controller, informing
it that we've handled the interrupt.  At this point, we've done all the hardware
housekeeping necessary to manage the timer interrupt and keep it ticking on at
100Hz (roughly). We can now turn to the reason we enabled the timer to begin
with: implementing pre-emptive multi-tasking.

Since the interrupt began, the pre-empted process has had all of its state
pushed to the stack, and the state will be restored when we return. All we
should need to do is swap out that state with a _different process's state,_ and
that new process would be resumed instead. However, there's a catch! We're not
guaranteed that what was interrupted is _even a user-space process._ Interrupts
can happen at any time, and it's possible that the code which was interrupted
was actually the kernel itself, while it was running a system call. Since the
kernel is not a process, SOS's context switching system can't simply swap it
out. To ensure that we only swap out processes (and kernel threads, which are
implemented as processes too), we check to see what mode the process we
interrupted was in. If we interrupted something in user mode (i.e. a process) or
system mode (i.e. a kernel thread), then we are safe to schedule a new process.
However, if we interrupted supervisor mode (i.e. a system call) then we simply
return.

### Scheduling & Beyond

At this point, we've seen the timer initialization, and we've seen the code that
runs (100 times per second!) to handle the interrupt. When the interrupted code
is a process, we call into the scheduler, which will select a new process and
resume that one instead. SOS currently uses a simple round-robin scheduler, and
I hope to write an article about that soon as well.

Hopefully this has been an interesting dive into the timer interrupt and
implementing pre-emptive multiprocessing. I've simplified things a bit, to make
this a quick article. Here's a peek at some of the extra complexity I left out:

1. I didn't really touch on the assembly code to save and restore process state.
   This code is superficially simple, but very fragile and requires lots of
   tweaking to get right. If you grab the [SOS source][sos] you can see it in
   `kernel/entry.s`.
2. Processes also can be suspended by making system calls. For example, using
   the `relinquish()` system call I described above, or if it's waiting for user
   input. When I implemented pre-emptive multitasking, I had to revisit a lot of
   code to make sure that process context switching could support both
   interrupts and system calls.
3. System calls run in a different mode (superviser mode) than interrupts (IRQ
   mode). Each of these modes uses a different stack. So the code which knows
   how to context-switch needs to be able to find the stored context we pushed
   on the stack, regardless of the mode.
4. If we interrupted the kernel as it performs a system call, then we won't
   schedule a new process. This means that whichever process made the system
   call will get an extra time slice. This is pretty unfair, and I haven't yet
   addressed this unfairness.
5. Sometimes there are no processes available to schedule, and so the CPU needs
   to idle. I went ahead and implemented a whole "idle process" just to satisfy
   this need.

If you are interested in seeing more about this operating system, please check
it out [on Github][sos] and look out for more articles about its innards!

[sos]: https://github.com/brenns10/sos
[armv7-ref]: https://static.docs.arm.com/ddi0406/c/DDI0406C_C_arm_architecture_reference_manual.pdf
[dtree]: https://en.wikipedia.org/wiki/Device_tree
