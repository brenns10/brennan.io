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
recommend it; if you have the time and interest, read it after you finish this!

To understand what programming is and why we need it, you have to understand
what a computer is at its most basic level.  At the center of every computer,
you have something called a *processor*.  This is what you might think of as the
"brain" of the computer.  But there's one crucial difference between a processor
and a brain: a processor can't think.  It can, however, follow instructions very
quickly.  Every time its internal clock ticks (up to billions of times per
second), a processor reads another instruction and executes it.  The instruction
is always something simple.  If you were to translate these instructions into
English, they'd read something like this:

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
`mult`.  So maybe you could guess what those commands do.  But what about the
ones like `beq` and `mflo`?  And even if you did understand all the
instructions, understanding what the code does as a whole is very difficult.  I
wrote this code, but it still takes me a while of looking at it to remember how
it works.  So it doesn't get much easier with more experience!

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

As far as making processors do our bidding, all the code we give a processor
*must* be machine code.  But that doesn't mean we have to write that code in
assembly.  Instead, we can write code in a "high level language."  Then, we can
use a special piece of software called a *compiler* to translate that code into
assembly code, or even directly to machine code.  This can give us tons of
benefits.  Most of them come from one simple fact.  High level languages are
created by programmers, for programmers.  As a result, code written in high
level languages is easier to read and write than code in assembly.

To understand why it's so much better, think about writing a recipe.  When you
write a recipe, you have lots of options about how detailed you can be.  You
could write an incredibly detailed recipe that describes each move the chef
should make.  A recipe written with this much detail would probably take several
pages (and that's not even including the diagrams that would have to go with
it!).  Here's how (part of) such a recipe might go:

> 1. Take five steps forward.
> 2. Locate the drawer directly in front of you, just below the counter.
> 3. Pull it at least 10 inches open.
> 4. Locate the large spoons, in the second bin from the left.
> 5. Extend your hand and pick up the spoon.

You can see that it's pretty absurd to give somebody this much detail in a
recipe.  For one thing, what if their kitchen isn't laid out the same way as
yours?  And for another, the most important part of your recipe is probably not
how the chef gets the spoon.  The important part is what they use that spoon
for.  You would much rather just tell them to stir with a spoon, and leave them
to figure out how to get the spoon from their kitchen.

This is exactly what higher level languages do.  They allow you to express the
steps in your program more in terms of *what you want to happen* rather than
*how you want the computer to do it.* As a consequence, they're much more
readable.  And as another consequence, they happen to be more *portable* too.
The compiler generates assembly for a particular processor, but you can always
use a different compiler and get assembly for an entirely different processor.
Suddenly, with the addition of high level languages, we are able to write code
once, and run it on more than one type of processor!

> **What is portability?** To a conscientious laptop buyer, portability has to
> do with the size and weight of a laptop.  But to a programmer, portability is
> about how easily your code runs on different types of computers.  Right now,
> we've been talking about writing code that runs on different processors.
> Soon, we'll see that it's even more difficult to write code that runs on
> different operating systems (like Windows and Mac OS), even on the same
> processor!

There are several programming languages that are "a step up" from assembly:
[FORTRAN][], [COBOL][], [ALGOL][], and [LISP][] are some rather old (but not
dead) examples.  I'm going to skip tons of programming language history and show
you one of the most common ones still in use today: [C][].  Here is some C code
that does what the assembly code I showed before does:

```c
int atoi(char *s)
{
  int value = 0;
  while (*s != '\0') {
    value = value * 10;
    value = value + (*s - '0');
    s = s + 1;
  }
  return value;
}
```

Hopefully, this looks strikingly different from the assembly example I showed
you earlier.  For one thing, it's a bit shorter.  It also uses bigger, more
English-like words, which is better for trying to read it.  Another great thing
is that you can see the structure of the code by looking at the indentation.
plus, you can get more ideas about what's happening because you're familiar with
the already existing meanings of symbols like `=`, `*`, and `+`.

C is used for a lot of things.  If you've used Windows, Mac OS, or Linux, you
may not know it, but large portions of the software you run every day is written
in C.  Unfortunately, C isn't perfect!  For one thing, C is infamous for making
it very easy for a programmer to write code that has errors (or even security
holes) in it.  Also, even though it is much higher level than assembly language,
C still makes the programmer do a lot of extra work to solve problems.  So many
programmers use even higher level languages!

These higher(er) level languages usually make it easier for programmers to do
more complicated things, with fewer lines of code.  Many of them do this by
being *interpreted*, rather than *compiled*.  Recall that a compiler is a
program that takes a high level language, and translates it into assembly.
Well, an interpreter is a program that takes a high level language, and runs it
directly!  While this makes these programming languages very powerful, it also
makes them much slower than languages like C, or (God forbid) assembly.  Some
common interpreted languages are [Python][], [Ruby][], [JavaScript][], and
[Perl][].

Finally, I'll mention that there are even programming languages that are
somewhere in between compiled and interpreted.  They gain some of the benefits
and drawbacks of both.  Some common examples of those are [Java][] and [C#][]

## Why so many languages?

OK, so now that I've filled your mind with the names of all these programming
languages, you're probably wondering why we need so many of them.  The answer to
that involves a lot  of factors.

* For one thing, there are a lot of ways that programming languages can be
  different.  Most of them I haven't even mentioned in this article.  So it
  makes sense that there would be lots of languages, just so we could explore
  those differences.
* All these languages come with different tools for doing different things.  If
  you wanted to make an operating system, you'd use C for that, but if you
  wanted to create a cool website, you'd probably want to use Ruby or Python, as
  well as JavaScript!
* Programming languages are also rather personal.  Just like a favorite pen,
  programmers become attached to certain programming languages, or strongly
  dislike others.  When that happens, they sometimes like to make new ones.

The last thing I'd like to mention deserves some special attention.  Throughout
the article you may have noticed a progression.  The low level languages were
very difficult to use, but very fast.  By the time you got to the very high
level languages at the end, the languages were much easier to use, but also
slower.  This is one of the first instances of a major trade-off you'll find in
computer science.  Trade-offs are huge in computer science, and you'll be seeing
plenty more of them if you keep reading my Computer Science Fundamentals
articles!

## Closing remarks

This has only been a brief introduction into what programming is, and what the
different languages are.  I hope that everything has been understandable!  If
you're looking to learn even more details (again delivered for a non-technical
audience), I highly recommend you check out the ["What Is Code?"][what-is-code]
article I mentioned earlier.  If this has convinced you to start learning to
write code yourself, that's great!  I'd recommend you start with one of the
simpler (higher level) languages, like Python.  You can start learning it with a
completely free website called [Code Academy][codeacademy-python].  You don't
need to install anything, just click "Start" to begin learning!

Check back later for newer Computer Science Foundations articles.  I'll update
this article with a link to the new one when it comes out!

[what-is-code]: http://www.bloomberg.com/graphics/2015-paul-ford-what-is-code/
[wiki-binary]: https://en.wikipedia.org/wiki/Binary_number
[LISP]: https://en.wikipedia.org/wiki/Lisp_%28programming_language%29
[ALGOL]: https://en.wikipedia.org/wiki/ALGOL
[COBOL]: https://en.wikipedia.org/wiki/COBOL
[FORTRAN]: https://en.wikipedia.org/wiki/Fortran
[C]: https://en.wikipedia.org/wiki/C_%28programming_language%29
[Python]: https://en.wikipedia.org/wiki/Python_%28programming_language%29
[Ruby]: https://en.wikipedia.org/wiki/Ruby_%28programming_language%29
[JavaScript]: https://en.wikipedia.org/wiki/JavaScript
[Perl]: https://en.wikipedia.org/wiki/Perl
[Java]: https://en.wikipedia.org/wiki/Java_%28programming_language%29
[C#]: https://en.wikipedia.org/wiki/C_Sharp_%28programming_language%29
[codeacademy-python]: https://www.codecademy.com/en/tracks/python
