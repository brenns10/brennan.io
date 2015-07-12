---
title: What's an Internet?
layout: post
todo:
  - Also, at the end of the link layer, I start to get really rushed.  I'll
    definitely want to go over than and smooth out my writing.
  - The explanation of TCP could use an analogy - perhaps page numbering.
  - Similarly, DNS is pretty much like a phone book or address book.

---

Some days it shocks me how much people rely on things they don't understand.
Billions of people use the Internet.  They use it to communicate, socialize,
learn, explore, and entertain themselves.  Business communication relies on it.
A huge portion of the economy relies on it.  The Internet is a major part of the
lives of untold millions of people, and so it can really come as surprise to me
when I realize most of them have no clue how it all works!

Of course, those are the days when I *know* I'm being a tech snob.  After all,
the whole world is complicated these days.  There are a whole lot more things
that I don't understand than things I do understand about the world.  The only
reason I know anything about the Internet is because I'm a programmer, and I've
even taken classes about the Internet.  So it's a bit unreasonable to think that
people should know anything about how the Internet, even if they use it every
day.

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
nicer name for something computer scientists call a [graph][].  And that's just
a collection of "things" and connections between the "things".  One type of
network you're probably familiar with is a "social network".  (When I say
"social network", I don't mean Facebook or Twitter, just the underlying people
and their friendships).  In the case of a social network, the "things" are
people, and the connections are friendships.  Another network you're probably
familiar with is a road map.  With roads, the "things" are intersections, and
the connections are roads.

Well, the Internet is just another one of those networks.  The "things" are
computers, and the connections are, well, connections.  They can be anything
that allows the two computers to communicate.  Cables and radio waves are common
connections in the Internet.

In a social network, information can spread from person to person through
friendships.  Rumors, jokes, and stories are common examples of this.  On the
road network, mail, packages, and people can be delivered through the roads.
The interesting thing about networks is that you can usually get information
from one point of the network to another, without them even being directly
connected.  For instance, there's probably not a road running directly from your
house to the grocery store, but you still can get there on the roads.  And when
you start a rumor about someone who isn't your friend, that rumor *always*
manages to reach them.

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
The Internet also has structure.  We typically don't think about the Internet as
"one big network", but rather as "a network of networks".  I'll explain more
about this a little later.

The social and road network analogies are getting old, but I'd like to make one
final observation, and then we'll move on from them for a while.  When you think
about these example networks, you'll notice that they all have rules.  Social
networks have social rules.  For instance, you don't talk while somebody else is
talking... that's just rude!  On the road, you have a whole set of motor vehicle
laws telling you how to behave.  The Internet is the same way.  There are tons
of very detailed rules about how computers talk to each other.  They're called
*protocols*.  I will also talk more about these later on.

## Terms

While computer terms like "graph", "network", and "protocol" can be intimidating
to you, the reality (which you may be realizing) is that they're just dressed-up
words for concepts we see every day.  If you have ever had friends, driven a
car, made a phone call, or sent a letter, you are equipped with the knowledge
and experience to understand the basics of the Internet, since these are all
very good analogies for how the different parts of the Internet work.
Unfortunately, like any technical field, computer scientists have filled up the
the computer world with jargon.  Jargon is important for us to quickly and
accurately convey our meaning to other specialists.  But jargon also intimidates
and alienates non-specialists.  So I'm going to pause to explain some pieces of
"jargon" that I'll be using throughout this article.

*   **Protocols:** These are sets of rules describing how computers should
    "talk" with each other.  As I wrote in an
    [older article about the Lenovo/Superfish vulnerability][superfish]:

    > In order for the internet to work, computers need to know how to talk to
    > each other.  Protocols are like sets of instructions for how computers
    > behave when they interact with each other.  For instance, humans know that
    > when they walk into a restaurant, they wait to be seated, read their
    > menus, order food, wait, eat, pay, and tip their waiter or waitress.  This
    > is a protocol for eating out.

    There are protocols *everywhere* in the Internet, and they are just like the
    traffic rules of the road.  They enable everything to function smoothly
    safely -- without them, everything would "crash and burn".  Just like
    traffic laws, protocols aren't really "things", just rules that were agreed
    upon and written down by experts (we hope).  What makes them powerful is
    that (for the most part) people and computers follow them.

*   **Routers:** A router is "just" a computer.  But unlike your computer, a
    router's purpose in life is to help shove other people's information around
    the Internet.  They go through life receiving bits of data, looking at them,
    and sending them in the correct direction.

    In the "road map" analogy, a router is like a traffic light or a stop sign.
    The traffic light organizes the cars going through the intersection,
    ensuring that nobody crashes, and everyone can go in the direction they
    need.  Routers do the same thing, except that the cars are Internet
    communications, and the roads are connections to other routers.

    On a road map, the opposites of traffic lights are the destinations.  You
    don't go on the road to visit a traffic light, but you might drive to the
    grocery store, or your friend's house.  These are the "points of interest"
    on the roads.  Similarly, everything that's not a router on the Internet is
    probably some sort of "computer of interest" - either a PC that's using the
    Internet to get content, or a "server" that provides content (like a
    website).

With these bits of jargon under our belts, we can start our explanation of the
Internet, beginning with its structure!  After that, we'll move on to the "Nitty
Gritty", an overview of each part of the Internet and how they all work
together.

## Structure

As you hopefully recall, we've seen how the Internet isn't all that different
from other networks that we deal with every day.  It's a bunch of "things"
connected together in an organized manner.  Information can flow through the
network, and there are rules (protocols) about how the information goes from
place to place.

Like I mentioned before, we usually think of the Internet as "a network of
networks".  So, there are a bunch of smaller networks hooked together to form
the Internet.  Your home and work networks are probably among them.  At home,
you probably have a router (wireless or wired) that all of your Internet
connected devices use to access the Internet.  Well, that means you have a "home
network".  At work, your IT people probably have created a work network that
provides everyone with Internet access as well.  Both home and work networks are
good examples of "border", "edge", or "access" networks.  These are parts of the
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
computer world, and it's pretty darn important.  It simply means, "getting rid of
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
I'm not going to go into the solutions to this problem.  Each type of physical
layer has its own unique set of problems like this to address: radio waves are
different from copper wires, or fiber optic cables.  There could be books
written on the solutions to these problems for all the different types of
physical layers you could have.  Suffice to say that, while it's the lowest
level of the network, the physical layer is definitely not the easiest one.  The
fact is, none of the layers have easy problems to solve.

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
somebody else that is on the same "link" (that is, connection) as us.  All of
last section, I talked about the physical layer as connecting two devices, but
the fact is, many devices can be connected together at once by the physical
layer.  After all, many people use a single WiFi hotspot.  And, believe it or
not, you can have more than two computers connected with each other on a single
Ethernet connection.  All we figured out last section was how we could send
bits.  So, the link layer has to be able to send a message to any of the people
that share a link with us.

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
address on the frame matched their own, they would open it up and read it.

Sadly, things aren't usually that simple.  Since multiple devices can be
connected to the same link, it'll probably happen that two of them will try to
talk at the same time.  If they do, the other devices on the link won't be able
to understand either of their messages, because they'll interfere with each
other.  This is called the multiple access problem.  A simple way to think of
the multiple access problem is to imagine a small dinner party where everyone is
sitting around the table talking.  In small groups like this, only one person
can talk at a time.  The strategies we use in networks to solve this problem are
remarkably similar to strategies people us in these "dinner party" situations.

*   The most obvious rule: if you hear that somebody else is talking, don't
    start talking!  In networking, this is called collision avoidance.
*   If you are talking, and you hear somebody else starting to talk, stop
    talking!  They should probably stop talking as well, and then you can figure
    out who should talk from there.  (Although this makes sense as a strategy,
    it's not always possible.  For instance, WiFi devices are usually not
    capable of sending and receiving at the same time.  Once you start sending a
    message, you have no idea if someone else started sending one too.)  This is
    called collision detection.
*   When you do "collide" with somebody in conversation, you typically wait a
    moment and then try again.  In human conversation, there's usually some
    negotiation about who should talk first, but in networking, devices just
    wait a random amount of time before trying.  That way, there's a decent
    chance that the two devices that colleded will go at different times.  This
    is typically referred to as random backoff.
*   Finally, people frequently acknowledge that they've understood what you've
    said by nodding.  Some link layers use acknowledgements just like this.
    WiFi has lots of interference, so it uses these.  It also retransmits if
    there was an error in the message.  Ethernet, on the other hand, does not
    (since errors are uncommon in Ethernet).

This isn't really a description of any particular multiple access protocol.
Each link layer typically combines these elements as well as other ones in a way
that can ensure that collisions will be handled and messages will get across the
link quickly.

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

In conversation, humans *sort of* use checksums too.  You have no guarantee that
the person you talk to will hear you correctly.  But, we generally talk in
complete sentences.  If somebody misheard you, it wouldn't make sense, and
they'd probably stop you to ask what you actually said.  Checksums in action!

### The Network Layer

Whew!  That link layer was hard, for something that seemed so simple.  What did
we gain from it?  Now, we know that we can send messages addressed to somebody
we share a connection with.  What do we do with it?

Well, like I mentioned way earlier, the fun thing about networks is being able
to get messages to places in the network that you aren't even directly connected
to.  So, it would be nice if we had a way to get messages across the network.
That is what the network layer is there for!  The network layer enables
computers that are connected with each other to forward information along the
network toward its destination.  Get ready for some fun!

#### Routing, Part 1

Imagine that you would like to send a message from your computer to a computer
on the other end of the Internet.  You don't have a direct connection to that
computer, but you are connected to the Internet.  Presumably, there is a path
from your computer to the destination.  How do you send your message so that it
will reach the other computer?

One potential way would be for your computer to know the entire layout of the
Internet.  It could determine what the best route through the network is, put
all that information along with the message, and send it on its way (now that
we're on the network layer, we typically refer to these messages as packets or
datagrams).  All the intermediate computers (routers) would simply need to know
how to follow the instructions your computer put in the packet, and eventually
it should show up at its destination.

Well, that's not a bad way of doing it.  It would mean that all the computers
along the way could be pretty dumb.  All they'd have to do is know how to follow
instructions.  They wouldn't need to know anything about what paths were the
best way to get from one place to another along the network, because your
computer would do that for them.  Unfortunately, there are some serious
drawbacks to that:

* The Internet is pretty huge.  A map of the Internet (which your computer would
  need in order to plan the packet's "road trip") would take up a significant
  amount of space.  How would you like it if your smartphone was so full of
  "Internet roadmaps" that you couldn't take any more pictures or download more
  music?
* Internet companies would rather not tell you all about the road map inside
  their networks.  How an ISP structures its network is part of what makes them
  different from another ISP.  So, in a sense, it's proprietary information.
* What if an ISP's router broke?  Everyone else on the Internet would have a map
  showing that router still works, and they'd continue sending their packets to
  what is, in effect, a broken bridge!  You would have to constantly update
  everyone's road map with every change to its structure.  Since the Internet is
  constantly changing, this is a terrible problem.

So, unfortunately, we can't all keep road maps of the Internet and send our
packets out with a set of instructions.  Back to the drawing board!

Instead of treating the stuff we want to send across the network as a car going
across roads, maybe we ought to think of it more like mail.  When you want to
mail a letter to somebody, all you need to know is their address.  You drop the
addressed envelope into a mailbox, and your job is done.  The postal *network*
takes care of the rest.

#### Addressing

This strategy sounds promising!  It sounds like we're going to need a way to
address computers.  Let's take the analogy further.  A normal street address
(here in America) looks something like this:

> Johnny Appleseed  
> 123 Maple Road, Apt. 5  
> Cleveland, OH, 44106

(If there is indeed a Johnny Appleseed residing at this address, you have my
sincerest apologies!)

This address has some interesting qualities that make it useful for postal
workers to get it to where it needs to go.  Notice how it goes from specific to
general.  It starts out with the most specific identifier, the street and
apartment number.  Then, it names the street, then the city, and state.  Anybody
could deliver a letter with this address.  They may not know where to find
Johnny Appleseed, but they certainly can find Ohio.  Once they get near Ohio,
they can probably get pointed towards Cleveland.  Once they arrived in
Cleveland, they could probably get directions toward Maple Road.  Once on the
road, they could certainly look for the correct house and apartment numbers, and
deliver the letter successfully to our friend Johnny.  The wonderful thing about
addresses is that almost anybody can point you in the direction of the most
general part of the address, and once there, you can find the more specific
parts.

If we wanted the Internet to have a delivery system similar to the post office
(hint: *it does!*), then we need to have an address system that's organized in a
similar way!  We already know of MAC addresses from our discussion of the link
layer.  These addresses are assigned uniquely by manufacturers to our devices.
Unfortunately, a MAC address tells you nothing about where in the network a
device is.  Two devices made by the same manufacturer with nearly identical MAC
addresses are not guaranteed to be near each other.  Really, a MAC address is
more like a Social Security Number in the US.  These numbers, assigned at birth,
tell us nothing about where a person resides.  That's why we use a street
address to send mail, and not a SSN.

So, from the looks of it, we'll need a new way to "address" devices.  This
address is called an Internet Protocol (IP) address!  These addresses are
carefully designed to mimic street addresses.  Whenever the first numbers of an
IP address are the same, you know that the addresses are within a network
together.  If more numbers at the beginning of the address are the same, then
these devices are within an even smaller network, and therefore closer together.
This makes sense when you think about the street address analogy.  My next door
neighbors share most of my address, and we're next door.  My relatives in other
states don't have any parts of their street address in common with me, because
we live so far away.  Of course, IP addresses are slightly different than cities
and states.  There is a central organization that gives ranges of IP addresses
out to companies (like ISPs).  This organization is called the Internet Assigned
Numbers Authority (IANA), and it's a part of a larger organization called the
Internet Corporation for Assigned Names and Numbers (ICANN).  We'll meet ICANN
again later on!

IP addresses are numbers that look like this: `12.34.56.78`.  Each of the four
numbers can range from 0 to 255.  When IP addresses were created, the plan was
to give them to organizations in blocks of different sizes.  Class A blocks were
networks that shared only one number at the beginning (the "prefix").  The three
remaining numbers (a total of around 16 million addresses) were given to the
organization to do whatever they'd like with.  For instance, Google might have
been given the Class A network `12.x.x.x`.  That would mean that they were given
all the IP addresses that start with 12, to do whatever they wanted with.
Similarly, Class B networks share the first two numbers, and the last two vary
(65,536 addresses).  Finally, Class C networks hold the first three numbers
constant, and let the last one vary.  There are only 256 addresses in a Class C
network.

Somewhere along the line, people realized that this wasn't the best idea.  The
gap between the size of a Class C network (256 addresses) and a Class B network
(65,536 addresses) was pretty big.  If I'm a company that wants a few thousand
addresses for my employees, I would have to get a Class B network, wasting
around 60,000 addresses.  So, Classless Inter-Domain Routing (CIDR) was
introduced.  It works like this: IP addresses can also be represented in binary
(in fact, that's how they're always represented within computers!).  For
instance, the address `12.34.56.78` would be
`00001100.00100010.00111000.01001110` in binary.  Instead of giving people class
A, B, or C IP ranges, CIDR gives people a prefix of a certain amount of bits.  A
prefix of 24 bits leaves the remaining 8 bits to vary, which is the same as a
Class C network.  But, you could instead change the prefix to 22, giving 1024 IP
addresses, and allowing much more conservative allocation of IP addresses.
There is even a way of writing this out without using binary, called CIDR
notation.  However, to explain that would be going down a rabbit trail!  Suffice
to say, IP addresses always have prefixes that indicate what network they belong
to.

So, with addresses like these, we can begin to imagine what life must be like as
a router!  Your physical layer starts receiving bits.  Your link layer reads the
frame, and discovers that it was meant for your MAC address.  So, it takes the
data and sends it up to your network layer.  Your network layer reads the
packet's *headers* (which are like the outside of an envelope) to see where it
is going.  You don't know where that exact address is in the world, but you have
a list of IP address prefixes, and you know the general direction of where those
prefixes live on the network.  You find whatever prefix matches the address on
the packet, and send the packet out in that direction.

Keep in mind that this is no different than somebody asking you for directions
to an address!  You tell them that you don't know where that address is exactly,
but you know where to find the city (or the street).  By using this same power
of IP addresses, routers can do the same thing.

#### Routing, Part 2

Well, this is exciting!  Assuming every router on the Internet has a list of
prefixes and their corresponding "directions" (which we call a "routing table"),
they can send packets along their merry way!  If you think about how these
"routing tables" will look, it's somewhat similar to a human's understanding of
driving directions around them.  For instance, here is my "routing table":

* I could tell you how to get to a few places in Cleveland, where I live.  If
  you told me the area or the street, there's a decent chance I could get you
  there.
* I know a few of the outlying suburbs and cities around Cleveland.  Chances
  are, I could tell you how to get on a freeway that might take you there.
* Similarly, for the big cities around Cleveland, I could tell you what freeways
  would get you there.
* For more distant places, I could probably give you a compass direction toward
  that city or country.  But that's pretty much it!

I learned my routing table doing a number of things.  I drove around a lot with
a GPS.  I planned some routes while looking at Google Maps so I would understand
how the roads connect.  Eventually, I got comfortable enough with my area that I
didn't need to have a GPS with me if I knew where my destination was.  The
knowledge about the more distant places, I got mostly from geography in school.

Unfortunately, routers don't spend much time "driving around" the Internet, and
they certainly don't go to school to learn "Internet geography"!  We made a big
assumption in thinking that routers have a "routing table".  It turns out, each
router having one of these tables is pretty darn difficult.  So, how do we make
it happen on the Internet?

This is a huge, mind-numbingly complex topic.  So, I'm going to skim over it,
enough to explain the simple concepts.  The Internet, like I mentioned at the
beginning of this post, is a giant "graph".  A guy named Edsger Dijkstra came up
with this neat method ("algorithm") for finding the shortest path from one node
in a network to another.  His algorithm (conveniently named "Dijkstra's
Algorithm") is so important, that it's actually what Google Maps and your GPS
use to plan your routes on the road network!  It's also what powers the ideas
behind building up routing tables.

There are two main strategies for building routing tables.  The first one is
called a "link-state" protocol.  This is where each router keeps an internal map
of the network.  It uses Dijkstra's Algorithm on this map to come up with a list
of shortest paths for different prefixes, and makes a routing table like this.
In order to keep maps up to date, the routers will periodically broadcast a
message to everyone else about the "state" of their links.  If they got any new
connections, or lost any old ones, they'll tell everyone else in the network, so
everyone can update their maps!  This strategy is pretty good, but it is
difficult to use in a large-scale way, because holding an entire Internet map is
difficult.  You can think of this strategy like keeping your own map at your
house.  When a neigbor tells you about a road closing, you update your map to
reflect it.  When a road near you closes, you tell everyone you meet about it so
they know to update their maps.

The second strategy is called a "distance-vector" protocol.  In these protocols,
a router just keeps track of its routing table (that is, prefixes, directions,
and distances).  Periodically, routers will "advertise" to each other how
quickly they can get a packet to a destination.  When a router hears an
advertisement for a faster time, it updates its table with a new distance and
direction.  In essence, all a router ever knows is its routing table, and it
just updates it with new information.  If I were under the impression that the
fastest way to get to Chicago from Cleveland was through Columbus, I would be
very pleased to hear that I could get there faster through Toledo, and I would
update my routing table accordingly.

While these strategies sound similar, they're subtlely different, and they have
different strengths and weaknesses.  As such, one isn't really better than the
other.  Therefore, the Internet actually has two different types of routing
protocols.  One (the external one) is for finding paths from one big network to
another, and the other (the internal) is for finding paths within the same
network.  Remember how I said way earlier in this post that ISPs like to call
their networks "autonomous systems"?  Well, this is why.  Inside their own AS,
the ISP gets to decide what routing protocol they use to build their routing
tables.  However, in order to share information between all of the different
AS's on the Internet, there has to be a single universal protocol.  This
protocol is called the Border Gateway Protocol (BGP).  It's called this because
it is used at the borders between AS's, in order to tell other networks where
you can go by going through your network.  BCP uses the distance-vector strategy
from above.

Internal routing protocols are used within a AS to give all the routers within
the AS their routing tables.  They use information gained from BGP, along with
the structure of the AS and the rules imposed by the ISP, to construct routing
tables.  There are quite a few of them, since it is up to the people who
administer the AS to decide what they want to use.  Here are the names of a few:

* Routing Information Protocol (RIP) - uses the distance-vector strategy.
* Open Shortest Path First (OSPF) - uses the link-state strategy
* Intermediate System to Intermediate System (IS-IS) - uses the link-state
  strategy.
* Internal BGP (iBGP) - there is a version of the BGP protocol that can be used
  within an AS.  Like its external version (eBGP), iBGP also uses the
  distance-vector strategy.

#### Network Layer: Putting it all Together

OK, so that was a ton of new information.  Let's recap:

1. The link layer gave us the ability to send information across a link to
   somebody else who is listening.
2. The network layer aims to allow us to send information through a series of
   links to a destination you're not directly connected to.
3. The network layer uses IP addresses, which are similar to street addresses,
   in that different parts of them tell us more or less general information
   about where a computer is.
4. Routers can use "routing tables", or lists of IP prefixes and directions, to
   figure out which way to send a packet they receive.
5. In order to compute routing tables, routers use routing protocols to
   communicate information about how to get to places.
6. There are two types of routing strategies, link-state and distance-vector.
7. External routing protocols are used between Autonomous Systems (AS's) as a
   standard way of communicating routing information across the Internet.  The
   only standard Internet external routing protocol is BGP.
8. Internal routing protocols are used within AS's.  There are many of these,
   since there is no standard one.

Recap done!  If you kinda followed all of those points, then you have a basic
understanding of how the Network layer of the Internet works!  Congratulations!

### The Transport Layer

We're over the hump.  Three layers down, and two more to go.  Now that we can
send a packet from one place in the network to anywhere else, what more is there
to do?  Plenty!  While the network layer was all about communicating between two
different computers, the transport layer is all about communicating between two
programs on those two computers.  Let's make an analogy!  At your house, you may
have multiple people living there.  You all have the same street and apartment
addresses, but you are different people.  Mail that has your housemate's name on
it goes to your housemate, not you.  You don't need to read their mail, and you
don't want them reading your mail.  In the same way, you don't want your web
browser to get interference if you run it at the same time as you listen to
music on Spotify!

The other problem that the transport layer tries to solve is something we've
been pointedly ignoring so far: reliable data transfer.  I told you that the
Network Layer can get your data from one end of the network.  What I didn't say
is that it can do it 100% reliably (*spoiler alert: it can't!*).  There are tons
of reasons that the Network Layer might fail to deliver your packets.  There
could be an error in communication, corrupting your packet.  Or, the network
could be really congested along the path from you to your destination.  In order
to cope, the routers along the path might have just "dropped" your strange!

In addition, you have no guarantee that the network layer can deliver your
packets in the same order that you sent them!  Due to the way that routing
protocols work, a router's table could be updated at any time, sending two
packets with the same destination careening down completely different paths.
It's entirely possible that one would arrive before the other.

This all makes it difficult to make useful programs using the network layer.
Who would browse the web if chunks of the pages were swapped around and garbled
randomly?  Nobody.  So, another thing that the transport layer tries to provide,
beyond delivering messages between programs, is doing it 100% reliably!

It's worth mentioning that "reliable data transfer" doesn't *have* to be done by
the transport layer.  It *is* done that way on the Internet, but you could also
make a link- or network- layer protocol that can guarantee reliable data
transfer.  However, the good folks responsible for designing the Internet, the
Internet Engineering Task Force (IETF) weighed the options and decided that the
Internet would be most scalable if it left that up to the transport layer to do.
And that's what we do!

Down to business!  What are the major protocols of the transport layer, and how
do they work?  Well, when you talk about network layer protocols, there are
really only two names in the game: TCP and UDP.  TCP, or Transmission Control
Protocol, is by far the dominant protocol of the Internet.  It provides all of
the services I just described: communication between applications, and reliable
data transfer.  On the other hand, UDP (User Datagram Protocol) simply provides
communication between applications, and error detection mechanisms (**not**
error *correction* mechanisms).

Both of these protocols use something called "ports".  These are simply
transport layer addresses, similar to how IP addresses are network layer
addresses.  TCP and UDP both allow you to have port numbers ranging from 0 to
65,536.  However, TCP ports are different from UDP ports (a message to TCP port
22 will not get picked up on UDP port 22 as well).  And, it's important to keep
in mind that these are not actual physical ports like your USB port.  They only
exist in the code on your computer and the minds of programmers!

#### TCP

TCP accounts for a huge majority of Internet traffic.  The reasons are simple:
it provides incredibly convenient reliable transfer guarantees.  TCP provides
applications with an ordered stream of bytes (just a unit of computer data).
Whatever you put into the TCP stream (often called a socket) will come out
unharmed and in order on the other end.  Webpages, audio and video streams,
email, and files are all usually sent over TCP (using their corresponding
application layer protocols, which we'll cover soon enough).  How does it do it?
By applying a couple of strategies, which are summarized below:

* Numbering and acknowledging bytes.  Each byte has a number in TCP, so that the
  application on the other end knows where the bytes belong in the message.
  When a TCP connection receives bytes, it will respond with an acknowledgement
  saying something like "I've received everything up to byte *n* just fine!".
* A send and receive window.  TCP pretends to have a window of information it
  can be sending at any given time.  At the beginning of the window is the stuff
  that it has sent, but hasn't heard an acknowledgment about.  Anything from
  there to the end of the window can be sent, but nothing after that can be sent
  (until a new acknowledgement arrives, shifting the window).
* Retransmitting bytes that are inferred to be lost.

There is a lot more complexity to how the acknowledgement system works, but
that's the idea in a nutshell.  While this system does an excellent job
addressing the problems of packet loss due to corruption, and packets arriving
out of order.  Hoewever, there are types of packet loss that don't happen due to
corruption.  Sometimes, routers become overwhelmed with traffic, and just can't
handle any more packets.  So, they ignore them.  If TCP just resends those lost
packets, it'll just cause those routers to continue to be overwhelmed, failing
to address the root cause of the packet loss.  This will make everybody's
connections slow to a crawl.  So, in addition to the error prevention strategies
above, TCP also will scale back the rate at which it sends data when it detects
lots of packet loss.  Once the packet loss dies down, it tries to gradually
increase it to find the best speed to send at.

By combining the reliable data transfer mechanisms with flow control, TCP
provides a very valuable tool for making Internet programs.  It's great for
things like sending web pages and files, but it's not perfect for everything.
One problem with TCP is that, in order to provide all these features, it's
rather complicated.  Some programs don't need that complexity.  Plus, TCP's
reliable data transfer can sometimes slow down connections when errors are
present (because it has to resend data).  Real-time programs like online games
and video conferencing programs might prefer to just ignore those errors so that
they can send data faster, and so TCP is not right for them.

#### UDP

For those applications where TCP isn't right, we have UDP.  There's actually not
very much to say about it.  Like TCP, UDP uses port numbers to identify
applications.  It also can detect errors in transmission, like TCP, but it
doesn't fix them.  Additionally, it doesn't provide you with the "byte stream"
interface TCP does.  You simply send "datagrams" that will (maybe) arrive at
their destination.

### The Application Layer

Congratulations, everyone!  We've reached the top layer of the Internet, the
Application Layer.  The Application Layer is where the magic happens, as far as
users of the Internet are concerned.  Most of the Internet applications you love
are an application layer protocol!  Quite simply, the job of the application
layer is to use the program-to-program communication provided by the transport
layer and below to make cool programs!  So, I'll take this time to give a brief
overview of a few application layer programs, to give you a picture of how
everything works together.  Without a doubt, the most famous application layer
program of the Internet is called "the World Wide Web".

#### The World Wide Web

At this point, you may be pumping the breaks.  After all, isn't the "world wide
web" just a nineties style way of saying the Internet?  The answer to that is a
resounding *no*!  Technically, there is a huge difference between the Internet
and the Web!  I have spent this entire blog post so far discussing the Internet:
a layered set of protocols that make a bunch of connected computers into a true
network that can send and receive information.  The Web is a set of
application-level protocols that *use* the Internet.  It allows people to browse
"web pages" on computers all over the Internet.  The Web defines the languages
and protocols these programs use to communicate pages, and the Internet is the
set of protocols the Web relies on to communicate!

This is a major distinction, but it's also a pretty technical one.  After this
whole novel about how the Internet works, the distinction is pretty clear, but
in normal conversation, nobody really cares (including me) when you use the two
terms interchangably!

So, how is it that when you type `www.google.com` into your browser, you see
Google?  There are a number of application-level protocols that work together to
make this possible.  The first one you interact with is called DNS, for the
Domain Name System!

##### DNS

To us, `www.google.com` is the name of a website.  However, nowhere in the
entire internet protocol stack did we ever use text names to address computers!
The Domain Name System is what is responsible for translating these names into
the IP addresses that the Internet uses for routing.

DNS is one of those "simple" protocols that doesn't need the complexity of TCP.
So, it operates on UDP port 53.  When you want to go to a domain, like
`stephen-brennan.com`, your computer sends a question ("DNS query") to the local
DNS server.  The DNS server (which is just a computer) figures out what IP
address that stands for, and sends back a response to your computer.

The DNS server figures it out by consulting its own internal table.  If the name
isn't in its table, the server then consults the rest of the DNS network.  There
is a whole hierarchy of authoritative domain name servers that contain the true
information, as published by the people who own the domain names.  People can
buy these domain names from companies called "registrars", who will allow them
to set their website's IP address in the authoritative DNS servers.

##### HTTP

Once your computer knows the IP address of the website you'd like to visit, it
needs to talk with the website computer in order to get the page you want.  In
order to do so, your computer and the website need to speak the same language,
and this language is called HTTP (HyperText Transfer Protocol).  HTTP is a
protocol built on top of TCP.  In HTTP, your computer sends a message to the
website that looks something like this:

```
GET /resume.html
Host: stephen-brennan.com

```

The website will receive this message and respond back, usually like this:

```
200 OK

<!doctype html>
<html>
...
```

The message your computer sent is called a request.  It has a "method", which
tells the website what you want it to do.  The most common one is "GET", which
tells the website that you'd like it to send you a page.  The remainder of that
line specifies the URL, or path, to the file.  The rest of the request contains
things called "headers" telling the server more information about who you are
and what you want.

The message the website sends back is called a response.  It starts with a
status code.  The most common one is 200, meaning "everything went well".
Responses can also include headers, which tell you more about the server, and
can even give your computer instructions on what to do with the response.  After
the status code and header comes the response "body", which contains the web
page you asked for.

This web page is written in "the language of the web", HTML, which stands for
HyperText Markup Language.  This is just a text file that gives web browsers
detailed instructions on how to display information.  Web pages can also list
additional resources your computer should get, such as images, fonts, style
sheets, and scripts.  Your computer may have to make additional HTTP requests
until it has everything required.  Then, it displays the page for you!

#### Email

Another classic "application" on the Internet is Email.  It actually is older
than the Web.  In essence, you have many different "mail servers" run by people
like Yahoo, Google, Microsoft, etc.  Each one corresponds for a type of email
address (`@yahoo.com`, `@gmail.com`, `@hotmail.com`, etc).  When you'd like to
send a message to somebody, your mail program logs into your mail server using a
protocol called SMTP (Simple Mail Transfer Protocol).  Here's an example
exchange between you and a mail server to send a message.  Lines starting with
`>` are you sending to the mail server, and lines starting with `<` are you
receiving.  The `>` and `<` aren't actually part of the protocol, they just make
it easier to read.

```
> HELO smtp.example.com
< 250 smtp.example.com at your service!
> MAIL FROM:me@example.com
< 250 2.1.0 Ok
> RCPT TO:friend@another-example.com
< 250 2.1.5 Ok
> DATA
< 354 End data with <CR><LF>.<CR><LF>
> To: friend@another-example.com
> From: me@example.com
> Subject: Test message
>
> Hello friend, this is a test message.
> From,
> me
> .
< 250 2.0.0 Ok: queued as 0B2F3E0115
> QUIT
> 221 2.0.0 Bye
```

In this exchange, you log into your mail server and tell it you'd like to 

[graph]: https://en.wikipedia.org/wiki/Graph_(mathematics)
[superfish]: {% post_url 2015-02-20-superfish-explained %}
