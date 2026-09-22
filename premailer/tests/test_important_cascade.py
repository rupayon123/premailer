import unittest

import cssutils
from lxml import html

from premailer import transform


class ImportantCascadeTests(unittest.TestCase):
    def test_inline_precedence_respects_importance(self):
        for strip in (False, True):
            for stylesheet, inline, expected, important in [
                ("red !important", "blue", "red", True),
                ("red", "blue", "blue", False),
                ("red !important", "blue !important", "blue", True),
                ("red", "blue !important", "blue", True),
            ]:
                with self.subTest(strip=strip, stylesheet=stylesheet, inline=inline):
                    document = (
                        "<html><head><style>p {color:%s}</style></head>"
                        '<body><p style="color:%s">hello</p></body></html>'
                    ) % (stylesheet, inline)
                    result = html.fromstring(transform(document, strip_important=strip))
                    style = cssutils.parseStyle(result.find("body/p").get("style"))
                    self.assertEqual(style.getPropertyValue("color"), expected)
                    self.assertEqual(
                        style.getPropertyPriority("color"),
                        "important" if important and not strip else "",
                    )

    def test_literal_important_text_is_not_stripped(self):
        document = """<html><head><style>p {font-family: ' !important';}</style></head>
        <body><p>hello</p></body></html>"""
        result = html.fromstring(transform(document))
        style = cssutils.parseStyle(result.find("body/p").get("style"))
        self.assertEqual(style.getPropertyValue("font-family"), '" !important"')

    def test_important_unset_can_still_be_removed(self):
        document = """<html><head><style>p {color: unset !important;}</style></head>
        <body><p>hello</p></body></html>"""
        result = html.fromstring(transform(document, remove_unset_properties=True))
        self.assertIsNone(result.find("body/p").get("style"))
