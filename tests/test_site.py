from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        value = " ".join(data.split())
        if value:
            self.text.append(value)


class LandingPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        cls.parser = SiteParser()
        cls.parser.feed(cls.html)
        cls.page_text = " ".join(cls.parser.text)

    def attributes_for(self, tag):
        return [attrs for name, attrs in self.parser.tags if name == tag]

    def test_page_exposes_the_approved_identity_and_actions(self):
        for expected in (
            "Kevin Ngongang",
            "Software Developer",
            "Germany",
            "contact@kevinpaulidor.de",
        ):
            self.assertIn(expected, self.page_text)

        links = self.attributes_for("a")
        expected_actions = {
            "button button-primary": "https://www.kevinngongang.dev",
            "button button-secondary": "https://github.com/bakadja",
        }
        for css_class, href in expected_actions.items():
            link = next(attrs for attrs in links if attrs.get("class") == css_class and attrs.get("href") == href)
            self.assertEqual(link.get("target"), "_blank")
            self.assertEqual(set(link.get("rel", "").split()), {"noopener", "noreferrer"})

        contact = next(attrs for attrs in links if attrs.get("href") == "mailto:contact@kevinpaulidor.de" and attrs.get("class") == "button button-secondary")
        self.assertIsNotNone(contact)

    def test_document_has_accessible_semantics_and_images(self):
        html_attrs = self.attributes_for("html")
        self.assertEqual(html_attrs[0].get("lang"), "en")
        self.assertTrue(self.attributes_for("main"))
        self.assertTrue(self.attributes_for("h1"))

        images = self.attributes_for("img")
        self.assertGreaterEqual(len(images), 2)
        for image in images:
            self.assertTrue(image.get("alt"))
            self.assertTrue(image.get("width"))
            self.assertTrue(image.get("height"))

    def test_all_runtime_assets_are_local_and_present(self):
        self.assertFalse(self.attributes_for("script"))

        asset_refs = []
        for tag, attrs in self.parser.tags:
            if tag in {"img", "script"} and attrs.get("src"):
                asset_refs.append(attrs["src"])
            if tag == "link" and attrs.get("href"):
                asset_refs.append(attrs["href"])

        self.assertTrue(asset_refs)
        for ref in asset_refs:
            self.assertFalse(ref.startswith(("http://", "https://", "//")), ref)
            self.assertTrue((ROOT / ref).is_file(), ref)

    def test_qr_code_is_a_self_contained_svg_asset(self):
        qr_path = ROOT / "images" / "qrcode.svg"
        self.assertTrue(qr_path.is_file())
        svg = qr_path.read_text(encoding="utf-8")
        root = ET.fromstring(svg)
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("viewBox", root.attrib)
        self.assertNotRegex(svg, r"(?:href|src)=[\"']https?://")

    def test_styles_support_keyboard_focus_and_small_screens(self):
        self.assertRegex(self.css, r":focus-visible\s*\{")
        breakpoint = re.search(r"@media\s*\(max-width:\s*(\d+)px\)", self.css)
        self.assertIsNotNone(breakpoint)
        self.assertGreaterEqual(int(breakpoint.group(1)), 900)
        self.assertEqual(self.css.count("{"), self.css.count("}"))


if __name__ == "__main__":
    unittest.main()
