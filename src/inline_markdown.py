from textnode import TextNode, TextType 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        current_nodes = []
        splitted = node.text.split(delimiter)
        for ix, node_text in enumerate(splitted):
            if (ix % 2) == 0:
                current_nodes.append(TextNode(node_text, TextType.TEXT))
            else:
                current_nodes.append(TextNode(node_text, text_type))
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