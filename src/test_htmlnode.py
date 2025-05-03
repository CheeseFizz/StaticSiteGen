import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        testpropdict = {"href": "https://www.google.com", "target":"_blank"}
        testpropstr = ' href="https://www.google.com" target="_blank"'
        node1 = HTMLNode("a", "Test", props=testpropdict)
        htmlprops = node1.props_to_html()
        self.assertEqual(htmlprops, testpropstr)
    
    def test_repr(self):
        testpropdict = {"href": "https://www.google.com", "target":"_blank"}
        node1 = HTMLNode("a", "Test", props=testpropdict)
        node2 = HTMLNode("h1", "Test", [node1])
        testnoderepr1 = "HTMLNode(\nTag: a\nValue: Test\nChildren:\nProperties:\n\thref: https://www.google.com\n\ttarget: _blank\n)"
        testnoderepr2 = "HTMLNode(\nTag: h1\nValue: Test\nChildren:\n\ta\nProperties:\n)"
        self.assertEqual(node1.__repr__(), testnoderepr1)
        self.assertEqual(node2.__repr__(), testnoderepr2)

    def test_to_html(self):
        testpropdict = {"href": "https://www.google.com", "target":"_blank"}
        node1 = HTMLNode("a", "Test", props=testpropdict)
        self.assertRaises(NotImplementedError,node1.to_html)



if __name__ == "__main__":
    unittest.main()