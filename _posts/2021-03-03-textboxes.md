---
layout: post
title: Please Stop Form Validation on Key Strokes
description: |
  Formerly "Please Stop Using keyCode for Form Validation".
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

The requirement that I use Shift to access numbers in my keyboard layout is the
reason why I couldn't enter digits into the form field. The form used a type of
"form validation" which attempts to _prevent you from entering invalid input_.
The problem is that the code which implements this does not handle keyboard
layouts properly. If I change my keyboard layout to QWERTY -- or copy-paste some
text[^1] -- I'm able to enter numbers. The reason behind this is some Javascript
code which I'll reproduce here:

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

This code is wired up to the `keydown` event of the text box. The `keyCode`
value is [documented here][]. At the end of the day, it seems to be some weird
mashup of ASCII codes to refer to keys. The problem with this code lies in the
second if statement (under the comment "Ensure that it is a number and stop the
keypress if not"). The if condition is a bit messy, so I indented it across
multiple lines and commented the keys to make it more readable.

    e.keyCode == 13             // ENTER
    || e.keyCode == 109         // Subtract
    || (
        e.shiftKey
        || (
            e.keyCode < 48      // 0 above letters
            || e.keyCode > 57   // 9 above letters
        )
    )
    && (
        e.keyCode < 96          // numpad 0
        || e.keyCode > 105      // numpad 9
    )

Honestly that's not much better, but here are a few interesting cases:

- Enter and subtract are always blocked
- If shift key is held (and the key press was not a numpad button), block the
  key press.

This last one is what matters. Holding down shift while hitting the number key
(_even if you are in fact entering a digit_) results in a blocked keyboard
event. And this is all because of the faulty assumption that numbers can only be
entered without holding shift. The Programmer Dvorak layout does not follow this
assumption.

It seems to me that this sort of form validation just sucks. I get that client
side validation is pretty convenient, but straight-up *preventing* invalid input
by making it impossible to type is... terrible! There's no visual indication to
the user that their input is blocked because it's invalid. They might assume
(like I did) that their keyboard may not be working, or that the OS is having an
issue.  At the very least, it would be better to have a visual aid, like a
quick flash of a red outline on the text box, to let the user know their action
was "invalid."

But that wouldn't solve the problem that in this case, the logic for blocking
the "invalid input" was just plain wrong. This sort of code is difficult to get
right, especially considering the possible keyboard layouts and variations
between OS and browser. I'd argue it'd be better (and easier to maintain) to
just ditch it. Instead, just validate the contents of the text field against a
regex after each change.

[documented here]: https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode

**Update, Nov 2022**: My original version of this article incorrectly focused
on whether keyCode values vary across different keyboard layouts. That's largely
irrelevant. I've updated the article to focus on the core issue: Shift key
blocking numeric input from being registered. Thanks to Matthew Wilcox for
pointing it out. You can find the original version of the article in [git][].

[git]: https://github.com/brenns10/brennan.io/blob/1d7fa8921ad886e7a23b11fc5d9946e57d5a9b40/_posts/2021-03-03-textboxes.md

---

#### Footnotes
[^1]:
    What's even more frustrating is that due to the same "form validation"
    described in this article, the Ctrl-V keyboard shortcut for pasting is also
    blocked. I need to manually paste via right-click.
