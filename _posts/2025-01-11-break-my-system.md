---
layout: post
title: Break my System, Please!
---

For what feels like a year at this point, I've been receiving this wonderful
message from `pip` when I try running `pip install --user SOME_PACKAGE`:

```
$ pip install --user virtme-ng
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try 'pacman -S
    python-xyz', where xyz is the package you are trying to
    install.

    If you wish to install a non-Arch-packaged Python package,
    create a virtual environment using 'python -m venv path/to/venv'.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip.

    If you wish to install a non-Arch packaged Python application,
    it may be easiest to use 'pipx install xyz', which will manage a
    virtual environment for you. Make sure you have python-pipx
    installed via pacman.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

I'm using Arch (BTW) and while I don't recall exactly which Python/pip version
brought this in, I'm quite confident that I understand the error that they're
referring to, and quite frankly, I don't care.

### What's going on

Say my Linux distribution includes `awesome_package`, a Python application which
has a specific set of dependencies. In particular, it depends on `great_dep<2.0`,
which is a popular dependency for many Python applications. But
`awesome_package` in only compatible with verisons of `great_dep` that are
before the version 2.0, which apparently broke compatibility with an API.

Later, I decide to install `latest_package`, another Python application. It
uses even more recent Python dependencies, and in particular, it requires
`great_dep>=2.0`. If I install that with `pip install --user`, it can either
upgrade `great_dep` (breaking `awesome_package`) or it can refuse to install due
to the incompatibility. In my experience, pip does the former: it installs the
new version, silently breaking `awesome_package`.

So later on, if I run a command from `awesome_package`, it will try to import
`great_dep` but it will get the incompatible version that was installed into my
home directory, rather than the compatible version installed by my Linux
distribution. This would cause problems!

### The Cure is Worse Than the Disease

So now, Python (or Pip, I'm not really sure) displays this great error whenever
I attempt to install packages into my home directory! Because any package that
exists in my home directory _might_ get accidentally used by a package installed
at the system level. We've traded an error that _might_ occur, for one that will
*definitely* occur, and which will cause far more trouble!

And what's funny about this is that Arch (in particular) is a rolling release
distribution. So all the Python packages it releases are (putatively) bleeding
edge, unlikely to be broken by the installation of a slightly newer dependency.

### The Best Cure was Easy

And of course, the piece-de-resistance is the fact that Python has shipped with
a command line option, `-s`, for quite a while now:

```
-s     : don't add user site directory to sys.path; also PYTHONNOUSERSITE=x
```

Say that you have a system-level script. You could simply update its shebang
line to read:

```
#!/usr/bin/python -s
```

This would ensure that user-specific site directories aren't added to the Python
path, effectively removing the entire risk of breakage here!

And most Linux distributions already have packaging scripts that manage the
shebang lines of Python (and other) scripts. So this isn't a big ask: it's just
the cost of doing business, yet Python/Pip decided the best option is to create
this silly error message.

### The "Right Way"

Search or post online about this and you'll hear that the "right way" to handle
this is with `pipx` or some other package manager _du jour_. These package
managers maintain separate virtual environments for every application. I think
it's good to have this option around: some applications may need that level of
control of their dependencies. But on average it's just wasteful -- I don't
really want the equivalent of a giant `node_modules` directory for every Python
script I install.

I could spend my time arguing that this is a bad way of packaging applications,
and that Linux distributions can do better. I would then fall into the rabbit
hole of static vs dynamic linking, and have to address the benefits & drawbacks
of Flatpak, Snap, Docker, etc... While I enjoy that debate, and I definitely
have opinions on it, it is a rabbit hole. And honestly, my main issue isn't
whether this is a good way to package applications.

My main complaint is simpler. I know that Python lets me break my system! That's
been the assumption. I shouldn't need to tell it that. I expect that. I want
that.

Seriously: Python & Pip are not distribution systems for user apps. They're
tools, to be used by developers who understand them. They should be allowed to
break things when used incorrectly: that's what tools do (just watch me attempt
to use a wrench on my car!). Leave it to other applications (like `pipx`!) to
innovate in the space of delivering applications, and don't break the workflows
that people use with `pip`.

I love that Python lets me break things. I love that system apps can import code
out of my user site directory, and I'm ok with that. I use that feature. I'm ok
with the risk that I may install a newer version of `requests` that causes
problems. If I do, I'll figure it out. That's what happens when I use developer
tools like `pip`.

So really: break my system packages, Pip. I'm begging you.
