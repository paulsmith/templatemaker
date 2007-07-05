from templatemaker import Template

def test_holes():
    TESTS = (
        # input1, input2, tolerance, output
        # All tests use "!" as the marker character in the output.
        (('<title>123</title>',), 0, '<title>123</title>'),
        (('<title>123</title>', '<title>a2c</title>'),  0, '<title>!2!</title>'),
        (('<b>this and that</b>', '<b>alex and sue</b>'), 0, '<b>! and !</b>'),
        (('<b>this and that</b>', '<b>alex and sue</b>', '<b>fine and dandy</b>'), 0, '<b>! and !</b>'),
        (('<b>this and that</b>', '<b>alex and sue</b>', '<b>fine and dandy</a>'), 0, '<b>! and !</!>'),
        (('<b>this and that</b>', '<b>alex and sue</b>', '<a>fine and dandy</a>'), 0, '<!>! and !</!>'),
        # Test one character at start of string.
        (('hello dad', 'hello mom'), 0, 'hello !'),
        (('hello dad', 'hello mom', 'hello son'), 0, 'hello !'),
        (('hello dad', 'hello mom', 'hi dude'), 0, 'h!e!'),
        # Test one character at end of string.
        (('hello there', 'goodbye there'), 0, '!e! there'),
        # Test tolerance.
        (('<title>123</title>',   '<title>a2c</title>'),  1, '<title>!</title>'),
        (('<title>123</title>',   '<title>a2c</title>'),  2, '<title>!</title>'),
        (('<title>1234</title>',  '<title>a23c</title>'), 0, '<title>!23!</title>'),
        (('<title>1234</title>',  '<title>a23c</title>'), 1, '<title>!23!</title>'),
        (('<title>1234</title>',  '<title>a23c</title>'), 2, '<title>!</title>'),
        (('<title>1234</title>',  '<title>a23c</title>'), 3, '<title>!</title>'),
        (('http://suntimes.com/', 'http://someing.com/'), 0, 'http://s!me!.com/'),
        (('http://suntimes.com/', 'http://someing.com/'), 1, 'http://s!me!.com/'),
        (('http://suntimes.com/', 'http://someing.com/'), 2, 'http://s!.com/'),
        (('http://suntimes.com/', 'http://someing.com/'), 3, 'http://s!.com/'),
        (('http://suntimes.com/', 'http://someing.com/'), 4, 'http://s!.com/'),
        # The marker character (\x1f) is deleted from all input.
        (('<title>\x1f1234</title>',  '<title>5678\x1f</title>'), 0, '<title>!</title>'),
    )
    for input_list, tolerance, expected in TESTS:
        t = Template(tolerance=tolerance)
        for inp in input_list:
            t.learn(inp)
        got = t.as_text('!')
        if got != expected:
            print "Input:\n%s" % '\n'.join(['  %r' % inp for inp in input_list])
            print "Tolerance: %s\nExpected: %r\nGot: %r\n" % (tolerance, expected, got)

if __name__ == "__main__":
    test_holes()
