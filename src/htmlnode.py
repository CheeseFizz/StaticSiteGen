class HTMLNode():
    def __init__(
            self, 
            tag: str = None, 
            value: str = None, 
            children: list = None, 
            props: dict = None
        ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return (self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) and (self.props == other.props)

    def __repr__(self):
        childstr = "Children:\n"
        if self.children:
            for child in self.children:
                childstr += f"\t{child.tag} | {child.props} | {child.children}\n"
        propstr = "Properties:\n"
        if self.props:
            for prop in self.props:
                propstr += f"\t{prop}: {self.props[prop]}\n"
        tagstr = f"Tag: {self.tag}"
        valuestr = f"Value: {self.value}"

        return f"HTMLNode(\n{tagstr}\n{valuestr}\n{childstr}{propstr})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prophtml = ""
        if self.props != None:
            for prop in self.props:
                prophtml += f" {prop}=\"{self.props[prop]}\""
        return prophtml


class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: str, 
            value: str, 
            props: dict = None
        ):
            super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNodes must have a value")
        if self.tag == None:
            return str(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict = None
    ):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNodes must have a tag")
        if self.children == None:
            raise ValueError("ParentNodes must have children")
        htmlstr = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            htmlstr += child.to_html()
        htmlstr += f"</{self.tag}>"
        return htmlstr