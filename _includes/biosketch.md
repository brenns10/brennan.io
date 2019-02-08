I'm a software engineer who also likes to cook, bake, and mix cocktails.
This is my infrequently-updated site, which contains some documentation of
things I've done, my resume, and some blog posts I've written.

Below are some of my most popular blog posts, which you may be interested in
reading:

{% for post in site.posts %}{% if post.featured %}
- [{{ post.title }}]({{ post.url }}) <small>{{ post.date | date_to_long_string }}</small>{% endif %} {% endfor %}
