import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("content" , TextType.BOLD_TEXT)
        node2 = TextNode("content" , TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        # url defaults to None
        node1 = TextNode("content" , TextType.BOLD_TEXT)
        node2 = TextNode("content" , TextType.BOLD_TEXT, None)
        self.assertEqual(node1, node2)

    def test_eq3(self):
        node1 = TextNode("content" , TextType.BOLD_TEXT, "youtube.com")
        node2 = TextNode("content" , TextType.BOLD_TEXT, "youtube.com")
        self.assertEqual(node1, node2)

    def test_neq1(self):
        # type mismatch
        node1 = TextNode("content" , TextType.ITALIC_TEXT)
        node2 = TextNode("content" , TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        # content varried
        node1 = TextNode("content" , TextType.BOLD_TEXT)
        node2 = TextNode("content2" , TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_neq3(self):
        # URL varied
        node1 = TextNode("content" , TextType.BOLD_TEXT, "youtube.com")
        node2 = TextNode("content" , TextType.BOLD_TEXT, "www.youtube.com")
        self.assertNotEqual(node1, node2)


    def test_text_is_string(self):
        node1 = TextNode("content" , TextType.ITALIC_TEXT)
        self.assertIsInstance(node1.text,str)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, plain, https://www.boot.dev)", repr(node)
        )



    # def test_none_text_raises(self):
    #     with self.assertRaises():
    #         TextNode(None, TextType.ITALIC_TEXT)

    # def test_invalid_text_type_raises(self):
    #     with self.assertRaises(TypeError):
    #         TextNode("content" , 4)

if __name__ == "__main__":
    unittest.main()
