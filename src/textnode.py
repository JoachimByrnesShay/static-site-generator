from enum import Enum 
from htmlnode import LeafNode 

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text 
        self.text_type = text_type 
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url 
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    type = text_node.text_type 
    if type is TextType.TEXT:
        return LeafNode(None, text_node.text)
    if type is TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if type is TextType.BOLD:
        return LeafNode("b", text_node.text)
    if type is TextType.CODE:
        return LeafNode("code", text_node.text)
    if type is TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if type is TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
