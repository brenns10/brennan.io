---
title: Projects
layout: contentbase
gh: <span class="fa fa-github fa-lg"></span>
bb: <span class="fa fa-bitbucket fa-lg"></span>
web: <span class="fa fa-globe fa-lg"></span>
pdf: <span class="fa fa-file-pdf-o fa-lg"></span>
tw: <span class="fa fa-twitter fa-lg"></span>
---


# Publications

### Improving Communication Through Overlay Detours: Pipe Dream or Actionable Insight?

_Stephen Brennan & Michael Rabinovich_, IEEE International Conference on
Distributed Computing Systems, July 2018.

This paper describes "Detour Collectives" or DCol, a system which allows gigabit
users to use Multipath TCP to add detour routes to normal TCP connections. This
can enable you to achieve better throughput by circumventing bottlenecks in the
Internet's default routes. This paper builds on the previous work in my Master's
Thesis.

[{{page.pdf}} Read the paper](/papers/dcol.pdf)

### Exploring Alternative Routes Using Multipath TCP

My master's thesis! You can find my page about it [here](/thesis).

# Course Projects

### DPath---Filesystem Querying with XPath

A tool written in Go that allows you to query your filesystem using XPath. This
was a project for my EECS 433 Database Systems course in the fall of 2016.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/dpath)  
[{{page.pdf}} Read the report](/papers/dpath_report.pdf)

### YAMS: Awesome MIPS Server

My EECS 314 project group (Jeff Copeland, Andrew Mason, Thomas Murphy, Katherine
Cass, Aaron Neyer, and myself) created a HTTP 1.0 web server, written entirely
in MIPS assembly.  In addition to serving static pages, it also comes with
"dynamic content" courtesy of a
[Brainf***](https://en.wikipedia.org/wiki/  Brainfuck) interpreter also written in
assembly.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/yams)  
[{{page.web}} Read the blog post]({% post_url 2015-05-17-yams %})  
[{{page.pdf}} Read the report](/papers/yams_report.pdf)

### PyWall---A Python Firewall

My EECS 444 project group (Jeff Copeland, Andrew Mason, Yigit Kucuk) implemented
a firewall in Python.  While obviously not practical for normal use, this
firewall illustrates the basics of packet filtering (including TCP connection
tracking) in a high-level lanugage, which is much easier to understand and
extend than C.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/pywall)  
[{{page.pdf}} Report](/papers/pywall_report.pdf)

# Personal Projects

### Funlisp

An implementation of a small but mighty lisp in standard C89, portable to any
POSIX compliant operating system.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/funlisp)  
[{{page.web}} Read the docs](https://funlisp.readthedocs.io)

### CWRU Love---Web Service for Spreading Love

I've launched a version of the
open-source [Yelp Love](https://www.yelpblog.com/2017/02/need-yelp-love) for
students, faculty, staff, and alumni of my school. This web application lets
users send short notes of appreciation (aka "love") to each other. In addition
to setting up our version of the web service on Google Appengine, I've been
contributing features and bugfixes back to Yelp's open source project.

[{{page.gh}} CWRU Love](https://github.com/hacsoc/love)  
[{{page.gh}} Yelp Love](https://github.com/Yelp/love)  
[{{page.web}} Blog Post]({% post_url 2017-02-19-cwru-love %})  
[{{page.web}} Try it out (must be affiliated with CWRU)](https://cwrulove.appspot.com)

### KChat---In-Kernel Chat Server

A kernel module that implements a special device file that allows everyone with
a file open to send each other messages in real time, like a chat server. If you
think about it, it is acutally an IPC mechanism. Whatever you call it, it's a
lot of fun.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/kchat)

### PySwizzle---A Twitter Bot

[Hacker's Society](http://hacsoc.org) hosted an event called "Python and Pie"
for incoming freshmen during Fall 2015 orientation.  I gave an intermediate
Python tutorial, which was all about writing a Twitter bot using Python.  As a
result, this bot and the accompanying tutorial are now on GitHub for others to
learn from.  The bot responds to any @mention with a randomly chosen Taylor
Swift lyric.

[{{page.gh}} Code and Tutorial at GitHub](https://github.com/brenns10/pypie15int)  
[{{page.gh}} Latest Version at GitHub](https://github.com/brenns10/pyswizzle)  
[{{page.web}} Blog Post]({% post_url 2015-08-22-python-and-py %})  
[{{page.tw}} Tweet at the Bot](https://twitter.com/pyswizzle)

### A Simple Shell in C

I wrote this to illustrate the different system calls and mechanics that
underlie one of a programmer's fundamental tools: the shell.  I also wrote a
tutorial about it.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/lsh)  
[{{page.web}} Read the tutorial]({% post_url 2015-01-16-write-a-shell-in-c%})

### Tetris in C!

A 24 hour Tetris implementation written in C, using the `ncurses` library.  I
wrote an accompanying blog post about it, which also touched on how important I
find my personal projects, even if some are reimplementations.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/tetris)  
[{{page.web}} Read the blog post]({% post_url 2015-06-12-tetris-reimplementation %})

### Libstephen

This library extends the standard C library with dynamic lists, hash tables,
regular expressions, command line argument parsing, several string-handling
utilities, logging, and lightweight unit testing.  It's an experiment in making
an API as well as sharing code.  Several of my other C projects depend on it
already.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/libstephen)  
[{{page.web}} Documentation and Code Coverage](/libstephen/)

### NOSJ---A JSON Library in C

NOSJ is a simple JSON parser written in C.  It focuses on simplicity, especially
with respect to memory allocation.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/nosj)  
[{{page.web}} Documentation and Code Coverage](/nosj/)

### tswift---A Python MetroLyrics API

Get your Taylor Swift lyric fix with this quick'n'dirty tool for downloading
song lyrics from MetroLyrics.  Or, you know, any other artist's lyrics.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/tswift)  
[{{page.web}} It's on PyPI!](https://pypi.python.org/pypi/tswift)

### CBot---IRC Bot in C

A fun little challenge - write a functioning IRC bot in C!  This little guy was
a great excuse to use Libstephen's regular expressions in the real world, as
well as learn all about dynamic loading of modules and the IRC protocol.  CBot
currently has the basic functions necessary for a chatbot, and I'm sure I'll
return every now and then to expand on his available plugins.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/cbot)

### Minesweeper

A minesweeper game written entirely in C, with both a command line and graphical
interface.  This was a fun and short project to apply my C knowledge, as opposed
to my more ambitious, long running projects above.

[{{page.gh}} Visit it at GitHub](https://github.com/brenns10/minesweeper)

[Jeff Copeland]: https://github.com/jpcjr
[Kyle Deal]: https://github.com/dealie16
