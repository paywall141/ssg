from split_nodes_image_and_link import split_nodes_image, split_nodes_link
from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode( text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,  "**" )
    nodes = split_nodes_delimiter(nodes,  "*" )
    nodes = split_nodes_delimiter(nodes,  "`" )
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes