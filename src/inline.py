from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        splitted = node.text.split(delimiter)
        # "This is text with a `code block` word"
        # "`code block` word"
        # " `code block` word"
        # "a `code block word"
        # "`code block`"
        # " `code block` word ` bad stuff"
        if len(splitted) % 2 == 0:
            raise ValueError("invalid markdown, delimiter is not closed")
        
        current_nodes = []
        for (ix,text) in enumerate(splitted):
            if text == "":
                continue 
            if ix % 2 == 0:
                current_nodes.append(TextNode(text, TextType.TEXT))
            else:
                current_nodes.append(TextNode(text, text_type))
        new_nodes.extend(current_nodes)
    return new_nodes


node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
print(new_nodes)
expected = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
print(expected == new_nodes)