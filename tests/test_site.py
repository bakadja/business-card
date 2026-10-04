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

        links = {attrs.get("href"): attrs for attrs in self.attributes_for("a")}
        self.assertIn("https://www.kevinngongang.dev", links)
        self.assertIn("https://github.com/bakadja", links)
        self.assertIn("mailto:contact@kevinpaulidor.de", links)

        for href in ("https://www.kevinngongang.dev", "https://github.com/bakadja"):
            self.assertEqual(links[href].get("target"), "_blank")
            self.assertEqual(set(links[href].get("rel", "").split()), {"noopener", "noreferrer"})

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
        self.assertRegex(self.css, r"@media\s*\([^)]*max-width\s*:")
        self.assertEqual(self.css.count("{"), self.css.count("}"))


if __name__ == "__main__":
    unittest.main()
