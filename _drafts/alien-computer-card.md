---
layout: post
title: Creating an Alien Themed Linux Greeting Card
description: Creating an Alien Themed Linux Greeting Card
---

Recently I've been saying goodbye to a lot of friends as I prepare to move
across the country. In the case of my roommate of three years, a simple goodbye,
or even my best homemade card just would not be good enough (I can't draw). So I
decided to apply my programming and Linux skillset to what just might be the
weirdest e-card anyone has ever made: a bootable Linux flash drive.

My roommate is a big fan of the *Alien* series, especially the classic first
movie, and the really awesome video game, *Alien: Isolation* (I guess you could
say I'm a fan too!). So I thought it would be really neat to create a bootable
flash drive that has the same feel - complete with the same boot image as
computers from the movie, sound effects from the movie and game, and programs
that look like the ones you interact with in the game. Everything turned out
much better than I could have hoped. I'll describe the basics of how I did it in
this article, and then provide some downloads and a link to the source.

## The foundation

I'm an Arch Linux user, so when I think of creating a bootable Linux ISO, the
first thing that comes to mind is the [archiso][] tool. This is the set of
scripts that creates the bootable Arch Linux "installer" ISO, and it can be
customized for a lot of other stuff.

I started my project by copying all of the scripts and configuration files into
my own repository, which I could customize to my heart's delight.

## Customized boot splash

The first thing I wanted to do was have a similar boot up splash screen to the
computers you see in the film *Alien*. At the [beginning of the movie][yt-boot],
you can see a splash screen that contains `NOSTROMO`, the ship's name, and a
serial number. Here's a capture of that particular moment:

![Nostromo boot screen capture][]

I was able to find an artist's reproduction of this image on [DeviantArt][],
which I figured I could use (sans the watermark) as the boot image. Of course,
to make it a boot image, I had to use a special program, [Plymouth][]. This
tool, used on a number of Linux distributions, allows you to create a boot theme
which is displayed instead of the console messages your kernel and init system
would otherwise output.

However, creating a theme requires either writing a C extension to Plymouth, or
learning an arcane scripting language and writing the extension in that. I opted
for the scripting language. But I guess the more accurate way to put it was that
I followed a set of [tutorials][brej] right up until the point where I had what
I wanted. The result: [`plymouth-theme-nostromo`][], which is incidentally
available in the [AUR][aur-ptn].

## Sound effects

At the beginning of *Alien*, the computer makes all sorts of beeping, whirring,
and clattering noises. Since I really enjoy all of the sounds in the movie and
game, I had to get these sound effects into the boot sequence as well! So, I
found a video containing all of these sound effects on Youtube.

<iframe width="100%" height="480" src="https://www.youtube.com/embed/2ywWFvjE-yU" frameborder="0" allowfullscreen></iframe>

I used `youtube-dl` to get the audio from this video, and I cut it to just the
first part (nothing involving the later scene with Mother). Then, I wrote a
systemd unit file which would play the sound as soon as sound is available:

```
# /etc/systemd/system/startupsound.service
[Unit]
Description=Boot Sound
After=alsa-restore.target

[Service]
Type=simple
ExecStart=/usr/bin/startupsound

[Install]
WantedBy=multi-user.target
```

This just calls a shell script:

```bash
#!/bin/sh
amixer sset Master unmute
aplay /var/local/startup.wav
```

The script just unmutes sound and then plays my startup sound. Of course,
there's more than just computer sounds, if you want to create a real atmosphere.
Another thing I wanted was to have some ambient "spaceship"
sound. [Another Youtube video][yt-ambient] provided this. I trimmed a portion of
that and set it on a loop in another bash script, and then created another
systemd unit file for that.

Finally, I wanted to add a bit of tension to the atmosphere... as if an alien
could come at you at any moment. So I found some alien noises from *Alien:
Isolation* in [yet another Youtube video][yt-alien]. I selected my favorites and
put them in a directory. Then I created this Bash script to play a randomly
selected sound every 30-90 seconds:

```bash
#!/bin/bash

files=(/var/local/alien-sfx/*.mp3)
while :
do
	sleep $[ ( $RANDOM % 60 ) + 30 ]s
	mpg123 "${files[RANDOM % ${#files[@]}]}"
done
```

Again, I hooked it up to a systemd unit file, and I was set.

## Retro terminal

Now, what to do once the flash drive actually boots? In *Alien* all of the
computers are stylized with green text on black background, on CRT screens. The
default Linux console can probably be customized a little bit, but not to the
extent I would like to make it immersive. So I decided to go a different route.

[cool-retro-term][] is a terminal emulator which aims to look like an old CRT
screen. It is also fairly customizable, so I was able to create a profile that
looks exactly like I envision a computer on the Nostromo would look like.

[archiso]: https://wiki.archlinux.org/index.php/archiso
[code]: https://github.com/brenns10/alien-iso
[yt-boot]: https://www.youtube.com/watch?v=2ywWFvjE-yU
[DeviantArt]: http://quadrafox700.deviantart.com/art/Nostromo-boot-screen-127110997
[Plymouth]: https://wiki.archlinux.org/index.php/plymouth
[brej]: http://brej.org/blog/?p=174
[`plymouth-theme-nostromo`]: https://github.com/brenns10/plymouth-theme-nostromo
[aur-ptn]: https://aur.archlinux.org/packages/plymouth-theme-nostromo
[yt-ambient]: https://www.youtube.com/watch?v=U4p1mZnKkhc
[yt-alien]: https://www.youtube.com/watch?v=qiyXFQKheOU
[cool-retro-term]: https://github.com/Swordfish90/cool-retro-term


[Nostromo boot screen capture]: /images/alien-splash.png
{: style="max-width: 100%;"}
