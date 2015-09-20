---
title: Superfish Explained
layout: post
description: >
  Lenovo preloaded software on their personal computer line that compromises the
  security of SSL-enabled websites.  Read this article to understand what these
  words even mean!
keywords: Security Internet
---

Yesterday a big story was broken about Lenovo selling computers with malware,
called Superfish, preinstalled.  Most people are familiar with the typical crap
that comes preloaded on a new computer.  They are usually low quality "trial"
programs that you'll need to upgrade if you want to use them.  Your computer
manufacturer puts them on their computers because they are paid by the people
who make these programs.  But these programs aren't usually malware.  They may
be crap, wastes of space, or just plain annoying, but rarely are they malware.

Superfish is a step beyond your typical preinstalled "crapware".  It's a program
that listens in on your web browsing, analyzes the images that are being
downloaded, and inserts advertisements for products that are visually similar.
The technology (visual search) is pretty cool, but it's not OK to listen into
web browsing without telling a user.  Unfortunately, the problem with Superfish
isn't just the privacy concerns, it's the fact that it opens a gaping security
hole in Lenovo computers.

In this post I'm going to explain the security vulnerability that Superfish
creates, in plain English.  I want this to be accessible to readers of all
levels of computer understanding.  I'll explain how it works so you can
understand why you should care about it.  In order to do that, let me start with
some small explanations.

## Protocols: the building blocks of the Internet

In order for the internet to work, computers need to know how to talk to each
other.  Protocols are like sets of instructions for how computers behave when
they interact with each other.  For instance, humans know that when they walk
into a restaurant, they wait to be seated, read their menus, order food, wait,
eat, pay, and tip their waiter or waitress.  This is a protocol for eating out.

Computers have protocols for things like browsing the Web.  That protocol is
called HTTP.  When you decide you want to go to Google, your computer starts
speaking HTTP with one of Google's computers.  It asks for the home page, and
the website sends it back.  One problem with HTTP is that it's not private.  I
could listen into your conversation with a website and know every page you asked
for, and all the pages the website sent back to you.

That's why we have another protocol called TLS.  It makes your conversations
private by doing three things:

* Authentication: Ensuring that the website you're talking to is the one that
  you think you're talking to.  (Imagine that you thought you were talking to
  your online banking site, but instead you talked to a hacker's website.)
* Confidentiality: Ensuring that people can't listen into your conversations.
* Integrity: Ensuring that people can't change your messages as they go between
  you and the website you're talking to.

When you take HTTP, the web protocol, and put it inside TLS, the privacy
protocol, you get HTTPS, the secure web browsing protocol.  When you have a
green lock displayed in your browser, you know you're using HTTPS.

## How TLS does authentication

If we lived in a perfect world, TLS could do its job perfectly, without any
help.  But we don't, so it doesn't.  In order to verify that a website is who it
says it is, TLS needs to know whether or not it can trust the website.  It does
that using a rather complicated system of private keys and certificates.  The
basic ideas are like this:

* A certificate can either represent a website, or a "certificate authority."
* Certificates can be signed by other certificates to show that they are trusted
  by the signer.
* Behind every certificate is a private key.  It must be kept secret, since it
  is the critical bit of information that is used to sign other certificates.
* Your computer has a list of "trusted root certificates".  These are the
  certificate authorities that your computer trusts to verify the identity of
  websites' certificates and sign them.  Your computer will trust any website
  whose certificate is signed by a trusted root.

The root certificate authorities will sell signed certificates, usually for a
hefty fee and some stringent requirements of proving your identity.  The result
is that, if I wanted to create a certificate that said I was "google.com", I
couldn't verify it with the root certificate authorities.  They wouldn't sign my
certificate, and so, your computer wouldn't trust that I was Google.  If I could
somehow get a fake certificate signed by a trusted root, then I would be able to
pretend to be a website that I wasn't.

## The Superfish Vulnerability

So, now we get to the meat of the issue.  Superfish, as explained above, likes
to listen into your web browsing so it can look at the images you see, and then
advertise similar looking products.  But when you use HTTPS, Superfish can't
intercept, read, or change your conversation with websites -- just as intended.
Lenovo and Superfish, however, got their heads together and came up with a
crafty way around this.

Since Lenovo makes the computers, it gets to do whatever it wants to them before
it sells them.  So, it had Superfish create its own certificate and private key.
It adds the Superfish certificate into the computer's list of trusted root
certificate authorities.  Now, any certificate signed by Superfish's certificate
will be trusted unconditionally be Lenovo computers.

Now, every time a Lenovo computer starts connecting to a HTTPS website, the
Superfish program running on the computer generates a fake certificate for that
website, and signs it with the Superfish root certificate (**using the private
key**).  Then, it intercepts the conversation, pretending to be that website.
From there, it can do exactly what it's supposed to -- look at images and insert
advertisements.

The problem (which I put in bold above) is that in order for a root certificate
to sign a website certificate, you need to have the root's private key.  These
are usually kept very, very secret.  But in order for Superfish to work as I
just described, every copy of the program (and every Lenovo computer) needs to
have a copy of the private key.  If someone were to find that private key, they
would be able to pretend to be any website they'd like, and any Lenovo computer
with the Superfish root certificate would believe them.

And guess what?  That's exactly what happened.  In
[this article](http://blog.erratasec.com/2015/02/extracting-superfish-certificate.html),
you can read the details of how someone was able to extract the private key from
the Superfish program and crack the password.

Armed with this private key, a hacker could pretend to be your bank, or your
email provider, or anyone else.  They could steal your passwords, money, and
other intimate knowledge about you, if you own a Lenovo computer.  And all
because Lenovo wanted to get a few extra advertising dollars from your private
web browsing.

## Why it matters

This is a situation where the ethics of a company's decision making comes into
question.  Somewhere down the line, someone at Lenovo had to make the call and
say: "yeah, I think we should put this snooping program with the private key on
our computers!"  Anybody who knew what that meant knew the dangers, but was
willing to sacrifice their customers' security in order to earn a few extra
dollars.  And that seems like something worth knowing.
