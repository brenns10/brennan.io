---
title: "Computer Science Fundamentals: Algorithms"
layout: post
description: >
  Algorithms are the first step beyond just writing code.
  If you know what they are, you can begin to appreciate how computer science is
  about more than just code.
keywords: algorithms computer science fundamentals
---

Welcome to the second article in my "Computer Science Fundamentals" series!
These articles are all about demystifying computer science.  While they're not
going to make anyone an expert on computers, I'm hoping that they will help
people understand what computer science is about.  You can read the previous
article (about programming) [here][csf-programming] if you haven't already.

If you've read my last article, you should know a bit about what programming is.
But the thing is, computer science is only a little bit about programming.  In
fact, many people will tell you that it's much more about math than code.  In
this article, I'll talk about a core part of computer science: algorithms.  If
you understand what these are and why we have them, you'll begin to understand
why computer science isn't just about programming.

## What's an algorithm?

When programmers write code, we often find that we have to solve the same
problem in all sorts of different places.  For instance, think about the problem
of sorting a list of "things".  Sorting is actually a really common thing to do
in software.  Here are a couple examples of sorting in software you've probably
used:

- Spreadsheet programs sort rows from a chart in ascending or descending order.
- Smartphone phonebook apps typically sort by last name.
- A card game probably should be able to sort the cards in your hand.

And these are just a few examples where sorting is visible to the user.  The
truth is, many more programs require sorting, but it's invisible to you.

When programmers notice that we have to solve a problem like this a lot, we tend
to focus on how we're solving it.  After all, if we find a better way to sort
things, we can improve all of our programs.  So, we come up with Algorithms,
which are steps for solving problems.  Algorithms are something like code, but
more general.  Instead of being a list of instructions that computers execute,
they are lists of steps that humans should be able to read and understand.  The
important thing is that these steps should be unambiguous.  That is, there
should only be one way of following the steps to solve the problem.  For
instance, here is a (simplified) algorithm for sorting a bunch of cards with
numbers on them.

1. Fan out all the cards in your right hand.  Your left hand starts out empty.
2. Repeat the following until your right hand is empty:
   - Select the smallest card from your right hand, and put it at the end of the
     cards in your left hand.
3. When your right hand is empty, your left hand should have all the cards
   sorted in increasing order.

Usually, this algorithm is written with slightly more "math-y" notation, but
this is actually a very well known algorithm called "Selection Sort".  The stuff
about cards and hands helps you think about it, but isn't really important to
what you're doing.  A programmer, after reading and understanding these steps,
could write code that would sort a list of numbers, using this exact sequence of
steps.  Now, this isn't the only algorithm you could use to sort things.  Here's
another one, which you may actually use when you play cards:

1. Fan out all the cards in your right hand.  Your left hand starts out empty.
2. Repeat the following until your right hand is empty:
   - Take the leftmost card out of your right hand.
   - Insert it in the correct sorted location in your left hand.
3. When your right hand is empty, your left hand should have all the cards in
   sorted order.

This one is called "Insertion Sort".  The names make a lot of sense when you
think about it.  With selection sort, you *select* the lowest card from your
right hand, and put it at the end of your left.  With insertion sort, you take a
card from the beginning of your right hand, and *insert* it in the correct
location in your left.

## Which algorithms are the best?

Alright!  So now I've shown two different ways to sort things.  As you might
imagine, there are [more][sorting-algorithms] than just two ways to do this.
Now you might begin to understand why we study algorithms.  With all these
different choices, which one should a programmer use when they need to sort
something?  In order to make these decisions, we need to be able to compare
algorithms.

Frequently, we like to compare algorithms based on how quickly they run.  After
all, a fast algorithm means a snappier, more responsive program, which is
usually what a user would like.  You may notice that neither Selection nor
Insertion sorts have a constant number of steps involved.  Instead, they depend
on the number of items they're sorting.  You could say that the number of
instructions it would take for a computer to run these algorithms is a function
of the size of the input list.

So, when we compare algorithms, we compare those functions that determine how
quickly they run.  We typically use something called "Big O Notation", which
simplifies comparing functions.  Basically, Big O Notation just considers the
biggest part of the function.  If you had `f(n) = 3n^2 + 2n + 5`, you should
only need to worry about the `n^2` part, since that's the biggest part of the
function.  So if an algorithm had that function, we would say that it runs in
`O(n^2)` (read that as: *oh of n squared*) time.

Sometimes we find that algorithms will run faster in certain cases, and slower
in others.  So, we usually have a few different runtimes associated with an
algorithm: the "best case", "worst case", and "average case".

The final thing is that sometimes, speed isn't the most important factor.
Sometimes, we're more concerned about how much space (i.e. memory) an algorithm
uses.  And there are even other factors we might be concerned about.  But no
matter what your performance metric is, you can usually analyze and compare
algorithms in the same way I explained above.

## No silver bullet

Unfortunately, just because we have a bunch of algorithms and a way to compare
them, that doesn't mean that we can find the "best" sorting algorithm and call
it a day.  In computer science, it's rare (or maybe just flat out impossible)
for there to be a silver-bullet (i.e. best in every situation) solution.

Even for a problem as simple as sorting, you can already see this.  The two
algorithms I described earlier both have average case runtimes that are
`O(n^2)`.  Meaning that on average, the time they take for a computer to run
them is a function whose biggest part is `n^2`.  But, Insertion sort has this
very nice property that when its input is "nearly sorted", it runs *very*
quickly.  Unfortunately, most lists aren't "nearly sorted".

There are even sorting algorithms that can do better when their input isn't
nearly sorted.  Algorithms like "Quicksort", "Mergesort", and "Heapsort" all
have runtimes that are `O(n * log(n))` (which is faster than `O(n^2)`, I
promise).  But each of those algorithms have drawbacks to them as well.

Finally, if you knew that all you were sorting were lists of small, positive
integers, you could use something called "Counting Sort", "Radix Sort", or
"Bucket Sort", which can sort those lists in `O(n)` time (sort of, I'm
simplifying quite a bit here).

Of course, if you're not a computer scientist or programmer, you shouldn't care
too much about the names or numbers.  What you should care about are these three
points that hopefully have become clear in the last couple paragraphs:

1. There are lots of ways to solve the same problem!
2. There are no "silver bullet" algorithms.
3. When you know more about your input, you can frequently come up with a better
   solution.

## Conclusion

I know this article has a lot of information in it.  What I hope any
non-programmer would get out of it is this: programming has much more to it than
just writing code.  When a good programmer does their job, they are considering
more than just "what code will get the job done?".  They need to be capable of
identifying problems which already have algorithms.  They need to be able to
understand these algorithms and make engineering decisions based on the
tradeoffs that occur naturally in computer science, and the business constraints
of their software.  It's not actually wizardry; it's just computer science and
engineering decisions.

[csf-programming]: {% post_url 2015-09-23-csf-programming %}
[sorting-algorithms]: https://en.wikipedia.org/wiki/Sorting_algorithm
