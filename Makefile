# This makefile does some preprocessing, namely converting latex math to mathml.
# I commit the resulting files, so that Github pages need not run this.

all: _posts/2016-07-23-bart-fare-hacking.md
all: _posts/2016-12-11-bart-revisited.md
all: _posts/2019-02-17-redesign.md

_posts/%: _posts/MATH-% _generate_mathml.py
	python _generate_mathml.py <$< >$@
