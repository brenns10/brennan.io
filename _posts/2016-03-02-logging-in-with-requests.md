---
title: Logging in With Requests
layout: post
description: >
  Web scraping in Python is a fun and useful skill.  In this article, I
  demonstrate basic web scraping using requests and lxml, and then explain how
  you can scrape sites that require you to log in.
---

One of my favorite types of quick side projects are ones that involve web
scraping with Python.  Obviously, the Internet houses a ton of useful data, and
you may want to fetch lots of that data to use within your own programs.  Python
has a few excellent tools which can be combined to create a powerful, easy to
use system for quickly harvesting this data from webpages.  I've used Python's
web scraping tools for fun projects like [downloading music lyrics][tswift], and
then using that to make a [Twitter][pyswizzle-tw] [bot][pyswizzle-gh] that
replies to you with Taylor Swift lyrics.  But these tools could also be useful
for serious projects, like aggregating course enrollment or evaluation data from
your college.  So how would you go about simple web scraping in Python?  Let's
dive in!

Web scraping involves writing code that uses HTTP or HTTPS (like a web browser)
to request pages from websites.  The Python library [requests][] is great for
that, and as a bonus, it is widely recognized as having one of the best APIs out
there!  Requests will make an HTTP(S) request and get you the page you asked
for.  Once you have the page, instead of displaying it to a user like a browser
would, you want to search through it for information.  This isn't a completely
automatic process.  Typically, you need to go to the website you want to scrape,
and look at the HTML source to figure out where your information is in the page.

Since webpage content is primarily written in HTML, getting your program to find
the data you want could be difficult.  Thankfully, the Python library [lxml][]
makes things a lot easier.  Not only will it parse HTML, but it includes a
powerful search tool called XPath, which allows you to craft a "query" that can
match particular HTML tags in a webpage.  You could think of it like regular
expressions, but for HTML (because regular expressions [won't work][re-html] on
HTML... but that's a discussion for another, lengthy blog post).

With these tools, the fundamental tasks of web scraping are very easy.  For
example, this code will get you the biosketch on the front page of my website
(as of this writing):

```python
>>> import requests, lxml.html
>>> page = requests.get('http://brennan.io')
>>> html = lxml.html.fromstring(page.text)
>>> content_divs = html.xpath('//main/div[@class="content"]')
>>> print(content_divs[0].text_content().strip())
And here you see my biosketch ...
```

The search query (`//main/div[@class="content"]`) is a bit complex, but if you
research [HTML][] and [XPath][] a little bit, and then look at my website's
source, it'll all make sense.  All it's asking is to find a `<div
class="content">` tag within a `<main>` tag.  If you were to look at the HTML of
my website's home page, you could find exactly that.  And inside of it -- my
biosketch.  If you don't believe me, try it!  Click "Home" at the top left of
this page, and then right click anywhere, and select "View page source".  Scroll
down to about line 109 (again, _at the time of this writing_) and you'll see
just what I'm talking about.

## Scraping Sites with Logins

Unfortunately, not every website is this easy to scrape.  There are many reasons
that a website may not be easy to scrape, but one common one is that it requires
you to log in.  For instance, colleges provide school directories and course
evaluation data to students, faculty and staff.  But they'd rather not provide
that to the rest of the world.  So, they make you log in to view the data.

Logging into a website is a process that can vary wildly between sites.  But,
here's an overview some of the common things that happen:

1. Your browser sends a HTTP GET request to login page.  The website responds
   with the page, and the page includes a form for you to enter your username
   and password.
2. You enter your username and password into the form and hit enter.
3. Your browser sends that info (this time using a HTTP POST request) back to
   the login page.
4. If the the username and password are correct, the server will "log you in"
   (more on that process later).

There are two very common parts of this process that you should understand:

- *Session Cookies:* A cookie (on the web) is a little piece of text that a web
  site asks your browser to save.  On each subsequent request, your browser
  sends it back to the web site.  Cookies can be used to store a unique
  identifier, so that the website knows which requests were made by you.  In
  this way, cookies can track your browsing session, and those that do are
  called "session cookies".  Normally, websites set a session cookie for you the
  moment you access their site for the first time.  When you submit your
  username and password correctly, the website makes a "mental note" that your
  session cookie is now logged in as you.  After that point, whenever you ask
  for a page, the website knows from your cookie that you're logged in, and
  starts behaving differently for you.
- *CSRF Tokens:* There is a whole class of security vulnerabilities in web
  applications called "Cross Site Request Forgeries", or CSRF for short.
  They're pretty basic vulnerabilities that allow malicious webpages to use your
  browser to make requests to a vulnerable site while you're logged in.  Now,
  since these vulnerabilities are rather common and well known, most websites
  use tools to make them impossible.  Usually, they include a random string
  hidden in every form (including the login form).  An attacker can't guess this
  string, but when you submit the form, it will get sent back to the website,
  which can then verify that it sent that token just a few minutes earlier.
  This random string is called a CSRF token, because it is a token that defeats
  CSRF attacks.

So, with these concepts in mind, we can begin to understand how we might
successfully log into a website in our own code.  We'd need to (a) make sure
that we keep track of all the cookies a website gives us, because one of them is
probably our session cookie.  And (b), we'd also need to request the form
beforehand so we can grab a CSRF token out of the form before we submit our
login credentials.

In order to accomplish goal (a), we can use a nifty feature of requests called a
`Session`.  If you create a session and do all of your HTTP requests using that
session, requests will save all your cookies and use them in subsequent
requests.  The only code change you'll notice is that we'll create a session
object like so: `s = requests.session()`.  Then, we use that for making HTTP
requests instead of the normal library.  That is, you'll see `s.get()` or
`s.post()` instead of `requests.get()` or `requests.post()`.  Tada!

In order to accomplish goal (b), we will have to do some manual inspection of
the login form we're using.  Since CSRF tokens are almost always 
`<input type="hidden">` tags within a form, we'll probably be able to write a
simple XPath to match any hidden tags in the login form, and then we'll be sure
to put them in our login message.

To put all this information together, let's try to log into a real-world site
using requests.  Since I'll be working there this summer, why not try Yelp?

```python
>>> import requests, lxml.html
>>> s = requests.session()

### Here, we're getting the login page and then grabbing hidden form
### fields.  We're probably also getting several session cookies too.
>>> login = s.get('https://www.yelp.com/login')
>>> login_html = lxml.html.fromstring(login.text)
>>> hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
>>> form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
>>> print(form)
{'csrftok': '9e34ca7e492a0dda743369433e78ccf10c1e68bbb1f453cbb80ce6eaeeebe928', 
 'context': ''}
 
### Now that we have the hidden form fields, let's add in our 
### username and password.
>>> form['email'] = # Enter an email here.  Not mine.
>>> form['password'] = # I'm definitely not telling you my password.
>>> response = s.post('https://www.yelp.com/login', data=form)

### How can we tell that we logged in?  Well, these worked for me:
>>> response.url
'https://www.yelp.com/cleveland'
>>> 'Stephen' in response.text
True
```

So, everything probably looks familiar right up until the line with XPath.  All
that the XPath does is search for any `<input type="hidden">` elements within a
`<form>`.  The next line turns them into a dictionary mapping names to values in
the form.  At the end of that little section of code, you can see that we have
captured two form elements that are hidden and set by the server already.
Great!

All that's left is to set the username and password, and then submit the login
form.  Once that's done, you can experiment a bit with the response Yelp gives
you to confirm that you are logged in.  For me, Yelp takes me directly to a
Cleveland page, and it has my name in the response as well.  From then on, since
the session `s` contains all the session cookies associated with your account,
you can use that to make requests as a logged in user.

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

This system has a name: [Central Authentication Service, or CAS][cas].  At first
glance, it sounds like all hope is lost for using Python to log into sites that
use CAS.  But, that's not true!  I've tried to do exactly that, and the code I
came up with isn't too much different from the last example.  The main
differences are:

- The login page is `login.case.edu`.
- The login page has a couple more hidden parameters that need to be copied into
  the login form.  Thankfully, our code from above does this all transparently
  for us.
- You have to include the URL you'd like to log into in the `service` GET
  parameter.
- You have to follow the redirects of the login server in order to get the
  site's session cookie.  Thankfully, requests follows redirects automatically!
  
So, without further ado, here's a function that will return a requests `Session`
where you are logged into a website via CWRU's CAS!

```python
import requests
import lxml.html

def cas_login(service, username, password):
    # GET parameters - URL we'd like to log into.
    params = {'service': service}
    LOGIN_URL = 'https://login.case.edu/cas/login'

    # Start session and get login form.
    session = requests.session()
    login = session.get(LOGIN_URL, params=params)

    # Get the hidden elements and put them in our form.
    login_html = lxml.html.fromstring(login.text)
    hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
    form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

    # "Fill out" the form.
    form['username'] = username
    form['password'] = password

    # Finally, login and return the session.
    session.post(LOGIN_URL, data=form, params=params)
    return session
```

The exciting thing is that, since Requests follows redirects by default, the
final `session.post()` call makes it all the way to the final url, which will
set your session cookie.  So the returned `Session` object will have all the
necessary cookies to access the site at `service` as a logged in user.  Say that
you wanted to log into the CWRU course evaluation site (say, to scrape some
evaluation reports).  All you'd have to do is call
`cas_login('https://webapps.case.edu/courseevals/', 'username', 'password)`.
Then, you could use the returned session to make all further requests.

## Conclusion

Hopefully this article will help people understand web scraping, and also how
logins work on the web.  If you decide to try this sort of thing on other sites,
keep in mind that none of this is exact - you may find that a strategy that
works on one site doesn't work on another.  This is usually because that site
may use an additional security technique to protect their login form.  If you
get comfortable with your browser's developer tools, you can inspect these login
forms carefully, and figure out how to modify your code to circumvent them.  In
general, just keep in mind that this process is almost always manual.
Hopefully, by reading this article, you should have the basic concepts under
your belt, so that you can dive right into logging into different sites.

[requests]: http://docs.python-requests.org/en/master/
[lxml]: http://lxml.de/
[tswift]: https://github.com/brenns10/tswift
[social]: https://github.com/brenns10/social
[HTML]: https://en.wikipedia.org/wiki/HTML
[XPath]: http://www.w3schools.com/xsl/xpath_intro.asp
[re-html]: http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags
[pyswizzle-tw]: https://twitter.com/pyswizzle
[pyswizzle-gh]: https://github.com/brenns10/pyswizzle
[CAS]: http://hacsoc.org/wiki/technical/cas.html
