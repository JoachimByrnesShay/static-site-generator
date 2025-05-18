import unittest 
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is _italic content_ in a paragraph

This is a paragraph with **bold text** and `a lot of code` here
This is a new line in the same paragraph

- This is a list
- with items
- and with more items here

# this is a heading
## and this is continuation of the heading block with another heading
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is _italic content_ in a paragraph",
                "This is a paragraph with **bold text** and `a lot of code` here\nThis is a new line in the same paragraph",
                "- This is a list\n- with items\n- and with more items here",
                "# this is a heading\n## and this is continuation of the heading block with another heading"
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        markdown = "# this is a heading\n### this is another heading\n##### and this is a heading"
        block_type = block_to_block_type(markdown)
        expected = BlockType.HEADING 
        self.assertEqual(block_type, expected)

    def test_not_heading_if_too_many_hash(self):
        markdown = "# this is a heading\n### this is another heading\n####### and this looks like a heading but it has too many hash symbols at start of line"
        block_type = block_to_block_type(markdown) 
        expected = BlockType.PARAGRAPH 
        self.assertEqual(block_type, expected)

    def test_not_heading_if_line_starts_space(self):
        markdown = "# this is a heading\n ### this is another heading\n### and this looks like a heading but it has too many hash symbols at start of line"
        block_type = block_to_block_type(markdown) 
        expected = BlockType.PARAGRAPH 
        self.assertEqual(block_type, expected)

    def test_ordered_list(self):
        markdown = "1. do this first thing\n2. do another thing\n3. do this third thing last"
        block_type = block_to_block_type(markdown)
        expected = BlockType.ORDERED_LIST 
        self.assertEqual(block_type, expected)

    def test_not_ordered_list_when_not_sequential(self):
        markdown = "1. do this first thing\n3. do another thing\n4. do this third thing last"
        block_type = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected)

    def test_unordered_list(self):
        markdown = "- do this first thing\n- do another thing\n- do this third thing last"
        block_type = block_to_block_type(markdown)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(block_type, expected)

    def test_quote(self):
        markdown = ">this is a great quote\n>and it has more than one line as well"
        block_type = block_to_block_type(markdown)
        expected = BlockType.QUOTE
        self.assertEqual(block_type, expected)

    def test_code(self):
        markdown = "```def this_is_code(string):\n    new_string = string + ' its a new ending'\n    print(new_string)```"
        block_type = block_to_block_type(markdown)
        expected = BlockType.CODE
        self.assertEqual(block_type, expected)