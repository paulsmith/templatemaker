r"""
templatemaker.py

Copyright (c) 2007 Adrian Holovaty
License: BSD

See readme.txt for full documentation.
"""

from _template import make_template, marker
import re

# The marker character lives in _templatemaker.marker() so we don't have
# to define it in more than one place.
MARKER = marker()

class NoMatch(Exception):
    pass

class Template(object):
    def __init__(self, tolerance=0, brain=None):
        self._brain = brain
        self._tolerance = tolerance
        self.version = 0

    def clean(self, text):
        """
        Strips any unwanted stuff from the given Sample String, in order to
        make templates more streamlined.
        """
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
        regex = '^(?s)%s$' % re.escape(self._brain).replace(re.escape(MARKER), '(.*?)')
        m = re.search(regex, text)
        if m:
            return m.groups()
        raise NoMatch

    def extract_dict(self, text, field_names):
        """
        Extracts the data from `text` and uses the `field_names` tuple to
        return a dictionary of the extracted data.

        Returns a dictionary of the raw data according to field_names, which
        should be a tuple of strings representing dictionary keys, in order.
        Use None for one or more values in field_names to specify that a
        certain value shouldn't be included in the dictionary.
        """
        data = self.extract(text)
        data_dict = dict(zip(field_names, data))
        try:
            del data_dict[None]
        except:
            pass
        return data_dict


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

class HTMLTemplate(Template):
    """
    A special version of Template that is a bit smarter about dealing with
    HTML, assuming you care about identifying differences in the *content* of
    an HTML page rather than differences in the markup/script.
    """
    def __init__(self, *args, **kwargs):
        Template.__init__(self, *args, **kwargs)
        self.unwanted_tags_re = re.compile(r'(?si)<\s*?(script|style|noscript)\b.*?</\1>')

    def clean(self, text):
        """
        Strips out <script>, <style> and <noscript> tags and everything within
        them.
        """
        text = self.unwanted_tags_re.sub('', text)
        return Template.clean(self, text)
