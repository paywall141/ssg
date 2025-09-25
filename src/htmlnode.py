class HTMLNode:
    def __init__(self, tag:str = None, value:str = None, children:list = None, props:dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        text = ""
        for key,value in self.props.items():
            text += f" {key}=\"{value}\""
        return text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

    
class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, children = None, props = None):
        super().__init__(tag, value, None, props)
        if value is None:
            raise ValueError("value is required")
        self.children = None

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, cannot have children, {self.props})"
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        output = ""
        if self.tag is None:
            return self.value
        output += f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return output
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if children is None:
            raise ValueError("children required")
        if tag is None:
            raise ValueError("tag is required")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All Parent nodes require a tag")
        if not self.children:
            raise ValueError("Parent nodes must have at least one child")
        
        output = "<" + self.tag + self.props_to_html() + ">"
        for child in self.children:
            output += child.to_html()
        output += "</" + self.tag + ">"
        return output
