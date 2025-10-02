from enum import Enum
from split_nodes_image_and_link import split_nodes_image, split_nodes_link
from split_nodes_delimiter import split_nodes_delimiter
from htmlnode import ParentNode, LeafNode
from text_to_children import text_to_children
import re

def markdown_to_blocks(markdown):
    stripped_blocks = [block.strip() for block in markdown.split("\n\n")]
    return [block for block in stripped_blocks if block]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    # takes one stripped markdown block
def block_to_block_type(markdown_block:str):
    if re.match(r"^#{1,6} .+", markdown_block):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif markdown_block.startswith(">"):
        lines = markdown_block.split("\n")
        if all( line.startswith(">") for line in lines if line ): 
            return BlockType.QUOTE
    elif markdown_block.startswith("- "):
        lines = markdown_block.split("\n")
        if all( line.startswith("- ") for line in lines if line ): 
            return BlockType.UNORDERED_LIST
    elif markdown_block.startswith("1. "):
        lines = markdown_block.split("\n")
        current = 1
        for line in lines:
            if not line.startswith(f"{current}. "):
                break
            current += 1
        else:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    # strip and seperate
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []

    for block in blocks:
        # start by finding block type
        block_type = block_to_block_type(block)

        # create tag based on block_type
        match block_type:
            case BlockType.HEADING:
                start_idx = block.find(" ")
                tag = f"h{start_idx}"
                trimmed_txt = block[start_idx+1:]
                children = text_to_children(trimmed_txt)
                parent = ParentNode(tag, children)
                htmlnodes.append(parent)   

            case BlockType.PARAGRAPH:
                tag = "p"
                children = text_to_children(block)
                parent = ParentNode(tag, children)
                htmlnodes.append(parent)   
            
            case BlockType.QUOTE:
                tag = "blockquote"
                lines = block.split("\n")
                trimmed_lines = [ line[1:].strip() for line in lines ]
                trimmed_txt = "\n".join(trimmed_lines)
                children = text_to_children(trimmed_txt)
                parent = ParentNode(tag, children)
                htmlnodes.append(parent)   

            case BlockType.UNORDERED_LIST:
                tag = "ul"
                lines = block.split("\n")
                trimmed_lines = [line[2:].strip() for line in lines]
                children = []
                for line in trimmed_lines:
                    li_node = ParentNode( "li", text_to_children(line) )
                    children.append(li_node)
                parent = ParentNode( tag, children)
                htmlnodes.append(parent)   

            case BlockType.ORDERED_LIST:
                tag = "ol"
                lines = block.split("\n")
                trimmed_lines = []
                for line in lines:
                    space_idx = line.find(" ")
                    trimmed_lines.append(line[space_idx + 1:])

                children = []
                for line in trimmed_lines:
                    li_node = ParentNode( "li", text_to_children(line) )
                    children.append(li_node)
                parent = ParentNode( tag, children)
                htmlnodes.append(parent)  

            case BlockType.CODE:
                tag = "code"           
                stripped_txt = block.strip("```")
                leaf = LeafNode( tag, stripped_txt)
                grandparent = ParentNode("pre", [leaf])
                htmlnodes.append(grandparent)
            
            case _:
                raise ValueError(f"Unsupported block type: {block_type}")
                # tag = "p"
                # children = text_to_children(block)
                # parent = ParentNode(tag, children)
                # htmlnodes.append(parent)   

    return ParentNode("div", htmlnodes)