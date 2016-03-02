---
title: Logging in With Requests
layout: post
description: >
  CWRU's single-sign-on system is a very great way to let web developers offload
  their authentication concerns for students.  But for people that like web
  scraping, it's more difficult to log into a site with SSO.
---

One of my favorite types of quick side projects are ones that involve web
scraping with Python.  Python has a few excellent tools which can be combined to
create a powerful, easy to use system for quickly harvesting data from webpages.
Web scraping involves writing code that uses HTTP (like a web browser) to
request pages from websites.  The Python library [requests][] is great for that,
and as a bonus, it is widely recognized as having one of the best APIs out
there!  Once you have the page, instead of displaying it to a user like a
browser would, you search through the code for information.  Since webpage
content is primarily written in HTML, parsing and searching them is difficult.
So, the Python library [lxml][] comes in handy here.  Not only will it parse
HTML, but it includes a powerful search tool called XPath, which allows you
craft a "query" that narrows down exactly what part(s) of a page you want to
inspect.

With these tools, the fundamental tasks of web scraping are very easy.  For
example, this code will get you the biosketch on the front page of my website
(as of this writing):

```python
# Load our libraries
import requests, lxml.html

# Request my homepage (using requests)
page = requests.get('http://brennan.io')
# Parse the HTML (using lxml)
html = lxml.html.fromstring(page.text)
# Search for the part of the HTML that has my biosketch
content_divs = html.xpath('//main/div[@class="content"]')
# Print out the first search result's text content, stripping away any
# extra whitespace.
print(content_divs[0].text_content().strip())
```

The search query (`//main/div[@class="content"]`) is a bit complex, but if you
research HTML and XPath a little bit, and then look at my website's source,
it'll all make sense.

## Scraping Sites with Logins

Unfortunately, not every website is this easy to scrape.  There are many reasons
that a website may not be easy to scrape, but one common one is that it requires
you to log in.  Fortunately, many websites that require you to log in also
provide a nicer way for programmers to access their data; typically an API.
However, for those sites that don't provide an API, you can still "fake it" by
pretending you're a user on a web browser!

When you log into pretty much any website, here's what happens:

1. Your browser requests (using a HTTP GET request) the login page.
2. You enter your username and password in the form and hit enter.
3. Your browser sends that info (this time using a HTTP POST request) back to
   the login page.
4. If the the username and password are correct, the server will send back a
   response that contains a "cookie".  This is just a piece of text that your
   browser will send back to the site with every subsequent request.  The
   website associates that cookie with your currently logged in session (that's
   why it's called a "session cookie").  Due to the way the Web was designed,
   this is pretty much the only way a website can keep you logged in.

If you're trying to scrape a website that requires you to log in, you can just
start at step 3: send your username and password (pretending you're a browser)
to the login page.  Then, hold onto the session cookie the website gives you and
use that on all future requests.  The website will treat you as logged in from
then on!

Let's check out some code that does exactly this!  For the sake of example,
we'll pretend that my website requires you to log in before you can access my
homepage (a pretty silly proposition, but whatever).  My login page would
probably be at `http://brennan.io/login`.  This code will "log in" to my site
and then use the cookies returned from that to access my homepage.  (Of course,
if you try to run this code, it won't work since I don't actually have a login
page or session cookies!)

```python
import requests

# You'd have to fill in the quotes with a real username and password.
login = {'username': '', 'password': ''}

# Send this info to the login page.  This time we use a POST!
result = requests.post('https://brennan.io/login', data=login)

# Note the https above!  I feel obligated to say, never send passwords unless
# you are using HTTPS!  (My site doesn't actually use HTTPS, sadly)

# This contains the awesome cookies that we just received.  One of them should
# be a session cookie.
print(result.cookies)

# Now, we do the same request as before, just adding in our cookies:
page = requests.get('https://brennan.io', cookies=result.cookies)

# And the example proceeds just like above.
```

That's not much more difficult, right?

## Dealing With Tickets

Well, sadly, it isn't always that easy either!  You see, the thing about web
forms is that, if they're really that easy to impersonate in code, then you can
bet that malicious attackers would take advantage of it.  In particular, if an
attacker managed to get you onto their website, they could load simple
Javascript code that runs in your browser and impersonates you submitting a form
on another website.  For example, they could change your password on a website
you're currently logged into!  This is called a Cross-Site Request Forgery
(CSRF), and it's a well known place for people to attack websites.  So people
who develop web applications include security measures against them.

The most common security measure is called a CSRF token.  The web site generates
a random string of text (the "token") whenever you request a form (using HTTP
GET).  This token will eventually expire.  When you submit the form (using HTTP
POST), the token will get sent back to the server.  So long as the token hasn't
expired, the server will accept your form.  Since the attacker couldn't have
gotten their hands on a valid token before impersonating you, the server will
always reject their faked forms.

This approach is applied to login forms just like any other form.  Sometimes, it
will be called a login ticket instead of a CSRF token, but it's the same thing.
You will know there is a login ticket in a site's login form if there is
something like this in the login page's source:

```html
<input type="hidden" name="ticket" value="LO56SB-RANDOM-VALUE-HERE-A23MS2B56">
```

One other approach that people sometimes use is to make sure that they set a
fresh session cookie whenever you GET the login page.  If session cookie and
login ticket don't match, they know there's a problem.

Thankfully, we're not attackers trying to exploit users in a browser.  So, we
have a bit more leeway to get around these protections.  To address the login
ticket issue, we'll need to add some code to request the login page once using a
GET request.  This gets us a ticket (and depending on how the site works, it may
also drop a session cookie right then instead of after we login).  We just have
to search for that token in the login page (we will once more employ lxml for
this task).  Then, we can send that ticket with the username and password, and
everything will work the same as before.

To deal with the fact that we don't know when the site will give us a session
cookie, we're going to start using a really useful feature of the `requests`
library: `Sessions`.  A `Session` holds onto all sorts of things between
requests, one of which is the cookies!  So if we make all our requests in the
same `Session`, we can be sure that we'll capture and hold onto the session
cookie.

Here I'm updating my example code from before, now pretending that my site uses
CSRF tokens too!

```python

import requests, lxml.html

# This will be our session the whole time.
session = requests.Session()

# First, we get the login page.
login_page = session.get('https://brennan.io/login')

# Next, we parse it with lxml and search for an field named "ticket".  Note that
# the name may not be "ticket" - you'd normally have to search through the page
# source and figure it out for yourself.
login_html = lxml.html.fromstring(login_page.text)
ticket_node = login_html.xpath('//input[@name="ticket"]')[0]
ticket = ticket_node.attrib['value']

# Just like before, add your username and password.
login = {'username': '', 'password': ''}

# Additionally, we add our ticket:
login['ticket'] = ticket

# Now we POST the username, password, and ticket to the login page.  Note we're
# using the session still.
result = session.post('https://brennan.io/login', data=login)

# We're logged in through the session object now.
page = session.get('https://brennan.io')
```

OK, so there's a little more code this time, but if you've been following along
so far, the code should vaguely make sense.  All we did was (1) grab a ticket to
log in, and (2) send it with our username and password.  And we used the
`Session` instead of manually copying cookies into requests.

Thankfully, unless the website uses crazy Captchas or two-step verification,
this is probably the most complicated you'll see a "username and password" login
page get.  With this sort of strategy, you can log into most websites and scrape
as a logged in user.

For those who aren't interested in my school's login system, this article pretty
much ends here.  For those interested, read on!

## Single Sign On

Of course, not all websites directly ask you for a username and password.
Sometimes, they delegate authentication to somebody else.  The best example I
have of this is at my school, CWRU.  Everyone here has a single "account" that
they can log into all school-related websites with.  The thing is, your school
account is too valuable to let every single school website handle your username
and password.  So the way the system is designed, there is only one login page.
In the case of my school, it's `https://login.case.edu/cas/login`.  When a site
wants you to log in with your school account, it does the following:

1. It redirects you to `https://login.case.edu/cas/login`.  It adds on a
   parameter named `service` that indicates where the login server should send
   you when you're all done.
2. You enter your username and password and submit.  Your browser posts this to
   the login server (along with a session cookie and a login ticket, like we
   discussed above).
3. If the username and password are correct, the login server redirects you back
   to the `service` specified in step 1.  It adds on the "service ticket" to the
   URL.
4. The original site gets your service ticket from the URL, and verifies it with
   `login.case.edu`.  If the ticket is valid, the site will set its session
   cookie, marking you logged in!

This system has a name: Central Authentication Service, or CAS.  At first
glance, it sounds like all hope is lost for using Python to log into sites that
use CAS.  But, that's not true!  Earlier today I was trying to do exactly that,
and the code isn't too much different from the last example.  The main
differences are:

- The login page is `login.case.edu`.
- The login page has a couple more hidden parameters that need to be copied into
  the login form.
- You have to include the URL you'd like to log into in the `service` parameter.
- You have to follow the redirects of the login server in order to get the
  site's session cookie.  Thankfully, requests follows redirects automatically!
  
So, without further ado, here's a function that will return a requests `Session`
where you are logged into a website via CWRU's CAS!

```python
def cas_login(self, final_url, username, password):
    # GET parameters - URL we'd like to log into.
    params = {'service': final_url}

    # This will contain data we POST to the login page.
    form = {'username': username, 'password': password}

    # Start session
    session = requests.Session()

    # Get login form.
    login_form = session.get(_CAS_LOGIN_URL, params=params)

    # Harvest necessary login ticket and other hidden fields.
    tree = html.fromstring(login_form.text)
    login_ticket_element = tree.xpath('//form//input[@name="lt"]')[0]
    form['lt'] = login_ticket_element.attrib['value']
    execution_element = tree.xpath('//form//input[@name="execution"]')[0]
    form['execution'] = execution_element.attrib['value']
    form['_eventId'] = 'submit'

    # Finally, login and return the session.
    session.post(_CAS_LOGIN_URL, data=form, params=params)
    return session
```

The exciting thing is that, since Requests follows redirects by default, the
final `session.post()` call makes it all the way to the final url, which will
set your session cookie.  So the returned `Session` object will have all the
necessary cookies to access the site at `final_url` as a logged in user.

[requests]: http://docs.python-requests.org/en/master/
[lxml]: http://lxml.de/
[tswift]: https://github.com/brenns10/tswift
