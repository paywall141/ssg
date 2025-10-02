import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_multiple_paragraphs(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
Block 1


Block 2



Block 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block 1",
                "Block 2",
                "Block 3",
            ],
        )

    def test_markdown_to_blocks_with_whitespace(self):
        md = """
  Paragraph with leading spaces  

    Another block with spaces    
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph with leading spaces",
                "Another block with spaces",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = """
Just one block of text
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block of text"])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only_blocks(self):
        # This test catches the bug in the "solution"
        md = "Block 1\n\n   \n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])
        # Should NOT include empty string in middle

    def test_markdown_to_blocks_tabs_and_spaces(self):
        # Blocks that are only whitespace (spaces, tabs) should be removed
        md = "Block 1\n\n\t\t\n\n    \n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_mixed_whitespace(self):
        # Mix of empty and whitespace-only blocks
        md = "A\n\n\n\n  \n\n\t\n\nB"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["A", "B"])


