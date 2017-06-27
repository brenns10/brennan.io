I'm a programmer, teacher, reader, writer, chef, and plenty of other
things when the mood strikes.

There's a lot more to know about me, but I doubt my website would do a good job
explaining it.

If you want, you can check out [what I'm doing now](/now/) and my
[links](/links/).  You can also check out some of my most popular blog posts:

{% for post in site.posts %}{% if post.featured %}
- [{{ post.title }}]({{ post.url }}) <small>{{ post.date | date_to_long_string }}</small>{% endif %} {% endfor %}
