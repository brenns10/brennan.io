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

This gets rid of the URL bar that pops open to exceed its size. While it looked
funny, the bigger issue (IIRC) is that it messed up the standard keyboard
shortcuts (Ctrl-L to focus on URL bar, ESC to stop).

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
