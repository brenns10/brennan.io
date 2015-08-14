---
title: The Wild World of Open-Source Licensing
layout: post
---

Imagine that you've just finished an awesome program.  As a programmer, you're
faced with a slightly weirder intellectual property world than most other
creative disciplines.  In most of those disciplines, when you create something
you take steps to protect it -- patent, copyright, or whatever legal protection
is applicable to your creation.  But in the world of software development, we
have these crazy things called "open source" and "free software," and a lot of
people make their programs open source.  But then we also have licenses with
lots of legal language in them.  For many new programmers, this raises a lot of
questions, like "why would I want to make my code open source?", "how do I make
my code open source?", and "what are all these licenses?".  This article will
hopefully help answer those questions for new programmers and non programmers
alike.

## Why would you make your code open source?

I'm going to assume that everyone that reads this article is at least familiar
with what open source software is.  If not, [Wikipedia][oss] can probably
explain it to you.

So, why would you make your code open source?  As an individual, and especially
as a college computer science student, there are very few reasons not to.  When
you don't work for a company, you aren't required to keep your work secret.  How
will other people appreciate your software if not by seeing and running it?
Plus, writing and publishing open source software is a nice way to show
potential employers that you do, in fact, know how to write code.

So maybe the question we should be asking is, "why *not* make your code open
source?"  For individuals, the biggest reason that I could think of is to
prevent others from stealing it and claiming that they wrote it.  There is also
the risk of someone suing you for your program causing damage to their computer,
which would be a bad thing, but also pretty darn unlikely for most software.

Thankfully, open source licenses exist exactly to address these concerns.

## The politics of open source

Unfortunately, there's really no way to talk about open source licensing without
getting into the political ideas behind open source software.  Like many other
computer related "holy wars", there are two camps.  The first camp cares more
about the practical benefits of open source software, and the other camp
believes in the ethical benefits of free software.  I'll refer the the former
camp as "open source advocates", and the latter as "free software advocates".

### Open source advocates

Open source advocates value open source software for its practical advantages.
It isn't hard to observe that open source software is very successful (see
Firefox, Linux, etc).  Open source advocates argue that open source is
successful because it is a way of doing things that allows better software to be
written.  The most concise description of this viewpoint is given by Eric
S. Raymond in his book [*The Cathedral and the Bazaar*][bazaar]:

> Given many eyeballs, all bugs are shallow.  (Linus's Law)

The idea is that when software development happens in public, where anyone can
see the source code, errors in the code are identified more quickly and the
software can become improve faster.  (Side note: *The Cathedral and the Bazaar*
is really more of a comparison of open source development models.  Linus's Law
is a point in favor of the "bazaar" model, but it also applies very well here).

### Free software advocates

Free software advocates believe in something more than just having source code
publically available.  They believe that software users have important rights
that must be protected, such as the right to see, modify, and distribute
modifications to the software they use.  In this perspective, open source
software is superior not just for any practical benefits, but also due to the
fact that it "respects" the rights of its users.  This approach is spearheaded
by Richard Stallman, the founder of the [Free Software Foundation (FSF)][fsf].
He has a lot to say about the subject, much of which can be found in the
Philosophy section of the [GNU][] website.

It's probably also worth noting that most free software advocates will agree
with the practical benefits given by open source advocates.  However, free
software advocates additionally believe in this ethical perspective, while open
source advocates either disagree or believe that the moral perspective is bad
for the cause of open source software, especially when it comes to convincing
businesses to create and use open source software.

## Types of open source licenses

With that background on open source politics, it may be a bit easier to
understand why there are many different open source licenses: different
political opinions inspire different licenses.  In fact, just like there are two
camps above, there are two major types of licenses.  There's a third type of
license as well, which is something of a compromise between the two major ones.
I'll talk about that a bit later.

### Permissive Licenses

Permissive licenses are licenses that are more ideologically aligned with open
source advocates.  They are generally simple and cover a few main issues:

* **Attribution:** Pretty much every license will require some sort of
  attribution from people who use or modify your code.  Some require it only in
  the source code, and others require it in the compiled program and/or
  documentation.
* **Protection:** Most permissive licenses also include legal language about how
  the authors provide no warranty for their code, and take no responsibility for
  the results of using the software.
* **Name Protection:** An additional protection that the Revised BSD license
  provides is that the authors' name(s) can't be used to endorse any software
  derived from the original.

Permissive licenses are the oldest type of software license.  The most commonly
known permissive licenses are the [MIT License][] and the [BSD Licenses][].
Both of these licenses are simple enough that you can read through them and
understand them.  Neither is much more than a few couple paragraphs long.  There
are a couple versions of the BSD licenses, which are explained on the
[Wikipedia page][BSD Licenses] quite well.  For most software developers,
especially those who are just starting out, the differences between the MIT and
the versions of the BSD licenses mean nothing.  If you're especially paranoid
about people using your name to promote something, you can go with the Revised
BSD, but other than that they are very similar.

All permissive licenses are called "permissive" because they don't place very
many restrictions on how other developers reuse the code.  All they typically
require is attribution.  This means that anybody could find some permissively
licensed code and copy it into their closed source project.  They would only
need to provide a legal disclaimer giving you attribution.  The bad part here is
that when they do this, they may end up fixing bugs and adding features to the
code.  But all of those improvements will be closed source, not added back into
the open source project.  This can occur on various scales, from little bits of
code all the way up to large projects.

Understandably, it would be very frustrating to write some software and
effectively "donate" it to the open source cause, only to have it stolen, and
have the improvements made by the "thief" not donated back in the same way you
did.  This frustration is what eventually gave rise to the second class of open
source licenses: copyleft.

### Copyleft Licenses

Copyleft licenses are ideologically aligned with free software advocates.  They
typically include most of the protections of permissive licenses, except for one
crucial difference: they require that any "derivative" work also be made open
source, under the terms of the same license!  This means that a company (or
anyone, really) with a closed source codebase could not copy portions of
"copylefted" code into their own codebase without making all of their code open
source and "copyleft" as well.

The term copyleft comes from the concept of using copyright laws to enforce what
most people consider to be the opposite of normal copyright rules.  Typically,
when you copyright code, you do it to restrict the abilities of other people to
copy your code.  With copyleft, you copyright it and grant people the right to
use your code **only** if they place the result into copyleft as well.

The main copyleft license is the [GNU General Public License (GPL)][GPL].

Copyleft licenses can be a highly political and moralized topic.  As a result,
both sides of the debate about them use some interesting tactics to discuss
them.  At one point, former Microsoft CEO Steve Ballmer referred to the GPL as a
"viral" license, due to the way it "infects" other code and "spreads" through it
like a virus.  This was during a time when Microsoft viciously opposed open
source software (a time which, thankfully, ended when Steve Ballmer stepped
down).

On the flip side of the topic, you'll find that advocates for GPL and copyleft
will argue in terms of "guaranteeing the rights of users" (in the sense of the
free software advocates).  This is all just a game of wordplay, since
"guaranteeing the rights of users" means restricting how developers reuse your
code, and having a permissive license (i.e. permissive about how developers
reuse code), would mean restricting the rights of users.  Everyone prefers to
use happy, positive language when talking about their opinions.

### Interlude: Libraries and Linking

Before I continue the discussion about the GPL, I have to pause and define
"static" and "dynamic" linking, since I'm sure many programmers of today don't
even use programming languages where you deal with that!

Most programmers are familiar with libraries.  In essence, they're just
collections of functions (and maybe classes) that somebody else wrote, and you
use in a program.  Obviously, you need to respect the license of any library you
use in your code.  In programming languages like C and C++, when you use
libraries, you need to "link" them to your program at some point.  That is, you
need to provide the machine code that implements the functions in the library.
There are two main ways of doing that.  The easiest way is to provide that code
when you compile your application.  This is called static linking.  It means
that the library's code will be included in your binary application.  The more
common (and complex) way of linking a library is to tell the compiler to search
for and load the library when you run the program.  (`.dll`, `.dylib`, and `.so`
are common file extensions for these dynamic libraries.)  That way, your
compiled program doesn't actually contain the library's code.

### Back to the GPL

Perhaps the most interesting issue regarding copyleft licenses is how they apply
to software libraries.  If I use a GPL-licensed library, am I required to
release my project as GPL licensed as well?  Unfortunately, there is really no
right answer.  You see, the GPL's copyleft requirement is only for "derivative
works."  So, if you copied a GPL'd project and improved it, you'd obviously have
to GPL your copy as well.  However, when you simply use a GPL'd library, the
issue is whether your use of the library constitutes a "derivative work."  There
are many different perspectives on this issue, and there has been no definitive
answer yet.

The FSF would argue that any use of a GPL library requires that your project
also be GPL'd.  However, many people hold that so long as you dynamically link
the GPL'd library, your software doesn't "incorporate" the GPL'd code, so your
code isn't a derivative.  Still others might say that it all depends on the
nature of your program: if your program simply uses the library and adds little
other complexity/functionality, chances are it's a derivative.  The fact of the
matter is that all of this depends on the legal interpretation of the GPL, which
hasn't yet been tested too much.  However, the safest approach in general is to
assume that if you use a GPL library, your project must also be GPL'd.

### Compromise: the LGPL

Because of this, there is a "compromise" license called the LGPL, which sits
somewhere in between permissive and copyleft.  The LGPL (Lesser GPL) is very
similar to the GPL, except that when other programs use LGPL libraries, they
need not be LGPL themselves.  However, this is only the case if the user could
replace the LGPL library with a different version of it.

This is very easy if you dynamically link to the library.  All the user would
have to do is change the installed version of the LGPL library on their
computer.  However, if you statically link with an LGPL library, you need to
provide everything that a user would need to use your program with a different
version.  If you use an open source (but not necessarily copyleft) license, then
simply making your source code available so that the user could compile and link
it with a new version of the library is *probably* sufficient.  Closed source
programs need to make object files available so that users could re-link them
with a different version of the LGPL'd library.

Of course, any other modifications or derivative works of an LGPL'd library must
also be made available under the terms of the LGPL, so for any use other than
linking, the LGPL is still copyleft.

### AGPL For Web Services

Imagine that you wrote an awesome web application, and made it open source.
Someone else could download your code, improve it, and host it themselves.
Since they're not distributing their derivative work (only hosting it), they
wouldn't have to share their improvements to your code!  This means that they
could make a knockoff of your web application with a few new features, and start
stealing your customers!

The AGPL is a solution to this loophole.  If you use the AGPL, in addition to
all the terms of the GPL, you must provide a download link to anyone who uses
your code over a network (e.g. the Internet).  Any derivative work must provide
this download link as well, thereby ensuring that derivatives become open
source, even if they don't redistribute your code.  It's a pretty niche license,
but useful if you are creating an open source web application and you're
passionate about copyleft.

## Making your code open source

After all that discussion about open source, license types, linking, and
libraries, what is the take home message for making open source software?  How
do you do it and decide on a license?  As you might have noticed, a lot of it is
based on opinion.  I've tried to be rather impartial in my description of the
perspectives and licenses above so that you could form your own opinions about
these matters.  Hopefully, I've succeeded in that.  From here on out, I'm going
to discuss how to make software open source, and how to choose a license.  I'm
going to be giving some recommendations based on a few different situations, and
my own opinions.  So take everything from here on out with a grain of salt, and
also with the disclaimer that *I am not a lawyer.*

The first step in making your code open source is making it publicly available.
Frequently people use something like [GitHub][gh-noncoders] for that.  However,
**simply putting your code on GitHub does not make it open source!** Legally
speaking, you retain the copyright to any code you write.  This means that
anyone who modifies and redistributes your code is in violation of copyright
law.  So nobody can really use your code!  In order to make your software open
source, you acknowledge that you have a copyright on the code, and then use a
license to grant people the rights to use, modify, and redistribute the code.
**You must have a license in order for your code to be open source!** Also, this
means that all your public GitHub repositories should have licenses on them!

If you still haven't formed an opinion about what license your code should use,
here is a list of steps that may help you narrow things down:

1. Do you use any libraries?  If so, what are their licenses?  If any are GPL,
   you need to use the GPL as well.  If any are LGPL, you can use any license so
   long as your users are able to swap out the LGPL portion for another version
   if they'd like.
2. Is there a serious chance you might use this code in a future job, where code
   must be closed source?  If so, a permissive license (MIT or BSD - reader's
   choice) will allow you to use your code without open-sourcing your future
   company's code.  Even the LGPL would be no good, unless your company is OK
   with dynamically linking to your library.
3. At this point, you have no real "restrictions" on your license choice.  If
   you don't want to force others into using the GPL, use a permissive license.
   If you want to ensure that all future versions of your code remain open
   source, use GPL.  If you want to ensure that all future versions of your code
   remain open source, but want to allow library users to use any license they'd
   like, LGPL is the way to go!
4. If all else fails, slap on a Revised BSD license!

## What about the other licenses??

You've probably heard of a slew of other licenses.  Several software projects
have their own licenses (Apache, Mozilla, and Python, to name a few), and some
people use those licenses on their code.  In my humble opinion, you really
should only ever be choosing from BSD, MIT, GPL, or LGPL.  Why?  These are very
common licenses.  Anyone who looks at your code and sees one of those
immediately knows what they can and can't do with your code.  If you write your
own license (**bad idea**) or use a less common one, you're forcing more work
onto potential users and developers.  If you need anything more than these four
basic licenses, chances are you are a company, and could hire a lawyer to help
you decide.

Of course there is one option that I haven't mentioned so far, which you could
do if you really don't want to deal with licenses at all.  You could just place
your code in the public domain.  In essence, this means that you give up your
copyright as the creator of the work, and allow anyone to do anything with it,
without you having any say in how they do it.  It's as simple as putting a
notice in your README saying that your code is in the public domain.  Legally
speaking, this may not mean much, since some copyright laws do not allow
copyright holders to relinquish their copyright.  So, you are better off with
using a license called CC0.  But remember, this relinquishes *all* right you
ever have over your creation!

## What about everything that's not code?

While it's a giant topic to get into, other types of media don't really mix well
with code licenses.  If you're looking for an open-source type license for your
non-code creations (text, images, music, etc), please see the
[Creative Commons][] licenses.  Their website has an interactive questionnaire
to help you choose the right license.  Just keep in mind that when they use the
term Share-Alike, they mean copyleft!

## Wrap-Up

This is pretty much all the knowledge I can impart about open source licenses.
If you need to know more about them, I find Wikipedia to be an excellent
reference, especially with regard to the general license topics:

- [Open Source Software][oss]
- [Permissive Licenses][permissive]
- [Copyleft Licenses][copyleft]
- [MIT License][]
- [BSD Licenses][]
- [GPL][]
- [LGPL][]

Additionally, the [Open Source Initiative][osi] maintains a convenient list of
licenses and templates, which are useful when you actually go to use one.  If
you're going to use the GPL or LGPL, the GNU site has a good
[article][gpl-howto] on how to use the GPL and LGPL in a project.

I really hope that this article helps to clear up the world of licensing!  If
you have any questions or comments (or errors), please leave them below!

[oss]: https://en.wikipedia.org/wiki/Open-source_software
[bazaar]: https://en.wikipedia.org/wiki/The_Cathedral_and_the_Bazaar
[fsf]: https://fsf.org
[GNU]: https://gnu.org
[MIT License]: https://en.wikipedia.org/wiki/MIT_License
[BSD Licenses]: https://en.wikipedia.org/wiki/BSD_licenses
[GPL]: https://en.wikipedia.org/wiki/GNU_General_Public_License
[LGPL]: https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License
[gh-noncoders]: {% post_url 2015-08-07-github-noncoders %}
[gh-tos]: https://help.github.com/articles/github-terms-of-service/
[permissive]: https://en.wikipedia.org/wiki/Permissive_free_software_licence
[copyleft]: https://en.wikipedia.org/wiki/Copyleft
[osi]: http://opensource.org/licenses
[gpl-howto]: http://www.gnu.org/licenses/gpl-howto.html
[Creative Commons]: https://creativecommons.org/
