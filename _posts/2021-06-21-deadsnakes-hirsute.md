---
layout: post
title: Use deadsnakes PPA on Ubuntu hirsute
description: |
  Get more mileage out of the amazing work by the deadsnakes team.
---

Today I upgraded a computer of mine from Ubuntu Groovy Gorilla (20.10) to
Hirsute Hippo (21.04). The process was mostly painless, but I had to go through
the standard process of evaluating each file in
`/etc/apt/sources.d/*.distUpgrade` to determine how all of my PPAs or other
software repositories needed to be updated. The one that took the most work was
the Deadsnakes PPA.

Deadsnakes is a truly wonderful repository containing builds of alternative
Python versions. Each recent Ubuntu version ships one Python 3 version that is
the system default -- currently version 3.9 on Hirsute. However, if you develop
Python tools or libraries, you may want alternate versions around for testing.
For instance, some projects of mine have Tox files to automatically run tests on
Python 3.6-3.10. The Deadsnakes repo provides several recent Python 3 releases,
except the system version for your OS. However, only LTS releases are supported.

This makes sense: the majority of Ubuntu installs are LTS, so the cost/benefit
tradeoff doesn't make sense to support the more frequent 6-monthly upgrades. But
I'm used to running Arch Linux and having very up-to-date packages, so the idea
of staying on an LTS version with packages that are already at least 1-2 years
out of date is... not pleasant. So I stick with the regular 6-monthly Ubuntu
releases, and I generally make do by installing packages from repos which are
targeted at the last LTS release. Surprisingly, this works quite well[^1].  For
example, on Groovy, I was able to just edit my Deadsnakes `sources.list.d` file
to look for packages for `focal` (the prior version).

Unfortunately, this doesn't work for Hirsute. While Focal and Groovy both have
the same system Python (3.8), Hirsute upgrades it to 3.9. If I installed the
Deadsnakes Focal Python packages, then the `python3.9` package within the PPA
could replace the default Ubuntu system python -- which is not ideal. Plus,
since the Focal repository omits `python3.8` in order to avoid replacing the
system Python on Focal, I wouldn't be able to get that version!

There is a way to get the best of both worlds though. Apt (the Ubuntu package
manager) has a directory where you can place "preferences" that help prioritize
(or "pin") packages on your system. With it, you can do the following:

1. Block all packages from the Deadsnakes PPA from being installed.
2. Re-enable packages which match a particular Python version.

So, if you add the Deadsnakes Focal repository to your system, you could use
this approach to ensure that the Python 3.9 package can't be installed. But,
you'd still need to find a way to install Python 3.8. You can manage this by
simply going back one more Ubuntu release, to Bionic. The default Python there
was 3.6, so there is a 3.8 package available to install. Thus, the final
approach is:

1. Add an entry for Focal and Bionic Deadsnakes repositories within
   `/etc/apt/sources.list.d`. This entry looks something like this, and can be
   saved in any filename within the directory (you may already have a relevant
   one if you used `add-apt-repository` to add the PPA -- in this case, just
   modify it).

       deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu/ focal main
       deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu/ bionic main

2. Add the following rules which blacklist all packages from the repos, and then
   selectively enable Python versions from the correct locations. This can be
   put in any filename within the directory `/etc/apt/preferences.d/`

       Explanation: Prevent installing from deadsnakes repo.
       Package: *
       Pin: release o=LP-PPA-deadsnakes
       Pin-Priority: 1

       Explanation: Allow installing python 3.{6,7} from deadsnakes/focal
       Package: *python3.6* *python3.7*
       Pin: release o=LP-PPA-deadsnakes,n=focal
       Pin-Priority: 500

       Explanation: Allow installing python 3.8 from deadsnakes/bionic
       Package: *python3.8*
       Pin: release o=LP-PPA-deadsnakes,n=bionic
       Pin-Priority: 500

3. Run `sudo apt update` to update your cached package info, and then you should
   be able to install other Python versions! You can use `sudo apt policy` to
   view the rules, and `sudo apt policy python3.7` (for example) to see the
   different package versions your system is choosing from, along with their
   priorities.

So, is this a particularly safe setup? Well, I haven't had too much trouble.
It's definitely not supported -- so you shouldn't bug the Deadsnakes maintainers
with issues that spring up if you try this approach. If you're familiar with the
tooling (read through `man apt_preferences`) and comfortable poking around if
things get a bit messed up, then you should have no problem using this as a
daily driver.

#### Footnotes

[^1]:
    I believe that most of the issues of using packages stem from misaligned
    library versions, for example your package requires libfoo version X, and you have
    installed version Y. If version X and Y aren't compatible (e.g. Y has
    changes incompatible with X, or is missing symbols from X), then you would
    get an error from the dynamic linker when you try to run the program: "DLL
    hell". libc seems like the most frequent, obvious source for this sort of
    error, since it's used by virtually all software. But for whatever reason, I
    don't encounter issues with libc frequently. I would love to learn more
    about why!
