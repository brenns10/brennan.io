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
examples of "border", "edge", or "access" networks.  These are parts of the
Internet that exist mainly so that end users can communicate with other people
located on other "sides" of the Internet.

Your home and work networks are more than likely wired into an Internet Service
Provider (ISP).  ISPs are just companies that have large networks which are a
large part of what the Internet is.  You pay them to connect you to their
network, providing you with access to the whole Internet.  Some well known ones
are AT&T, Comcast, Verizon, and Time Warner Cable.  Your ISP probably has a
small local network that hooks up all of its customers in and around your
neighborhood.  Then, it probably has a larger regional network connecting the
small local networks.  It may even have larger networks connecting each region.
These different size networks are similar to the different types of roads -
residential roads, main roads, and highways.  But, each ISP has its own
organization of its own networks.  They are free to manage their networks
however they like, which is why the ISP networks are sometimes referred to as
"Autonomous Systems", or AS's.

Now, ISPs know that you don't want to communicate solely with their customers.
So, even though they're competitors, ISPs have to negotiate agreements among
each other to connect their networks.  These connections are called "peering
links".  I'm not exactly sure how they're negotiated, or who pays whom in these
agreements.  However, the end result is a huge system of interconnected
networks.  If you pay an ISP to connect you, you can use the Internet to
communicate with any other computer.

## The Nitty Gritty

Essentially, what I have explained so far is the physical layout of the
Internet - what a network is, and how the Internet in particular is laid out.
But, that doesn't explain how the computers that make up the Internet are
capable of communicating with each other.  How is it that my computer can simply
*ask* for a page from Google, and hundreds of miles away, Google's computers
somehow hear my request and send me the page I asked for?  It's not like my
computer is directly connected to Google.  How does the Internet know where to
send my message so that it eventually gets to Google?  Well, that is the field
of computer networking.

Creating a computer network on the scale of the Internet is massively complex,
so we typically treat the Internet as an ogre.  Or an onion.  Or maybe a
parfait.  The point is, it has layers.  These layers serve as "levels of
abstraction".  Abstraction is a big word that gets thrown around a lot in the
computer world.  It's pretty darn important.  It simply means, "getting rid of
the little details to focus on the big picture."  You probably do it all the
time.  When you tell somebody how to get to your house, you don't instruct them
to stop at each stop light, or what gear to use as they drive.  You probably
don't give them exact distance measurements, or tell them how fast they should
go.  These are all things they'll eventually need to figure out.  But if you
covered all those details, you probably wouldn't get halfway through the
directions.  Instead, you focus on the big picture: what are the major road
names?  Which landmarks tell you when to turn?  What does your house look like?
You just trust that the other person has the actual driving part covered.

In the same way, the only way you can create a massive network where anyone can
send a message to anyone else is through abstraction.  You start by solving the
little problems.  Then, you forget about them, and work on the bigger problems.
At each level, you forget about the details of the previous solutions, and solve
bigger and more important problems.  When you get to the top layer, you're able
to do some fantastic things.  The Internet is made with five layers:

* Physical Layer (the most detailed)
* Link Layer
* Network Layer
* Transport Layer
* Application Layer (the most powerful)

So, without further ado, let's get exploring these layers.

### The Physical Layer

The Physical layer is the lowest layer.  It is the physical "thing" you use to
hook up network devices.  For instance, if you use WiFi, then your physical
layer is radio waves, in a specific frequency range.  If you use fiber optic
cables, your physical layer is light.  The physical layer is so low level, that
sometimes it's more like talking about physics, or electrical engineering.  For
instance, you could use a single copper wire as your physical layer.  But then,
the question would be, how to transmit information across it?  There are many
different ways that electricity could be used to send information.  For
instance, if you wanted to send a number, you could simply put that amount of
volts on a circuit.  But what if the number you wanted to send was large?  Say,
a million?  It might be dangerous to put that many volts across a small copper
wire.  Plus, depending on the length of a wire, there is resistance within it.
The device on the other side may only read 4.5 volts when you actually sent 5.
Obviously, encoding numbers directly as voltages is not how we send data across
circuits.

Instead, we represent numbers (which can represent any data) using "binary".
This is a number system that uses ones and zeros as its digits (usually called
"bits" for "binary digits").  All numbers can be represented in binary.  We
assign one to some voltage (typically 5V), and zero to something else (typically
0V).  To send a number, you send a series of voltages in order.  If your 5V
deteriorates down to 4.5V on the other end, it's OK, because that's still close
to 5.  No information was lost.  This is usually called "digital", because you
are encoding information as a series of digits.  Directly sending a number as a
voltage would be an example of "analog".

One thing you need to do when you have digital signals is decide on a "clock
rate".  Basically, you need to know how long each digit lasts.  Otherwise, how
could you tell the difference between 11111, and just 1?  Making sure that both
devices have their clock rates the same, and synchronized, is a difficult task.
Plus, you might have to agree upon a way that both sides of the connection could
send and receive without talking over each other.  This problem is called the
"multiple access problem", and it's an extremely common problem in networking.

I'm not going to go into the solutions to these problems.  Each physical layer
has its own unique set of problems to address: radio waves are different from
copper wires, or fiber optic cables.  There could be books written on the
solutions to these problems for all the different types of physical layers you
could have.  Suffice to say that, while it's the lowest level of the network,
the physical layer is definitely not the easiest one.  The fact is, none of the
layers have easy problems to solve.

### The Link Layer

So, all of that electricity and binary, and what do we have to show for it?
Well, we know that we have a way to send bits across a connection.  And that's
pretty much it.  Now, we apply our "abstraction", and forget about all the
problems of the physical layer.  Are we using radio waves, or a wire?  Who
cares!  We know that we can send a bit out onto our physical layer, and that
*maybe* someone on the other end will receive it.  We can't be certain that
they'll get it.  After all, the physical layer never guaranteed us that it would
send the bits correctly.  It'll obviously be designed to do its best at it, but
there are no guarantees.

So what does our link layer do?  Its job is deceptively simple: get a message to
somebody else that is on the same link as us.  All of last section, I talked
about the physical layer as connecting two devices, but the fact is, there may
be more.  After all, many people use a single WiFi hotspot.  And, believe it or
not, you can have more than two computers connected with each other on a single
Ethernet connection.  All we figured out last section was how to send bits.  So,
the link layer has to be able to make those bits into a message directed to a
single device on the link.

So, how do we send a message to a specific device?  The simplest way is by
putting the recipient's name on the envelope!  After all, you don't just stick a
letter in the mail without a salutation or address, and just hope that the
intended recipient gets it.  You put the address on an envelope and you put the
letter in there.  That way, whoever sees it at the post office knows whom to
send the letter to.  Similarly, the link layer takes whatever data you want to
send, puts it into an envelope (called a "frame"), and puts the device's address
on the envelope (along with other information, like how long the message is).
So, what is a device's address?  It could vary among link-layers, but for the
most common ones, it's always a MAC address (which stands for Media Access
Control).  This is just a long number.  There are agreements among everyone that
makes devices like these, ensuring that MAC addresses are always unique.

So, in the simplest link layer, when a device wants to send a message to another
device it shares a link with, it simply wraps the message up in a frame, slaps
the correct MAC address on it, and gives the frame to the physical layer to put
those bits onto the wire.  The other devices would receive that, and if the MAC
address on the frame matched their own, they would open it up and read it.  But,
things aren't usually that simple.  If you have multiple devices on the same
link, there's no guarantee that someone else won't start sending a message at
the same time you do.  This is the multiple access problem again.  There are a
number of ways of dealing with this.  One way is by splitting the available
connection.  For instance, if there are 5 devices on a WiFi network, each device
could get 1/5 of the time to send messages.  But, that just means that you could
only use 1/5 of the available connection speed, and that's nowhere near enough
for Netflix!  We can do better!  Usually, the strategies for solving multiple
access involve a few things:

* If you hear somebody else sending a message, don't start sending your own!
  This is called collision avoidance.
* If you are sending a message, and you hear somebody else starting to send a
  message, stop sending!  Your message is probably corrupted already, so you'll
  need to start over anyway.  (Although this is an obvious strategy, it's not
  always possible.  For instance, WiFi devices are usually not capable of
  sending and receiving at the same time.  Once you start sending a message, you
  have no idea if someone else started sending one too.)  This is called
  collision detection.
* When you do stop due to a collision, wait a random amount of time!  That way,
  there's a decent chance that you and the person you collided with will go at
  different times.  This can be done in a lot of ways, and is typically referred
  to as random backoff.
* Finally, some link layers use acknowledgements, just little messages that say
  "hey, I got your message, it's all good".  WiFi has lots of interference, so
  it uses these.  It also retransmits if there was an error in the message.
  Ethernet, on the other hand, does not (since errors are uncommon in Ethernet).

Note that this isn't a description of any particular multiple access protocol.
Each link layer typically combines these elements as well as other ones in a way
that can ensure that messages get across the link quickly.  In the end though,
all of these strategies can be compared to how you would engage in conversation
in a large group of people (say, at a dinner party).  If you reread the list
above, you can easily see the similarities.  This is pretty much all I want to
say on the topic of multiple access.  It's a tricky problem to solve right.

OK, so with MAC addresses, and a properly designed multiple access protocol, the
link layer is mostly complete.  However, there are a few other issues to solve!
First is error detection.  Like I said earlier, we have no guarantees that the
physical layer will perfectly send all our bits.  For all we know, it could get
them wrong.  So, most link-layer protocols implement a "checksum", which is just
a number computed from the data in the frame.  They add this checksum to the
frame, and send it with.  The receiver will compute the checksum itself, and
compare it to the checksum included with the data.  If they don't match, the
receiver will typically drop the frame.  Some link-layers will actually tell the
sender that they didn't receive the message correctly, and retransmit the
message.  But not all.  The link layer, in general, doesn't guarantee that it
will reliably get a message across to the other person.  But, if it does, it
will get it there pretty much intact, due to checksums.

The last thing that may be weighing on your mind right now is, how do you know
what MAC address you want to send messages to?  Unfortunately, the other layers
don't know or care about MAC addresses.  They do have their own address schemes
though.  Most importantly, the network layer above has IP addresses.  There is a
protocol called ARP (Address Resolution Protocol) that basically broadcasts the
question, "who has the address xx.xx.xx.xx?", and waits for a response.  ARP is
a strange beast that straddles the link and network layers, but it's necessary
in order to know the MAC address you want to send to.
