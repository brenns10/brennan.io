---
layout: post
title: When it comes to git history, less is more
description: |
  One person's entry-level contribution is another person's difficult bugfix or backport.
---

At a previous company, there was an "infamous" commit in our main repository.
The commit was about 10 years old, and it replaced every tab with 4 spaces. When
the commit was authored, the repository was likely in the hundreds of thousands,
or maybe millions, of lines of code. For folks like me, who liked to go
"spelunking" through git history, it was a frustrating barrier, but no more than
a moderate frustration. It didn't impact day-to-day work. After all, this repo
was a regularly-deployed web application. Development happened on the master
branch, deploys happened multiple times per business day, and old revisions were
quickly forgotten.

When I started trying to contribute to the Linux kernel, the commonly suggested
way to get started was to contribute coding style fixes, or to correct simple
warnings from a static analyzer. But this came with some advice: try to keep
your submissions within the `drivers/staging` directory, because many core
kernel subsystem maintainers and reviewers don't appreciate those trivial
patches. I remember being quite frustrated at that. It felt quite unwelcoming to
be restricted to what I saw as a "playground", rather than working on "real
kernel code."

Now, my day-to-day work involves diagnosing, reproducing, and fixing bugs in
Linux kernel versions which have been released for years. Unlike a web app, the
kernel has long-term stable releases that continue to be supported long after
the master branch has moved on. Fixing a bug on the master branch doesn't
magically fix all those released kernels; instead the fix must be backported to
each older release.

In the simplest case, this "backport" could just be `git cherry-pick`, which
simply applies a change to a different branch. However, if the surrounding code
is at all modified, then the commit may not apply cleanly, and you'll need to
manually apply the changes and resolve conflicts. Now, it's important to say
that just because a commit applies cleanly to an older version of code, _doesn't
mean that it's a valid backport_. For instance, a function you call may have
changed its behavior, and some side-effect that your patch relied upon could no
longer exist. But for the majority of the time, a clean cherry pick is likely a
safe backport. And, each time you encounter a commit which doesn't apply
cleanly, your backport becomes much more labor-intensive.

So there's a really strong incentive to make sure commits backport cleanly! The
easier it is to backport, the more efficient it is to get bug fixes to users on
the stable versions they actually use. Engineers can be more efficient and
customers will be happier.

What's really impressive to me is just how good the Linux community is at this.
I've seen bugfixes apply cleanly to release branches from 10 years ago with no
issues, something that would be completely impossible with the infamous
tabs-to-spaces commit at my previous company.

Since starting the (slightly less glamorous) job of wrangling bugs in stable
kernels, I've come to appreciate the discipline exercised by kernel maintainers.
Their unwillingness to accept more trivial patches is something like a first
line of defense. When patches fail to apply, it's less likely to be due to small
style refactors, and more likely to be due to real differences between versions
that need to be addressed. This means that automated tools can handle more of
the simple cases, leaving the difficult ones up to developers, without quite so
much of the tedium.

I guess there are two morals to this story. First is that with experience comes
perspective. I felt that the `drivers/staging` guideline was restrictive and
maybe a bit elitist, but now that I understand the reasoning, it makes sense.
Second is that, as always, there's no silver bullet. It would be fun and punchy
to end this post with the advice that "you should never do big code style
changes" and "you should always discourage trivial, non-functional patches". But
for the regularly deployed web application with no legacy versions to maintain,
that just doesn't make sense. So instead, maybe this post can help provide some
perspective on why the kernel is maintained the way it is.
