---
layout: post
title: The Windows 10 Installer Dystopia
description: |
  How do you install Windows without linking your computer to an online account?
  It's nearly impossible.
---

A few days ago I had the displeasure of helping a friend reinstall Windows on
their laptop, which had previously contained Ubuntu. The reason for their switch
isn't that important -- although I helpfully suggested keeping Linux, it was
their machine and their decision. I didn't expect the process to be particularly
difficult. After all, I work on operating systems for a living now, so I didn't
expect any trouble. But to my surprise, I encountered a nearly dystopian
situation before I even got to the desktop.

I started the process by creating a bootable USB from the ISO downloaded from
Microsoft's [download page][1]. It feels weird writing that, but yes, the ISO
seems to be freely, easily downloaded. No product key was required to download,
or even install. The USB creation process was not easy (Microsoft suggests using
Windows to create the bootable USB, a chicken-and-egg problem if ever there was
one). It seems that the standard `dd` process used by every Linux vendor does
not work here -- instead you need to get the correct magic incantations of
partition types and filesystems, and then copy files from the ISO file into the
USB. I ended up falling back to a tool called [WoeUSB][2] to do this process,
after three failed manual attempts.

[1]: https://www.microsoft.com/en-us/software-download/windows10ISO
[2]: https://github.com/slacka/WoeUSB

The real fun started after I (finally) successfully booted from the USB and
started through the installation wizard. Cortana loudly greeted me, telling me
she'd walk me through the installation process using my voice. I must say that,
while I don't really care to have a voice assistant guide me through OS
installation, I can see it helping a lot of folks out there, if it works
properly (I did not test it). I'm glad that Microsoft is at least trying this
out!

I went through the (impressively quick) installation process, and the laptop
automatically rebooted. It prompted me to connect to the Internet, which I
foolishly did. Directly after connecting to WiFi, the wizard asked me to login
with a Microsoft account!

I chuckled internally. "Classic Microsoft, asking for a silly cloud login just
to use Windows," I thought. I don't know my friend's MS account login, and even
if I did I wouldn't link their OS account to some cloud account!

I searched for the cancel button, but couldn't find one. I tried to submit the
form with empty username and password, but that didn't work. Realizing that I
might be trapped, I got my phone and fired up Google.  Surely, Microsoft
wouldn't make it _impossible_ to setup a new PC without linking it to their
cloud, right?

I found an [article][3] which said that, by disabling the Internet connection I
had just configured, I could skip the login process. So, I hit the back button
on the installer. The wizard animated for a moment as if it was working, and
then showed me the same login screen. No matter how many times I hit the back
button, the wizard did not let me go back to the Internet configuration page!

[3]: https://helpdeskgeek.com/windows-10/how-to-setup-windows-10-without-a-microsoft-account/

"They haven't got me yet," I thought. I held down the power button and rebooted
the computer. Certainly on reboot I would restart the process, and could skip
the Internet configuration, right?

The laptop rebooted to a Microsoft Account login page.

So, I did what any self-respecting, conscientious friend would do for a friend:
**I reinstalled Windows all over again.**  This time, during the setup wizard
after the reboot, I skipped configuring an Internet connection. I was greeted
with this page:

![win10-nointernet]

[win10-nointernet]: /images/win10-nointernet.png
{: class="body-responsive" }

This, to me, felt kind of chilling. After all, it's not like I asked not to use
a MS account. All I did was decide not to configure Internet on my first boot,
which has nothing to do with linking a MS account. After all, maybe I just don't
have Internet access at the moment, or maybe I forgot the WiFi password.  Why
should the installer lecture me about the benefits of a MS account when simply I
did not configure WiFi? It felt obvious that this was a bald-faced statement:
"we know you're avoiding our login process, and in a few years we'll get rid of
this loophole too. Welcome to the future!"

I clicked the text (which wasn't highlighted as a link or as a button) which
said "Continue with limited setup". This was an odd phrasing, given that none of
the operating system features I'm familiar with (scheduling processes, providing
a unified interface to hardware devices, etc) requires a cloud account.

At this point, I was allowed to create a "local account" for my friend, and
finish the setup. I was presented with a list of preferences, all helpfully
enabled by default:

![win10-privacy]

[win10-privacy]: /images/win10-privacy.png
{: class="body-responsive" }

The irony here is beautiful. Ads "may be less relevant to you". The only entity
this harms is Microsoft, being able to avertise at you less (within your very
_operating system_, no less). Why should they bill this as a negative?

After disabling all of the toggles, the desktop loaded for the first time, I
noticed the following at the bottom right:

![win10-edge]

[win10-edge]: /images/win10-edge.png
{: class="body-responsive" }

I used MS Edge to install Firefox, and closed it out. On reboot, the login
screen contained two advertisements (!!!) for MS Edge. I returned the laptop to
my friend, grateful I didn't have to use this horror show of an operating
system.

## Why does this even matter?

I spend my workday working on operating systems. Don't get me wrong, I'm new to
the field, and I have a lot to learn. But as far as I know, **there is no
feature in a modern operating system which requires a cloud account login.** (I
would love to be educated if this claim is false, please get in touch!)

I used to spend my career working on machine learning and data analysis. One
thing I remember from my "past life" is that **there's nothing better than
linking different types of identifiers together.** If Microsoft can track you by
your "Windows installation ID" and also by your "Microsoft Account", then _of
course_ they want to link those two identifiers together.

More links means more data about you. What applications you run, what sites you
visit, etc. An operating system as at the root of what you trust when you use a
computer. Do you use online banking? Your operating system can read the password
to your bank account, the balances, and more, directly out of memory! I'm not
suggesting that Windows does that -- I just want to illustrate the sort of trust
you implicitly use every time you login to your bank account on Windows (or Mac
OS for that matter). But maybe Microsoft just looks at how frequently you login
to your computer, or what sites you're interested in. What DNS queries does your
OS resolve? What IP addresses have you used in the last 90 days?

All of the data which is obvious to your operating system, can be linked to your
personal identity when you connect it to a cloud account. Don't get me wrong,
even if you don't connect it to a cloud account, you still are getting
incredible amounts of telemetry and tracking recording your every move. But why
would you voluntarily give more links and data to Microsoft?

I don't think most people understand the sort of data they're giving over to
Microsoft when they login and use Windows. These dark patterns that Microsoft
employs are sickeningly obvious, and really difficult to avoid. Why would I
trust a company that tries to manipulate its customers into such total data
collection, to be responsible with the data it receives?

I can't imagine how frustrating it must be to be an operating system developer
at Microsoft. I have a lot of respect for the operating system kernel they make.
It seems to be one of the few major non-Unix like kernels out there. It seems
fascinating and I'd love to learn more about it. But it must be frustrating to
see the product of your hard work go out packaged with software capable of
collecting and tracking your users' every move, and thrown together with an
installer intent on forcing them to submit to this data collection.
