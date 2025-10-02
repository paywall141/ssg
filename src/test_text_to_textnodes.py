import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    
    def test_full_example_from_assignment(self):
        """Test the exact example from the assignment"""
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)
    
    def test_plain_text_only(self):
        """Test plain text with no markdown"""
        text = "Just plain text with no formatting"
        result = text_to_textnodes(text)
        expected = [TextNode("Just plain text with no formatting", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_bold_only(self):
        """Test text with only bold formatting"""
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_italic_only(self):
        """Test text with only italic formatting"""
        text = "This is *italic* text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_code_only(self):
        """Test text with only code formatting"""
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_image_only(self):
        """Test text with only an image"""
        text = "Check out this ![cool image](https://example.com/image.jpg)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("cool image", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(result, expected)
    
    def test_link_only(self):
        """Test text with only a link"""
        text = "Visit [my website](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("my website", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_formatting_types(self):
        """Test text with multiple different formatting types"""
        text = "**bold** and *italic* and `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result, expected)
    
    def test_image_and_link_together(self):
        """Test text with both images and links"""
        text = "An ![image](img.jpg) and a [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com")
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_of_same_type(self):
        """Test multiple instances of the same formatting type"""
        text = "**bold1** middle **bold2**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD)
        ]
        self.assertEqual(result, expected)
    
    def test_consecutive_formatting(self):
        """Test consecutive formatting with no space between"""
        text = "**bold***italic*`code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result, expected)

