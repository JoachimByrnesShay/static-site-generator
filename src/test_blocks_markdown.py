import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        result = markdown_to_blocks(markdown)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(expected, result)

    

    def test_markdown_to_blocks_many_newlines(self):
        markdown = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items





"""  
        result = markdown_to_blocks(markdown)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(expected, result)


class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_blocktype_basic_heading(self):
        md_block = "##### a great heading\n#### a pretty good heading\n## an ok heading\n"
        result = block_to_block_type(md_block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_blocktype_basic_code(self):
        md_block = "```var b = 500;var c = 1000; console.log(b + c);```"
        result = block_to_block_type(md_block)
        self.assertEqual(BlockType.CODE, result)

    def test_block_to_blocktype_basic_quote(self):
        md_block = "> the loud orator may not be eloquent\n> the soft one you cannot hear\n>why does the soaring bird weep for my heart\n>-- <cite>Gu Goh 1245 abrms dynasty<cite>"
        result = block_to_block_type(md_block)
        self.assertEqual(BlockType.QUOTE, result)

    def test_block_to_blocktype_basic_ulist(self):
        md_block = "- ive got to do the dishes\n- water the frog\n- dont eat something from terrarium\n- vacuum that part of the floor over there"
        result = block_to_block_type(md_block)
        self.assertEqual(BlockType.ULIST, result)


    def test_block_to_blocktype_basic_olist(self):
        md_block = "1. first item\n2. second item\n3. third item"
        result = block_to_block_type(md_block)
        self.assertEqual(BlockType.OLIST, result)

    def test_block_to_blocktype_basic_paragraph(self):
        md_block = "this is the first line of a paragraph\nand this is the second line of the same paragraph"
        result = block_to_block_type(md_block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_blocktype_not_heading(self):
        md_block = "#### this is ok\n####### but this isnt"
        result = block_to_block_type(md_block)
        self.assertNotEqual(BlockType.HEADING, result)

    def test_block_to_blocktype_not_ulist(self):
        md_block = "- its a great start to an unordered list\n- still looking good\n-this guy really messed it up right here"
        result = block_to_block_type(md_block)
        self.assertNotEqual(BlockType.ULIST, result)
        self.assertEqual(BlockType.PARAGRAPH, result)
        
    def test_block_to_blocktype_not_olist_not_sequential(self):
        md_block = "1. ok its an ordered list, right?\n2. i think so\n4. this couldnt possibly be an ordered list\n5. this really isnt an ordered list"
        result = block_to_block_type(md_block)
        self.assertNotEqual(BlockType.OLIST, result)
        self.assertEqual(BlockType.PARAGRAPH, result)
    
    def test_block_to_blocktype_not_list_formatting(self):
        md_block = "1.is it an ordered list\n2. looks sort of good\n3. but i think not"
        result = block_to_block_type(md_block)
        self.assertNotEqual(BlockType.OLIST, result)
        self.assertEqual(BlockType.PARAGRAPH, result)

if __name__ == "__main__":
    unittest.main()