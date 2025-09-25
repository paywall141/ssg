import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node1 = HTMLNode("a", "youtube", [], {"href":"https://www.youtube.com", "target": "_blank"})
        self.assertEqual(repr(node1),
            "HTMLNode(a, youtube, [], {'href': 'https://www.youtube.com', 'target': '_blank'})")

    def test_props_to_html_multiple(self):
        test_props = {"href": "https://www.google.com","target": "_blank"}
        expected_res =  ' href="https://www.google.com" target="_blank"'
        node1res = HTMLNode(None,None,None, test_props).props_to_html()
        self.assertEqual(node1res, expected_res)

    def test_props_to_html_none(self):
        node1 = HTMLNode()
        result = node1.props_to_html()
        self.assertEqual("", result)
    
    def test_props_to_html_empty(self):
        node1 = HTMLNode(props = {})
        result = node1.props_to_html()
        self.assertEqual("", result)

    def test_props_to_html_single(self):
        node = HTMLNode(props={"id": "test"})
        self.assertEqual(node.props_to_html(),' id="test"' )

    def test_props_to_html_various_types(self):
        node = HTMLNode(props={"data-num": 42, "hidden": True})
        expected = ' data-num="42" hidden="True"'
        self.assertEqual(node.props_to_html(), expected)

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            [],
        )
        self.assertEqual(
            node.props,
            {},
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_repr(self):
        node1 = LeafNode("a", "youtube", [], {"href":"https://www.youtube.com", "target": "_blank"})
        self.assertEqual(repr(node1),
            "LeafNode(a, youtube, cannot have children, {'href': 'https://www.youtube.com', 'target': '_blank'})")

    def test_none_text_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("a",None)
    
    def test_leaf_to_html_one_prop(self):
        node = LeafNode("a", "Click me!",None ,props ={"href": "https://www.google.com"}).to_html()
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node, expected)

    def test_leaf_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.").to_html()
        expected ="<p>This is a paragraph of text.</p>"
        self.assertEqual(node, expected)

    def test_leaf_to_html_no_props_w_children(self):
        test_children = [HTMLNode() for i in range(5)]
        node = LeafNode("p", "This is a paragraph of text.",children = test_children ).to_html()
        expected ="<p>This is a paragraph of text.</p>"
        self.assertEqual(node, expected)

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_leaf_child_no_props(self):
        arr = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        node1 = ParentNode("p", children=arr, props=None)
        self.assertEqual(node1.to_html(),
                         "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_to_html_leaf_child_w_props(self):
        arr = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        node1 = ParentNode("p", children=arr, props={"class":"test parent"})
        self.assertEqual(node1.to_html(),
                         "<p class=\"test parent\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_to_html_parent_child_no_props(self):
        arr2 = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        arr = [
            ParentNode("p", children=arr2, props=None),
        ]
        node1 = ParentNode("div", children=arr, props=None)
        self.assertEqual(node1.to_html(),
                         "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>")        

    def test_parent_to_html_parent_and_leaf_child_no_props(self):
        arr2 = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        arr = [
            ParentNode("p", children=arr2, props=None),
            LeafNode("a", "link", props={"href": "youtube.com"})
        ]
        node1 = ParentNode("div", children=arr, props=None)
        self.assertEqual(node1.to_html(),
                         "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><a href=\"youtube.com\">link</a></div>")
    def test_parent_to_html_only_child_has_props(self):
        arr2 = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        arr = [
            ParentNode("p", children=arr2, props={"class":"text-para"}),
        ]
        node1 = ParentNode("div", children=arr, props=None)
        self.assertEqual(node1.to_html(),
                         "<div><p class=\"text-para\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>")        
                
    def test_parent_to_html_no_tag_kills_props(self):
        arr = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text", props={"class": "stylized-1"}),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        node1 = ParentNode("p", children=arr, props={"class":"test parent"})
        self.assertEqual(node1.to_html(),
                         "<p class=\"test parent\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_parent_to_html_child_and_parent_have_props(self):
        arr = [
            LeafNode("b", "Bold text", props={"class": "stylized-1"}),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        node1 = ParentNode("p", children=arr, props={"class":"test parent"})
        self.assertEqual(node1.to_html(),
                         "<p class=\"test parent\"><b class=\"stylized-1\">Bold text</b>Normal text<i>italic text</i>Normal text</p>")