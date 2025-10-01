import unittest
from link_extractors import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractors(unittest.TestCase):
    
    def test_extract_images(self):
        """Test basic image extraction"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)
    
    def test_extract_links(self):
        """Test basic link extraction"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)
    
    def test_no_matches(self):
        """Test text with no markdown"""
        text = "This is just plain text"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])
    
    def test_mixed_content(self):
        """Test that links don't match images"""
        text = "![image](img.jpg) and [link](site.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertEqual(images, [("image", "img.jpg")])
        self.assertEqual(links, [("link", "site.com")])

