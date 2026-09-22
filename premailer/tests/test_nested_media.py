import unittest

import cssutils
from lxml import html

from premailer import transform


class NestedMediaTests(unittest.TestCase):
    def test_nested_media_rules_keep_their_conditions_and_priority(self):
        document = """<html><head><style>
        @media screen {
            .outer { color: red; }
            @media (max-width: 630px) {
                .inner { color: blue; }
                @media (orientation: landscape) {
                    .deep { color: green !important; }
                }
            }
        }
        </style></head><body><p class="inner">hello</p></body></html>"""
        result = html.fromstring(transform(document, strip_important=False))
        stylesheet = cssutils.parseString(result.find("head/style").text)
        outer = stylesheet.cssRules[0]
        self.assertEqual(outer.media.mediaText, "screen")
        nested = outer.cssRules[1]
        self.assertEqual(nested.media.mediaText, "(max-width: 630px)")
        deep = nested.cssRules[1]
        self.assertEqual(deep.media.mediaText, "(orientation: landscape)")
        for rule, color in [
            (outer.cssRules[0], "red"),
            (nested.cssRules[0], "blue"),
            (deep.cssRules[0], "green"),
        ]:
            self.assertEqual(rule.style.getPropertyValue("color"), color)
            self.assertEqual(rule.style.getPropertyPriority("color"), "important")
        self.assertIsNone(result.find("body/p").get("style"))
