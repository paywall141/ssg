import unittest
from textnode import TextType, TextNode
from split_nodes_delimiter import split_nodes_delimiter, split_single_node

class TestSplitSingleNode(unittest.TestCase):
    
    def test_single_code_delimiter(self):
        """Test splitting text with one code block"""
        result = split_single_node("This is text with a `code block` word", "`")
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_single_bold_delimiter(self):
        """Test splitting text with one bold section"""
        result = split_single_node("This is **bold** text", "**")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_single_italic_delimiter(self):
        """Test splitting text with one italic section"""
        result = split_single_node("This is *italic* text", "*")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_code_delimiters(self):
        """Test splitting text with multiple code blocks"""
        result = split_single_node("Here is `code1` and `code2` blocks", "`")
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_delimiter_at_start(self):
        """Test when delimiter appears at the beginning"""
        result = split_single_node("**bold** at start", "**")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_delimiter_at_end(self):
        """Test when delimiter appears at the end"""
        result = split_single_node("Text ending with **bold**", "**")
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
    
    def test_only_delimited_content(self):
        """Test when entire text is delimited"""
        result = split_single_node("**just bold**", "**")
        expected = [
            TextNode("just bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
    
    def test_empty_delimited_content(self):
        """Test empty content between delimiters"""
        result = split_single_node("Empty `` code", "`")
        expected = [
            TextNode("Empty ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_no_delimiters(self):
        """Test text with no delimiters"""
        result = split_single_node("Plain text with no formatting", "**")
        expected = [
            TextNode("Plain text with no formatting", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_consecutive_delimiters(self):
        """Test consecutive delimiter pairs"""
        result = split_single_node("**bold1****bold2**", "**")
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode("bold2", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
    
    def test_invalid_delimiter(self):
        """Test unsupported delimiter raises error"""
        with self.assertRaises(ValueError) as context:
            split_single_node("Some text", "~~")
        self.assertIn("not accepted", str(context.exception))
    
    def test_unclosed_delimiter(self):
        """Test unclosed delimiter raises error"""
        with self.assertRaises(ValueError) as context:
            split_single_node("This has `unclosed code", "`")
        self.assertIn("No closing delimiter", str(context.exception))
    
    def test_empty_string(self):
        """Test empty string input"""
        result = split_single_node("", "**")
        expected = []
        self.assertEqual(result, expected)

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_single_node_with_code(self):
        """Test splitting a single node with code delimiter"""
        nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`")
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_text_nodes(self):
        """Test splitting multiple text nodes"""
        nodes = [
            TextNode("First **bold** text", TextType.TEXT),
            TextNode("Second **bold** text", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**")
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_mixed_node_types(self):
        """Test that non-TEXT nodes are preserved"""
        nodes = [
            TextNode("Regular text with **bold**", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More text with **bold**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**")
        expected = [
            TextNode("Regular text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
    
    def test_nodes_without_delimiters(self):
        """Test nodes that don't contain the delimiter"""
        nodes = [
            TextNode("Plain text", TextType.TEXT),
            TextNode("More plain text", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**")
        expected = [
            TextNode("Plain text", TextType.TEXT),
            TextNode("More plain text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_empty_nodes_list(self):
        """Test empty nodes list raises error"""
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([], "**")
        self.assertIn("No nodes to split provided", str(context.exception))
    
    def test_all_non_text_nodes(self):
        """Test list with no TEXT type nodes"""
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Code text", TextType.CODE),
        ]
        result = split_nodes_delimiter(nodes, "**")
        expected = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Code text", TextType.CODE),
        ]
        self.assertEqual(result, expected)


class TestEdgeCases(unittest.TestCase):
    
    def test_delimiter_overlap_bold_italic(self):
        """Test potential conflicts between * and ** delimiters"""
        # This should find ** first, not individual *
        result = split_single_node("This is **bold** text", "**")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        
        # This should find * for italic
        result = split_single_node("This is *italic* text", "*")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_special_characters_in_content(self):
        """Test delimited content with special characters"""
        result = split_single_node("Code: `print('hello!')` here", "`")
        expected = [
            TextNode("Code: ", TextType.TEXT),
            TextNode("print('hello!')", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_whitespace_handling(self):
        """Test handling of whitespace in delimited content"""
        result = split_single_node("Text with `  spaced code  ` here", "`")
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("  spaced code  ", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_mixed_delimiters_unclosed_bold(self):
        """Test what happens with ** delimiter but only single * closing"""
        # This should fail because it looks for ** to close, not finding it
        with self.assertRaises(ValueError):
            split_single_node("This is **bold* text", "**")

    def test_mixed_delimiters_unclosed_italic(self):
        """Test what happens with * delimiter but ** in the middle"""  
        # could be duplicate too lazy to check
        result = split_single_node("This is *italic **still italic* text", "*")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic ", TextType.ITALIC), 
            TextNode("still italic", TextType.ITALIC), 
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_overlapping_delimiters(self):
        """Test overlapping ** and * delimiters"""
        # this...well just leave this alone lol
        with self.assertRaises(ValueError):
            split_single_node("*bold **and italic**", "*")