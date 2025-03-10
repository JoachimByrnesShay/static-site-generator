import re
from textnode import TextNode, TextType 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type is TextType.TEXT:
            new_nodes.append(node)
            continue

        current_nodes = []
        splitted = node.text.split(delimiter)
    
        if len(splitted) % 2 == 0:
            raise ValueError("there is no closing delimiter")
        for ix, node_text in enumerate(splitted):
            if node_text == "":
                continue
            if (ix % 2) == 0:
                current_nodes.append(TextNode(node_text, TextType.TEXT))
            else:
                current_nodes.append(TextNode(node_text, text_type))
        new_nodes.extend(current_nodes) 
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[^\].]+)\]?\((http[s]?://.+?)\)"
    result = re.findall(pattern, text)
    return result

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[^\].]+)\]?\((http[s]?://.+?)\)"
    result = re.findall(pattern, text)
    return result
    

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type is TextType.TEXT:
            new_nodes.append(node) 
            continue

        nodes_from_current_node = []
        text =node.text 
        extracted_images = extract_markdown_images(node.text)

        if not extracted_images:
            new_nodes.append(node)
            continue
        
        for image in extracted_images:
            split_on = f"![{image[0]}]({image[1]})"
            splitted = text.split(split_on)
            if splitted[0] != "":
                nodes_from_current_node.append(TextNode(splitted[0], TextType.TEXT))
            nodes_from_current_node.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = splitted[1]
        if text:
            nodes_from_current_node.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(nodes_from_current_node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type is TextType.TEXT:
            new_nodes.append(node) 
            continue

        nodes_from_current_node = []
        text = node.text 
        extracted_links = extract_markdown_links(node.text)

        if not extracted_links:
            new_nodes.append(node)
            continue
        
        for link in extracted_links:
            split_on = f"[{link[0]}]({link[1]})"
            splitted = text.split(split_on)
            if splitted[0] != "":
                nodes_from_current_node.append(TextNode(splitted[0], TextType.TEXT))
            nodes_from_current_node.append(TextNode(link[0], TextType.LINK, link[1]))
            text = splitted[1]
        if text:
            nodes_from_current_node.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(nodes_from_current_node)
       
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes





