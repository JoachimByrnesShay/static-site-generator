import re
from textnode import TextNode, TextType 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # print("text type is: ", text_type)
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
    pattern = r"[^!]\[([^\[^\].]+)\]?\((http[s]?://.+?)\)"
    result = re.findall(pattern, text)
    return result
    

text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://www.obiwan.com/bio)"
print(extract_markdown_images(text))

print(extract_markdown_links(text))


