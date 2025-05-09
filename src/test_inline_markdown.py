import unittest 
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is some kind of `special fancy code block` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is some kind of ", TextType.TEXT),
            TextNode("special fancy code block", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_multiple_blocks(self):
        node = TextNode("This is an __italic block__ and this is another one of those __italic things here__, ok?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" and this is another one of those ", TextType.TEXT),
            TextNode("italic things here", TextType.ITALIC),
            TextNode(", ok?", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_multiple_blocks_with_string_start(self):
        node = TextNode("**bold text** is my **favorite** kind of text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold text", TextType.BOLD),
            TextNode(" is my ", TextType.TEXT),
            TextNode("favorite", TextType.BOLD),
            TextNode(" kind of text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    
    def test_bold_multiple_blocks_with_string_end(self):
        node = TextNode("some exciting **bold text** is my **favorite**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("some exciting ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" is my ", TextType.TEXT),
            TextNode("favorite", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)


    def test_bold_and_italic_blocks(self):
        node = TextNode("Hi, this is **bold stuff here** and over here is some __spicy italic stuff__, ok?  is that fine with you?", TextType.TEXT)
        new_bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        bold_with_new_italic_nodes = split_nodes_delimiter([*new_bold_nodes], "__", TextType.ITALIC)
        expected = [
            TextNode("Hi, this is ", TextType.TEXT),
            TextNode("bold stuff here", TextType.BOLD),
            TextNode(" and over here is some ", TextType.TEXT),
            TextNode("spicy italic stuff", TextType.ITALIC),
            TextNode(", ok?  is that fine with you?", TextType.TEXT),
        ]
        self.assertEqual(bold_with_new_italic_nodes, expected)

    def test_multiple_nodes(self):
        node1 = TextNode("Hi this is **bold text block here** and it is good", TextType.TEXT)
        node2 = TextNode("Hi this is an __italic text block here__ and it is very very good", TextType.TEXT)
        new_bold_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        bold_with_new_italic_nodes = split_nodes_delimiter([*new_bold_nodes], "__", TextType.ITALIC)
        expected = [
            TextNode("Hi this is ", TextType.TEXT),
            TextNode("bold text block here", TextType.BOLD),
            TextNode(" and it is good", TextType.TEXT),
            TextNode("Hi this is an ", TextType.TEXT),
            TextNode("italic text block here", TextType.ITALIC),
            TextNode(" and it is very very good", TextType.TEXT),
        ]
        self.assertEqual(bold_with_new_italic_nodes, expected)

    def test_raise_correct_exception_with_unclosed_delimiter(self):
        node = TextNode("this is some very bad markdown attempt text with what is supposed to be **bold__, but it isn't.  Sorry.", TextType.TEXT)

        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected_message = str(context.exception)
        self.assertIn("delimiter not closed", expected_message)