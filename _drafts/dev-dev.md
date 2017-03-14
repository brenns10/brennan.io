---
title: Development of a Developer
layout: post
---

I was a curious child. I spent hours on the family computer, exploring every
menu in Windows 95, and later XP. My exploration sometimes ended badly, like the
time when I changed our computer's language to Portuguese, or the time I set the
foreground and background colors of the menus to lime green[^1]. Exploring and
learning about computers has never failed to put that elated, soaring feeling in
my chest.

More recently, I've discovered how much I like teaching others. Helping somebody
else reach that "aha" moment can be even more gratifying than reaching it
yourself[^2]. As a result of these two loves, I've done a lot of learning (you
might say, "development" as a developer), and I've watched many others as they
learn too. Sometimes I feel like we all go through some common stages while
growing up as programmers. I recently did some thinking about what those stages
might be, and this article is the result. My development is probably not
universal, but the retrospective helped me remember what it was like to be a
beginner. Hopefully it will help others remember that too.

## Step 0: Fascination

As I've already said, my fascination with computers was evident early in my
life. I spent plenty of hours exploring Microsoft Office, managing my first
music library with Windows Media Player, and competing with my brother in
pinball and Sonic. It wasn't long before I became curious about how people
actually made those things. Unfortunately, Windows 95 didn't ship with any tools
or documentation for development. It's funny, because older PCs probably had to
include programming tools out of necessity, but I was "lucky" enough to be
growing up at the beginning of a "user-friendly" world of computing, where users
didn't have to be bothered with programming.

The biggest barrier to entry at this point was not a lack of information, but
rather not knowing where to begin. Internet time was a scarce resource back
then. Library books were not likely to contain up-to-date information. Without a
parent or friend who knew anything about programming, and without built-in
development tools or documentation, I had no way of discovering anything more
about programming. Part of me wonders how my life might be different if I had
had a computer that shipped with programming tools.

## Step 1: Initial Discovery

The summer after middle school, I went to a camp at the University of Michigan
called Camp CAEN. There, I had my first ever exposure to "real" programming, in
the form of C#! Over the course of around a week, the instructors---mostly
college students, bless their hearts---taught us how to use Visual Studio 2005.
We learned to use the form designer to drag and drop buttons onto windows. A
double click on the button would bring you right to the part of the code that
ran when your button was clicked. We learned how to make variables and how to
write "if" statements and loops. By the end of the week, I had learned enough to
make a silly (but functional enough) version of pong out of Windows Forms.

This phase of development was truly exciting for me. In a few days, I had gone
from wondering how people gave computers instructions, to giving them
instructions myself. Even simple projects like adding two numbers and displaying
the result were exciting, because I could tell the computer what I wanted it to
do. For a time, this exciting new world was all I needed to know.

But soon, questions began to form in my head. I felt like I wasn't getting the
whole truth about how programming worked. After all, what was my program doing
when the button *wasn't* getting pressed? How did the computer put the window
onto the screen? What happened when the program first starts? I felt like the
truth was being hidden from me, and I didn't like it.

## Step 2: Confusion and Intimidation

These questions quickly lead me into the next step in my development: confusion
and intimidation. After camp, I had one simple goal: create a game that kept
track of high scores. As I researched a way my program could save data for the
next time it ran, I stumbled upon MSDN videos about "SQL Databases". I followed
along with these videos to the best of my knowledge, installing scary programs
like "SQL Server Express Edition" onto my computer. Soon I was lost in a sea of
big words and complicated interfaces that looked like spreadsheets, but weren't!
What was a schema, and why did I need one just to keep track of high scores?

I never did get my database-driven high scores to work. It was a demoralizing
experience, to say the least. Poor 14-year-old Stephen had no idea what
databases were or why they existed. He sure didn't realize that there were much
simpler ways to store data (like, a file).

This was the first time I began to feel lost and confused about programming, but
it surely wasn't the last. It happened again the time 15-year-old Stephen tried
to understand assembly and [two's complement][2c] signed integers. The biggest
problem I had was that most of the "help" I found online assumed I knew a whole
bunch of other things. Learning how to use a database in C# is hard enough, but
it is darn near impossible when you don't actually know what a database schema
is. I really needed someone who could give me high level explanations of what
things were.

## Step 3: Getting Cocky

In my final years of high school, I became more confident in spite of these
setbacks. I did manage to solve some of my early challenges: I learned to use a
database, and I even wrote a few tiny assembly programs. I had transitioned to
Java and I was even self-teaching myself the AP Computer Science course, since
my high school didn't have one. Somehow my school let me do an independent
study, which meant I had an hour per day to ~~mess around on my computer~~ teach
myself Java. So things were going pretty well.

I certainly didn't think I knew *everything* about computers, but I figured I
had pretty much mastered programming. I knew that people studied it in college,
so there must have been [a *few* things I hadn't learned yet][snow]. But I just
could not imagine what they could be. After all, I knew about classes,
functions, arrays, and loops. I could make windows on screens and I had even
made a web site.

&nbsp;&nbsp;&nbsp;&nbsp;*I was basically a coding expert.*

The biggest thing that prevented me from moving past this stage was that I
didn't have good opportunities for broadening my knowledge. To me, the happy,
walled garden of classes, functions, and loops in simple Java programs was
everything I needed to know. Meanwhile, I didn't understand how much was going
on behind the scenes---I had no idea about things like garbage collection,
memory management, concurrency, networking, etc.

## Step 4: Head Above Water

Finally, I started college. The first few years of school were truly eye-opening
and humbling. As it turned out, there are more data structures than just arrays,
and algorithms can be more complicated than a single for loop. My formal
education did a lot to help me mature as a developer, but probably even more
significant were the things I continued to learn outside of class.

I started by switching my main computer to Linux. And not just Linux, but Arch
Linux, which forced me to learn a lot about the nitty-gritty side of Linux. I
finally learned bash well. In those years, I learned my first version control
systems (Mercurial, and then Git). I learned C and started writing all sorts of
awful code in it. Slowly but surely I began to gain perspective about the
complexity of a computer system.

A turning point came thanks to my Networks class. In this course, we walked down
the Internet protocol stack, from the application layer down to the link layer.
For the first time, I "understood" the pieces of the puzzle that made the
Internet work. The machinery made sense. But I also quickly recognized that
nobody *really* understands all of how the Internet works. It's just way too
complicated!

## Step 5: Deep Dive

From my late undergrad years, I'm too close to now to say anything with
confidence. I don't believe that there is a well-defined end of Step 4. It's
mostly just a gradual realization of how little you know. For me, at some point
a "big picture" started to come together. While I don't know much of that big
picture, I have general ideas about how a lot of these things work together, and
I know how I can start to learn about them.

Now, I feel like I'm entering a new stage, which is characterized by delving
deep into the parts of the big picture that interest me. In the past year I've
had the opportunity to learn more about machine learning and data analysis
during my time at Yelp, as well as kernel development and networking for my
thesis. I'm far from reaching the end of this stage, and I doubt I'll ever truly
"master" any subfield like those.

## Takeaways

In these (nearly) nine years of learning, I'm amazed at how much technical
knowledge I've gained, but even more surprised at how much perspective I have on
it already. Below, I've distilled a few of the thoughts I have about my learning
process, although maybe my thoughts will be wildly different in another nine
years.

### Nobody Knows Everything

Nobody knows everything about computers. Nobody knows one percent of everything
about them. There's too much to know! The best thing you can do is make a mental
map and try to know what things you don't know.

### Respect What You Don't Know

A simple corollary is that you should always respect the complexity of the
things you don't know well. There is nothing cool about "oh, they just do
front-end" or "they're just a designer". Chances are, if you're dismissive about
a field, you haven't learned enough about it, and you're too ignorant to
consider that there even *is* anything you've missed.

### Learn to Learn

The most valuable skill you can have is learning. The only constant in my
development has been teaching myself new skills. Each time I learn something
new, the bar has gotten higher. As the topics get harder, there's less
documentation, fewer books, and more misinformation to sift through. But each
time I learn something new, I get better at asking the right questions and
looking for answers in the right places.

### Embrace Uncertainty

I always thought that the uncertainty, intimidation, and confusion I experienced
early on ("Step 2") would go away with experience. But yet every time I try to
learn something new, I experience it all over again. A few weeks ago it was with
trying to figure out Docker. For the past few months it's also been about
wrapping my head around kernel development. It seems to me that I will never not
feel uncertain and confused when I try something new. And, I'd be willing to bet
that I'm not the only one that still feels that way. So instead of letting that
uncertainty feed into self-doubt, I'm learning to redirect it into confidence.
If I'm feeling lost and confused, that means I'm moving forward.

[2c]: https://en.wikipedia.org/wiki/Two's_complement
[snow]: http://i0.kym-cdn.com/photos/images/facebook/000/527/985/04f.gif

***

#### Footnotes

[^1]:
    Thus revealing two of my longest lasting loves in life: computers, and the
    color green.

[^2]:
    What a selfish reason to teach people!
