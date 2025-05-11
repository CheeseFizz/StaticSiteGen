import re
from enum import Enum

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "Paragraph",
    HEADING = "Heading",
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"

def text_node_to_html_node(textnode):
    if not isinstance(textnode, TextNode):
        raise ValueError("textnode argument should be type TextNode")
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
        case _:
            raise ValueError(f"Invalid text_type: {textnode.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            splitnodes = node.text.split(delimiter)
            for n in splitnodes:
                if ((splitnodes.index(n) % 2) == 1) and (n != ""):
                    new_nodes.append(TextNode(n, text_type))
                elif (n != ""):
                    new_nodes.append(TextNode(n, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    regmatch = r"!\[(.+?)\]\((\S+)\)" #very basic md image link parsing
    imagetuples = re.findall(regmatch, text)
    return imagetuples

def extract_markdown_links(text):
    regmatch = r"(?<!!)\[(.+?)\]\((\S+)\)" #very basic md hyperlink parsing
    linktuples = re.findall(regmatch, text)
    return linktuples

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if (node.text_type == TextType.TEXT) or (node.text_type == TextType.BOLD) or (node.text_type == TextType.ITALIC):
            links = extract_markdown_images(node.text)
            if len(links) > 0:
                remainingtext = node.text
                for link in links:
                    splitnodes = remainingtext.split(f"![{link[0]}]({link[1]})") # split on entire link
                    if splitnodes[0] != "":
                        new_nodes.append(TextNode(splitnodes[0], node.text_type))
                    new_nodes.append(TextNode(link[0], TextType.IMAGE, link[1]))
                    chopstr = f"{splitnodes[0]}![{link[0]}]({link[1]})"
                    choplength = len(chopstr)
                    remainingtext = remainingtext[choplength:] # remove already processed text

                if remainingtext != "":
                    new_nodes.append(TextNode(remainingtext, node.text_type)) # process remaining text into a node

            else:
                new_nodes.append(node) # pass-through nodes that don't need splitting
        else:
            new_nodes.append(node) # pass-through nodes that are image, code, or links

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if (node.text_type == TextType.TEXT) or (node.text_type == TextType.BOLD) or (node.text_type == TextType.ITALIC):
            links = extract_markdown_links(node.text)
            if len(links) > 0:
                remainingtext = node.text
                for link in links:
                    splitnodes = remainingtext.split(f"[{link[0]}]({link[1]})") # split on entire link
                    if splitnodes[0] != "":
                        new_nodes.append(TextNode(splitnodes[0], node.text_type))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    choplength = len(f"{splitnodes[0]}[{link[0]}]({link[1]})")
                    remainingtext = remainingtext[choplength:] # remove already processed text

                if remainingtext != "":
                    new_nodes.append(TextNode(remainingtext, node.text_type)) # process remaining text into a node

            else:
                new_nodes.append(node) # pass-through nodes that don't need splitting
        else:
            new_nodes.append(node) # pass-through nodes that are image, code, or links

    return new_nodes
        
def text_to_textnodes(text):
    # Doing all of these with intermediate variables, because it's going to be ugly if nested. 
    initial = TextNode(text, TextType.TEXT)
    Italics = split_nodes_delimiter([initial], "_", TextType.ITALIC)
    Bolds = split_nodes_delimiter(Italics, "**", TextType.BOLD)
    Codes = split_nodes_delimiter(Bolds, "`", TextType.CODE)
    Images = split_nodes_image(Codes)
    finalnodes = split_nodes_link(Images)
    return finalnodes

def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split("\n\n")
    for split in splits:
        stripped = split.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks

def block_to_block_type(block):
    default = False
    match block[0]:
        case "#":
            try:
                if (block[0:7].lstrip("#")[0] == " "):
                    return BlockType.HEADING
            except IndexError:
                pass # don't need to do anything extra for IndexError
            default = True
        
        case "`":
            try:
                if (block[0:3] == "```" and block[-3:] == "```"):
                    return BlockType.CODE
            except IndexError:
                pass # don't need to do anything extra for IndexError
            default = True

        case ">":
            if all(list(map(lambda x: x[0] == ">", block.split("\n")))):
                return BlockType.QUOTE
            default = True

        case "-":
            try:
                if all(list(map(lambda x: x[0:2] == "- ", block.split("\n")))):
                    return BlockType.UNORDERED_LIST
            except IndexError:
                pass # don't need to do anything extra for IndexError
            default = True

        case "1":
            try:
                splits = block.split("\n")
                if all(list(map(lambda x: int(re.match(r"^(\d+?)\.\s", x)[1]) == (splits.index(x) + 1), splits))): # all lines start with "(line index +1). "
                    return BlockType.ORDERED_LIST
            except IndexError:
                pass # don't need to do anything extra for IndexError
            except TypeError:
                pass # don't need to do anything extra for TypeError
            default = True

        case _:
            default = True

    if default:
        return BlockType.PARAGRAPH

def tag_and_strip_block(block):
    blocktype = block_to_block_type(block)
    tag = ""
    match blocktype:
        case BlockType.CODE:
            return ("code", block[3:-3])

        case BlockType.HEADING:
            hnum = len(block) - len(block.lstrip("#"))
            return (f"h{str(hnum)}", block.lstrip("#").lstrip())

        case BlockType.PARAGRAPH:
            return ("p", block)

        case BlockType.ORDERED_LIST:
            return ("ol", block)

        case BlockType.UNORDERED_LIST:
            return ("ul", block)

        case BlockType.QUOTE:
            splits = block.split("\n")
            new_splits = []
            for split in splits:
                new_splits.append(split[2:])
            return ("blockquote", "\n".join(new_splits))

def list_item_to_html_node(block, block_type):
    # might be better to redo other functions and structures to support this... but this works too.
    nodes = []
    if block_type == BlockType.UNORDERED_LIST:
        splits = block.split("\n")
        for split in splits:
            nodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(split[2:])))))
    elif block_type == BlockType.ORDERED_LIST:
        splits = block.split("\n")
        for split in splits:
            chop = len(re.match(r"(\d+?\.\s)", split)[1])
            nodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(split[chop:])))))
    else:
        raise ValueError(f"unexpected block_type: {block_type}")
    return nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocknodes = []
    for block in blocks:
        tag, newblock = tag_and_strip_block(block)
        if tag == "code":
            blocknodes.append(ParentNode(tag, children=[text_node_to_html_node(TextNode(newblock, TextType.TEXT))]))
        elif tag == "ol":
            blocknodes.append(ParentNode(tag, children=list_item_to_html_node(block, BlockType.ORDERED_LIST)))
        elif tag == "ul":
            blocknodes.append(ParentNode(tag, children=list_item_to_html_node(block, BlockType.UNORDERED_LIST)))
        else:
            blocknodes.append(ParentNode(tag, children=list(map(text_node_to_html_node, text_to_textnodes(newblock)))))
    return ParentNode("div", children=blocknodes)

def extract_title(markdown):
    #feels a bit redundant to tag_and_strip_block?
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.match(r"^#\s", block):
            return block[2:].strip()
    raise ValueError("No h1 found")

