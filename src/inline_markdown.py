from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splitted = node.text.split(delimiter)
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

