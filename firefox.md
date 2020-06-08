---
layout: contentbase
title: Firefox Configuration
---

# Firefox Configuration

Each time I set up a new computer, I have to do a set of steps to get Firefox
into a usable state. This set constantly grows as Firefox adds new 'features'.
This page is not meant as a dig at the Firefox team (thanks for the great
browser, seriously!), it's just so I can have a easy-to-find reference on how I
like it set up.

### Disable comically large URL bar

Open up [about:config](about:config) and search "urlbar" in the settings. Toggle
all four of the following to false:

- browser.urlbar.openViewOnFocus
- browser.urlbar.update1
- browser.urlbar.update1.interventions
- browser.urlbar.update1.searchTips

This does two things: first, disabling "openViewOnFocus" means that the
auto-complete dropdown will only appear once you start typing into the url bar.
It will not pop up simply because you've clicked into (or used Alt-D or Ctrl-L
to focus on) the URL bar. Second, the "update1" configs disable the oversized
URL bar when it is in focus, which just looks stupid and distracting.

I would also like to make it so that clicking the URL bar will insert the caret
at the point in the text where you clicked (like any normal text input).
However, it seems that Firefox developers have completely removed this ability,
defaulting the click action to "select the whole darn contents of the URL bar".

### Disable "most frequently used" tab cycling

Open up [about:preferences](about:preferences) and uncheck the "Ctrl+Tab cycles
through tabs in recently used order" option. This enables normal tab cycling,
and in particular, reverse tab cycling with Shift+Ctrl+Tab

![ff-ctrl-tab](/images/ff-ctrl-tab.png)

### Install extensions

- [LastPass](https://addons.mozilla.org/en-US/firefox/addon/lastpass-password-manager/)
- [Tree Style Tab](https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab/)
- [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/)
- [Container Tabs](https://addons.mozilla.org/en-US/firefox/addon/multi-account-containers/)
  (How is this not built-in yet?)
- [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/)
  (This is surprisingly useful for scripting)
