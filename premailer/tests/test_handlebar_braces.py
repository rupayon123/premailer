import unittest

from premailer import transform


class HandlebarBracesTests(unittest.TestCase):
    def test_preserve_encoded_attribute_contents(self):
        document = (
            "<html><body><a href=\"{{ user | default: 'a & b' }}\">x</a></body></html>"
        )
        result = transform(document, preserve_handlebar_syntax=True)
        self.assertIn("href=\"{{ user | default: 'a & b' }}\"", result)

    def test_preserve_does_not_decode_other_urls(self):
        document = '<html><body><a href="https://example.com/a%20b">x</a></body></html>'
        result = transform(document, preserve_handlebar_syntax=True)
        self.assertIn('href="https://example.com/a%20b"', result)
