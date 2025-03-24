import unittest 
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "a great paragraph", None, {"lang": "en", "style":"color:red;"} )
        node2 = HTMLNode("p", "a great paragraph", None, {"style":"color:red;", "lang": "en"} )
        self.assertEqual(node1, node2)

    def test_repr(self):
         node1 = HTMLNode("p", "a great paragraph", None, {"lang": "en", "style":"color:red;"} )
         expected = "HTMLNode(tag=p, value=a great paragraph, children=None, props={'lang': 'en', 'style': 'color:red;'})"
         result = repr(node1)
         self.assertEqual(expected, result)

    def test_eq_with_children(self):
        children1 = [HTMLNode("p", "a great paragraph", None, {"lang": "en", "style":"color:red;"})]
        children2 = [HTMLNode("p", "a great paragraph", None, {"lang": "en", "style":"color:red;"})]
        node1 = HTMLNode("div", None, children1, {"lang": "en"})
        node2 = HTMLNode("div", None, children2, {"lang": "en"})
        self.assertEqual(node1, node2)

    def test_props_to_html(self):
        node1 = HTMLNode("a", "a great link", None, {"href": "https://www.yahoo.com", "target": "_blank", "rel": "noopener noreferrer"})
        expected = ' href="https://www.yahoo.com" target="_blank" rel="noopener noreferrer"'
        result = node1.props_to_html() 
        self.assertEqual(expected, result)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "a simple paragraph")
        expected = "<p>a simple paragraph</p>"
        result = node.to_html()
        self.assertEqual(expected, result)

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link to good thing", {"href": "https://www.awesomesite.com/seeithere/101", "lang": "en", "target": "_blank"})
        expected = '<a href="https://www.awesomesite.com/seeithere/101" lang="en" target="_blank">link to good thing</a>'
        result = node.to_html()
        self.assertEqual(expected, result)
        

if __name__ == "__main__":
    unittest.main()
