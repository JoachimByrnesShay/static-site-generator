import unittest 
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image

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

    def test_code_start_of_string(self):
        node = TextNode("`This is code at start of text` and the rest of this stuff isn't", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is code at start of text", TextType.CODE),
            TextNode(" and the rest of this stuff isn't", TextType.TEXT)
        ]

        self.assertListEqual(expected, result)

    def test_italic_end_of_string(self):
        node = TextNode("So far we have only regular text but in a second we have _way too much italic text_", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("So far we have only regular text but in a second we have ", TextType.TEXT),
            TextNode("way too much italic text", TextType.ITALIC),
        ]

        self.assertListEqual(expected, result)

    def test_raise_exception_with_unclosed_delimiter(self):
        node = TextNode("I don't like this text because the **bold delimiter is not closed, you see?", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_exception = str(context.exception)

        self.assertIn("invalid markdown, delimiter is not closed", expected_exception)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_one_image(self):
        text = "This is markdown text with an image of a ![bad type of fish](https://www.lookoutforthisfish.com/fishes/gX4zq.jpeg)"
        result = extract_markdown_images(text)
        expected = [("bad type of fish", "https://www.lookoutforthisfish.com/fishes/gX4zq.jpeg")]
        
        self.assertListEqual(result, expected)

    def test_multiple_image(self):
        text = "More text with image of ![wrongway fellow](https://www.guywhoisalwaysgoingthewrongway.com/nogood.jpg) and image of ![water in showercap](http://www.ifthirstyhaveadrink.com/delicious.jpeg), and that's all"
        result = extract_markdown_images(text)
        expected = [("wrongway fellow", "https://www.guywhoisalwaysgoingthewrongway.com/nogood.jpg"), ("water in showercap", "http://www.ifthirstyhaveadrink.com/delicious.jpeg")]

        self.assertListEqual(result, expected)

    def test_no_image_if_its_a_link(self):
        text = "This is markdown text with a link to a [fish](https://www.igoheretogetmyspecialfish.com/randomfish)"
        result = extract_markdown_images(text)
        expected = []

        self.assertListEqual(result, expected)

    def test_text_starts_with_image(self):
        text = "![Ms. Ladi Walindera](http://www.suspectmanager.com/ladindera_p_walindera_posing_with_rooibos_tea_at_desk.jpg) is what you should be looking at and thinking about before you say anything else"
        result = extract_markdown_images(text)
        expected = [("Ms. Ladi Walindera", "http://www.suspectmanager.com/ladindera_p_walindera_posing_with_rooibos_tea_at_desk.jpg")]

        self.assertListEqual(result, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_one_link(self):
        text = "This is markdown text with a link to a [fish](https://www.igoheretogetmyspecialfish.com/randomfish)"
        result = extract_markdown_links(text)
        expected = [("fish", "https://www.igoheretogetmyspecialfish.com/randomfish")]

        self.assertListEqual(result, expected)

    def test_multiple_links(self):
        text = "Link here to a [bad guy's webpage](https://www.awefulguy.com) and to a [mango](http://www.eatmorefruitthatnotanapple.com/howaboutmango)"
        result = extract_markdown_links(text)
        expected = [("bad guy's webpage", "https://www.awefulguy.com"), ("mango", "http://www.eatmorefruitthatnotanapple.com/howaboutmango")]

        self.assertListEqual(result, expected)


    def test_no_link_if_its_an_image(self):
        text = "Link here to ![bad guy's mango](https://www.notreallymineistoleit.com/kidsmango), ok?"
        result = extract_markdown_links(text)
        expected = []

        self.assertListEqual(result, expected)

    def test_text_starts_with_link(self):
        text = "[water](https://www.maybedisappointing.com/itsjustwater), ok?  I wanted you to check it out anyway."
        result = extract_markdown_links(text)
        expected = [("water", "https://www.maybedisappointing.com/itsjustwater")]

        self.assertListEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", 
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]

        self.assertListEqual(result, expected)

    def test_split_two_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), ok?",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(", ok?", TextType.TEXT)
            ],
            new_nodes,
        )
    def test_split_three_image_and_adjacent(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)![third image](https://i.imgur.com/4elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/4elNhQu.png"
                ),
            ],
            new_nodes,
        )
