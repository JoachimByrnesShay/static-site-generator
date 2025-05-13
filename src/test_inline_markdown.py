import unittest 
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        text = "This is an image of a ![bad-haired cat](https://www.mycatwillscratchandbiteifyoutrytofixitshair.com/7aOb5z.jpg) and this is the ![guy I saw standing near cat yesterday](https://www.weheartcats.com/in-memoriam/tony-'kc'-tunason.jpeg)"
        result = extract_markdown_images(text)
        expected = [("bad-haired cat", "https://www.mycatwillscratchandbiteifyoutrytofixitshair.com/7aOb5z.jpg"), ("guy I saw standing near cat yesterday", "https://www.weheartcats.com/in-memoriam/tony-'kc'-tunason.jpeg")]
        self.assertEqual(result, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links(self):
        text = "This is a link to [where to find after-puddles](https://www.puddles.com/no-more-puddles-later) and [to rabbit skates](http://www.animalskates.com/self-rolling-for-difficult-animals/rabbits)"
        result = extract_markdown_links(text)
        expected = [("where to find after-puddles", "https://www.puddles.com/no-more-puddles-later"), ("to rabbit skates", "http://www.animalskates.com/self-rolling-for-difficult-animals/rabbits")]
        self.assertEqual(result, expected)

    def test_extract_no_links_if_image_syntax(self):
        text = "This is an image of a ![bad-haired cat](https://www.mycatwillscratchandbiteifyoutrytofixitshair.com/7aOb5z.jpg) and this is the ![guy I saw standing near cat yesterday](https://www.weheartcats.com/in-memoriam/tony-'kc'-tunason.jpeg)"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_two_links(self):
        node = TextNode(
            "This is text with a link [to a surfboard's homepage](https://www.jonnysurfboard.com/aboutme) and [to some unused articles](https://www.youllneverfindthem.com/cantusethem/articles)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to a surfboard's homepage", TextType.LINK, "https://www.jonnysurfboard.com/aboutme"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to some unused articles", TextType.LINK, "https://www.youllneverfindthem.com/cantusethem/articles"
            ),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_text_starts_with_link(self):
        node = TextNode(
            "[early link guy](https://www.firstinmarkdownstring.com/checkitout) is a good link to look at", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("early link guy", TextType.LINK, "https://www.firstinmarkdownstring.com/checkitout"),
            TextNode(" is a good link to look at", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_does_not_capture_images(self):
        node = TextNode("this is not a link but some guy thinks it is and is about to click it, always watch out for ![pic of sad guy at desk](http://www.fooledagain.com/brown-hair-blue-slacks-guy/itsreallyhim)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertListEqual(new_nodes, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_two_images(self):
        node = TextNode(
            "This is text with an ![ocelot image](https://wildandcrazylifeimages.com/Az7f0.jpeg) and a ![garage door image](http://www.partsofabuilding.com/doors/garage/fJab9q.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        
        expected = [ 
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("ocelot image", TextType.IMAGE, "https://wildandcrazylifeimages.com/Az7f0.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("garage door image", TextType.IMAGE, "http://www.partsofabuilding.com/doors/garage/fJab9q.jpg"),
        ]
        self.assertEqual(
            expected,
            new_nodes,
        )
    
    def test_text_starts_with_image(self):
        node = TextNode("![coffee bird](http://www.womanlefthercoffee.com/outsidetable/birdcome/lovesit-pigeon/5yUp9.jpg) is a picture of a crazed bird with high heart rate and nervous pacing", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("coffee bird", TextType.IMAGE, "http://www.womanlefthercoffee.com/outsidetable/birdcome/lovesit-pigeon/5yUp9.jpg"),
            TextNode(" is a picture of a crazed bird with high heart rate and nervous pacing", TextType.TEXT)
        ]
        self.assertEqual(
            expected,
            new_nodes
        )
                    
    def test_does_not_capture_links(self):
        node = TextNode("this is suposed to be an image but it really isn't, [not an image, its a link](https://dontclickonit.com/itssupposedtobeanimage/59.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected = [node]
        self.assertListEqual(new_nodes, expected)