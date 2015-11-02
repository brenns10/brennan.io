---
title: Spooky Garbage Collection
layout: post
description: An introduction to a scary topic - garbage collection!
keywords: c programming garbage collection
---

Since Halloween was a few days ago, I wanted to write about a spooky topic:
implementing garbage collection!  I say spooky because garbage collection is one
of those ubiquitous things that programmers use, but some may not understand
(like [shells][how-to-write-a-shell]).  I'm a fan of demystifying these sorts of
things, so I thought I'd share some of the experience I gained implementing it.

## Intro to Garbage Collection

A quick refresher on garbage collection: Let's imagine that you're implementing
a programming language interpreter in C.  Say, your own implementation of a
[Lisp][lisp].  When code executes, it will use memory resources.  It will have
strings, numbers, functions, and more, and all of that will need to reside
somewhere in memory.  More importantly, when the program is done with those
resources, it will want to use the space they took up for other things.  In
programming languages like C, the programmer has to explicitly request and
release memory.  But in programming languages like Lisp (and Python, and Java,
etc.), the programmer doesn't have to think about it.  Unfortunately, that means
that you, the creator of this interpreter, will have to do the thinking for the
programmers.  You will have to come up with a system that will detect when
program resources are no longer being used, and free them up.  This is called
garbage collection.

There are two main techniques people use to implement garbage collection.  The
first one is called reference counting, and the second one is called
mark-and-sweep.  I'm not going to talk about mark-and-sweep in this article, but
the idea is pretty simple.  At any point when you're running a program, you know
what variables are in scope.  You can simply look at all the resources the
program has, find all of the ones that are reachable from the variables in
scope, and free up the rest.  This approach is guaranteed to eliminate
everything that is unneeded, but it requires you to "pause" the program while
you separate out the reachable resources from the unreachable ones.
Mark-and-sweep is used by Java.

The technique I'm going to demonstrate is reference counting.  Here's the idea
behind it.  Every memory resource that a program uses will be given a "reference
count."  The reference count represents the number of different places where
that resource is being used (or "referenced").  Whenever some code is done using
a memory resource, it subtracts one from its reference count.  When the
reference count reaches zero, this means nothing is using the memory any more,
so it can be freed.  Reference counting has the advantage that unused memory can
be freed as it becomes unused, and so you don't need to "pause" the program to
find unused memory.  Unfortunately, there is at least one downside to reference
counting, which I will explain at the end of this post.

## Implementation of Reference Counting

Now that we have a pretty good understanding of reference counting, let's dive
into some C code that would allow our hypothetical Lisp interpreter to use
reference counting garbage collection.  First, let's create a struct that will
be included at the top of every data type in the programming language (think of
it like a base class):

```c
struct lisp_value {
  struct lisp_type *type;
  unsigned int refcount;
};
```

Both items are necessary for our garbage collection system!  The `refcount`
variable does exactly what you'd expect -- it holds the number of things that
own references to this object.  As you might expect, this count always starts at
one.  It's unsigned because it'll never be negative -- as soon as it becomes
zero, the object will be freed.

But how do you free an object you don't know anything about?  At first, you
might think you could just call `free()` on the pointer and be done with it.
That works for something like an integer, but what if it's a linked list?  In
that case, you'd have to also decrement the reference count of the object stored
in the linked list node, and then do the same for each subsequent linked list
node!  Now, it seems clear that we can't write a `free()` routine that would
work on every possible data type in our Lisp.  That's where the `type` pointer
in the `struct lisp_value` comes in.  Here is what we define a `struct
lisp_type` to be:

```c
struct lisp_type {
  const char *tp_name;
  lisp_value* (*tp_alloc)(void);
  void (*tp_dealloc)(lisp_value*);
  void (*tp_print)(lisp_value*, FILE *, int);
};
```

This struct is really handy.  It contains, among other things, a pointer
(`tp_dealloc`) to a function that knows how to free objects of some type.  We
can create one (static) instance of this struct for each type we define.  We put
the implementation of the type's `tp_dealloc()` routine in the struct, and then
put a pointer to this struct into each instance of that type.  Now, for any
`lisp_value`, we know how to free it: just look for the `tp_dealloc()` function
in its type object!

In case this was a bit confusing, let's get concrete.  Let's look at an integer
type:

```c
struct lisp_int {
  lisp_value lv;
  long int value;
};
```

The first element of the struct includes our `lisp_value` "base class" (i.e.,
the refcount and pointer to type object).  The second element is the integer
value.  Now, here is what the definition of the type object looks like:

```c
struct lisp_type tp_int = {
  .tp_name = "int",
  // one function to allocate them:
  .tp_alloc = &lisp_int_alloc,
  // one function to free them:
  .tp_dealloc = &generic_dealloc,
  // one function to print them:
  .tp_print = &lisp_int_print
  // ... and in the darkness, bind them
};
```

Whenever we create a new instance of an integer (say, in `lisp_int_alloc()`), we
simply set the `refcount` and `type` fields correctly:

```c
static struct lisp_value *lisp_int_alloc(void)
{
  struct lisp_int *rv = malloc(sizeof(struct lisp_int));
  rv->lv.type = &tp_int; // ptr to type object!
  rv->lv.refcount = 1; // the caller owns a reference
  rv->value = 0;
  return (struct lisp_value *)rv;
}
```

So long as we do this for every type we define in our language, we know that
every object's lifetime can be managed through the reference counting system.
All you have to do from here is use functions like these to increment and
decrement reference counts:

```c
void lisp_incref(struct lisp_value *lv)
{
  if (lv == NULL) return;
  lv->refcount += 1;
}

void lisp_decref(struct lisp_value *lv)
{
  if (lv == NULL) return;
  lv->refcount -= 1;
  if (lv->refcount == 0) {
    // use the type object's function pointer to free it:
    lv->type->tp_dealloc(lv);
  }
}
```

As a side note, the strategy of creating "type" objects with pointers to
functions is a solid way to start implementing a lot of high level programming
language features.  This is one of the few good ways of achieving "dynamic
dispatch" (not knowing what function you're calling until runtime) for objects
in C.  Dynamic dispatch is one of the important pieces of an object oriented
programming language.  So if you ever wanted to implement an object oriented
programming language with C, chances are you should start with type objects
similar to these!

## Reference Counting Semantics

You may think that we're done now.  After all, we have objects we know we can
always free, and we have functions to update reference counts and free objects
when we no longer need them.  But one major question remains to be answered:
"when do we increment and decrement reference counts?"  This is pretty critical;
if you mess up your reference counting, one of two things will happen:

- Your reference count is too high, and you end up never freeing that object.
  This is a "memory leak", and if it happens too frequently, your program will
  run out of memory and crash.  Not good!
- Your reference count is too low, and you end up freeing objects too early.
  Later (probably well after the *actual* error), your program will try to to
  use the prematurely freed object, resulting in a segmentation fault.  This is
  also very bad, and a nightmare to debug.

Sadly, there's no real "automatic" way to get it right.  The best way to avoid
these errors is by creating a standard set of rules for dealing with reference
counts, and then following them rigidly.  Here are rules that I use:

- No code "owns" an object.  It may only own a reference to an object.
- Any data structure that contains an object *must* own a reference to it.
- When a function is called with a reference to an object, it can (*usually*)
  use that reference to do whatever it would like, without incrementing or
  decrementing reference counts.  In essence, it "borrows" the reference that
  its caller owns.
    - The exception to this rule would be when the function stores the reference
      in a data structure.  Then, as mentioned in the second rule, the object
      must be incref'd to show that the data structure owns a reference.
- Whenever a function "evaluates" an expression, it returns a *new* reference to
  the expression result.

These rules are actually remarkably similar to the [rules][py-refcount] used by
Python's standard implementation, CPython.  In fact, my entire implementation of
reference counting is based on CPython's implementation!  So if you really want
to learn more, you should check out the CPython source.  I learned a ton by
working on a C extension to the interpreter, and I highly recommend that as a
learning experience!

## Downside of Reference Counting

Unfortunately, there is one major downside to reference counting.  The downside
is that there are some ways that you can "fool" simple reference counting into
not freeing memory that is unused.  Here is an example of Python code that would
"fool" a simple reference counter:

```python
def some_function():
    person_a = Person('Stephen')
    # person_a now owns a reference to Stephen (count=1)
    person_b = Person('Tyler')
    # person_b now owns a reference to Tyler (count=1)
    person_a.friend = person_b
    # now, Stephen owns a reference to Tyler (count=2)
    person_b.friend = person_a
    # similarly, Tyler now owns a reference to Stephen (count=2)
    return
    # person_a and person_b go out of scope, so Stephen and Tyler now have count=1
```

As you can see, at the end of this function, "Stephen" and "Tyler" are unused,
and should be gotten rid of.  But since they own references to each other, their
reference counts never reach zero, and they never get freed.  There are ways of
fixing this problem (for instance, CPython has a fix for this issue), but for
this article, I'll leave it to your (and my) imagination how to do it.

## Conclusion

You know how this whole time I was writing code for a "hypothetical" Lisp
interpreter?  Turns out, it's not really hypothetical.  All this code is taken
from my [lisp][gh-link] project on GitHub.  You should really check that out,
because then you can see this simple reference counting code in action!

**Easter Egg:** There is currently at least one memory leak in my Lisp
  implementation (as of commit `c99f4b5345ec651c9d6cd51358e2d9595c71c356`).  See
  if you can find it!  My only hints:
  - It has something to do with the `(define ...)` function.
  - You may find `valgrind` incredibly useful for this sort of debugging,
    especially with the option `--leak-check=full`.

[how-to-write-a-shell]: {% post_url 2015-01-16-write-a-shell-in-c %}
[lisp]: https://en.wikipedia.org/wiki/Lisp_%28programming_language%29
[py-refcount]: https://docs.python.org/3.5/extending/extending.html#reference-counts
[gh-link]: https://github.com/brenns10/lisp
