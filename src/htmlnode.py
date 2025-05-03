class HTMLNode():
    def __init__(
            self, 
            tag: str = None, 
            value = None, 
            children: list = None, 
            props: dict = None
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        childstr = "Children:\n"
        if self.children:
            for child in self.children:
                childstr += f"\t{child.tag}\n"
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
        for prop in self.props:
            prophtml += f" {prop}=\"{self.props[prop]}\""
        return prophtml
