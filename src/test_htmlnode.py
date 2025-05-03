import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        testpropdict = {"href": "https://www.google.com", "target":"_blank"}
        testpropstr = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode("a", "Test", props=testpropdict)
        htmlprops = node.props_to_html()
        self.assertEqual(htmlprops, testpropstr)
    
    def test_repr(self):
        testpropdict = {"href": "https://www.google.com", "target":"_blank"}
        node1 = HTMLNode("a", "Test", props=testpropdict)
        node2 = HTMLNode("h1", "Test", [node1])
        testnoderepr1 = "HTMLNode(\nTag: a\nValue: Test\nChildren:\nProperties:\n\thref: https://www.google.com\n\ttarget: _blank\n)"
        testnoderepr2 = "HTMLNode(\nTag: h1\nValue: Test\nChildren:\n\ta\nProperties:\n)"
        self.assertEqual(node1.__repr__(), testnoderepr1)
        self.assertEqual(node2.__repr__(), testnoderepr2)

    def test_eq(self):
        testpropdict = {"href": "https://www.google.com", "target":"_blank"}
        childnode1 = HTMLNode("a", "Test", props=testpropdict)
        parentnode1 = HTMLNode("h1", "Test", [childnode1])
        childnode2 = HTMLNode("a", "Test", props=testpropdict)
        parentnode2 = HTMLNode("h1", "Test", [childnode2])

        self.assertEqual(childnode1, childnode2)
        self.assertEqual(parentnode1, parentnode2)

    def test_to_html(self):
        testpropdict = {"href": "https://www.google.com", "target":"_blank"}
        node = HTMLNode("a", "Test", props=testpropdict)
        self.assertRaises(NotImplementedError,node.to_html)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "Click here", {"href": "https://www.google.com"})
        expected = "<a href=\"https://www.google.com\">Click here</a>"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html_requires_value(self):
        node = LeafNode("p", None, None)
        self.assertRaises(ValueError, node.to_html)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )


if __name__ == "__main__":
    unittest.main()