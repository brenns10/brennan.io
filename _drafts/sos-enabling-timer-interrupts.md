---
layout: post
title: "Build your own OS: Enabling Timer Interrupts"
description: "Build your own OS: Enabling Timer Interrupts"
---

One of my recent long-running projects has been building my own operating
system. It's called [SOS][sos], for Stephen's OS (real creative, I know). And
beyond all odds, this project has progressed really well! As of recently, my
operating system is able to run several processes at the same time, context
switching periodically between them, to provide the illusion of concurrency.
This is how modern operating systems manage running multiple processes in
parallel, even if there's just one CPU. It's called "pre-emptive multitasking",
and it only took me 116 commits and 1.5 years of on-and-off effort to get there!

Something I've realized is that this project has been a pretty quiet one. I
haven't written much about it on this blog. Operating systems are difficult to
"show off". A properly written OS is unexciting; it runs programs and has no wow
factor. What's more, it's difficult to write about operating systems without
trying to explain _everything from the beginning_, which is far too much to
explain.

However, I really want to share this project, so I'm going to try to start
writing about small components about it, in shorter, digestible posts. I'll
start with enabling timer interrupts.

---

### Why do we need timer interrupts?

An OS kernel's primary job is to manage resources, and one of the most basic
resources to manage is the CPU. The OS needs to be able to let a program run for
a while, but then pause its execution and allow other programs to get their fair
share of CPU time. This gives the illusion of several programs running in
parallel, even though only one can ever be running at a time.

But most programs are not written to be considerate of other running programs by
pausing their own execution. (And even if they were, it would only take one
buggy or malicious program to starve the rest of the programs of CPU time). So
the OS needs a way to pause the execution of a program without its cooperation.
This is where the timer comes in. Timers tick at a regular interval, and can be
configured to trigger an interrupt after a certain number of ticks. This
interrupt will pause whatever the CPU is doing, giving the OS the opportunity to
let another process use the CPU.

### Enabling timer interrupts in SOS

When I began implementing timer interrupts in SOS, the OS already supported
multiple processes, using system calls. Processes could "cooperatively
multitask" by calling a `relinquish()` system call which would allow the OS to
schedule another process. I wanted to switch to the pre-emptive multitasking
model by enabling timer interrupts and allowing the OS to schedule new processes
during the interrupt.

SOS targets the ARMv7-A architecture. While it is "optional", the architecture
includes the "ARM Generic Timer". You can read all about it in Chapter B8 of the
[reference manual][armv7-ref]. This timer consists of three registers:

- `CNTFRQ` - a 32-bit read-only register containing the frequency of the timer.
- `CNTPCT` - a 64-bit read-only register containing the current value of the
  timer.
- `CNTP_CVAL` - the CompareValue register, a 64-bit register which is compared
  against `CNTPCT`, triggering an interview when both are equal.
- `CNTP_TVAL` - the TimerValue register, a 32-bit register which counts downward
  and causes an interrupt when it reaches 0.
- `CNTP_CTL` - the Control register, which enables and disables the timer.

This is the initialization function I created for the timer:

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
given as argument.

I wanted to have the interrupt trigger 100 times per second, so I defined that
as the constant `HZ`. This value effectively subdivides CPU time into 100
slices per second.  We divide the frequency by this value to determine the
number of timer ticks to wait until the interrupt to fire. We set this into the
TimerValue register, which will count down and fire an interrupt when it hits
zero. Finally, we set the control regester to the value 1. This value enables
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
few pieces of state, and immediately jumps to address 0x18. From there, the SOS
interrupt handler does a few critical steps:

1. Store the CPU's return state onto a stack which was previously configured to
   be used just for interrupt mode. This includes the address of the instruction
   which we will continue executing once the interrupt has finished being
   handled.
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
interrupt controller, which tells us which interrupt ID triggered this. Again,
if the OS were more mature, we could have dynamically looked up which interrupt
corresponded to which device, but I hard-coded it here as well.

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
should need to do is swap out that state with a different process's state, and
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
resume that one instead. The details of the scheduler get into an entirely
separate area of SOS, but here are some broad strokes to give you an idea what
happens next:

- The scheduler is a simple round-robin algorithm, which means that each
  currently running process gets a turn in order, until we get back to the first
  one. This is pretty easy to implement, but leaves some room to improve in
  terms of fairness. Hopefully I can write more about that in another post.
- Not all processes are ready to run. Some could be waiting for something to
  happen. If the only process ready to run is the one we interrupted, then we'll
  just continue running that one.
- Sometimes, it can happen that no processes are ready to run. In this case, we
  need to idle the processor until a process becomes ready to run.

Hopefully this has been an interesting dive into the timer interrupt and
implementing pre-emptive multiprocessing. I've simplified things a bit to fit
into this article. Here are some issues which I've left out, but which do need
to be considered in a full implementation:

1. Processes also can be interrupted by system calls. Sometimes, a system call
   needs to block a process (for example, if a process wants to read from the
   console, but the user hasn't typed anything yet). So, we need to be able to
   context switch processes in which had been paused by a syscall, and vice
   versa.
2. System calls run in a different mode (superviser mode) than interrupts (IRQ
   mode). Each of these modes uses a different stack. So the code which knows
   how to context-switch needs to be able to find the stored context we pushed
   on the stack, regardless of the mode.
3. If we interrupted a system call, then we won't schedule a new process. This
   means that whatever process the syscall was executing on behalf of will get
   an extra time slice. This is pretty unfair.

[sos]: https://github.com/brenns10/sos
[armv7-ref]: https://static.docs.arm.com/ddi0406/c/DDI0406C_C_arm_architecture_reference_manual.pdf
[dtree]: https://en.wikipedia.org/wiki/Device_tree
