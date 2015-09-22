---
title: "Computer Science Fundamentals: Programming"
layout: post
description: What programming is, and how we do it.
keywords: programming computer science fundamentals
---

When I'm around friends and family I frequently get the question, "what is it
exactly that you do?"  I really appreciate questions like that, but they're also
really difficult to answer.  Computer science is a world full of jargon, and
when I start using that jargon in my explanations, it inevitably leads to blank
looks.  But the thing is, contrary to what some people seem to think, you
*don't* need to be a genius or a computer wizard to understand the ideas of what
computer scientists and programmers do.

So what I'd like to do is start up a series of articles on this blog, called
"Computer Science Fundamentals," that gives broad, non-technical overviews of
topics of computer science.  My goal is that one day I could give these articles
to someone who knows nothing more than the basics of how to use a computer, and
they would come away from the experience understanding that computer science and
programming aren't wizardry.

## What is programming?

I'm going to start off this series with an introduction to what programming is.
Explaining something as big and general as programming is a difficult task, and
I'm going to do my best.  But right off the bat, I think it's worth pointing out
that there's already a truly excellent article written on the subject: "What is
Code?", by Paul Ford in *Bloomberg*.  You can find it [here][what-is-code].
It's very long and goes into much more detail than I will here.  I'd highly
recommend it -- if you have the time and interest, read it after you finish
this!

To understand what programming is and why we need it, you have to understand
what a computer is at its most basic level.  At the center of every computer,
you have something called a *processor*.  This is what you might think of as the
"brain" of the computer, although it doesn't actually think.  What it does do is
follow instructions.  Every time its internal clock ticks (up to billions of
times per second), a processor reads another instruction and executes it.  The
instruction is always something simple.  If you were to translate these
instructions into English, they'd read something like this:

* "add A and B, and store the result in C"
* "move the number from A into B"
* "if A equals B, start executing a different list of instructions"

Unfortunately, these instructions aren't in English.  Instead, they're stored as
a sequence of binary codes called "machine code".  Humans can't read them unless
they're experts -- and even then, experts have to spend a lot of time reading
them.  In order for humans to be able to read and edit those instructions
easily, we need to have a way to represent them as readable, editable text.  And
this is why programming languages exist.

> **What is Binary?** Binary is a way of representing numbers.  We as humans
> normally use a number system called base 10, where we have 10 digits, and each
> decimal place is a power of 10.  Binary is just base 2: it has 2 digits (0 and
> 1), and each decimal place is a power of 2.  As an example, the number 13 in
> binary would be 1101.  [Read more on Wikipedia][wiki-binary]

## The most basic programming language

The first, most basic programming language is called "Assembly".  Assembly is
just plain machine code, but written in text instead of as a series of binary
codes.  You can use a special type of program (called an "assembler") to convert
assembly into machine code, and another program (called a "disassembler") to
convert machine code into assembly.

In fact, assembly is not a single language, but rather a type of language.  Just
like there are different brands and models of cars, there are also different
brands and models of processors.  Since each one has a different set of
instructions it understands, they each have their own machine code and assembly
to go with them.

Like machine code, assembly is extremely basic.  When you're writing assembly,
you're telling a computer how to shuffle around its bits and bytes, at the
lowest level possible.  This means it's rather difficult to read, write, and
understand assembly.  Here is some assembly I once wrote so you know what I
mean:

```asm
atoi:
    move $v0, $zero
    li $t0, 10
_atoi_loop:
    lbu $t1, 0($a0)
    beq $t1, $zero, _atoi_return
    mult $v0, $t0
    mflo $v0
    subi $t1, $t1, '0'
    add $v0, $v0, $t1
    addi $a0, $a0, 1
    j _atoi_loop
_atoi_return:
    jr $ra
```

This particular assembly language is for a type of processor called MIPS.  The
job of this code is to take a number written as text in base 10, and convert it
into a binary number that the computer can understand.  I won't explain anything
about how it works, but I think one thing about it is clear: it looks very
confusing!  Maybe you're able to recognize a couple words, like `add` and
`mult`, where you could guess what they do.  But what about the ones like `beq`
and `mflo`?  And even if you did understand all the instructions, understanding
what the code does as a whole is very difficult.  I wrote this code, but it
still takes me a while of looking at it to remember how it works.  So it doesn't
get much easier with more experience!

Besides the readability issue, there is another major issue with assembly code.
Like I said above, there are plenty of processor types, and each one understands
a different assembly/machine code combination.  That means that the code I wrote
above would only run one one type of processor.  Unfortunately, the MIPS
processor isn't one that you commonly find on desktops, laptops, tablets, or
smartphones.  So chances are, most people could not run the code I wrote up
there.  This really stinks for me as a developer, because I'd like to write code
that lots of people can use.

When you take those two problems together, you realize that it would be very
convenient if we had languages that solved those problems.  And we do.

## Higher level languages



[what-is-code]: http://www.bloomberg.com/graphics/2015-paul-ford-what-is-code/
[wiki-binary]: https://en.wikipedia.org/wiki/Binary_number
