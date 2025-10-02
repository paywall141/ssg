from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children