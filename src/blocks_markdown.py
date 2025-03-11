
def markdown_to_blocks(markdown_string):
    blocks_with_no_empty_strings = filter(lambda str: str, markdown_string.split("\n\n"))
    return list(map(lambda string: string.strip(), blocks_with_no_empty_strings))


