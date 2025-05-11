from textnode import TextType, TextNode
import re 

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


def extract_markdown_images(text):
    pattern = r"!\[(.+?)\]\((https?://.+?)\)"
    images = re.findall(pattern, text)
    return images 

    #"![obi wan](https://i.imgur.com/fJRm4Vk.jpeg"

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.+?)\]\((https?://.+?)\)"
    links = re.findall(pattern, text)
    return links 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue 
        pattern = r"(?<!!)\[.+?\]\(https?://.+?\)"
                  #r"(?<!!)\[(.+?)\]\((https?://.+?)\)"
        splitted = re.split(pattern, node.text)
        links = extract_markdown_links(node.text)
        for ix in range(len(splitted)):
            text_nodes = []
            text = splitted[ix]
            if text != "":
                text_nodes.append(TextNode(text, TextType.TEXT))
            if ix < len(links):
                link_text, link_url = links[ix]
                text_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            new_nodes.extend(text_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        pattern = r"!\[.+?\]\(https?://.+?\)"
        splitted = re.split(pattern, node.text)
        images = extract_markdown_images(node.text)
        for ix in range(len(splitted)):
            text_nodes = []
            text = splitted[ix] 
            if text != "":
                text_nodes.append(TextNode(text, TextType.TEXT))
            if ix < len(images):
                alt_text, url = images[ix]
                text_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            new_nodes.extend(text_nodes)
    return new_nodes

