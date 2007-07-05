r"""
templatemaker.py

Copyright (c) 2007 Adrian Holovaty
License: BSD

See readme.txt for full documentation.
"""

from _templatemaker import make_template, marker
import re

# The marker character lives in _templatemaker.marker() so we don't have
# to define it in more than one place.
MARKER = marker()

unwanted_tags_re = re.compile(r'(?si)<\s*?(script|style|noscript)\b.*?</\1>')

class NoMatch(Exception):
    pass

class Template(object):
    def __init__(self, tolerance=0):
        self._brain = None
        self._tolerance = tolerance
        self.version = 0

    def clean(self, text):
        """
        Strips any unwanted stuff from the given Sample String, in order to
        make templates more streamlined.
        """
        text = unwanted_tags_re.sub('', text)
        text = re.sub(r'\r\n', '\n', text)
        return text

    def learn(self, text):
        """
        Learns the given Sample String.

        Returns True if this Sample String created more holes in the template.
        Returns None if this is the first Sample String in this template.
        Otherwise, returns False.
        """
        text = self.clean(text)
        text = text.replace(MARKER, '')
        self.version += 1
        if self._brain is None:
            self._brain = text
            return None
        old_holes = self.num_holes()
        self._brain = make_template(self._brain, text, self._tolerance)
        return self.num_holes() > old_holes

    def as_text(self, custom_marker='{{ HOLE }}'):
        """
        Returns a display-friendly version of the template, using the
        given custom_marker to mark template holes.
        """
        return self._brain.replace(MARKER, custom_marker)

    def num_holes(self):
        """
        Returns the number of holes in this template.
        """
        return self._brain.count(MARKER)

    def extract(self, text):
        """
        Given a bunch of text that is marked up using this template, extracts
        the data.

        Returns a tuple of the raw data, in the order in which it appears in
        the template. If the text doesn't match the template, raises NoMatch.
        """
        text = self.clean(text)
        regex = '(?s)' + re.escape(self._brain).replace(re.escape(MARKER), '(.*?)')
        m = re.search(regex, text)
        if m:
            return m.groups()
        raise NoMatch

    def from_directory(cls, dirname, tolerance=0):
        """
        Classmethod that learns all of the files in the given directory name.
        Returns the Template object.
        """
        import os
        t = cls(tolerance)
        for f in os.listdir(dirname):
            print t.learn(open(os.path.join(dirname, f)).read())
        return t
    from_directory = classmethod(from_directory)

    #    def optimize(self, text_list):
    #        """
    #        NOT YET FINALIZED
    #
    #        Given a list of Sample Strings, optimizes the current template. Returns
    #        True if at least one hole has been named pointless. Otherwise, returns
    #        False.
    #
    #        Specifically, this marks certain holes as "pointless" holes. Pointless
    #        holes are those in which content either duplicates that of other holes,
    #        or in which content is whitespace or other inconsequential characters.
    #        """
    #        # First, create a dictionary that maps template hole indexes to lists
    #        # of data in that index, e.g.:
    #        #     {0: ['Headline 1', 'Headline 2'], 2: ['Dec. 2', 'Jan. 31']}
    #        output = {}
    #        for text in text_list:
    #            for i, bit in enumerate(self.extract(text)):
    #                output.setdefault(i, []).append(bit)
    #        # Remove any data bits that contain only whitespace for every document.
    #        for i, bits in output.items():
    #            if sum([len(bit.strip()) for bit in bits]) == 0:
    #                print "Deleting output[%d] because it's only whitespace." % i
    #                print output[i]
    #                del output[i]
    #        # Remove any data bits that are duplicates. We only need one hole for
    #        # each type of data.
    #        # (NOT IMPLEMENTED YET)
    #        return output

if __name__ == "__main__":
    strings = (
        '<b>this and that</b>',    # '<b>this and that</b>'     
        '<b>that and this</b>',    # '<b>th! and th!</b>'    {'prev': {0: 'is', 1: 'at'}}
        '<b>heaven and hell</b>',  # '<b>!h! and !h!</b>'    {'prev': {0: 't', 2: 't'}, 'reorder': {0: 1, 1: 3}} # old pos -> new pos
        '<a>fine and dandy</a>',   # '<!>! and !</!>'        {'prev': {0: 'b', 1: '!h!', 2: '!h!'}, 'reorder': {0: 1, 1: 1, 2: 2, 3: 2}}
    )

    t = Template()
    for i, s in enumerate(strings):
        t.learn(s)
        print repr(t.as_text('!'))
        if i > 0:
            print repr(t.extract(s))
            print repr(t.extract(strings[i-1]))
        print

    # data = []
    # t = Template()
    # for s in strings:
    #     new_holes = t.learn(s)
    #     if new_holes:
    #         lc = t.last_change

    # import doctest
    # doctest.testmod()
    # Template.from_directory('/Users/adrian/tmp/suntimes', tolerance=4)
    