---
layout: post
title: "Piano to Computer: MIDI on Arch Linux"
description:
---

I have an 88-key digital keyboard, and one of its neat features I never bothered
with before was a little USB port on the back.  Today, I bothered with it.
Turns out, that USB port is a MIDI output, which means that you can record
everything from your keyboard directly to your computer, with no background
noise or anything!  However, it's a bit difficult to get it working, especially
on Arch Linux.  So in this article I'll explain the basics.  First, let's start
with a little background knowledge.

### Digital Audio versus MIDI

*Most of this is relevant, but you'll have to bear with me, because I think this
stuff is pretty fascinating.*

Digital audio is an incredibly awesome breakthrough that lets us record, store,
edit, and play back sound on computers.  The idea isn't actually that difficult,
even though the world of digital audio is incredibly complex.  Sound is a wave.
Its amplitude determines its "loudness" and its frequency determines its pitch.
In order to record sound, we need to save this wave somehow.  We do this by
every so often taking a "sample" of the current amplitude of the sound wave, and
turning that into a digital number.  If you do that fast enough (say, 44,100
times per second), you can get a pretty good picture of this wave.  Later on,
you can send those same samples to circuits which will convert them back to an
analog wave, and then send that wave to speakers.  That is, in a nutshell,
digital audio.  So, if I used a microphone to record myself playing my keyboard,
I would be using digital audio.

[MIDI](https://wiki.archlinux.org/index.php/MIDI) is nothing like that.  It's a
protocol that allows musical instruments (like digital keyboards) to communicate
with other devices.  Instead of sending samples of sound waves, it sends
information like "play a C" and "stop playing C".  When I plug my keyboard into
my computer, this is the information that gets sent to the computer.  Sadly, my
computer has no concept of how to play notes---it only deals with digital audio
samples.  So in order to do anything 
