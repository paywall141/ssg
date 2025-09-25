import unittest

from textnode import TextNode, TextType, text_node_to_html_node  


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("content" , TextType.BOLD)
        node2 = TextNode("content" , TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        # url defaults to None
        node1 = TextNode("content" , TextType.BOLD)
        node2 = TextNode("content" , TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_eq3(self):
        node1 = TextNode("content" , TextType.BOLD, "youtube.com")
        node2 = TextNode("content" , TextType.BOLD, "youtube.com")
        self.assertEqual(node1, node2)

    def test_neq1(self):
        # type mismatch
        node1 = TextNode("content" , TextType.ITALIC)
        node2 = TextNode("content" , TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        # content varried
        node1 = TextNode("content" , TextType.BOLD)
        node2 = TextNode("content2" , TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq3(self):
        # URL varied
        node1 = TextNode("content" , TextType.BOLD, "youtube.com")
        node2 = TextNode("content" , TextType.BOLD, "www.youtube.com")
        self.assertNotEqual(node1, node2)


    def test_text_is_string(self):
        node1 = TextNode("content" , TextType.ITALIC)
        self.assertIsInstance(node1.text,str)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, plain, https://www.boot.dev)", repr(node)
        )

# tests for text_node_to_html_node
    def test_text_type(self):
        """Test TEXT type creates LeafNode with no tag"""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})
    
    def test_bold_type(self):
        """Test BOLD type creates LeafNode with 'b' tag"""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, {})
    
    def test_italic_type(self):
        """Test ITALIC type creates LeafNode with 'i' tag"""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, {})
    
    def test_code_type(self):
        """Test CODE type creates LeafNode with 'code' tag"""
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, {})
    
    def test_link_type(self):
        """Test LINK type creates LeafNode with 'a' tag and href prop"""
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
    
    def test_image_type(self):
        """Test IMAGE type creates LeafNode with 'img' tag, empty value, and src/alt props"""
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Empty string for img tags
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.jpg",
            "alt": "Alt text"
        })
    
    def test_link_without_url_raises_error(self):
        """Test that LINK type without URL raises ValueError"""
        node = TextNode("Click here", TextType.LINK)  # No URL provided
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Link nodes must have a URL", str(context.exception))
    
    def test_image_without_url_raises_error(self):
        """Test that IMAGE type without URL raises ValueError"""
        node = TextNode("Alt text", TextType.IMAGE)  # No URL provided
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Image nodes must have a URL", str(context.exception))
    
    def test_non_textnode_raises_error(self):
        """Test that passing non-TextNode raises Exception"""
        with self.assertRaises(Exception) as context:
            text_node_to_html_node("not a text node")
        self.assertIn("Input must be a TextNode instance", str(context.exception))
    
    def test_empty_text_values(self):
        """Test that empty text values work correctly"""
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "")
    
    def test_special_characters_in_text(self):
        """Test that special characters are preserved"""
        node = TextNode("Special chars: <>&\"'", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "Special chars: <>&\"'")


if __name__ == "__main__":
    unittest.main()
