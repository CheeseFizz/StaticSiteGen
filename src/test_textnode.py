import unittest

from textnode import TextNode, TextType
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


if __name__ == "__main__":
    unittest.main()