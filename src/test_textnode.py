import unittest 
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

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
    
class TextTextNodeToHtmlNode(unittest.TestCase):

    def test_text_node_text_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_img_to_html_node(self):
        node = TextNode("image of animal", TextType.IMAGE, "https://www.animalimages.com/x4sjsI.jpg")
        html_node = text_node_to_html_node(node)
        expected = LeafNode("img", "", {"src": "https://www.animalimages.com/x4sjsI.jpg", "alt": "image of animal"})
        self.assertEqual(html_node, expected)

    def test_text_node_link_to_html_node(self):
        node = TextNode("link to animal bio", TextType.LINK, "https://www.readthisanimalsbio.com/bio")
        html_node = text_node_to_html_node(node)
        expected = LeafNode("a", "link to animal bio", {"href":"https://www.readthisanimalsbio.com/bio"})
        self.assertEqual(html_node, expected)


if __name__ == "__main__":
    unittest.main()
