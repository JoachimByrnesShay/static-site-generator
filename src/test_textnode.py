import unittest 
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import LeafNode 
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("an italic text node", TextType.ITALIC)
        node2 = TextNode("an italic text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("an italic text node", TextType.ITALIC)
        node2 = TextNode("a bold text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_with_one_url(self):
        node = TextNode("a great link", TextType.LINK, "https://www.yahoo.com")
        node2 = TextNode("a great link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_with_urls(self):
        node = TextNode("a great link", TextType.LINK, "https://www.yahoo.com")
        node2 = TextNode("a great link", TextType.LINK, "https://www.yahoo.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("a great link", TextType.LINK, "https://www.yahoo.com")
        expected = "TextNode(a great link, link, https://www.yahoo.com)"
        result = repr(node)
        self.assertEqual(expected, result)

class TestTextNodeToHTML(unittest.TestCase):
    def test_text_node_to_bold_element(self):
        node = TextNode("do it now", TextType.BOLD)
        result = text_node_to_html_node(node)
        expected = LeafNode("b", "do it now")
        self.assertEqual(result, expected)

    def test_text_node_to_raw_text(self):
        node = TextNode("raw text", TextType.TEXT)
        result = text_node_to_html_node(node)
        expected = LeafNode(None, "raw text")
        self.assertEqual(result, expected)

    def test_text_node_to_image(self):
        node = TextNode("a fish", TextType.IMAGE, "https://www.fishpics.com/lakefish/fI4LZx.jpg")
        result = text_node_to_html_node(node)
        expected = LeafNode("img", None, {"src": "https://www.fishpics.com/lakefish/fI4LZx.jpg", "alt": "a fish"})
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main() 
