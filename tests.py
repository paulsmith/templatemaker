import unittest
from templatemaker import Template

class TemplatemakerTestCase(unittest.TestCase):
    def create(self, tolerance, *inputs):
        """
        "Helper method that returns a Template with the given tolerance and
        inputs.
        """
        t = Template(tolerance=tolerance)
        for i in inputs:
            t.learn(i)
        return t

    def assertCreated(self, tolerance, expected, *inputs):
        """
        Asserts that a Template with the given tolerance and inputs would be
        rendered as_text('!') to the expected string.
        """
        t = self.create(tolerance, *inputs)
        self.assertEqual(t.as_text('!'), expected)

class Creation(TemplatemakerTestCase):
    def test_noop(self):
        self.assertCreated(0, '<title>123</title>', '<title>123</title>')
        self.assertCreated(0, '<title>123</title>', '<title>123</title>', '<title>123</title>')
        self.assertCreated(0, '<title>123</title>', '<title>123</title>', '<title>123</title>', '<title>123</title>')

    def test_one_char_start(self):
        self.assertCreated(0, '!2345', '12345', '_2345')
        self.assertCreated(0, '!2345', '12345', '12345', '_2345')
        self.assertCreated(0, '!2345', '12345', '_2345', '^2345')

    def test_one_char_end(self):
        self.assertCreated(0, '1234!', '12345', '1234_')
        self.assertCreated(0, '1234!', '12345', '12345', '1234_')
        self.assertCreated(0, '1234!', '12345', '1234_', '1234^')

    def test_one_char_middle(self):
        self.assertCreated(0, '12!45', '12345', '12_45')
        self.assertCreated(0, '12!45', '12345', '12345', '12_45')
        self.assertCreated(0, '12!45', '12345', '12_45', '12^45')

    def test_multi_char_start(self):
        self.assertCreated(0, '!345', '12345', '_2345', '1_345')
        self.assertCreated(0, '!345', '12345', '1_345', '_2345')
        self.assertCreated(0, '!45', '12345', '_2345', '1_345', '12_45')
        self.assertCreated(0, '!5', '12345', '_2345', '1_345', '12_45', '123_5')

    def test_multi_char_end(self):
        self.assertCreated(0, '1234!', '12345', '1234_')
        self.assertCreated(0, '123!', '12345', '1234_', '123_5')
        self.assertCreated(0, '12!', '12345', '1234_', '123_5', '12_45')
        self.assertCreated(0, '1!', '12345', '1234_', '123_5', '12_45', '1_345')

    def test_empty(self):
        self.assertCreated(0, '', '', '')

    def test_no_similarities(self):
        self.assertCreated(0, '!', 'a', 'b')
        self.assertCreated(0, '!', 'ab', 'ba', 'ac', 'bc')
        self.assertCreated(0, '!', 'abc', 'ab_', 'a_c', '_bc')

    def test_left_weight(self):
        self.assertCreated(0, '!a!', 'ab', 'ba') # NOT '!b!'
        self.assertCreated(0, 'a!b!', 'abc', 'acb')

    def test_multihole(self):
        self.assertCreated(0, '!2!', '123', '_23', '12_')
        self.assertCreated(0, '!2!4!', '12345', '_2_4_')
        self.assertCreated(0, '!2!4!', '12345', '_2345', '12_45', '1234_')
        self.assertCreated(0, '!2!456!8', '12345678', '_2_456_8')
        self.assertCreated(0, '!2!456!8', '12345678', '_2345678', '12_45678', '123456_8')
        self.assertCreated(0, '!e! there', 'hello there', 'goodbye there')

    def test_marker_char(self):
        "The marker character (\x1f) is deleted from all input."
        self.assertCreated(0, '<title>!</title>', '<title>\x1f1234</title>', '<title>5678\x1f</title>')

class CreationWithTolerance(TemplatemakerTestCase):
    def test_tolerance(self):
        self.assertCreated(1, '<title>!</title>', '<title>123</title>', '<title>a2c</title>')
        self.assertCreated(2, '<title>!</title>', '<title>123</title>', '<title>a2c</title>')
        self.assertCreated(0, '<title>!23!</title>', '<title>1234</title>', '<title>a23c</title>')
        self.assertCreated(1, '<title>!23!</title>', '<title>1234</title>', '<title>a23c</title>')
        self.assertCreated(2, '<title>!</title>', '<title>1234</title>', '<title>a23c</title>')
        self.assertCreated(3, '<title>!</title>', '<title>1234</title>', '<title>a23c</title>')
        self.assertCreated(0, 'http://s!me!.com/', 'http://suntimes.com/', 'http://someing.com/')
        self.assertCreated(1, 'http://s!me!.com/', 'http://suntimes.com/', 'http://someing.com/')
        self.assertCreated(2, 'http://s!.com/', 'http://suntimes.com/', 'http://someing.com/')
        self.assertCreated(3, 'http://s!.com/', 'http://suntimes.com/', 'http://someing.com/')
        self.assertCreated(4, 'http://s!.com/', 'http://suntimes.com/', 'http://someing.com/')

class TemplateExtractionTests(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
