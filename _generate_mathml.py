import re
import subprocess
import sys


def convert(m):
    return subprocess.run(
        ["pandoc", "--mathml"],
        capture_output=True,
        input=m.group(0),
        check=True,
        text=True,
    ).stdout.removeprefix("<p>").removesuffix("</p>\n")


def convertinline(m):
    # kramdown sees HTML tags at the start of a line and if they're not a
    # normal inline tag, it ends the current <p>. To avoid this, wrap in a
    # span.
    return "<span>" + convert(m) + "</span>"


data = sys.stdin.read()
data = re.sub(r"\$\$[^$]+\$\$", convert, data)

# Inline math is a bit trickier.
#  - Require it all on one line (even if that's not a "real" requirement)
#  - Use negative look ahead/behind to avoid matching double dollar signs
#    (though they should already be consumed anyway).
#  - Use the positive assertions to avoid confusion with dollar signs in
#    prose. EG: "I got $5 by: $2 + 3$" or "I made $5, but lost $100". By
#    enforcing that the character after the opening $, and before the close,
#    are not whitespace, we can prevent most confusions.
data = re.sub(r"(?<!\$)\$(?=\S)[^$\n]+(?<=\S)\$(?!\$)", convertinline, data)
sys.stdout.write(data)
