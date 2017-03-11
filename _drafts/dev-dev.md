---
title: Development of a Developer
layout: post
---

I was a curious child. I spent hours on the family computer, exploring every
menu in Windows 95, and later Windows XP. My exploration sometimes ended badly,
like the time when I changed our computer's language to Portuguese, or the time
I set the foreground and background colors of the menus to lime green[^1].
Exploring and learning about computers has never failed to put that excited
feeling in my chest, like I'm flying.

More recently, I've discovered how much I like teaching others. Helping somebody
reach that "aha" moment can be even more gratifying than learning it
yourself[^2]. As a result of these two loves, I've done a lot of "development"
as a developer, and I've watched a fair amount of it too. Sometimes I feel like
there are some distinct stages I've gone through, and I can even recognize them
in others too. While I wouldn't presume that my experiences are universal, or
even normal, I do think most people will be able to relate to at least some
portion.

## Step 0: Fascination

As I've already said, my fascination with computers was evident early in my
life. I spent plenty of hours exploring Microsoft Office, managing my first
music library with Windows Media Player, and competing with my brother in
pinball and Sonic games. Inevitably I became curious about how people made
computers behave the way they wanted. Unfortunately, Windows 95 did not ship
with development tools, unlike earlier home computers.

The biggest barrier to entry at this point was not a lack of information, but
rather not knowing where to begin. Internet time was a scarce resource in my
early childhood, and library books were not likely to contain up-to-date
information. Without a parent or friend who knew anything about programming, and
without built-in development tools or documentation, I had no way of discovering
anything more about programming. Part of me wonders how my life might be
different if I had had a computer that made development tools available to
end-users.

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
do. For a while, the happy walled garden of C# and Windows Forms was everything
I needed to know.

But soon, questions began to form in my head. I felt like I wasn't getting the
whole truth about how programming worked. After all, what was my program doing
when the button *wasn't* getting pressed? How did the computer put the window
onto the screen? What happens when the program first starts? I felt like the
truth was being hidden from me, and I didn't like it.

## Step 2: Confusion and Intimidation

These questions quickly lead me into the next step in my development: confusion
and intimidation. After camp, I had one simple goal: create a game that kept
track of high scores. To be able to store these scores, I stumbled upon MSDN
videos about "SQL Databases". I followed along with these videos to the best of
my knowledge, installing programs like "SQL Server Express Edition" onto my
computer. Soon I was lost in a sea of big words and complicated interfaces. What
was a schema, and why did I need one just to keep track of high scores?

I never did get my database-driven high scores to work. It was a demoralizing
experience, to say the least. Poor 14 year old Stephen had no idea what
databases were or why they existed. He sure didn't realize that there were much
simpler ways to store data (like, a file).

A similar experience happened probably a year later. During my golden years
of [TI-Basic][basic], I learned that the "best" way to write calculator programs
was using Z80 Assembly. I tried desperately to learn from a tutorial, but failed
miserably. Especially when the tutorial went into [Two's Complement][2c].

## Step 3: Getting Cocky

In my final years of high school, I became more confident. I solved some of my
early challenges: I learned to use a database, and I even wrote a few tiny
assembly programs. I had transitioned to Java and I was even self-teaching
myself the AP Computer Science course, since my high school didn't have one.
Somehow my school let me do an independent study, which meant I had an hour per
day to ~~mess around on my computer~~ teach myself Java.

I certainly didn't think I knew *everything* there was to know about computers,
but I figured I had pretty much mastered programming. I knew that people went to
college for programming (which I wanted to do), so I knew there had to be some
stuff I didn't know yet. But I just could not imagine what it could be. After
all, I knew about classes, functions, arrays, and loops. I could make windows on
screens and I had even made a web site.

The biggest thing that prevented me from moving past this stage was that I
didn't have good opportunities for gaining breadth of knowledge. To me, the
happy, walled garden of classes, functions, and loops in simple Java programs
was everything I needed to know. Meanwhile, I didn't understand how much was
going on behind the scenes---I had no idea about things like garbage collection,
memory management, concurrency, networking, etc.

## Step 4: Head Above Water

Finally, I started college. The first few years of school were truly eye-opening
and humbling. As it turned out, there are more data structures than just arrays,
and algorithms can be more complicated than a single for loop. My formal
education did a lot to help me mature as a developer, but probably even more
significant were the things I continued to learn outside of class.

I started by switching my main computer to Linux. And not just Linux, but Arch
Linux, which forced me to learn a lot about the "operations" side of computers.
I finally learned the Linux command line well. In those years, I learned my
first version control systems (Mercurial, and then Git). I learned C and started
writing all sorts of awful code in it. Slowly but surely I began to gain
perspective about the complexity of a computer system.

Perhaps the biggest single moment for my "maturing" was when I took my Networks
class. In this course, we walked down the protocol stack, from the application
layer down to the link layer. For the first time, I "understood" how the
Internet worked. The machinery made sense. But I also quickly recognized that
nobody *really* understands all of how the Internet works. It's just way too
complicated!

## Step 5: Deep Dive

From here on, I'm too close to the action to say anything with confidence. I
don't believe that there is a well-defined end of Step 4. It's mostly just a
gradual realization of how little you know. For me, at some point a "big
picture" started to come together. While I don't know much of that big picture,
I have general ideas about how a lot of these things work together, and I know
how I can start to learn about them.

Now, I feel like I'm entering a new stage, which is characterized by delving
deep into the parts of the big picture that interest me. In the past year I've
had the opportunity to learn more about machine learning and data analysis
during my time at Yelp, as well as kernel development and networking for my
thesis. I'm far from reaching the end of this stage, and I doubt I'll ever truly
"master" any subfield like those.

## Takeaways

In my (almost) nine years of development, I've learned a lot of technical
things, and probably forgotten a lot of them. But I think the biggest takeaways
are nontechnical.

### Nobody Knows Everything

Nobody knows everything about computers. Nobody knows one percent of everything
about them. There's too much to know! The best you can hope for is to build a
big picture of the things you know that you know, and the things you know that
you don't know.

### Respect What You Don't Know

A simple corollary is that you should always respect the complexity of the
things you don't know well. There is nothing cool about "oh, they just do
front-end" or "they're just a designer". Chances are, if you're dismissive about
a field, you haven't learned enough, and you're too ignorant to consider that
there even *is* anything you've missed.

### Learn to Learn

The most valuable skill you can have is learning. The only constant in my
development has been teaching myself new skills. Each time I learn something
new, the bar has gotten higher. As the topics get harder, there's less
documentation, fewer books, and more misinformation to sift through.

### Embrace Uncertainty

I always thought that the uncertainty, intimidation, and confusion I experienced
early on ("Step 2") would go away with experience. But yet every time I try to
learn something new, I experience it all over again. A few weeks ago it was with
trying to figure out Docker. For the past few months it's also been about
wrapping my head around kernel development. It seems to me that I will never not
feel uncertain and confused when I try something new. And, I'd be willing to bet
that I'm not the only one that still feels that way. So instead of letting that
uncertainty feed into self-doubt, I'm learning to redirect it into confidence.
If I'm feeling lost and confused, that means I'm moving forward---I'll figure it
out eventually, though probably not without help!

[basic]: {% post_url 2015-11-22-ode-to-ti-basic %}
[2c]: https://en.wikipedia.org/wiki/Two's_complement

#### Footnotes

[^1]:
    Thus revealing two of my longest lasting loves in life: computers, and the
    color green.

[^2]:
    What a selfish reason to teach people!
