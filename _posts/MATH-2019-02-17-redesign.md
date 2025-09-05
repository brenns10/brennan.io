---
layout: post
title: Site Update
description: A brief rundown of changes made to the site.
---

Today I made a few changes to my site's design which hopefully makes things a
bit more user-friendly for anyone using this site.

## No more trackers

My site has used Google Analytics for quite a while. This was mostly born out of
my idle curiosity about how many people view my site. I had quite an appetite
for seeing the "reddit effect" or "HN effect" in my analytics if a post got
popular. Of course that comes at the price of Google tracking people around my
pages in order to better target ads at them. So, I've removed Google Analytics
from my site.

I also used to integrate with Disqus, to allow people to comment on my posts.
This was a genuinely useful feature, but Disqus is full of ad trackers as well.
So I removed the comments integration. There may be some future work to
re-attach existing comments to the site without JS, but it's not super high
priority to me right now.

Finally, I used to place social media buttons at the bottom of each post. These
buttons came with some Javascript probably did all sorts of tracking as well.
I've replaced them with simple links that should achieve the same result, but
without the trackers.

All of these trackers provided me some sort of feeling of pride or recognition
or validation. Analytics showed me that people were visiting, comments showed me
that people wanted to talk about what I wrote, and the buttons got to show the
world how many people liked my posts. But all of these things traded off against
the privacy of readers, and it's time for me to correct that.

## No more MathJax

In order to include fancy equations like the following:

$$
    \begin{equation*}
      e^{i \pi} + 1 = 0
    \end{equation*}
$$

I had been using [MathJax][] to render the equations in the browser. Now I just
render them to images and embed them. I lose out on a few features (text
zooming) but I gain in having a usable site for those who would prefer to leave
JS disabled.

There are some other cosmetic changes (serif to sans-serif fonts, new images,
etc), but nothing too dramatic. Hopefully these things make the site a bit
better!

[MathJax]: https://www.mathjax.org/
