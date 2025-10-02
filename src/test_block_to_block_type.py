import unittest
from markdown_blocks import block_to_block_type, BlockType  

class TestBlockToBlockType(unittest.TestCase):
    
    # HEADING TESTS
    def test_heading_single_hash(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_double_hash(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_six_hashes(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_seven_hashes_not_heading(self):
        block = "####### Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_no_space_not_heading(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_with_long_text(self):
        block = "### This is a longer heading with multiple words"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_empty_after_space(self):
        block = "# "
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # CODE BLOCK TESTS
    def test_code_block_simple(self):
        block = "```code here```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_multiline(self):
        block = "```\nprint('hello')\nprint('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_only_backticks(self):
        block = "``````"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_starts_only_not_code(self):
        block = "```code here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block_ends_only_not_code(self):
        block = "code here```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    # QUOTE BLOCK TESTS
    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_multiple_lines(self):
        block = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_missing_arrow_on_second_line(self):
        block = "> Line 1\nLine 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote_first_line_only(self):
        block = "> Line 1\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    # UNORDERED LIST TESTS
    def test_unordered_list_single_item(self):
        block = "- Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_missing_dash_on_second_line(self):
        block = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_no_space_after_dash(self):
        block = "-NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    # ORDERED LIST TESTS
    def test_ordered_list_single_item(self):
        block = "1. Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_items(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_five_items(self):
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_wrong_starting_number(self):
        block = "2. Item 1\n3. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_skipped_number(self):
        block = "1. Item 1\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_wrong_order(self):
        block = "1. Item 1\n2. Item 2\n4. Item 4"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_no_space_after_period(self):
        block = "1.NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    # PARAGRAPH TESTS
    def test_paragraph_simple(self):
        block = "This is just a regular paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nthat don't match any pattern"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_empty_string(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_with_special_chars(self):
        block = "This has # and > and - but not at the start"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

