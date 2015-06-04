---
title: Introducing Libstephen
layout: post
tags:
 - Linux
 - Unix
 - C
 - Programming
 - Library
---

A couple years back, I implemented a linked list in C.  It was nothing more than
an experiment to show that I was capable of making Java data structures in C.
So I never would have thought that that very linked list implementation would
become the foundation of my own C library over the course of the next few years.
But that's exactly what happened!  Over the past couple years, I've been
spending bits of time adding features to my own personal C library called
libstephen.  Now, I feel like the time is right to talk about it.

## What Is Libstephen?

What started out as a single linked list implementation has grown into a library
containing everything I think may be useful for programming in C.  Mainly, that
means: data structures, unit testing, argument parsing, logging, and string
manipulation.  I'll go into each one briefly below.

## Data Structures

C offers you a rich set of built-in data structures, so long as you consider
constant sized arrays "rich".  If you don't, then you'll understand why I wanted
to add some data structures of my own to make things a bit smoother.  The first
data structure I ever implemented in C was my linked list.  I extended my
original linked list implementation with an iterator that allows for efficient
iteration over linked lists.
