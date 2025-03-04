import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType 

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT )
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(new_nodes, expected)


