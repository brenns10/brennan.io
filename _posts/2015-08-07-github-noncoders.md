---
title: GitHub for Non-Coders
layout: post
---

I've heard the phrase "GitHub is like Facebook for programmers" a lot.  In fact,
I've used it myself a few times when trying to explain GitHub to people who
don't program.  But it's not really accurate, so I thought I'd take the time to
write a little article targeted at non-programmers to explain exactly what
GitHub is.  Unlike what many programmers might want you to think, it's not too
complicated.

The analogy to Facebook is only partially right.  Really, a better analogy might
be to Google Docs.  GitHub provides a way for programmers to collaborate with
each other on programs.  Using GitHub, programmers across the world can
collaborate seamlessly on open source software.  They can also post their own
projects so that other programmers can see, use, and even improve them.  This
all works due to GitHub's core feature: Git hosting.

## Git, for Non-Coders

Git is the name of a *version control system* (which likely doesn't help you
understand what it is).  A version control system is a way for programmers to
keep track of the changes they make to their code.  They can also use it to try
out new ideas without messing up their progress.  The easiest way to understand
version control is with an example:

Imagine that you are writing a resume for the first time.  You pop open
Microsoft Word, open a resume template, and start filling in information.
Before long, you've got a first draft, and you're absolutely sick of writing
resume stuff!  So, you save it as `Resume Draft 1.docx`, and print a few copies.
You give one to your parents, another to your career center, and another to a
close friend.  Being nice people, they read it and mark it with suggestions.
Next time you feel up to resume writing, you go back to your computer with the
marked up copies.

The first thing you do is open the draft and save it as `Resume Draft 2.docx`,
so that you can keep the old copy of your resume.  Then, you start working on
improvements.  You may repeat the "improve, save, distribute" process a few
times, until you're pretty confident that your resume content is very good.

Next, you realize that your resume is very black, white, and Times New Roman.
While you don't need neon colors, maybe you want something a bit more pleasing
to the eye.  So, you open a new copy, save it as `Resume New Theme Idea.docx`,
and start making changes.  You change the font to something sans serif, add some
accent colors, and do some other styling changes.  If it ends up looking gaudy,
you can always just delete the "New Theme Idea" copy and go back to your old
one.  But, if it ends up looking better, you can save it as your newest draft,
or even `Resume Final.docx`.

This process (which you may have done yourself) is like a version control
system.  You don't want to lose old copies of your resume, and you don't want to
mess up your current copy when you change it, so you clutter your
`Documents\Resume\` folder with a bunch of different versions.  Programmers, who
work on files all the time, are very familiar with the necessity to keep around
old copies of things.  What if they make a change that breaks their program?
What if they forget what they did, and can't get it working again?  It may sound
silly, but that's an easy thing to do when you're working on a project with more
than a few files filled with code.

Thankfully, programmers are very lazy, so they came up with ways to relieve
themselves of the burden of constantly making copies of their code.  Rather
predictably, they wrote programs that do it for them, and Git is one such
program.  Git works by keeping a "timeline" of an entire folder (this is usually
called a "repository").  Every so often, a programmer will make a checkpoint of
their code (this is called a "commit" or a "check in").  This adds the current
state of the folder to Git's timeline.  If they do this consistently, they can
always go back and look at older versions of their code, and even restore the
older version of their code.

They can even make different "branches" of the timeline, where they try out
different things.  Branches are just like branches in a tree - places where the
history splits off in two directions.  This is just like the copy of the resume
where you changed fonts and added colors.  If you don't like it, you can get rid
of the branch.  If you do like it, you can "merge" your main resume with your
newly themed resume.

![resume history](/images/resume-vcs.png)

Here is an example of what your git "timeline" might look like if you had used
Git while writing your resume.  Each circle represents a git "checkpoint", and
the rectangles are just labels for branches.  The master branch is the official
version of the resume.  The "new theme" branch is where you tried out the new
theme idea, but didn't want to commit to it yet.

So, that's the basic idea of version control.  With the timeline and branching
features, programmers are able to have access to any version or branch of their
code they'd like, and it's all done transparently by Git.  While there's plenty
more details, this is the general idea.

## Collaboration, GitHub Style

Now that you know what Git is, you'll understand what I mean when I say that
GitHub just holds people's Git repositories.  It's a website just filled with
different users and their Git repositiories.  Each one contains code and
timelines just like the one above.  And as convenient as Git was for keeping
track of versions of our resume, it becomes even cooler when you allow other
people to use it with you.

If you've ever collaborated with someone on a Google Doc, you may be familiar
with what it's like to accidentally step on your collaborator's toes while
making changes.  If you both edit the same text at the same time, who knows what
will happen?  This is just as much of a problem when you have multiple people
working on code.  Thankfully, the Git branches we saw above are perfect for
solving this problem.  Whenever you need to work on something, you can start your
own branch, make changes on that branch, and when you're done, you and your
collaborators can merge those changes into the master branch!

This could all be done without GitHub.  People could organize themselves using
email, and pick somebody's computer to hold the main copy of the code.  However,
GitHub provides a much more "slick" way to do this.  Programmers can put their
Git repositories on GitHub, and invite other programmers to join their project.
Whenever one person has a branch they'd like to merge into master, they create
something called a "Pull Request".  This is an awesome tool that brings
everyone's attention to the new changes.  It allows everyone to comment on lines
of code, suggesting improvements.  When it's agreed that the changes are ready
to incorporate into the master branch, the project owner can accept the pull
request, which merges the branch.

For example, [here][example-pr] is a pull request a classmate of mine made on
one of our projects (YAMS) last semester.  He wrote code to implement a feature
in our project.  I tried out the code he wrote, found an error, and he fixed it.
After that, we approved his changes and added them to our project.  The pull
request allowed us to communicate quickly, see his changes, and even test them
out before approving them.  There were 6 people working on that project, but by
using the branching and pull requests, everyone was able to work simultaneously
without stepping on each other's toes.

## GitHub as the "Facebook of Programmers"

That's an overview of what GitHub actually does for programmers.  It has plenty
more features that I could explain, but it's enough to say that most of them
give programmers better ways to communicate about their code, and fix problems
with it.  After learning about all the productivity tools that GitHub has to
offer, it may seem a little silly that people call it the "Facebook of
Programmers".  Why not the "Microsoft Office of Programmers", or "Google Docs of
Programmers"?  Well, while GitHub does provide an excellent venue for getting
things done, it also is full of social features.

### Programmer Street Cred

Every member of GitHub gets a profile page.  [Here's][profile] mine.  The
profile page is full of information about you.  It has a list of your
repositories, ordered by how many people have "starred" them.  It also shows the
repositories belonging to other people that you've contributed to.  And, perhaps
the most popular form of programmer street cred, there is the contribution
graph!  The contribution graph is a yearly calendar with marks on each day that
you "contributed" to code on GitHub.  It also counts up the total number of
contributions you've made over the last year, and your longest streak of
contributions.  Here is my contribution graph:

![My contribution graph](/images/contributions.png)

In essence, your GitHub profile is like a "scorecard", and it makes everything a
bit more competitive.  The result of this friendly competition between
programmers is that everyone learns more, and open source software is improved.

### Following Your Friends

GitHub allows you to "follow" your friends' profiles, as well as "star" their
repositories.  When you do this, they get added to the news feed on your GitHub
homepage.  You get to see when they create new projects or improve existing
ones.  Plus, followers and stars can be another metric to go on your
"scorecard".

### Programmer Portfolio

One benefit of GitHub is that once you're a member for a few years, you start
racking up a pretty excellent list of programming projects in your profile.  If
nothing else, you can use this list to prepare for interviews.  But sometimes,
recruiters may even look at your GitHub portfolio to see what sort of projects
you have done.

## Conclusion

GitHub is a pretty excellent tool for programmers, for both productivity and
social networking.  It's not purely social like Facebook, or pure productivity,
like MS Office.  But it's a really powerful combination of the two that allows
for a lot of possibilities.

To be clear, GitHub isn't the only website like this.  Many other websites host
programmers' repositories, like [Bitbucket][], [SourceForge][], [GitLab][],
[CodePlex][], and [Visual Studio Online][].  But GitHub just has the most users
(at least, in my demographic), so I use it the most.

Hopefully, this article has helped you understand what GitHub is, especially if
you've never written a line of code in your life.  Let me know in the comments
whether it helped!

[example-pr]: https://github.com/brenns10/yams/pull/18
[profile]: https://github.com/brenns10
[Bitbucket]: https://bitbucket.org
[SourceForge]: http://sourceforge.net/
[GitLab]: https://about.gitlab.com/
[CodePlex]: https://www.codeplex.com/
[Visual Studio Online]: https://www.visualstudio.com/en-us/products/what-is-visual-studio-online-vs
