---
title: What's an Internet?
layout: post
---

Some days it shocks me how much people rely on things they don't understand.
Billions of people use the Internet.  They use it to communicate, socialize,
learn, explore, and entertain themselves.  Business communication relies on it.
A huge portion of the economy relies on it.  The Internet is a major part of the
lives of untold millions of people, and so it can really come as surprise to me
when I realize nearly none of them know how it works.

Of course, those are the days when I *know* I'm being a snob.  After all, the
whole world is complicated these days.  I don't understand a whole lot more than
I do understand about the world.  The only reason I know anything about the
Internet is because I'm a programmer, and I've even taken classes about the
Internet.  So it's a bit unreasonable to think that people should know anything
about how the Internet, even if they use it every day.

But just because I don't understand everything in the world doesn't mean I don't
want to try to learn.  The world would be a sad place if there was nobody to
explain the complex things to those who don't have the technical background in
the field.  I think that there are plenty of people that would be fascinated
with an explanation of how the Internet works, but aren't particularly computer
oriented.  So this post is for all of those people.  My aim with this article is
to summarize the main points of a college networking course in an interesting
and understandable way.  I hope I have some success in doing so!

## Networks

Computer scientists talk about networks a lot.  Not all of them are "internet"
type networks (that is, networks of computers).  A network is really just a
nicer name for something computer scientists call a
[graph](https://en.wikipedia.org/wiki/Graph_(mathematics)).  And that's just a
collection of "things" and connections between the "things".  One type of
network you're probably familiar with is a "social network".  In that case, the
"things" are people, and the connections are friendships.  Another one you're
probably familiar with is a road map.  With roads, the "things" are
intersections, and the connections are roads.

Well, the Internet is just another one of those networks.  The "things" are
computers, and the connections are, well, connections.  Anything that allows the
two computers to communicate.  Cables and radio waves are common connections in
the Internet.

In a social network, information can spread from person to person through
friendships.  Rumors, jokes, and stories are common.  On the road network, mail,
packages, and people can be delivered through the roads.  The interesting thing
about networks is that you can usually get information from one part of the
network to another, without them even being directly connected.  For instance,
there's probably not a road running directly from your house to the grocery
store, but you still can get there on the roads.  And when you start a rumor
about someone who isn't your friend, that rumor *always* manages to reach them.

The Internet works precisely because of those same qualities of other networks.
You can't physically connect every computer to every other computer, any more
than you could be friends with everyone, or have a road between every pair of
destinations.  But with a well created network of roads, everyone can still get
where they need to go.

Here's another interesting thing about networks: no matter what network you look
at, you'll almost always find that there is some sort of structure to it.  The
road network has neighborhoods, with roads connecting them.  Then there are
cities that contain all of those neighborhoods, and highways connect the cities.
Social networks are a bit less organized, but there are still friend groups.
Some people are social butterflies, and they connect all the groups together.
The Internet is also like this.  We typically think about the Internet not as
"one big network", but rather as "a network of networks".  I'll explain more
about this a little later.

The social and road network analogies are getting old, but I'd like to make one
final observation, and then we'll move on from them for a while.  When you think
about these example networks, you'll notice that they have some rules.  Social
networks have social rules.  For instance, you don't talk while somebody else is
talking, that's just rude.  On the road, you have a whole set of motor vehicle
laws telling you how to behave.  There are all sorts of kinds of rules.  Some
tell you when you can use the roads, like stop signs, traffic lights, etc.  Some
regulate the extent to which you use them, like speed limits.

The Internet is the same way.  There are tons of very detailed rules about how
computers talk to each other.  They're called *protocols*.  I will also talk
more about these later on.

## Structure

So far, we've seen how the Internet isn't all that different from other networks
that we deal with every day.  It's a bunch of "things" connected together in an
organized manner.  Information can flow through the network, and there are rules
("protocols") about how the information goes from place to place.

But that doesn't explain why the Internet is capable of providing us with
unlimited pictures of cats, while social networks and roads obviously fail at
that task.  So let's start talking about what makes the Internet different from
other networks.  We'll start with the structure of the Internet, and then talk
about the nitty gritty of how the pieces work together.

Like I mentioned before, we usually think of the Internet as "a network of
networks".  So, there are a bunch of smaller networks hooked together to form
the Internet.  Your home and work networks are probably one of them.  At home,
you probably have a router (wireless or wired) that all of your Internet
connected devices use to access the Internet.  Well, that means you have a "home
network".  At work, your IT people probably have created a work network that
provides everyone with Internet as well.  Both home and work networks are good
examples of "border" or "edge" networks
