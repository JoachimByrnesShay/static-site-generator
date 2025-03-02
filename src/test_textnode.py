import unittest 
from textnode import TextNode, TextType 

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_with_one_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.textnodesaregreat.com")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
      
    def test_not_eq_with_diff_types(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_with_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text nodes", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_with_urls(self):
        node = TextNode("This is a text node", TextType.LINK, "https://agreatlink.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://agreatlink.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a great text node", TextType.LINK, "https://www.yahoo.com")
        expected = "TextNode(This is a great text node, TextType.LINK, https://www.yahoo.com)"
        self.assertEqual(repr(node), expected)
    

if __name__ == "__main__":
    unittest.main()
