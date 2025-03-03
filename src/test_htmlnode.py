import unittest 
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
   def test_props_to_html(self):
      node = HTMLNode("a", "great link", None, {"lang": "en", "href": "www.googleawho.com", "target": "_blank"})
      expected = ' lang="en" href="www.googleawho.com" target="_blank"'
      self.assertEqual(expected, node.props_to_html())

   def test_repr(self):
      children = [HTMLNode("a", "great link", None, {"href": "www.yahoo.com"})]
      node = HTMLNode("p", "awesome paragraph", children, None)
      expected = f'HTMLNode(p, awesome paragraph, {children}, None)'
      self.assertEqual(expected, repr(node))

   def test_child_repr(self):
      node = HTMLNode("div", None, [HTMLNode("p", "really great", None, None)], None)
      expected = f'HTMLNode(p, really great, None, None)'
      self.assertEqual(repr(node.children[0]), expected)

   def test_props_none_to_html(self):
      node = HTMLNode("p", "great paragraph", None, None)
      expected = ""
      self.assertEqual(expected, node.props_to_html())

class TestLeafNode(unittest.TestCase):
   def test_leaf_to_html_p(self):
      node = LeafNode("p", "Hello, world!")
      self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

   def test_leaf_to_html_no_tag(self):
      node = LeafNode(None, "hi world")
      self.assertEqual(node.to_html(), "hi world")

   def test_leaf_to_html_a(self):
      node = LeafNode("a", "link to stuff", {"href":"https://www.greatlink.com"})
      expected = '<a href="https://www.greatlink.com">link to stuff</a>'
      self.assertEqual(node.to_html(), expected)

   def test_leaf_to_html_no_value_with_exception(self):
      node = LeafNode("div", None)
      with self.assertRaises(Exception) as context:
         node.to_html()
      self.assertTrue("leaf node requires value" in str(context.exception))

class TestParentNode(unittest.TestCase):
   def test_parent_node_to_html(self):
      children = [
         LeafNode("b", "Bold text"),
         LeafNode(None, "Normal text"),
         LeafNode("i", "italic text"),
         LeafNode(None, "Normal text")
      ]
      node = ParentNode("p", children)
      expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
      self.assertEqual(expected, node.to_html())


   def test_parent_node_to_html_nested_child(self):
      child_with_children = ParentNode("div", [LeafNode("a", "a link", {"href": "https://www.linkadoo.net"})])
      children = [
         LeafNode("p", "great stuff"),
         ParentNode("div", [LeafNode("p", "first p in a div"), LeafNode("p", "second p in a div"), child_with_children]),
      ]
      node = ParentNode("div", children)
      expected = '<div><p>great stuff</p><div><p>first p in a div</p><p>second p in a div</p><div><a href="https://www.linkadoo.net">a link</a></div></div></div>'
      self.assertEqual(expected, node.to_html())

   def test_parent_node_repr(self):
      self.maxDiff = None
      child_with_children = ParentNode("div", [LeafNode("a", "a link", {"href": "https://www.linkadoo.net"})])
      children = [
         LeafNode("p", "great stuff"),
         ParentNode("div", [LeafNode("p", "first p in a div"), LeafNode("p", "second p in a div"), child_with_children]),
      ]
      node = ParentNode("div", children)

      expected_repr_inner_child_with_child = "ParentNode(div, [LeafNode(a, a link, {'href': 'https://www.linkadoo.net'})], None)"
      expected_repr_outer_child_with_child = f"ParentNode(div, [LeafNode(p, first p in a div, None), LeafNode(p, second p in a div, None), {expected_repr_inner_child_with_child}], None)"
      expected = f"ParentNode(div, [LeafNode(p, great stuff, None), {expected_repr_outer_child_with_child}], None)"
   
      self.assertEqual(repr(node), expected)

   def test_parent_node_to_html_no_tag(self):
      node = ParentNode(None, [LeafNode("p", "hi i'm a leaf")])
      with self.assertRaises(Exception) as context:
         node.to_html() 
      self.assertTrue("parent node requires tag" in str(context.exception))

   def test_parent_node_to_html_no_children(self):
      node = ParentNode("div", None)
      with self.assertRaises(Exception) as context:
         node.to_html() 
      self.assertTrue("parent node requires children" in str(context.exception))

if __name__ == "__main__":
   unittest.main()