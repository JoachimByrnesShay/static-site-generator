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
    for i, node in enumerate(old_nodes):
        if not node.text_type is TextType.TEXT:
            new_nodes.append(node) 
        nodes_from_current_node = []
        text =node.text 
        extracted_images = extract_markdown_images(node.text)

        for j in range(0,len(extracted_images)):
            split_on = f"![{extracted_images[j][0]}]({extracted_images[j][1]})"
            splitted = text.split(split_on)
            if splitted[0] != "":
                nodes_from_current_node.append(TextNode(splitted[0], TextType.TEXT))
            nodes_from_current_node.append(TextNode(extracted_images[j][0], TextType.IMAGE,extracted_images[j][1]))
            text = splitted[1]
        if text:
            nodes_from_current_node.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(nodes_from_current_node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for i, node in enumerate(old_nodes):
        if not node.text_type is TextType.TEXT:
            new_nodes.append(node) 
        nodes_from_current_node = []
        text =node.text 
        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            return new_nodes
        for j in range(0,len(extracted_links)):
            split_on = f"[{extracted_links[j][0]}]({extracted_links[j][1]})"
            splitted = text.split(split_on)
            if splitted[0] != "":
                nodes_from_current_node.append(TextNode(splitted[0], TextType.TEXT))
            nodes_from_current_node.append(TextNode(extracted_links[j][0], TextType.LINK,extracted_links[j][1]))
            text = splitted[1]
        if text:
            nodes_from_current_node.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(nodes_from_current_node)
    return new_nodes
