from textnode import text_node_to_html_node, TextNode, TextType
from link_extractors import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes):
    if len(old_nodes) == 0:
        raise ValueError("No nodes to split provided")
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)  # Keep non-TEXT nodes as-is  
        else:
            nodes.extend(split_single_image(node.text))
    return nodes

def split_single_image(text):
    current_text = text
    images = extract_markdown_images(current_text)
    nodes = []
    if not images:
        return [TextNode(current_text, TextType.TEXT)]

    for img_alt, img_url in images:
        image_markdown = f"![{img_alt}]({img_url})"
        sections = current_text.split(image_markdown, 1)

        before =  sections[0]
        after = sections[1]
        if before:
            nodes.append( TextNode( before, TextType.TEXT) )
        nodes.append( TextNode( img_alt, TextType.IMAGE, img_url) )
        current_text = after
    if current_text:
        nodes.append( TextNode( current_text, TextType.TEXT) )
    return nodes


def split_nodes_link(old_nodes):
    if len(old_nodes) == 0:
        raise ValueError("No nodes to split provided")
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            nodes.extend(split_single_link(node.text))
    return nodes

def split_single_link(text):
    current_text = text
    nodes = []
    links = extract_markdown_links(current_text)
    if not links:
        return [TextNode(current_text, TextType.TEXT)]
    
    for link_alt, link_url in links:
        link_markdown = f"[{link_alt}]({link_url})"
        sections = current_text.split(link_markdown, 1)
        before = sections[0]
        after = sections[1]
        if before:
            nodes.append( TextNode ( before, TextType.TEXT))
        nodes.append( TextNode( link_alt, TextType.LINK, link_url))
        current_text = after
    if current_text:
        nodes.append( TextNode( current_text, TextType.TEXT) )
    return nodes
