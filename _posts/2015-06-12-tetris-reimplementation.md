---
title: On Tetris and Reimplementation
layout: post
---

I'm the kind of programmer that likes to implement everything myself.  That's
not to say I don't believe in other people's work.  But rather, I believe that
if I do something myself, I will gain a lot more from it than if I use someone
else's implementation.  For instance, I've implemented my own
[regular expression parser](https://github.com/brenns10/cky) in C, using my very
own [C data structures library](https://github.com/brenns10/libstephen).
Hopefully I'll post a bit more about those in the future.

Without a doubt I've gained tons of experience and knowledge by doing those
things myself.  So it kind of makes sense that I would continue that process by
doing another project that's already been done, all for the sake of learning how
to do it.  This time, I tackled the game of Tetris.  To keep it interesting, I
decided to do it in C.

This actually isn't my first game in C -- I wrote a
[Minesweeper](https://github.com/brenns10/minesweeper) clone in C a few weeks
back.  I never blogged about it, but I might in the future, since it was a fun
project.  That experience probably helped guide me through this process.

## Making C GUIs

The thing about writing games is that you have to focus on the interface.  I've
got plenty of experience writing libraries (i.e. code that other programmers can
use to make their programs).  Libraries are nice.  You think about how you, a
programmer, would like to use the service your library provides.  You come up
with names for all the functions, along with descriptions of how they should
work.  You write example code that uses your hypothetical library, to see how
comfortable it is.  Then, you start implementing those functions.  There's no
"user interface" per se.  You spend all your time thinking like a programmer,
which is very intellectually interesting.  But most software is written for
users, and games are probably the most user-oriented software around.

C doesn't really give you lots of simple options for user interfaces.  There is
the classic command line interface (read from the console, print to the
console).  That type of interface is nice, because all you need to do is deal
with incoming text and outgoing text.  Unfortunately, not only is that
unsuitable for most games, but most users run screaming away from a terminal
(i.e. command prompt) window.

On the other extreme of C GUI programming, you have the world of window
toolkits.  These libraries give you the power to create windowed programs like
you're used to seeing on a desktop computer.  There are quite a few of these
toolkits.  Microsoft Windows, of course, comes with one.  Linux has a wide array
of them, with the GTK being a prime example.  Unfortunately, any windowing
toolkit in C involves copious amounts of boring and difficult to understand
code.  The reason behind this is simple: C is a rather low level programming
language.  In general, programming languages are bad for describing GUIs.  The
lower level they are, the more work it is to describe what your interface looks
like in code.

Fortunately, there is a happy middle ground.  For somebody who wants to quickly
write a simple Tetris game, this middle ground is perfect.  Instead of printing
and reading lines of text to the console, what if you could draw your interface
on it?  Since consoles are simple grids of characters, it would be easy to make
a grid-oriented game like Tetris that way.  As it turns out, this is a fairly
common interface style (especially for Linux/Unix programs).  Plus, there is one
pretty much universal library for making these interfaces, called `ncurses`.

`ncurses` gives you the ability to do some very cool things with a terminal
window.  While a typical C program can only add text to the terminal by
printing, `ncurses` programs have the ability to move the cursor around on the
terminal, and put individual characters wherever you'd like on the screen.  In
this way, an `ncurses` program can build a user interface with lots of
interactivity, directly on the terminal window.

## Building Tetris

So, I decided pretty much from the beginning that I wanted to make Tetris using
`ncurses`.  The next step along the way was building the game logic.  My goal
was to have my Tetris game logic completely separate from the user interface
logic.  I achieved this by having two code files: `tetris.c` and `main.c`.
`tetris.c` has no idea about a user interface, because `main.c` handles all of
it.  Similarly, `main.c` doesn't know anything more about how Tetris is
implemented than what I made public in the `tetris.h` header file.  The
reasoning for this is pretty simple.  You should write code that does only one
thing, and does it well.  If you take a sloppy approach and do two things in the
same code (like implement Tetris game rules in your user interface), you're more
likely to mess up both of them.  Plus, an important bonus of this approach is
that I can make a new interface for my Tetris game without ever touching
`tetris.c`.

### Game Logic

I initially thought that Tetris would be trivially simple to write.  A little
bit of research showed me that there's actually a lot more to it than you might
think.  For instance, you take it for granted that when you rotate a block
against the wall, it will "kick" out (instead of getting stuck).  That (and
every other special behavior) is something you need to keep in mind as you build
the game.

I started with a simple game loop, and filled it out over time.  The function
`tg_tick()` (`tg` stands for `tetris_game`) performs a single iteration of the
game loop.  It looks like this:

```c
/*
  Do a single game tick: process gravity, user input, and score.  Return true if
  the game is still running, false if it is over.
 */
bool tg_tick(tetris_game *obj, tetris_move move)
{
  int lines_cleared;
  // Handle gravity.
  tg_do_gravity_tick(obj);

  // Handle input.
  tg_handle_move(obj, move);

  // Check for cleared lines
  lines_cleared = tg_check_lines(obj);

  tg_adjust_score(obj, lines_cleared);

  // Return whether the game will continue (NOT whether it's over)
  return !tg_game_over(obj);
}
```

Let's tackle this line by line.  First up is `tg_do_gravity_tick()`.  In Tetris,
the falling block moves down every so often due to gravity.  The higher your
level, the quicker it moves down.  So the gravity tick function will count down
how much longer until the next time gravity "acts".  If it is time to pull down
the block, the function does so, and then resets the timer, using your
difficulty level to figure out how long until the next gravity action.

After the gravity tick, the game handles user input by calling
`tg_handle_move()`.  This function takes a `tetris_move`, which can be any of
the moves you're used to doing in Tetris: move right, move left, drop, rotate,
or put a block on hold.  It executes that move, and returns.

Now that gravity and user input are handled, it's possible that some of the
lines of the board have been filled up.  So, we call the `tg_check_lines(obj)`
function to count those lines, and remove them.  And then we update the score
based on how many lines were cleared.  Scoring depends on both your level, and
the number of blocks you cleared.

Finally, the user interface code that calls this `tg_tick()` function will want
to know when the game is over.  So, `tg_tick()` returns `true` while the game is
running, and `false` once the game has ended.

There's a decent amount more code that goes into the tetris game logic -
`tetris.c` totals almost 500 lines.  I'm not going to present it all in a blog
post.  It's fairly interesting, because that code needs to know every type of
tetromino, and what orientations they have.  It has to do collision detection,
and handle "wall kicks" when you rotate the pieces.  If you're interested in
exactly how I did it, you can see more at the
[GitHub repository](https://github.com/brenns10/tetris).

### User Interface

Of course, all of the code for the game logic above did nothing to display the
game to the user.  It simply modified the structure of the game in memory.  The
job of displaying that game, and handling the user's input, was done by
`main.c`.

I would like to show the main function of `main.c`, but I feel like it is too
long to show in this block post.  It's not complex or difficult to understand,
but there are many lines and most of the specifics aren't relevant.  But, I can
give a reasonable pseudocode explanation of how it works.

```c
int main(int argc, char **argv)
{
  // If the user gave a filename, load the saved game.  Otherwise, start a new
  // game.

  // Initialize the ncurses display library.

  // Do the main game loop:
  while (running) {

    // Call tg_tick() to move the game forward.

    // Display the new game state.

    // Sleep for a bit (otherwise the game would be too fast.

    // Get user input for the next loop.
  }
}
```

For more information on the user interface code, you can look at `main.c` in the
[GitHub repository](https://github.com/brenns10/tetris).


## The End Product

At the end of the day, my simple Tetris implementation is pretty complete.  In
just over a day of work, I implemented most of the features of Tetris:

* The basics (i.e. gravity, movement, rotation, and line clearing).
* Storing blocks and swapping them out later.
* A scoring system copied from an earlier version of Tetris.
* A level progression that increases difficulty the longer you play.
* A pause menu (and "boss mode" pause menu, which replaces the game with a fake
  terminal screen that looks like you're working).
* A game save/load feature so you can come back to your games.

The only thing I really wasn't able to do was play the Tetris theme song in the
background.  Maybe some day I could come back to it, but the options out there
for simply playing sound in C aren't very good.

If you want to try it, it would be best for you to be running Linux.  You'll
need to have `ncurses` installed (for Ubuntu, that means running `sudo apt-get
install libncurses5-dev`).  Then, get the
[GitHub repository](https://github.com/brenns10/tetris), compile with `make`,
and run with `bin/release/main`.


## Conclusion

In this post, I've spent a lot of time on the implementation of my Tetris clone.
And, to be sure, I think it's worth talking about.  I think I came up with a
pretty decent design, and that makes some of the code (like `tg_tick()`) very
nice to look at.  What's more, it's a program I seriously enjoy playing, which
is an accomplishment in and of itself.  However, I'd like to conclude with a bit
of a philosophical diversion regarding reimplementation.

When I told my girlfriend I was writing Tetris, the first words out of her mouth
were along the lines of "hasn't that already been done?".  That's a pretty
reasonable reaction.  And the truth is, of course it has.  If that were the
criteria for writing programs, most of the code I've written in my life wouldn't
exist.  Sure, there's a lot to be said for doing something new and different,
and even more to be said for code reuse.  But doing something old and the same
is not nearly as bad as it's cracked up to be.  Practice makes perfect, and
practicing by reproducing the big name, important programs out there (like
[shells](https://github.com/brenns10/lsh),
[regular expressions](https://github.com/brenns10/cky),
[web servers](https://github.com/brenns10/yams),
[firewalls](https://github.com/brenns10/pywall), and
[other games](https://github.com/brenns10/minesweeper)) is the best way to hone
your programming skills, while expanding your domain-specific knowledge by leaps
and bounds.

Programmers that know loops, conditionals, functions, and classes are so common.
They come out of universities like cupcakes out of a mold.  You can do plenty
with just that knowledge, but to me, that's just the beginning of a much more
exciting education.  When you learn how real world problems are solved, you
finally have a chance to do the things that you probably were told about in
school, but never learned because you didn't actually implement them.  Plus, you
get started on learning the domain specific knowledge (e.g. Linux, HTTP, TCP,
`ncurses`, GTK, ...) that nobody teaches you in school, but someday you'll use
every day in your job.  And even if you don't use that specific set of
domain-specific knowledge, you'll benefit from having your mind broadened with
new tools and approaches that you wouldn't have otherwise encountered.

In short, doing these little "reimplementation" projects has been a vital part
of my education, complementing the computer science theory I learn in school.
I'm certain that I wouldn't be the programmer I am today without them.  I can
think in terms of C programming now.  Pointers, arrays, structs, bits, bytes,
and system calls are becoming second nature to me.  I understand how programs do
the things we take for granted like create processes, spawn threads, and
communicate.  I could talk your ears off about how packets are routed through
the Internet, and how a firewall sifts through them, especially in Linux.  I
adore the Chomsky Hierarchy, and would love to tell anybody who listens about
how the pure theory of regular languages and finite automata has led to the
implementation of regular expressions, one of the most widely used computer
tools in the world.

With the understanding and experience gained from reimplementation projects, I
think in new and better ways.  I see the connections between new problems and
old ones.  I think in terms of how to re-use the best ideas.  I'm getting better
at recognizing why design decisions were made.  I can approach problems in the
same disciplined manner I've observed in other implementations.  The discrete
bits of information I've picked up are merging into a new kind of understanding:
a combination of broad knowledge, better approaches, and a recognition of how
little I actually know.  And the best part is, I'm just 20 years old.  Some
people have been programming longer than that.  Imagine what sort of experience
I'll have in another 10 years!  Probably enough to make me think that everything
I'm doing now is silly!

So, as I get ready to stop the rambling and get off my soapbox, my final thought
is simple.  Let's do more re-implementation.  Let's try writing the code that we
rely on, even if we think we "already know how it works."  Chances are, it'll
make us all better.
