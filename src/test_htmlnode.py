import unittest 
from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_equal_leaf(self):
        node1 = LeafNode("a", "link to good thing", {"href": "https://www.awesomesite.com/seeithere/101", "lang": "en", "target": "_blank"})
        node2 = LeafNode("a", "link to good thing", {"href": "https://www.awesomesite.com/seeithere/101", "lang": "en", "target": "_blank"})
        self.assertEqual(node1, node2)

    def test_leaf_to_html_raise_error_with_no_value(self):
        node = LeafNode("a", value=None)
        with self.assertRaises(Exception) as context:
            node.to_html()
            
        expected = "a leaf node must have a value"
        result = str(context.exception)
        self.assertIn(expected, result)
        


class TestParentNode(unittest.TestCase):
    def test_parent_node_to_html_basic(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ],
        )

        result = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(result, expected)
        
    def test_parent_node_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span>child</span></div>"
        result = parent_node.to_html()
        self.assertEqual(result, expected)

    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span><b>grandchild</b></span></div>"
        result = parent_node.to_html()
        self.assertEqual(result, expected)

    def test_parent_node_to_html_with_grandchildren_w_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"lang": "en"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = '<div><span><b lang="en">grandchild</b></span></div>'
        result = parent_node.to_html()
        self.assertEqual(result, expected)

    def test_parent_node_to_html_raise_exception_no_tag(self):
        child_node = LeafNode("p", "paragraph")
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(Exception) as context:
            parent_node.to_html()
        expected = str(context.exception)
        self.assertIn("needs a tag", expected)

    def test_parent_node_to_html_raise_exception_no_children(self):
        parent_node = ParentNode("div", [])

        with self.assertRaises(Exception) as context:
            parent_node.to_html() 
        
        expected = str(context.exception)

        self.assertIn("parent node must have children", expected)
            

    # to do, test nexted parentnodes, text multiple sibling children, etc 

if __name__ == "__main__":
    unittest.main()
