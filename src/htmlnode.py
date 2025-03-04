
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value 
        self.children = children 
        self.props = props 
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        html = "" 
        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'
        return html 
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other_node):
        return (
            self.tag == other_node.tag and 
            self.value == other_node.value and 
            self.children == other_node.children and 
            self.props == other_node.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node requires value")
        elif self.tag is None:
            return self.value 
        else:
            return (
                f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            )
   
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node requires tag")
        elif self.children is None:
            raise ValueError("parent node requires children")
        else:
            child_html = ""
            for child in self.children:
                child_html += child.to_html() 
            return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"