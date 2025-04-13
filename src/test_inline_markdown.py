import unittest 
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is markdown text with a `code block`, ok?", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is markdown text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(", ok?", TextType.TEXT),
        ]

        self.assertEqual(actual, expected)
    
    def test_bold_and_italic(self):
        node = TextNode("This is markdown text with some **bold stuff here** and some _italic stuff here_, ok?", TextType.TEXT)
        with_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        actual_with_bold_and_italics = split_nodes_delimiter(with_bold, "_", TextType.ITALIC)
        expected = [
            TextNode("This is markdown text with some ", TextType.TEXT),
            TextNode("bold stuff here", TextType.BOLD),
            TextNode(" and some ", TextType.TEXT),
            TextNode("italic stuff here", TextType.ITALIC),
            TextNode(", ok?", TextType.TEXT),
        ]

        self.assertEqual(actual_with_bold_and_italics, expected)

    def test_bold_multiple(self):
        node = TextNode("This is markdown text with some **bolded text here** and even more **bolded text over here**, ok?", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is markdown text with some ", TextType.TEXT),
            TextNode("bolded text here", TextType.BOLD),
            TextNode(" and even more ", TextType.TEXT),
            TextNode("bolded text over here", TextType.BOLD),
            TextNode(", ok?", TextType.TEXT)
        ]

        self.assertEqual(result, expected)
