---
layout: post
title: Unwinding a Stack by Hand with Frame Pointers and ORC
description: |
  My article, posted on the Oracle Linux Blog, goes in depth on how the Linux
  kernel creates stack traces at runtime. It describes the common frame pointer
  approach, as well as the newer approach for x86_64 called ORC, which allows
  omitting the frame pointer, thus improving system performance.
---

My [article][post], posted on the Oracle Linux Blog, goes in depth on how the
Linux kernel creates stack traces at runtime. It describes the common frame
pointer approach, as well as the newer approach for x86_64 called ORC, which
allows omitting the frame pointer.

If you enjoy my writing here, then you'll enjoy this post as well. Please [check
it out!][post]

[post]: https://blogs.oracle.com/linux/post/unwinding-stack-frame-pointers-and-orc
