import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType

from utilities import *

class TestTextHTMLNodeConversion(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_to_html(self):
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        expected = LeafNode("a", "Click here", {"href": "https://www.google.com"})
        self.assertEqual(html_node, expected)

    def test_require_text_node(self):
        notnode = "Test"
        htmlnode = LeafNode(None, "Test text", None)
        self.assertRaises(
            ValueError,
            text_node_to_html_node,
            notnode
        )
        self.assertRaises(
            ValueError,
            text_node_to_html_node,
            htmlnode
        )

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_multiple_different(self):
        node = TextNode("This is text with a `code block` **and BOLD**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        newer_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" ", TextType.TEXT), 
            TextNode("and BOLD", TextType.BOLD)
            ]
        self.assertEqual(newer_nodes, expected)
    def test_split_multiple_same(self):
        node = TextNode("This text has **BOLD** and **MORE BOLD**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("MORE BOLD", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])
    
    def test_not_extract_link(self):
        matches = extract_markdown_images(
            "This is text with a [hyperlink](https://www.google.com)"
        )
        self.assertListEqual(matches, [])

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png); actually ![twice](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png"), ("twice","https://i.imgur.com/zjjcJKZ.png")])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_not_extract_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [])
    
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [hyperlink](https://www.google.com)"
        )
        self.assertListEqual(matches, [("hyperlink", "https://www.google.com")])

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [hyperlink](https://www.google.com) and [another](https://google.com)"
        )
        self.assertListEqual(matches, [("hyperlink", "https://www.google.com"), ("another", "https://google.com")])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],   
        )
    def test_split_images_bold(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.BOLD),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],   
        )
    def test_not_split_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another [second link](https://imgur.com)", TextType.TEXT),
            ],   
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another [second link](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://github.com"
                ),
            ],   
        )

    def test_split_links_italic(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another [second link](https://github.com)",
            TextType.ITALIC,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.ITALIC),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.ITALIC),
                TextNode(
                    "second link", TextType.LINK, "https://github.com"
                ),
            ],   
        )

    def test_not_split_images(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],   
        )

class TestTexttoTextNodes(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
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
        self.assertEqual(text_to_textnodes(text), expected)

    def test_links_in_bold(self):
        text = "This is **bold text with a [link](https://boot.dev)**"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text with a ", TextType.BOLD),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image_in_bold_trailing(self):
        text = "This is **bold text with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) in the middle.**"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text with an ", TextType.BOLD),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" in the middle.", TextType.BOLD)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line  

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_valid_heading(self):
        block1 = "### This is a valid heading"
        block2 = "###### This is a valid heading"
        block3 = "# This is a valid heading"
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type(block1), expected)
        self.assertEqual(block_to_block_type(block2), expected)
        self.assertEqual(block_to_block_type(block3), expected)
    
    def test_invalid_heading(self):
        block1 = "##This isn't a valid heading"
        block2 = "####### This isn't a valid heading"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block1), expected)
        self.assertEqual(block_to_block_type(block2), expected)

    def test_valid_ulist(self):
        block1 = "- A\n- Thing\n- in\n- list"
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(block_to_block_type(block1), expected)

    def test_invalid_ulist(self):
        block1 = "- A\n-Thing\n- in\n- list"
        block2 = "- A\n- Thing\n- in\nlist"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block1), expected)
        self.assertEqual(block_to_block_type(block2), expected)

    def test_valid_olist(self):
        block1 = "1. A\n2. Thing\n3. in\n4. list"
        expected = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(block1), expected)

    def test_invalid_olist(self):
        block1 = "1. A\n2.Thing\n3. in\n4. list"
        block2 = "1. A\n2. Thing\n3. in\nlist"
        block3 = "1. A\n3. Thing\n4. in\n5. list"
        block4 = "1 A\n2 Thing\n3 in\n4 list"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block1), expected)
        self.assertEqual(block_to_block_type(block2), expected)
        self.assertEqual(block_to_block_type(block3), expected)
        self.assertEqual(block_to_block_type(block4), expected)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = "### this is a heading\n\n```and\nsome\ncode```"
        html = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode("h3", children=[
                    LeafNode(None, "this is a heading")
                ]),
                HTMLNode("code", children=[
                    LeafNode(None, "and\nsome\ncode")
                ])
            ]
        )
        self.assertEqual(html, expected)

    def test_heading_with_format(self):
        markdown1 = "## _This heading is Italic_"
        markdown2 = "#### **This heading is bold**"
        html1 = markdown_to_html_node(markdown1)
        html2 = markdown_to_html_node(markdown2)
        expected1 = HTMLNode(
            "div",
            children=[
                HTMLNode("h2", children=[
                    LeafNode("i", "This heading is Italic")
                ])
            ]
        )
        expected2 = HTMLNode(
            "div",
            children=[
                HTMLNode("h4", children=[
                    LeafNode("b", "This heading is bold")
                ])
            ]
        )
        self.assertEqual(html1, expected1)
        self.assertEqual(html2, expected2)

    def test_ulist(self):
        markdown = "## This is a list:\n\n- one\n- two"
        html = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode("h2", children=[
                    HTMLNode(None, "This is a list:")
                ]),
                HTMLNode("ul", children=[
                    HTMLNode("li", children=[
                        HTMLNode(None, "one")
                    ]),
                    HTMLNode("li", children=[
                        HTMLNode(None, "two")
                    ])
                ])
            ]
        )
        self.assertEqual(html, expected)
    
    def test_olist(self):
        markdown = "## This is a list:\n\n1. one\n2. two"
        html = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            children=[
                HTMLNode("h2", children=[
                    HTMLNode(None, "This is a list:")
                ]),
                HTMLNode("ol", children=[
                    HTMLNode("li", children=[
                        HTMLNode(None, "one")
                    ]),
                    HTMLNode("li", children=[
                        HTMLNode(None, "two")
                    ])
                ])
            ]
        )
        self.assertEqual(html, expected)

class TestExtractTitle(unittest.TestCase):
    def test_h1_extract(self):
        markdown = "# Test Title\n\n## Some other title\n\nSome basic text"
        title = extract_title(markdown)
        expected = "Test Title"
        self.assertEqual(title, expected)

    def test_h1_later(self):
        markdown = "## Test Title\n\n# Some other title \n\nSome basic text"
        title = extract_title(markdown)
        expected = "Some other title"
        self.assertEqual(title, expected)

    def test_no_h1_found(self):
        markdown = "## Test Title\n\n## Some other title\n\nSome basic text"
        self.assertRaises(
            ValueError,
            extract_title,
            markdown
        )
