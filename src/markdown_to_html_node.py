
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode, HTMLNode 
from inline_markdown import text_to_textnodes, split_nodes_delimiter
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    print(blocks)

md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

markdown_to_html_node(md)

# Split the markdown into blocks (you already have a function for this)
# Loop over each block:
# Determine the type of block (you already have a function for this)
# Based on the type of block, create a new HTMLNode with the proper data
# Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
# The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
# Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.