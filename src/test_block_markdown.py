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
    def test_block_to_blocktype_heading(self):
        markdown = "# this is a heading\n### this is another heading\n##### and this is a heading"
        block_type = block_to_block_type(markdown)
        expected = BlockType.HEADING 
        self.assertEqual(block_type, expected)

    def test_block_to_blocktype_not_heading_if_incorrect_syntax(self):
        markdown = "# this is a heading\n### this is another heading\n####### and this looks like a heading but it has too many hash symbols at start of line"
        block_type = block_to_block_type(markdown) 
        expected = BlockType.PARAGRAPH 
        self.assertEqual(block_type, expected)

    def test_block_to_blocktype_ordered_list(self):
        markdown = "1. do this first thing\n2. do another thing\n3. do this third thing last"
        block_type = block_to_block_type(markdown)
        expected = BlockType.ORDERED_LIST 
        self.assertEqual(block_type, expected)

    def test_block_to_blocktype_not_ordered_list_when_not_sequential(self):
        markdown = "1. do this first thing\n3. do another thing\n4. do this third thing last"
        block_type = block_to_block_type(markdown)
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected)