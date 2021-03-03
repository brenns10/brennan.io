---
layout: post
title: Please Stop Using keyCode for Form Validation
description: |
  Not everyone uses QWERTY
---

Today I encountered a bug in a web form. A textbox required a numeric value, but
when I attempted to enter it, I found that none of my keystrokes resulted in
digits appearing in the box. I've experienced this bug once every few months for
several years at this point. I always knew the reason for it, but today I felt
just annoyed enough to fully research the issue and write about it.

I use a keyboard layout called "Programmer Dvorak" rather than the more standard
QWERTY. I'm not here to convince anyone it's better. I started using it 8-9
years ago in my freshman year of college because I was convinced it would help
me type faster (and it had programmer in the name). I'm not sure whether it
worked, but the muscle memory I developed has kept me with it for the better
part of a decade. The keys are arranged like this:

![layout](/images/dvp1.png){: class="body-responsive" alt="A diagram showing the layout of keys in Programmer Dvorak. Numeric digits are located on the same physical buttons, but are rearranged, and require the shift key to use them."}

In particular, the digits are weird. While they use mostly the same physical
keys as QWERTY, they are rearranged, and they require using the shift key in
order to use them. This is an interesting trade-off, as it allows you to more
easily access symbols (brackets, parens, etc) which you probably use more
frequently while programming, and the digit rearrangement makes it easier to get
to frequently used indices like 0 and 1. That, said, these changes were a major
pain, by far the hardest change to learn. Who knows if it was worth it?

The digit placement in my keyboard layout is the reason why I couldn't enter
digits into the form field. The form used a type of "form validation" which
attempts to _prevent you from entering invalid input_. The problem is that the
code which implements this does not handle keyboard layouts properly. If I
change my keyboard layout to QWERTY -- or copy-paste some text[^1] -- I'm able
to enter numbers. The reason behind this is some Javascript code which I'll
reproduce here:

```javascript
function(e) {
  // Allow: backspace, delete, tab, escape
  if ($.inArray(e.keyCode, [46, 8, 9, 27]) !== -1 ||
    // Allow: Ctrl+A, Command+A
    (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true)) ||
    // Allow: Ctrl+C, Command+C
    (e.keyCode == 67 && (e.ctrlKey === true || e.metaKey === true)) ||
    // Allow: Ctrl+X, Command+X
    (e.keyCode == 88 && (e.ctrlKey === true || e.metaKey === true)) ||
    // Allow: home, end, left, right, down, up
    (e.keyCode >= 35 && e.keyCode <= 40)) {
    // let it happen, don't do anything
    return;
  }
  // Ensure that it is a number and stop the keypress if not
  if (e.keyCode == 13 || e.keyCode == 109 || (e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
    e.preventDefault();
  }
  //allow only three digits and disallow negative, but only when the text is not highlighted
  if ($(e.target).val().length >= 3 && (e.target.selectionStart == e.target.selectionEnd)) e.preventDefault();
}
```

This code is wired up to the `keydown` event of the text box. It relies on the
`keyCode` attribute of the event. I'm not a frontend export, or even competent,
so I ended up searching and found [this great writeup][moz-article] on the
Mozilla Hacks blog. `keyCode` seems to refer to a physical button identifier on
your keyboard, whereas other (newer) attributes exist to refer to that button's
meaning within the user's keyboard layout. In particular, this snippet uses
`e.shiftKey` to ensure that you cannot use a digit key while holding down the
shift button.

The code written above is making one of two assumptions:

1. The charitable explanation is that they knew about the variations in keyboard
   layouts, and noticed that almost all keyboard layouts use the same digit
   placement as QWERTY, so they went ahead with using `keyCode`.
2. The more likely explanation is that the developer didn't know that `keyCode`
   doesn't work across keyboard layouts. The code uses 65, 67, and 88 to refer
   to the A, C, and X keys, and these would all be in different locations for
   different layouts as well.

It seems to me that it's time for code like this to go away. It's 2021, and
better web APIs seem to have existed since 2017. Lots of keyboard layouts exist,
and while this particular issue affected me on a pretty weird layout, this kind
of issue can affect lots more people. I have the programming knowledge to make
an educated guess and switch keyboard layouts, but most people probably don't.
So my appeal to frontend developers out there is: please remember that not
everyone uses QWERTY, and stop using `keyCode`.

While we're at it, can we stop using this kind of form validation? Straight-up
*preventing* invalid input by making it impossible to type seems both confusing
for the user and error-prone. What ever was wrong with highlighting invalid
input using Javascript, without directly blocking it?

[moz-article]: https://hacks.mozilla.org/2017/03/internationalize-your-keyboard-controls/

---

#### Footnotes
[^1]:
    What's even more frustrating is that due to the same "form validation"
    described in this article, the Ctrl-V keyboard shortcut for pasting is also
    blocked. I need to manually paste via right-click.
