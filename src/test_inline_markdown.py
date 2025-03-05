import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images
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

    def test_split_bold_block(self):
        node = TextNode("this is text with a **bold section** for your enjoyment", TextType.TEXT)
        expected = [
            TextNode("this is text with a ", TextType.TEXT),
            TextNode("bold section", TextType.BOLD),
            TextNode(" for your enjoyment", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, expected)

    def test_split_italic_block(self):
        node = TextNode("this is _italic text for italic guys_ so that you may enjoy italics", TextType.TEXT)
        expected = [
            TextNode("this is ", TextType.TEXT),
            TextNode("italic text for italic guys", TextType.ITALIC),
            TextNode(" so that you may enjoy italics", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(new_nodes, expected)

    def test_split_bold_and_italic_blocks(self):
        node = TextNode("this has **bold text for me** and also _italic text for you_ with some other words", TextType.TEXT)
        expected = [
            TextNode("this has ", TextType.TEXT),
            TextNode("bold text for me", TextType.BOLD),
            TextNode(" and also ", TextType.TEXT),
            TextNode("italic text for you", TextType.ITALIC),
            TextNode(" with some other words", TextType.TEXT)
        ]

        with_bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        with_italic_and_bold_nodes = split_nodes_delimiter(with_bold_nodes, "_", TextType.ITALIC)
        self.assertEqual(with_italic_and_bold_nodes, expected)

    def test_split_with_no_closing_delimiter(self):
        node = TextNode("this is a sentence with **bold text in it, ok?", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertTrue("no closing delimiter" in str(context.exception))

    def test_split_delimiter_at_start(self):
        node = TextNode("_this_ is a great _italic containing sentence_ to look at", TextType.TEXT)
        expected = [
            TextNode("this", TextType.ITALIC),
            TextNode(" is a great ", TextType.TEXT),
            TextNode("italic containing sentence", TextType.ITALIC),
            TextNode(" to look at", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(expected, new_nodes)

    def test_split_delimiter_multiple_bold(self):
        node = TextNode("this sentence has **this bolded section** and then also has **this other bolded section**, a good way to use bold inside of sentences", TextType.TEXT)
        expected = [
            TextNode("this sentence has ", TextType.TEXT),
            TextNode("this bolded section", TextType.BOLD),
            TextNode(" and then also has ", TextType.TEXT),
            TextNode("this other bolded section", TextType.BOLD),
            TextNode(", a good way to use bold inside of sentences", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, new_nodes)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_two_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and with another ![image2](https://i.imgur.com/gqhjfsF.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/gqhjfsF.png" )]
        result = extract_markdown_images(text)
        self.assertListEqual(result, expected)

    def test_extract_markdown_two_images_and_one_line(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and with another ![image2](https://i.imgur.com/gqhjfsF.png) and [a link](https://www.google.com/badwaytogo)" 
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/gqhjfsF.png" )]
        result = extract_markdown_images(text)
        self.assertListEqual(result, expected)

    def test_extract_markdown_images_with_content_between_groups(self):
        text = "This is text with an ![image]apples(https://i.imgur.com/zjjcJKZ.png) and with another ![image2](https://i.imgur.com/gqhjfsF.png)"
        expected = [("image2", "https://i.imgur.com/gqhjfsF.png" )]
        result = extract_markdown_images(text)
        self.assertListEqual(result, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "this is a great text with a link [to yahoo because it is good and has a great yet highly suspect name](https://www.yahoo.com), just in case you need the link"
        expected = [("to yahoo because it is good and has a great yet highly suspect name", "https://www.yahoo.com")]
        result = extract_markdown_links(text)
        self.assertListEqual(result, expected)

    def test_extract_markdown_two_links(self):
        text = "this is a great text with a link [to yahoo because it is good and has a great yet highly suspect name](https://www.yahoo.com), just in case you need the link, and [another link to nowhere](https://www.road-to-nowhere.com)"
        expected = [("to yahoo because it is good and has a great yet highly suspect name", "https://www.yahoo.com"), ("another link to nowhere", "https://www.road-to-nowhere.com")]
        result = extract_markdown_links(text)
        self.assertListEqual(result, expected)

    def test_extract_markdown_ignores_images(self):
        text = "here is more text with a proper link [to cnn](https://www.cnn.com) as well as an image of ![a cat chasing dust](https://www.cats.com/Rjc4U/craziest_cat_is_it_ok.jpg)"
        expected = [("to cnn", "https://www.cnn.com")]
        result = extract_markdown_links(text)
        self.assertListEqual(result, expected)