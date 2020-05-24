---
layout: post
title: Implementing simple cooperative threads in C
description: |
  Using setjmp(), longjmp(), and assembly to implement a simple threading system
  in C!
---

Multitasking, like many services an operating system provides, is something we
take for granted so much that it can feel mundane. With our powerful smartphones
and computers, the idea of a computer _not_ being able to juggle hundreds of
processes feels alien. I think it's features like this that make computers
incredibly useful, but also make them feel so complicated and magical.

It's hard to play around with the code that implements multitasking, and it's
not obvious how to implement it yourself without building a whole OS. I'm a firm
believer that you don't truly understand something until you've implemented it
yourself, so I wanted to write an article that lets people play around with a
simple thread implementation. In this post, we'll implement simple threads in a
normal C program (not an operating system).

## Detour through setjmp and longjmp

This scheduler is going to rely heavily on the functions `setjmp()` and
`longjmp()`. They feel a bit magical, so I want to first describe what they do,
and spend a little time demystifying how they do it.

The function `setjmp()` is a way of recording information about where a program
is in its execution, so that you can later jump back to that point. You give it
a variable of type `jmp_buf`, in which it will store that information.
`setjmp()` returns 0 the first time it returns.

Later on, you can use the function `longjmp(jmp_buf, value)` to immediately
begin execution back at the point where you called `setjmp()`. To your program,
it will look like `setjmp()` returned a _second time._ The `value` argument you
pass to `longjmp()` will be returned this time, to help differentiate the second
return. Here's an example to help illustrate:

```c
#include <stdio.h>
#include <setjmp.h>

jmp_buf saved_location;
int main(int argc, char **argv)
{
    if (setjmp(saved_location) == 0) {
        printf("We have successfully set up our jump buffer!\n");
    } else {
        printf("We jumped!\n");
        return 0;
    }

    printf("Getting ready to jump!\n");
    longjmp(saved_location, 1);
    printf("This will never execute...\n");
    return 0;
}
```

If you compile and run this program, you will get the following output:

```
We have successfully set up our jump buffer!
Getting ready to jump!
We jumped!
```

Wild! It's like a goto statement, but it can even be used to jump outside of a
function. It's also a lot more difficult to read than a goto, since it looks
like a regular function call. If your code used `setjmp()` and `longjmp()`
liberally, it would be incredibly confusing for anyone (including yourself) to
read.

Like with goto, the common advice is to avoid `setjmp()` and `longjmp()`.
However, just like with goto, there are some times where it can be useful to use
sparingly, and in a consistent way. A scheduler needs to be able to switch
contexts, and so we'll have to use these functions responsibly. Most
importantly, we'll hide the use of these functions from our API, so that users
of our scheduler won't have to deal with that kind of complexity.

## Setjmp and longjmp don't save your stack

The `setjmp()` and `longjmp()` functions aren't designed to support just _any_
kind of jumping around, however. They're designed for a pretty particular use
case.  Imagine that you are doing something complicated, like making an HTTP
request.  This will involve a complicated set of function calls, and if any of
them fail, you'll need to return a special error code from each one of them.
This leads to code like this, everywhere you call a function (possibly dozens of
times):

```c
int rv = do_function_call();
if (rv != SUCCESS) {
    return rv;
}
```

The idea of `setjmp()` and `longjmp()` is that you can use `setjmp()` to save
your place just before starting something complex. Then, you could centralize
all of your error handling into one place:

```c
int rv;
jmp_buf buf;
if ((rv = setjmp(buf)) != 0) {
    /* handle errors here */
    return;
}
do_complicated_task(buf, args...);
```

If any function involved in `do_complicated_task()` fails, it would just
`longjmp(buf, error_code)`. This means that every function within
`do_complicated_task()` can assume that every function call is a success, which
means you can get rid of that error handling code for each function call. (In
practice, this is almost never done, but that's a separate blog post.)

The big idea here is that `longjmp()` only allows you to jump _out_ of deeply
nested functions. You can't jump back _into_ a deeply nested function which you
had formerly jumped out of. Here's an illustration of the stack when you jump
out of a function. The asterisk `(*)` marks the stack pointer which `setjmp()`
stored.

```
      | Stack before longjmp    | Stack after longjmp
      +-------------------------+----------------------------
stack | main()              (*) | main()
grows | do_http_request()       |
down  | send_a_header()         |
 |    | write_bytes()           |
 v    | write()  - fails!       |
```

You can see that we only move back up the stack, and so there is no risk of data
corruption. On the other hand, imagine if you wanted to jump between tasks. If
you call `setjmp()` and then return, do some other stuff, and then attempt to
resume what you were doing before, you'll have a problem:

```
      | Stack at setjmp() | Stack later      | Stack after longjmp()
      +-------------------+------------------+----------------------
stack | main()            | main()           | main()
grows | do_task_one()     | do_task_two()    | do_stack_two()
down  | subtask()         | subtask()        | subtask()
 |    | foo()             |                  | ???
 v    | bar()         (*) |              (*) | ???               (*)
```

The stack pointer which `setjmp()` saved will point at a stack frame which no
longer exists, and may have been overwritten at some point with other data. When
you try to `longjmp()` back into the function you have already returned from,
you'll start experiencing some really weird behavior that will probably crash
your program.

The moral of this story is that, if you want to use setjmp() and longjmp() to
jump between complex tasks like this, you need to make sure each task has _its
own separate stack._ This completely eliminates the problem, because when
`longjmp()` resets the stack pointer, it will swap stacks for you, and no stack
overwriting will take place.

## Let's make a scheduler API

That was a bit of a long diversion, but equipped with this knowledge, we should
be able to implement userspace threads. To start out, I found it quite helpful
to design the API which should be used to initialize, create, and run the
threads. Doing this ahead of time really helps understand what we're trying to
build!

```c
void scheduler_init(void);
void scheduler_create_task(void (*func)(void*), void *arg);
void scheduler_run(void);
```

These functions will be used to initialize the scheduler, add tasks, and then
eventually begin running tasks in the scheduler. Once we start
`scheduler_run()`, it will run until all tasks are completed. For tasks which
are running, they will have the following APIs:

```c
void scheduler_exit_current_task(void);
void scheduler_relinquish(void);
```

The first function will exit the task. A task could also exit by returning from
its function, so this is simply a convenience. The second function is how our
threads will tell the scheduler to let another task run for a bit. When a task
calls `scheduler_relinquish()`, it could be suspended a bit for a bit, while
other tasks run, but eventually the function will return and the task can
continue running.

To give a concrete example of the API, here's a hypothetical use of this API,
which we'll use to test our scheduler:

```c
#include <stdlib.h>
#include <stdio.h>

#include "scheduler.h"

struct tester_args {
    char *name;
    int iters;
};

void tester(void *arg)
{
    int i;
    struct tester_args *ta = (struct tester_args *)arg;
    for (i = 0; i < ta->iters; i++) {
        printf("task %s: %d\n", ta->name, i);
        scheduler_relinquish();
    }
    free(ta);
}

void create_test_task(char *name, int iters)
{
    struct tester_args *ta = malloc(sizeof(*ta));
    ta->name = name;
    ta->iters = iters;
    scheduler_create_task(tester, ta);
}

int main(int argc, char **argv)
{
    scheduler_init();
    create_test_task("first", 5);
    create_test_task("second", 2);
    scheduler_run();
    printf("Finished running all tasks!\n");
    return EXIT_SUCCESS;
}
```

In this example, we create two tasks which run the same function, but they'll
use different arguments so that we can trace their execution separately. Each
task iterates a set number of times. Each iteration, it prints out a message and
then lets another task run. We would expect to see something like this as the
output of this program:

```
task first: 0
task second: 0
task first: 1
task second: 1
task first: 2
task first: 3
task first: 4
Finished running all tasks!
```

## Let's implement the scheduler API

To implement this API, we'll need some sort of internal representation of a
task, so let's go ahead and put together fields we'll need:

```c
struct task {
    enum {
        ST_CREATED,
        ST_RUNNING,
        ST_WAITING,
    } status;

    int id;

    jmp_buf buf;

    void (*func)(void*);
    void *arg;

    struct sc_list_head task_list;

    void *stack_bottom;
    void *stack_top;
    int stack_size;
};
```

Let's go through the fields one by one. All tasks should be in the "created"
state as soon as they're created. Once a task starts executing, it will be in
the "running" status, and if a task ever needed to wait for some asynchronous
operation, it could be placed in the "waiting" state. The `id` field is just a
unique identifier for the task. `buf` contains the data for when we `longjmp()`
to resume the task. `func` and `arg` are passed to `scheduler_create_task()` and
are necessary for starting the task.  The `task_list` field is necessary to
implement a doubly linked list of all tasks. The `stack_bottom`, `stack_top`,
and `stack_size` fields all relate to the separate stack allocated for this
task. The "bottom" is the address returned by `malloc()`, but the "top" is a
pointer to the address directly above the region of memory. Since the x86 stack
grows downward, we will need to set the stack pointer to `stack_top` rather than
`stack_bottom`.

Given this, we can implement the `scheduler_create_task()` function:

```c
void scheduler_create_task(void (*func)(void *), void *arg)
{
    static int id = 1;
    struct task *task = malloc(sizeof(*task));
    task->status = ST_CREATED;
    task->func = func;
    task->arg = arg;
    task->id = id++;
    task->stack_size = 16 * 1024;
    task->stack_bottom = malloc(task->stack_size);
    task->stack_top = task->stack_bottom + task->stack_size;
    sc_list_insert_end(&priv.task_list, &task->task_list);
}
```

Using a `static int` ensures that each time the function is called, the `id`
field increments to a new number. Everything else should be self-explanatory,
except the `sc_list_insert_end()`, which simply adds the `struct task` to the
global list.  The global list is stored within a second structure, which
contains all the private scheduler data. This structure is presented below,
along with its initialization function:

```c
struct scheduler_private {
    jmp_buf buf;
    struct task *current;
    struct sc_list_head task_list;
} priv;

void scheduler_init(void)
{
    priv.current = NULL;
    sc_list_init(&priv.task_list);
}
```

The `task_list` field is used to refer to the list of tasks (unsurprisingly).
The `current` field is used to store the currently executing task (or null if
none is curently running). Most importantly, the `buf` field will be used to
jump into the code of `scheduler_run()`:

```c
enum {
    INIT=0,
    SCHEDULE,
    EXIT_TASK,
};

void scheduler_run(void)
{
    /* This is the exit path for the scheduler! */
    switch (setjmp(priv.buf)) {
    case EXIT_TASK:
        scheduler_free_current_task();
    case INIT:
    case SCHEDULE:
        schedule();
        /* if return, there's nothing else to do and we exit */
        return;
    default:
        fprintf(stderr, "Uh oh, scheduler error\n");
        return;
    }
}
```

As soon as the `scheduler_run()` function is called, we set the `setjmp()`
buffer so we can always return to this function. The first time, 0 (`INIT`) is
returned, and we immediately call `schedule()`. Subsequently, we can pass the
`SCHEDULE` or `EXIT_TASK` constants into `longjmp()`, which will trigger
different behaviors. Let's ignore the `EXIT_TASK` case for now, and go directly
into the implementation of `schedule()`:

```c
static void schedule(void)
{
    struct task *next = scheduler_choose_task();

    if (!next) {
        return;
    }

    priv.current = next;
    if (next->status == ST_CREATED) {
        /*
         * This task has not been started yet. Assign a new stack
         * pointer, run the task, and exit it at the end.
         */
        register void *top = next->stack_top;
        asm volatile(
            "mov %[rs], %%rsp \n"
            : [ rs ] "+r" (top) ::
        );

        /*
         * Run the task function
         */
        next->status = ST_RUNNING;
        next->func(next->arg);

        /*
         * The stack pointer should be back where we set it. Returning would be
         * a very, very bad idea. Let's instead exit
         */
        scheduler_exit_current_task();
    } else {
        longjmp(next->buf, 1);
    }
    /* NO RETURN */
}
```

First, we call an internal function to select the next task which should be run.
This is going to be a simple round-robin scheduler, so it just chooses the next
ready task in the task list. If this function returned NULL, then we have no
more tasks to run, and we return. Otherwise, we need to either start the task
running (if it is in the `ST_CREATED` state) or resume running it.

To start a created task, we use an x86_64 assembly instruction to assign the
`stack_top` field to the `rsp` register (stack pointer). Then we change the task
state, run the function, and exit if the function returns. Note that `setjmp()`
and `longjmp()` store and swap stack pointers, so this is the only time where
we'll need to use assembly to modify the stack pointer.

If the task has already been started, then the `buf` field should contain the
context we need to `longjmp()` into to resume the task, so we just do that.
Next, let's look at the helper function which selects the next task to run. This
is the heart of a scheduler, and like I said earlier, this is a round-robin
scheduler:

```c
static struct task *scheduler_choose_task(void)
{
    struct task *task;

    sc_list_for_each_entry(task, &priv.task_list, task_list, struct task)
    {
        if (task->status == ST_RUNNING || task->status == ST_CREATED) {
            sc_list_remove(&task->task_list);
            sc_list_insert_end(&priv.task_list, &task->task_list);
            return task;
        }
    }

    return NULL;
}
```

If you're unfamiliar with my linked list implementation (which is taken from the
Linux kernel), that's ok. The `sc_list_for_each_entry()` function is a macro
that lets us iterate over each task in the task list. The first eligible (not
waiting) task we find is removed from its current position and inserted at the
end of the task list. This ensures that next time we run the scheduler, we'll
get a different task (if there is another). We return this first eligible task,
or NULL if there were no tasks at all.

Finally, let's get to the implementation of `scheduler_relinquish()` to see how
a task can switch itself out:

```c
void scheduler_relinquish(void)
{
    if (setjmp(priv.current->buf)) {
        return;
    } else {
        longjmp(priv.buf, SCHEDULE);
    }
}
```

This is the other use of the `setjmp()` function in our scheduler. As such it
can be slightly confusing. When a task calls this function, we use `setjmp()` to
save our current context (which includes the current stack pointer). Then, we
use `longjmp()` to enter into the scheduler (back in `scheduler_run()`), and we
pass the `SCHEDULE` function asking to schedule a new task.

When the task gets resumed, the `setjmp()` function will return non-zero and
we'll return out to whatever the task was doing before!

Finally, here's what happens when a task exits (either by explicitly calling the
exit function, or by returning from its task function):

```c
void scheduler_exit_current_task(void)
{
    struct task *task = priv.current;
    sc_list_remove(&task->task_list);
    longjmp(priv.buf, EXIT_TASK);
    /* NO RETURN */
}

static void scheduler_free_current_task(void)
{
    struct task *task = priv.current;
    priv.current = NULL;
    free(task->stack_bottom);
    free(task);
}
```

This process comes in two parts: the first function is called directly by the
task. We remove the task's entry from the task list, since it should no longer
be scheduled. Then, we `longjmp()` back to the `scheduler_run()` function. This
time, we use `EXIT_TASK`. This indicates to the scheduler that, before it
schedules a new task, it should first call `scheduler_free_current_task()`. If
you scroll back up to `scheduler_run()`, you'll see this is exactly what
`scheduler_run()` does.

We have to do this in two parts because, when `scheduler_exit_current_task()` is
called, it is actively using the stack contained in the task struct. If you free
the stack while still using it, there's the chance that the function will still
access the very stack memory we just freed! To ensure this doesn't happen, we
have to `longjmp()` back to the scheduler, which is using a separate stack. Then
we can safely free the task's data.

With that, we've covered the entire implementation of this scheduler. If you
were to go ahead and compile this, along with my linked list implementation and
the main program above, you would have a working scheduler! Instead of all that
copying and pasting, I'd encourage you to check out the [github
repository][repo] which contains all this code.

## Why is this useful?

If you've gotten this far, I assume I don't need to convince you that this is
interesting. However, it may not seem all that useful. After all, you can use
"real" threads in C, which can run in parallel and don't need to wait for each
other to call `scheduler_relinquish()`.

However, I see this as a jumping off point for a whole series of exciting
implementations of useful features. For I/O heavy tasks, this could also be used to
simply implement a single-threaded async application, the way that Python's new
async utilities work. This system could also implement generators and
coroutines. Finally, with enough effort, this system could even be coupled with
"real" operating system threads to provide more parallelism where necessary.
Each of these ideas is a fun project which I'd encourage the reader to try
before I get around to writing a new article about them!

## Is it safe?

I mean, probably not! It's probably not safe to use inline assembly to modify
the stack pointer. Don't use it in your production code, but do use it to mess
around and explore!

A safer implementation of this system could be built on the "ucontext" API (see
`man getcontext`), which provides a way to swap between these types of userspace
"threads" without needing to meddle with inline assembly. Unfortunately, the API
is non-standard (it was removed from the latest POSIX spec). However, you can
still use this API, as it is part of `glibc`.

## How to make it preemptive?

As it is currently written, this scheduler only works if threads explicitly hand
off control back to the scheduler. This is bad for a general purpose
implementation like an operating system, because a poorly behaved thread could
prevent all the others from running. (Of course, that didn't stop MS-DOS from
using cooperative multitasking!). I don't think that makes cooperative
multitasking bad, it's just going to depend on the application.

If one used the non-standard "ucontext" API, then POSIX signals would actually
store the context of the previously executing code. By setting a periodic timer
signal, a userspace scheduler could actually get preemptive multitasking
working! This is another really cool project that I hope to try out and write
about soon.

If you've gotten this far, thanks for reading, and I hope you get the chance to
try out a fun project based on this!

[repo]: https://github.com/brenns10/userspace_cooperative_multitasking
