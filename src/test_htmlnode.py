import unittest 
from htmlnode import HTMLNode 

class TestHTMLNode(unittest.TestCase):
   def test_props_to_html(self):
      node = HTMLNode("a", "great link", None, {"lang": "en", "src": "www.googleawho.com", "target": "_blank"})
      expected = ' lang="en" src="www.googleawho.com" target="_blank"'
      self.assertEqual(expected, node.props_to_html())