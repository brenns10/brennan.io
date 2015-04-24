---
title: Case's Missing Man Page
layout: post
tags:
 - Tutorial
---

If you ask me, my admission to Case Western Reserve University came missing one
critical feature: a [man page](https://en.wikipedia.org/wiki/Man_page) (for
those who don't know, it's a *manual* page, not testosterone-filled piece of
paper).  Here I am, at a really cool university with some really great IT
resources: high bandwidth internet connections, registered hostnames that show
up in DNS, integrated single-sign on system, Google Apps, etc.  And I'm a member
of a great Computer Science program with a heavily active student group,
Hacker's Society.  But somewhere along the way, it seemed to slip everyone's
minds that student hackers like me would want to create new websites,
applications, and tools to enhance the student experience here at CWRU.  And
what is the one thing that a hacker needs to use a tool?  That's right, a *man
page*.

So consider this CWRU's missing man page.  I'm going to outline a couple of the
technologies that Case uses in its web services, so that students have less
trouble getting started when they want to contribute a new tool to the campus.
I learned all of this the hard way: by digging until I found the right clues,
then researching the clues, and asking the right people the right questions.  I
definitely gained a lot by this process, but I believe that we all stand on the
shoulders of those who come before us, and I want to make it easier for the
people who come after me.


Single Sign On
--------------

Every CWRU student recognizes the universal
[login page](https://login.case.edu/cas/login) for web services.  But have you
ever noticed that a *lot* of sites use it?  Not just official CWRU websites.
There are even sites that were obviously not created by CWRU administrators
(like [Blackboard](https://blackboard.case.edu) or [HKN](https://hkn.case.edu))
that use the same login page.  The reason is that Case uses what's called a
[Single Sign-On system (SSO)](https://en.wikipedia.org/wiki/Single_sign-on).
This means you can have a single username and password, log in once, and be
signed into every service that uses Case's SSO.  Best of all, pretty much any
website you make can be a "service" that uses Case's SSO!  So let's get into the
nitty gritty of what it is, and how it works.

    https://login.case.edu/cas/login

Above is the URL for the CWRU SSO login page.  Right inside the URL is a hint at
what type of SSO Case uses: CAS.  This three letter acronym stands for
[Central Authentication Service](https://en.wikipedia.org/wiki/Central_Authentication_Service).
CAS is just a protocol, but it has a nearly universal implementation called
JASIG CAS, which is used by tons of universities, including CWRU.  The CWRU CAS
server is, in fact, `https://login.case.edu/cas`.

So how does an average web application use CAS?  Well, the application gives you
a login link.  This link goes to the CAS server URL (plus the `/login` command).
It also includes a GET parameter named "service", which is simply a URL that the
CAS server will redirect the user to once they have logged in.  So, if your
application is, say, `https://awesomeapp.case.edu`, then your login link URL
might be:

    https://login.case.edu/cas/login?service=https%3A%2F%2Fawesomeapp.case.edu%2Flogin

(`%3A` is a URL-encoded colon, and `%2F` is a URL-encoded forward slash).  When
the user clicks on this link, they are taken to the CAS login page, and they log
in.  When they successfully log in, they are redirected back to the URL
specified in the `service` parameter, except, it has an additional GET parameter
pinned onto it, called "ticket".  So, if you went to the URL above and signed
in, you would be redirected to:

    https://awesomeapp.case.edu/login?ticket=ST-XXX-XXXXXXXXXXXXXXXXXXXX

Except, `ST-XXX-XXXXXXXXXXXXXXXXXXXX` would have something else in the X fields.
This is called a service ticket.  It's big and random!  Now, the web application
doesn't know if the ticket is legitimate, or if someone just made up a ticket
and stuck it in their URL.  So, it has to call the CAS server.  This time,
instead of redirecting the user to CAS like it did last time, the web
application actually makes a HTTP request to the CAS URL, this time using the
`/serviceValidate` function.  It also sends along the two parameters we've seen
so far: the "service" that it originally included in its login link, and the
"ticket" that it just received.  So in this example, it would send a GET request
to the following URL:

    https://login.case.edu/cas/serviceValidate?service=https%3A%2F%2Fawesomeapp.case.edu%2Flogin&ticket=ST-XXX-XXXXXXXXXXXXXXXXXXXX

CAS should respond by returning a piece of XML telling the application whether
the ticket is valid, and if so, information about the newly authenticated user.
Here is a sample response by CAS (given in the
[protocol specification](https://jasig.github.io/cas/development/protocol/CAS-Protocol-Specification.html)):

{% highlight XML %}
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
 <cas:authenticationSuccess>
  <cas:user>username</cas:user>
  <cas:proxyGrantingTicket>PGTIOU-84678-8a9d...</cas:proxyGrantingTicket>
 </cas:authenticationSuccess>
</cas:serviceResponse>
{% endhighlight %}

And that's it!  The web application now knows for sure that the user has been
authenticated by the trusted CAS server, and it has all the information it needs
about the user to continue.  Typically, an application will then drop a session
cookie so that the user can stay logged in.  For that reason, whenever you write
an application that uses CAS, you need to use SSL -- even though you don't ever
touch the user's password!  So long as you are using a session cookie, you need
SSL to prevent session hijacking.

### CAS Clients

Coming up with a simple client that supports the bare minimum described above is
actually pretty simple.  The logic of your `login` page would look like this:

* If I got a `ticket` in the GET parameter:
    * Call `serviceValidate`.
    * If the ticket is valid:
        * User is logged in.  Create session.
    * Otherwise:
        * Login failure.  Show an error page.
* Otherwise:
    * Redirect to the CAS `login` page.

However, if you implemented this in your production code, I would come to your
dorm and kick you!  Unless you have studied the
[CAS protocol](https://jasig.github.io/cas/development/protocol/CAS-Protocol-Specification.html)
(it's worth reading) for a while, created a complete client implementation, and
thoroughly tested it, you probably shouldn't be creating a client
implementation.  Go with a pre-made one for your framework.  There are plenty
for Django, but my personal favorite is
[django_cas2](https://github.com/KTHse/django-cas2).  For Ruby, I believe I've
heard of something called RubyCAS that will probably do the trick, although I
have never used it.  And finally, for PHP, I'm sure there are many libraries
which can do the job for you.

By using these, you can make your service restricted to people with Case IDs,
and avoid requiring them to create a new username and password on your web
application.  Two points!
