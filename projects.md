---
title: Projects
layout: default
---
# Projects

## Active

### `libstephen` -- A C Library

This humbly-named library is the foundation for much of my C programming.  It
extends the standard C library with support for a few important data structures,
command line argument parsing, lightweight unit testing, and memory leak
detection.  I continue to rethink and improve its architecture, so it is not yet
at a place where other people should use it in their own programs.

[Visit it at GitHub](https://github.com/brenns10/libstephen)

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
