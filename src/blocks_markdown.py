from enum import Enum
import re


def markdown_to_blocks(markdown_string):
    blocks_with_no_empty_strings = filter(lambda str: str, markdown_string.split("\n\n"))
    return list(map(lambda string: string.strip(), blocks_with_no_empty_strings))

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


class Block():
    def __init__(self, block_text):
        self.block_text = block_text 

    def is_heading(self):
        splitted = self.block_text.splitlines() 
        for line in splitted:
            if not re.search('^#{1,6} .+', line):
                return False 
        return True

    def is_code(self):
        return self.block_text.startswith("```") and self.block_text.endswith("```")
    
    def is_quote(self):
        splitted = self.block_text.splitlines() 
        for line in splitted:
            if not line.startswith(">"):
                return False 
        return True 
    
    def is_ulist(self):
        splitted = self.block_text.splitlines() 
        for line in splitted:
            if not line.startswith("- "):
                return False 
        return True 
    
    def is_olist(self):
        splitted = self.block_text.splitlines()
        for ix in range(0, len(splitted)):
            line = splitted[ix]
            if not line.startswith(f"{ix+1}. "):
                return False 
        return True 
    
    

def block_to_block_type(md_block):
    block = Block(md_block)
    
    if block.is_heading():
        return BlockType.HEADING
    elif block.is_code():
        return BlockType.CODE
    elif block.is_quote():
        return BlockType.QUOTE
    elif block.is_ulist():
        return BlockType.ULIST 
    elif block.is_olist():
        return BlockType.OLIST 
    else:
        return BlockType.PARAGRAPH



