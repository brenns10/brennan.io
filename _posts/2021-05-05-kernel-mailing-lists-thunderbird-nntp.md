---
layout: post
title: Subscribe to Kernel Mailing Lists over NNTP on Thunderbird
description: And avoid drinking from the LKML firehose
---

Linux kernel mailing lists are really important to watch and learn. They're the
best place to watch what's happening upstream, you can see (almost) every change
and the review process that goes into it. They can help you build an
understanding for what sort of development is taking place on a particular
subsystem, and how the maintainer and reviewers feel about certain types of
changes.

However, subscribing to kernel mailing lists is a bit like trying to drink from
a fire hose. Sure, it's possible, but the volume is frequently so high that it
will overwhelm you. If you attach your work or personal email to that firehose,
you run the risk of burying your other important messages, or even filling up
the inbox completely. Until recently, the only other option I knew was browsing
the web archives, e.g. on [lore.kernel.org][lore].

However, I recently discovered a great alternative! The mailing list archives
provided by [lore.kernel.org][lore] are served via HTTP, but also via a protocol
called NNTP[^1]. You can point a newsgroup reader at these archives, and read
them in a way that is very similar to email. I think that Thunderbird happens to
be a great choice for this[^2]. It supports NNTP/newsgroups with an interface
very similar to an email mailbox, and it will track the read/unread status of
each message, show message threads as a tree, and even let you mark messages as
"important". Here's how to get it setup:

1. On the main startup page of Thunderbird, you may see a section
   that says "Set Up Another Account", with a button for "Newsgroups". If that's
   available, click it. Otherwise, use the menu button at the top right (three
   horizontal lines), click "New", and select "Other Accounts...". Either way,
   you'll find yourself at this dialog:

   ![setup-1]

2. Select Newsgroups, which brings you to this screen:

   ![setup-2]

3. As I did above, enter your name and email. You don't have to enter anything
   real here, because there is no login involved. I'm not really sure why this
   question is asked. Click Next to find this screen:

   ![setup-3]

4. Enter the text `nntp.lore.kernel.org` and click Next:

   ![setup-4]

5. Enter any name you want for the account. I chose to stick with the default,
   which was the URL from above. Click next to reach a confirmation screen, and
   click Finish. You'll find yourself at a new (empty) newsgroup account in
   Thunderbird:

   ![manage]

6. Click the "Manage newsgroup subscriptions" button so that you can select your
   mailing lists.

   ![subscribe]

7. Here you're presented with a nice big list of "newsgroups". These correspond
   with the actual mailing lists archived by [Lore][lore]. The naming is pretty
   self-explanatory. You can filter by the name of a mailing list with the
   search bar. Check every item you want to subscribe to, then hit Ok.

8. At this point, you find yourself at the home screen. You might need to expand
   the newsgroup account on the sidebar to see the mailing lists you've
   subscribed to. If you select one, you'll enter the viewer, and you'll get a
   prompt like this:

   ![download]

   I highly recommend you choose the second option and download a small portion
   of the history. Old history is great for data analysis or later reference,
   but I don't find myself ever wanting to go back and just browse it.

9. Finally, you should find yourself at a fully loaded mailing list view:

   ![done]

The end result is a mailbox for each mailing list. The default view is threaded,
and it gives you most of the options you would expect from an email inbox, with
the notable exception of composing or replying to messages. One notable oddity
(for folks like me who are used to GMail-like interfaces) is that Thunderbird
puts the newest messages at the _bottom_ of the list. You can individually
change the sort order using "View > Sort By > Descending", but it has to be done
per-list. Consider [this approach][sortorder] if you want to set the default
sorting order.

### Sending Messages

Since Thunderbird is reading from a mailing list archive, it may be a few
minutes behind, and it won't let you send messages. If you want to reply to
threads, then your best bet is to do the following:

1. Make sure your email account is configured in Thunderbird.
2. Make sure you're familiar with kernel mailing list etiquette. This is well
   documented in the kernel source tree.
3. Find the message you'd like to reply to in the [Lore web UI][lore], and there
   should be a little "reply" button at the bottom of the message. Follow the
   instructions there to download the message.
4. Open the mbox file in Thunderbird (File > Open > Saved Message) and you can
   reply with your email account.

It _may_ even be possible to reply directly from the newsgroup message using the
"Reply All" button. You would need to take care to remove the "newsgroup"
recipent, and also ensure that you've set the "From" account to your correct
outgoing email account. I have not tested this - drop me a line if it works!

###  Conclusion

Hopefully this provides a lower barrier to entry for browsing the kernel mailing
lists! Please let me know if it helped or if you learn another useful way to
engage with the mailing lists.

[setup-1]: /images/thunderbird/setup-1.png
{: class="body-responsive"}
[setup-2]: /images/thunderbird/setup-2.png
{: class="body-responsive"}
[setup-3]: /images/thunderbird/setup-3.png
{: class="body-responsive"}
[setup-4]: /images/thunderbird/setup-4.png
{: class="body-responsive"}
[manage]: /images/thunderbird/manage.png
{: class="body-responsive"}
[subscribe]: /images/thunderbird/subscribe.png
{: class="body-responsive"}
[download]: /images/thunderbird/download.png
{: class="body-responsive"}
[done]: /images/thunderbird/done.png
{: class="body-responsive"}

[lore]: https://lore.kernel.org
[sortorder]: https://superuser.com/questions/13518/change-the-default-sorting-order-in-thunderbird

---

#### Footnotes

[^1]:
    NNTP is "Network News Transfer Protocol", and it powers Usenet, which for
    people my age could be thought of as "Reddit for the 80's and 90's".
    Notably, it is the place where Linus Torvalds first posted an announcement
    about a tiny Unix clone he was working on.

[^2]:
    While I don't use Thunderbird as my primary email client, and certainly not
    directly for sending patches or replying to reviews, it happens to be a
    really convenient and well-made email client.
