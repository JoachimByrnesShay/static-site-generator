from textnode import TextType, TextNode 


def main():
    node = TextNode("a great link", TextType.LINK, "https://www.greatlink.com")
    print(node)

main()