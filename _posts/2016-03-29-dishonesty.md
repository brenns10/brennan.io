---
layout: post
title: Academic Dishonesty
description: It'll never get you where you want to go.
---

Last night I had a sobering experience.  A faculty member from another
university sent me a message letting me know that some of their students had
turned in modified versions of my shell, [lsh][], for a homework assignment.
Maybe I shouldn't be too surprised.  Writing a shell is a very common assignment
for computer science students.  My [tutorial][] based on lsh has somehow managed
to climb the ladder to the first page of search results for many queries related
to writing shells.  So at the end of the day, I guess this was bound to happen.
And even though I can't really be held responsible for what other people do with
my tutorial and code, I feel pretty bad about this.  Although there's not much I
can do to prevent students from presenting my shell as their own, I feel like I
should point out why it's such a terrible idea.

### You'll get caught.

This shouldn't be the first reason behind a concept as ethical as "don't cheat",
but I think it's the most convincing for people who are considering it.  There
are a number of reasons why you're going to get caught, no matter how clever you
think you are:

1. **If you can find my code easily, so can your professor.** It only takes one
   bad experience to get a grader in the habit of doing Google searches before
   they begin grading, just so they know the resources you may have stolen from.
2. **If you can find my code easily, so can other students.** Professors don't
   even need Google to realize that two assignments are drawing from the same
   source and modifying the same code.
3. **Just because you renamed things doesn't mean it's less obvious.** There are
   many well-researched automatic plagiarism detection tools for code out there,
   and lots of professors use them.  These tools don't just use text
   comparisons!  They don't particularly care what you name your variables and
   functions---they compare structure and control-flow to determine how similar
   two programs are.  It's difficult to fake these things.
   
### It's wrong.

Hopefully this one is obvious.  Even though legally, my shell is in the public
domain, meaning you are allowed to use my code without attribution, turning in
my code (however much you modified it) is wrong.  When you turn something in,
you're presenting it as your own work.  You're certifying that you took the time
to work through the problem at hand, and that you're turning in the result of
this work.  If you don't even bother to cite a source that you relied on, or
flat-out modified, you're misrepresenting your own work.  Even when you do cite
your sources, chances are your class and/or university has very specific
policies about how you can use external sources.

Schools, employers, and individuals take this very seriously.  Judging a
person's character can be difficult, and there are few red flags as obvious as
presenting someone else's work as your own.  Schools don't want their graduates
to represent them that way.  Employers don't want the liability of a cheater on
their staff.  People don't want to hang out with somebody who's willing to take
advantage of others that way.  And so, when you do something like this, you're
setting yourself up for a big problem---one that could go as far as expulsion
from your school.

### You don't learn.

I know that I wrote a tutorial.  It's easy to believe that by following the
tutorial, you will end up learning what your assignment meant for you to learn.
But that's really not true.  You can only fit so much into a single article, so
I compromised by only focusing on the high-level details.  I explained the
system calls like `fork()`, `exec()`, and `wait()`, but I didn't go into the
gory details of each line of C.  I didn't spend much time on memory management.
I didn't even justify why I designed the shell the way I did.

Following a tutorial doesn't give you the learning experience that an assignment
intends.  When I wrote lsh, I spent a fair amount of time poring over manual
pages, trying to get the magic invocations of system calls just right.  I didn't
have that clear vision that my tutorial has; I just hacked things together until
they worked.  A tutorial holds your hand and liberates you from the details so
you can focus on the stuff that matters in the problem domain.  In the process,
it robs you of the experience of researching and dealing with those details, and
it prevents you from thinking for yourself and creating your own designs.  This
experience is a huge part of what the assignment is there for.   I'd also be
willing to bet that it's probably something employers value a lot more than
being able to follow a tutorial.

This is why I made my code public domain in the first place.  I want it to be as
easy as possible for people to be able to take my code, modify it, understand
it, and build on it.  The really exciting part begins once you finish the
tutorial, and you start extending lsh with your own code.

Anyway, I'll get off my soapbox now!

[lsh]: https://github.com/brenns10/lsh
[tutorial]: {% post_url 2015-01-16-write-a-shell-in-c %}
