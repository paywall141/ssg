import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_basic_title(self):
        """Test basic h1 extraction"""
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_title_with_whitespace(self):
        """Test title with extra whitespace"""
        self.assertEqual(extract_title("# Hello World  "), "Hello World")
    
    def test_title_with_content_after(self):
        """Test h1 with content following it"""
        self.assertEqual(extract_title("# Title\n\nSome content here"), "Title")
    
    def test_title_not_at_beginning(self):
        """Test h1 that's not at the start of the document"""
        self.assertEqual(extract_title("Some text\n# My Title\nMore text"), "My Title")
    
    def test_multiple_headers(self):
        """Test that first h1 is returned when multiple exist"""
        self.assertEqual(extract_title("# First\n## Second\n# Third"), "First")
    
    def test_indented_title(self):
        """Test h1 with leading whitespace"""
        self.assertEqual(extract_title("  # Indented Title"), "Indented Title")
    
    def test_ignores_h2_and_h3(self):
        """Test that h2 and h3 are ignored"""
        self.assertEqual(extract_title("## Not This\n### Or This\n# This One"), "This One")
    
    def test_no_header_raises_exception(self):
        """Test exception raised when no h1 exists"""
        with self.assertRaises(Exception):
            extract_title("No header here")
    
    def test_only_h2_raises_exception(self):
        """Test exception raised when only h2/h3 exist"""
        with self.assertRaises(Exception):
            extract_title("## Only h2\n### Only h3")
    
    def test_hash_without_space_raises_exception(self):
        """Test exception raised when # has no space"""
        with self.assertRaises(Exception):
            extract_title("#NoSpace")
