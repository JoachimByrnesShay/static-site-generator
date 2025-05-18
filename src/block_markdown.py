from enum import Enum 
import re

def markdown_to_blocks(markdown):
    blocks = list(filter(lambda x: x, map(lambda x: x.strip(), markdown.split("\n\n"))))
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE 
    if markdown_block.startswith(">"):
        quote = True 
        for line in lines:
            if not line.startswith(">"):
                quote = False 
                break 
        if quote:
            return BlockType.QUOTE 
    if markdown_block.startswith("- "):
        unordered_list = True 
        for line in lines:
            if not line.startswith("- "):
                unordered_list = False 
                break 
        if unordered_list:
            return BlockType.UNORDERED_LIST 
    if markdown_block.startswith("#"):
        heading = True 
        for line in lines:
            if not re.match(r"#{1,6} .", line):
                heading = False 
                break 
        if heading:
            return BlockType.HEADING 
    if markdown_block.startswith("1"):
        ordered_list = True 
        for num in range(1, len(lines) + 1):
            line = lines[num-1]
            if not line.startswith(str(num) + ". "):
                ordered_list = False 
                break 
        if ordered_list:
            return BlockType.ORDERED_LIST 
    return BlockType.PARAGRAPH
    



# Create a block_to_block_type function that takes a single block of markdown text as input and returns the BlockType representing the type of block it is. You can assume all leading and trailing whitespace were already stripped (we did that in a previous lesson).
# Headings start with 1-6 # characters, followed by a space and then the heading text.
# Code blocks must start with 3 backticks and end with 3 backticks.
# Every line in a quote block must start with a > character.
# Every line in an unordered list block must start with a - character, followed by a space.
# Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
# If none of the above conditions are met, the block is a normal paragraph.