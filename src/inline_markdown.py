from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise ValueError("delimiter not closed")
        text_nodes = []
        for ix in range(len(splitted)):
            if splitted[ix] == "":
                continue 
            if ix % 2 == 0:
                text_nodes.append(TextNode(splitted[ix], TextType.TEXT))
            else:
                text_nodes.append(TextNode(splitted[ix], text_type))
        new_nodes.extend(text_nodes)
    return new_nodes 
