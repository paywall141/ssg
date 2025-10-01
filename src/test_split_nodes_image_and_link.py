import unittest
from textnode import TextNode, TextType
from split_nodes_image_and_link import (
    split_nodes_image,
    split_nodes_link,
    split_single_image,
    split_single_link
)

class TestSplitNodesImage(unittest.TestCase):
    
    def test_split_single_image(self):
        """Test splitting text with one image"""
        text = "This is text with an ![image](https://example.com/image.png)"
        result = split_single_image(text)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(result, expected)
    
    def test_split_multiple_images(self):
        """Test splitting text with multiple images"""
        text = "Start ![img1](url1.jpg) middle ![img2](url2.png) end"
        result = split_single_image(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1.jpg"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.png"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_split_no_images(self):
        """Test text with no images returns plain text node"""
        text = "Just plain text with no images"
        result = split_single_image(text)
        expected = [TextNode("Just plain text with no images", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_split_nodes_image_list(self):
        """Test split_nodes_image with a list of nodes"""
        nodes = [
            TextNode("Text with ![image](url.jpg)", TextType.TEXT),
            TextNode("bold text", TextType.BOLD)
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.jpg"),
            TextNode("bold text", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):
    
    def test_split_single_link(self):
        """Test splitting text with one link"""
        text = "This is text with a [link](https://www.boot.dev)"
        result = split_single_link(text)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(result, expected)
    
    def test_split_multiple_links(self):
        """Test splitting text with multiple links - matches assignment example"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = split_single_link(text)
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(result, expected)
    
    def test_split_no_links(self):
        """Test text with no links returns plain text node"""
        text = "Just plain text with no links"
        result = split_single_link(text)
        expected = [TextNode("Just plain text with no links", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_split_nodes_link_list(self):
        """Test split_nodes_link with a list of nodes"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected)

class TestMixedContent(unittest.TestCase):
    
    def test_image_doesnt_match_as_link(self):
        """Test that images aren't picked up by link splitter"""
        text = "![image](img.jpg) and [link](site.com)"
        result = split_single_link(text)
        expected = [
            TextNode("![image](img.jpg) and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "site.com")
        ]
        self.assertEqual(result, expected)
    
    def test_preserves_non_text_nodes(self):
        """Test that non-TEXT nodes are preserved unchanged"""
        nodes = [
            TextNode("plain with [link](url.com)", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("code text", TextType.CODE)
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("plain with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode("bold text", TextType.BOLD),
            TextNode("code text", TextType.CODE)
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()