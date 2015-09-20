---
title: Interacting With X Clipboard in Bash
layout: post
description: >
  A quick tip on how to copy and paste input and output directly from the
  command line.
keywords: bash tips
---

I ran across this neat trick a couple days ago.  I was looking for a way to copy
command output from my terminal, rather than using the clumsy selection
capabilities in my terminal emulator du jour.  I hit
[this](//stackoverflow.com/questions/749544/pipe-to-from-clipboard) Stack
Overflow article, which introduced me to `xclip`, a program that lets you
interface with X ['selections'](//en.wikipedia.org/wiki/X_Window_selection).
These selections are basically text buffers in the X window system.  The
clipboard is one of them (the `CLIPBOARD` selection), and so is any text you
highlight (the `PRIMARY` selection).  The `xclip` program lets you use those
buffers as the source or destination of a pipeline!

Unfortunately, using `xclip` to interface with the clipboard requires a few
non-obvious parameters.  You need to specify which selection you want to use.
In my case, I wanted to use the clipboard, so my selection is `c`.  The
parameter `-i` puts text into the buffer from stdin, and the parameter `-o`
takes text from the buffer and puts it into stdout.  If you use `-f` with `-i`,
it 'filters' the text--copies it, and then prints it to stdout.  So, with these
flags, you can come up with Bash equivalents for your typical cut, copy, and
paste operations.

```bash
$ xclip -selection c -i    # Cut (does not filter)
$ xclip -selection c -i -f # Copy (does filter)
$ xclip -selection c -o    # Paste
```

Of course, with a few simple lines in your `.bashrc`, you can do even better.
Take the keyboard shortcuts for cut, copy, and paste, and turn them into Bash
aliases!  (You could try to use the words cut, copy, and paste for the aliases,
but paste is already a command).

```bash
$ alias x='xclip -selection c -i'
$ alias c='xclip -selection c -i -f'
$ alias v='xclip -selection c -o'
```

Once you have that in your `.bashrc` and sourced that in your terminal, you can
start piping from `v`, and piping to `c` and `x`.  There are quite a few ways
you could use these commands.

- **Capturing command output.** This is pretty obvious--it's why I looked for
  these in the first place.  There are plenty of times you could use this, like
  getting command line output to post on a forum.  It's as simple as `$ command
  | c` if you want to see the output and copy it, or just `$ command | x` if you
  want to just copy it without seeing.

- **Saving a text selection to a file.** Instead of opening up an editor,
  pasting text, and saving it, you can just use the terminal: `$ v >
  /path/to/file`.

- **Exporting GPG keys.** If I want to copy my public key, I can just type `$
  gpg --export-key 0EC665D8 | x`.  Then I can go post it wherever I'd like.

- **Debugging pipelines.** If you're using a slightly complicated pipeline, you
  can insert `| c |` into whatever point you'd like to see what is going on.

I'm already finding these additions to my `.bashrc` to be really useful.  I hope
they're useful to you!
