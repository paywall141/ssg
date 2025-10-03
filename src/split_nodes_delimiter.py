from textnode import text_node_to_html_node, TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter):
    if len(old_nodes) == 0:
        raise ValueError("No nodes to split provided")
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)  # Keep non-TEXT nodes as-is  
        else:
            nodes.extend(split_single_node(node.text, delimiter))
    return nodes

def split_single_node(text, delimiter):
    DELIMITER_MAP = {
        "**": TextType.BOLD,
        "*" : TextType.ITALIC,
        "_" : TextType.ITALIC,
        "`" : TextType.CODE
    }
    if delimiter not in DELIMITER_MAP:
        raise ValueError(f"The chosen delimiter {delimiter} is not accepted")
    text_type = DELIMITER_MAP[delimiter]
    
    nodes = []
    current_text = text
    while delimiter in current_text:
        # find first occurance
        first_delim =  current_text.find(delimiter)
        # start search at last found + len of delimiter
        second_delim = current_text.find(delimiter, first_delim + len(delimiter))        
        # find returns -1 if not found
        if second_delim == -1:
            raise ValueError(f"No closing delimiter found for: {delimiter}")

        # split text into 3 parts
        before = current_text[:first_delim]
        between = current_text[first_delim + len(delimiter): second_delim]
        after =  current_text[second_delim + len(delimiter):]

        if before:  
            nodes.append(TextNode(before, TextType.TEXT))
        nodes.append(TextNode(between, text_type))
        current_text = after
        #loop finished
    if current_text:
        nodes.append(TextNode(current_text, TextType.TEXT))
    return nodes
