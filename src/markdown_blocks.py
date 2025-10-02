from enum import Enum
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
