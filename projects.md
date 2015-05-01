---
title: Projects
layout: contentbase
---
# Projects

## Future

### Using Prior Biological Information to Select Features for Predicting Cancer Phenotypes

This is a 10-week bioinformatics research project scheduled for the summer
of 2015.  I will be working in conjunction with Dr. Mehmet Koyuturk to develop
an algorithm for selecting combinations of somatic mutations which are
correlated with cancer phenotypes.

[View the Proposal](https://dl.dropboxusercontent.com/u/24472738/proposal.pdf)

## Current

### `PyWall` -- A Python Firewall

My EECS 444 project group (Jeff Copeland, Andrew Mason, Yigit Kucuk) implemented
a firewall in Python.  While obviously not practical for normal use, this
firewall illustrates the basics of packet filtering (including TCP connection
tracking) in a high-level lanugage, which is much easier to understand and
extend than C.

A GitHub link will be available once the project report is graded, sometime
after April 27.

### `yams` -- YAMS: Awesome MIPS Server

My EECS 314 project group (Jeff Copeland, Andrew Mason, Thomas Murphy, Katherine
Cass, Aaron Neyer, and myself) created a HTTP 1.0 web server, written entirely
in MIPS assembly.  In addition to serving static pages, it also comes with
"dynamic content" courtesy of a
[Brainf***](https://en.wikipedia.org/wiki/Brainfuck) interpreter also written in
assembly.

[Visit it at GitHub](https://github.com/brenns10/yams)

## Works in Progress

I may never decide these projects are *done,* since I'm always improving them.

### `libstephen` -- A C Library

This humbly-named library is the foundation for much of my C programming.  It
extends the standard C library with support for a few important data structures,
command line argument parsing, lightweight unit testing, and memory leak
detection.  I continue to rethink and improve its architecture, so it is not yet
at a place where other people should use it in their own programs.

[Visit it at GitHub](https://github.com/brenns10/libstephen)

[Visit the webpage!](/libstephen/)

### `cky` -- A Parser

This project is actively under construction.  It's intended to become an
impementation of the [CKY](http://en.wikipedia.org/wiki/CYK_algorithm) algorithm
for parsing [CFGs](//en.wikipedia.org/wiki/Context-free_grammar).  In the end, I
intend for it to be similar to, but not necessarily compatible with,
[Lex](http://en.wikipedia.org/wiki/Lex_(software)) and
[Yacc](http://en.wikipedia.org/wiki/Yacc).  In its current state, it has a
complete, from scratch regular expression parser, which will be used as the
foundation of the scanner.

`cky` is based on the `libstephen` library.

[Visit it at GitHub](https://github.com/brenns10/cky)

## Past

### Minesweeper

A minesweeper game written entirely in C, with both a command line and graphical
interface.  This was a fun and short project to apply my C knowledge, as opposed
to my more ambitious, long running projects above.

[Visit it at GitHub](https://github.com/brenns10/minesweeper)

### `caseid` -- Python module for Case IDs

This Python module aims to provide a plain and simple way for a programmer to
retrieve information about the owner of a Case ID.  It supports scraping CWRU
web services, as well as accessing the public LDAP server in order to find
people by their Case ID, and vice versa.

[Visit it at GitHub](https://github.com/brenns10/caseid)

[Also, visit its cousin, implemented by Andrew Mason in Ruby!](https://github.com/ajm188/cwru_directory)

### `lsh` -- A Simplistic Shell in C

I wrote this to illustrate the system calls and basic mechanics behind a Unix
shell.  The [accompanying blog post]({% post_url 2015-01-16-write-a-shell-in-c%})
had a modest positive audience response.

[Visit it at GitHub](https://github.com/brenns10/lsh)

### `wepa-linux` -- A CUPS Printer Driver

[WEPA](https://www.wepanow.com/) is a printing system used at my campus.  Users
'print' documents to their service, which stores them online to be printed at a
kiosk.  Drivers are available for Windows and Mac, but not Linux.

This driver, created at [HackCWRU](//www.hackcwru.com/) 2014, is a solution to
that problem.  It is a CUPS printer driver that allows rudimentary printing to
WEPA.  While the solution is not elegant (the security model of CUPS seriously
limits what a driver can do), it is effective.

[Visit it at Bitbucket](//bitbucket.org/brenns10/wepa-linux)

### `chat` -- A Quick and Dirty Chat System

This is a quick chat client/server implementation in Python (and a little C).
It served as my introduction to socket programming in both languages.  It is
intended to be used as a local chat server over SSH, instead of constantly
sending `wall` messages to other logged in users.

[Visit it at Bitbucket](//bitbucket.org/brenns10/chat)
