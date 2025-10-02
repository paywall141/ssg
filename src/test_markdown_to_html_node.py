import unittest
from markdown_blocks import markdown_to_html_node
from htmlnode import ParentNode, LeafNode

class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_simple_paragraph(self):
        markdown = "This is a paragraph."
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
    
    def test_paragraph_with_inline_markdown(self):
        markdown = "This is **bold** and *italic* text."
        result = markdown_to_html_node(markdown)
        paragraph = result.children[0]
        self.assertEqual(paragraph.tag, "p")
        # Should have multiple children for inline elements
        self.assertGreater(len(paragraph.children), 1)
    
    def test_heading_h1(self):
        markdown = "# This is a heading"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "h1")
    
    def test_heading_h2(self):
        markdown = "## This is a heading"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "h2")
    
    def test_heading_h6(self):
        markdown = "###### This is a heading"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "h6")
    
    def test_single_line_quote(self):
        markdown = "> This is a quote"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.children[0].tag, "blockquote")
    
    def test_multi_line_quote(self):
        markdown = "> Line one\n> Line two\n> Line three"
        result = markdown_to_html_node(markdown)
        quote = result.children[0]
        self.assertEqual(quote.tag, "blockquote")
    
    def test_unordered_list(self):
        markdown = "- Item one\n- Item two\n- Item three"
        result = markdown_to_html_node(markdown)
        ul = result.children[0]
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 3)
        self.assertEqual(ul.children[0].tag, "li")
        self.assertEqual(ul.children[1].tag, "li")
        self.assertEqual(ul.children[2].tag, "li")
    
    def test_unordered_list_with_inline_markdown(self):
        markdown = "- **Bold** item\n- *Italic* item"
        result = markdown_to_html_node(markdown)
        ul = result.children[0]
        self.assertEqual(ul.tag, "ul")
        # Each li should have children with inline formatting
        self.assertGreater(len(ul.children[0].children), 0)
    
    def test_ordered_list(self):
        markdown = "1. First\n2. Second\n3. Third"
        result = markdown_to_html_node(markdown)
        ol = result.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 3)
        self.assertEqual(ol.children[0].tag, "li")
    
    def test_code_block(self):
        markdown = "```\ncode here\nmore code\n```"
        result = markdown_to_html_node(markdown)
        pre = result.children[0]
        self.assertEqual(pre.tag, "pre")
        self.assertEqual(len(pre.children), 1)
        code = pre.children[0]
        self.assertEqual(code.tag, "code")
        self.assertIn("code here", code.value)
    
    def test_code_block_no_inline_parsing(self):
        markdown = "```\n**this should not be bold**\n```"
        result = markdown_to_html_node(markdown)
        code = result.children[0].children[0]
        # Should contain the raw text with ** still in it
        self.assertIn("**", code.value)
    
    def test_multiple_blocks(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n> A quote"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[2].tag, "blockquote")
    
    def test_complex_document(self):
        markdown = """# Title

This is a paragraph with **bold** text.

## Subtitle

* List item 1
* List item 2

> A quote here

```
code block
```"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 6)

    def test_empty_markdown(self):
        markdown = ""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 0)

    def test_whitespace_only(self):
        markdown = "   \n\n   "
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        # Should have no children after stripping
        self.assertEqual(len(result.children), 0)

def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )