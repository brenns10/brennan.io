---
layout: post
title: Hello, HTTPS!
description: Moving your site to SSL is hard.
---

An exciting announcement! Starting a few days ago, when you visit my website,
you should see a green padlock next to the URL bar.

![ssl-browser]

That's right, [brennan.io] is now SSL enabled! How did I do it? With just a
little help from magic and AWS! Well, mostly AWS, but the process was *almost*
magical. As a person who writes a tech blog, I'm pretty much obligated to write
a post about any change to my website. So, buckle up, cause this one's pretty
in-depth.

## History of my website

Long, long ago (my sophomore year of college) I owned the domain
`stephenbrennan.net` and an HP laptop. The laptop sat on a shoe rack in my dorm
room, running a Wordpress website that contained, well, pretty much nothing. By
the next summer, I realized that hosting a website on an old laptop on a shoe
rack was a bad idea, and I decided to switch to [GitHub Pages][ghp].

For those unfamiliar, GitHub Pages allows you to host simple websites generated
from GitHub repositories. It uses a program called [Jekyll], which generates a
full HTML site from some templates and your blog posts (as markdown). My site is
generated from my [`brenns10.github.io`][bgi] repository. Every time I push new
commits, GitHub Pages generates a new copy of my site and hosts it at
`brenns10.github.io`.

Of course, I didn't want a GitHub domain name, so I took advantage of the
"custom domain" feature to host my website at `stephen-brennan.com`, my "new"
domain at the time. Not too long ago, I changed that to `brennan.io`.

## Problems with GitHub Pages

GitHub Pages is a free service, and as far as free services go, it's downright
amazing. But you can't get always get what you want out of a free service.

One thing GitHub Pages can't do for you is provide SSL for custom domains. There
are some really great reasons why this is the case:

- For one, if GitHub were to get an SSL certificate signed for your domain, they
  would have to "prove" they own it. That would be rather difficult.
- What's worse, they might have to do some heavy infrastructure work on their
  web servers to support [Server Name Indication (SNI)][sni]. The reason for
  this is that they use the same web servers to host tons of different GitHub
  Pages sites. SSL is negotiated before any HTTP information is sent, and so
  their web servers wouldn't know ahead of time which SSL certificate (for which
  domain) they should use. Although SNI solves this problem (by allowing the
  client to declare what domain they think they're connecting to as SSL is
  negotiated), implementing it in a secure, distributed delivery network like
  GitHub Pages wouldn't be trivial.

Of course, my site is completely static, so it doesn't *need* SSL. Nobody's
sensitive information (except mine) is being exchanged. But I got pretty jealous
of everybody else's green padlocks on their sites. On a more practical note, I
also believe that universal SSL is an important goal for the Internet, and so I
wanted to do my part.

So, I decided to fix these problems by moving to a slightly less free, but
infinitely more powerful service: AWS!

## What can AWS do for you?

For somebody looking to host a static site on AWS, these are some important
services to be aware of:

- *Simple Storage Service (aka S3)* - As the name implies, this service stores
  files. These files can be made accessible over HTTP on an Amazon domain. If
  you set a CNAME pointing your domain to the Amazon domain, you can have a
  nifty HTTP-only site set up very quickly.
- *CloudFront* - A [Content Delivery Network (CDN)][cdn]. Basically, there are
  CloudFront servers all over the world. If you set it up properly, whenever a
  request for your website comes in, it goes to a CloudFront server
  geographically close to the client. The CloudFront servers will even cache
  your site's files to speed up site load speeds! CloudFront can serve content
  from S3, and it can also serve content over HTTPS with any custom domain.
- *AWS Certificate Manager* - The reason CloudFront can do HTTPS over custom
  domains is because AWS has put together a certificate management
  infrastructure. Amazon is a certificate authority, so if you can prove you own
  a domain, they'll sign a certificate for it and securely distribute it to
  CloudFront servers, which support [SNI][sni].
- *Route 53* - Amazon's DNS service, which has the nice feature that it can bind
  your domain directly to a CloudFront "distribution", instead of using a CNAME.
  This is important because I host this site on `brennan.io` instead of
  `www.brennan.io`, and using CNAME records on your raw (aka apex) domain is
  [not kosher][apex].

## Barriers to entry

It seems that AWS can do pretty much everything you might want in a static site
host. But you still lose the convenience of being able to push to GitHub and
have your site deployed in seconds. Instead it seems like you would be stuck
running Jekyll manually and then uploading it to S3 via the AWS console. Plus,
it would seem like there's a lot of confusing setup you'd have to do with AWS.

Thankfully, this has a very nice solution, discussed in this excellent
[post][publish-post]. I won't rehash all of the instructions given in the
article[^fn-ca], but the gist of it is that a nice gem called `s3_website` can
help sync your built Jekyll site and even configure AWS properly.

[^fn-ca]:
    Except to note that AWS will now sign certificates for you, free of charge,
    so you don't need to mess with the external CA's mentioned in the article.

A more tricky issue for me is all of my GitHub Pages project sites! I've taken
great advantage of these sites. Many of my programming projects have tool sites
which are automatically pushed by Travis-CI. They contain documentation and code
coverage for the `master` branch. It would be very sad to lose these sites. Even
more concerning is that the entire "Talks" section of my site (see the menu
above) is actually a separate Jekyll site on its own GitHub repository!

Since this was pretty much the only piece of the puzzle missing, I went ahead
and wrote my own little [tool][sitebuilder] that can take all of your GitHub
pages sites and automatically build them together into a single site, like
GitHub does. Combine this with the `s3_website` gem, and you're pretty much
there!

## Putting it all together

So I just described a ton of infrastructure I used to switch to HTTPS. But how
exactly was I able to do it without any downtime on the site?

By performing the migration over about the course of a week, and carefully
choosing the correct sequence of steps!

1. The first step of the process was a proof of concept. I created an S3 bucket
   and CloudFront distribution according to that [article's][publish-post]
   instructions. But instead of pointing my main domain at it, I created a
   subdomain [`staging.brennan.io`][stage] and used that instead. This way, I
   was able to verify that the setup would work for me.
2. The next step was migrating my DNS from Namecheap to Route 53, so that I
   could use the special ALIAS records to bind `brennan.io` directly to
   CloudFront. This step took about two days, since the TTL on my NS records was
   set to a whole day.
3. In the downtime, I got my [sitebuilder] tool written and set up, so that it
   could push all my site content to S3, not just `brenns10.github.io`.
4. I also had to do some [work][disqus-fix] migrating my Disqus comments to
   account for the new HTTPS URLs.
5. Once the DNS changes synced, I used `s3_website` to create the S3 bucket and
   CloudFront distribution for my main site. I updated my DNS to point at
   CloudFront, and *voila*! `brennan.io` began to redirect to HTTPS!

Now whenever I write a post or update my site, I push to GitHub as normal. But
afterwards, I have one more step:

```bash
$ cd ~/repos/sitebuilder
$ python sitebuilder.py
$ s3_website push
```

And my site is successfully deployed!

## Unanswered Questions

The only thing that remains to seen is how expensive this site will be. Due to
Amazon's free tiers, the hosting is nearly free, although the DNS hosting costs
about $0.51 per month. It will be interesting to see what this costs after a
month or two of use, not to mention the possibility of a Reddit or Hacker News
hug.

#### Footnotes

[ssl-browser]: /images/ssl-browser.png
[brennan.io]: https://brennan.io
[ghp]: https://pages.github.com/
[bgi]: https://github.com/brenns10/brenns10.github.io
[Jekyll]: https://jekyllrb.com/
[sni]: https://en.wikipedia.org/wiki/Server_Name_Indication
[cdn]: https://en.wikipedia.org/wiki/Content_delivery_network
[apex]: http://serverfault.com/questions/613829/why-cant-a-cname-record-be-used-at-the-apex-aka-root-of-a-domain
[publish-post]: https://davidcel.is/posts/publish-your-site-to-s3/
[sitebuilder]: https://github.com/brenns10/sitebuilder
[stage]: https://staging.brennan.io
[disqus-fix]: https://github.com/brenns10/brenns10.github.io/commit/37bfaefa1849f99a834a44349f1098ca2836781a
