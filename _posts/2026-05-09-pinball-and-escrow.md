---
layout: post
title: Space Cadet Pinball on Linux
---
To my fellow Linux users who grew up using Windows XP: did you know, you can
have Space Cadet Pinball on your Linux machine? This is not breaking news, but
it's exciting to me, and I'm the one who decides what I write about. So here's
your PSA!

Space Cadet Pinball was bundled with Windows XP, and growing up I played it a
lot. As a result it holds a special place in my heart. I found that it was the
most engaging game that was bundled with Windows.  Solitaire was too mindless,
and Freecell, Hearts, and Minesweeper were too complex and boring to me at that
age. But pinball held my attention, and so I played it a lot[^1].

Anyway, somebody has gone to the effort of using a decompiler and reverse
engineering tools to create source code, and then put in what I'd imagine is a
lot of effort to make it playable on a lot of platforms! All that results in
[this project on Github](https://github.com/k4zmu2a/SpaceCadetPinball). The
easiest way to play on Linux is actually to use the Flatpak, which comes bundled
with the original game resources from the Windows version. You can either
install it with a GUI (e.g. KDE Discover) or install on the CLI:

```
flatpak install com.github.k4zmu2a.spacecadetpinball
```

That's all you need to play & get a hit of nostalgia! I know there are
[browser-based versions](https://pinball.alula.me/) available too, but I would
rather have it installed on my computer directly.

### High(er) Resolution With Full Tilt Data

Graphics technology has come a long way since then, and the graphics are a bit
rough at 480p. But fear not: another version of the game existed, called Full
Tilt! Pinball. Its game data is capable of displaying at the massive screen
resolution 1024x768! You can find this game data [on
archive.org](https://archive.org/details/full_tilt_pinball) in a zip file.

Getting the flatpak version to use these data files is a bit tricky. The easiest
way is:

1. Ensure that you've run the game at least once prior to this, so that the data
   directory is created.
2. Extract the downloaded zip file directly into your data directory:
   ```
   cd ~/.var/app/com.github.k4zmu2a.spacecadetpinball/data/SpaceCadetPinball
   unzip ~/Downloads/CADET.ZIP
   ```
3. Delete (or, if you're cautious, rename) the old data directory which is
   bundled with the app. Unfortunately this is necessary because the game
   searches multiple locations for data, but once it finds data files in one
   directory, it won't continue looking for files in other locations.
   ```
   sudo rm -r $(flatpak info --show-location com.github.k4zmu2a.spacecadetpinball)/files/extra/Pinball
   ```
   You may not need the `sudo` call if your installation was per-user. Mine got
   installed to `/var/lib/flatpak` so I needed root.

It's possible you'd need to repeat step 3 if the game gets updated. However, [the
flatpak](https://flathub.org/en/apps/com.github.k4zmu2a.spacecadetpinball)
hasn't seen an update in over two years. I doubt one will happen, and if it
does, it won't be frequent.

### Random Notes

1. If you want, you can keep the original files and merge them together so that
   you have the full set of both the original (referred to as "3DPB" for 3D
   Pinball in the game) and the new (Full Tilt) data. Then, the game will let
   you toggle between them if you'd like.

2. The data files seem to have some impact on the game rules. For instance, in
   the original 3DPB version, the reentry lanes (and launch lanes) have lights
   which toggle as the ball passes over. In the Full Tilt version, the lights
   stay on (rather than toggling), making it easier to complete the set of
   lights and upgrade the associated set of bumpers. (Yes yes, I know I'm a nerd
   for noticing this.)

3. Apparently, there was a game called "Marble Blast" which came pre-installed
   on some Macs in a roughly similar time period, which I know people developed
   similar relationships to growing up. Unlike this pinball game, the Marble
   Blast series grew, and there are newer versions available to play today.

### Bonus Thoughts

I think it's great that this old game was beloved to enough people (and
especially at least one very competent & motivated person) to do this work.
Having (any) source code available makes this game portable to all sorts of
platforms, which is really great. You can play this on Mac, Windows, Linux, and
even Android & Nintendo Switch, apparently.

Personally, I would be happy to pay the original developers for their work on
this game, and I understand that there's some concern about the legality of
downloading game data files, especially for the Full Tilt version of the game.
After all, they are copyrighted art & data which was part of a commercial
product. It seems like an unpopular opinion in today's world, but I don't
advocate for piracy. Paying people for their work is important, even when it
feels like you're paying a faceless corporation. While I'd prefer things be
created with a FOSS license, the world doesn't always work that way. At the end
of the day, I want people to be paid to create good things, because that's how
we get more good things!

On the other hand, I feel software preservation is an important goal too.
Ideally, I'd like to see a world where proprietary software like this could be
placed into some sort of [source code
escrow](https://en.wikipedia.org/wiki/Source_code_escrow). As long as the
original copyright holders are in the business of selling their product, their
rights should be respected. But if they elect to stop selling it, I think that
code should revert to a FOSS license that allows users to improve & maintain the
software they use. This would help balance the rights of creators, users, and
the goals of preservation.

---

[^1]: I also played another pinball game called 3D Ultra Pinball, but that came
      on a CD presumably for purchase. I have no idea whether my parents went
      out and bought it, or if it came in a cereal box. (Yes, game CDs did show
      up in cereal boxes sometimes.)
