import unittest 
from htmlnode import HTMLNode 

class TestHTMLNode(unittest.TestCase):
   def test_props_to_html(self):
      node = HTMLNode("a", "great link", None, {"lang": "en", "src": "www.googleawho.com", "target": "_blank"})
      expected = ' lang="en" src="www.googleawho.com" target="_blank"'
      self.assertEqual(expected, node.props_to_html())

   def test_repr(self):
      children = [HTMLNode("a", "great link", None, {"src": "www.yahoo.com"})]
      node = HTMLNode("p", "awesome paragraph", children, None)
      expected = f'HTMLNode(p, awesome paragraph, {children}, None)'
      self.assertEqual(expected, repr(node))

   def test_child_repr(self):
      node = HTMLNode("div", None, [HTMLNode("p", "really great", None, None)], None)
      expected = f'HTMLNode(p, really great, None, None)'
      self.assertEqual(repr(node.children[0]), expected)