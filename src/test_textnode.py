import unittest 
from textnode import TextType, TextNode 

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


if __name__ == "__main__":
    unittest.main() 
