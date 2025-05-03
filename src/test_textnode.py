import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_urleq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://test.test")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://test.test")
        self.assertEqual(node, node2)

    def test_urlneq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://test.test")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_typeneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

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



if __name__ == "__main__":
    unittest.main()