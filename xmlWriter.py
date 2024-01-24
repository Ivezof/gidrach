class XmlElemFormatError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return "Xml elem format error"


class Elem:
    def __init__(self, name: str, attr: dict = None, content: str = None):
        self.name = name
        self.attr = attr
        self.child_elements = []
        self.content = content

    def add_child(self, elem):
        if self.content:
            raise XmlElemFormatError('content and children cannot exist in an element at the same time')
        self.child_elements.append(elem)

    def set_content(self, content: str):
        if self.child_elements:
            raise XmlElemFormatError('content and children cannot exist in an element at the same time')
        self.content = content

    def get_xml(self):
        xml = f"<{self.name} "
        if self.attr:
            for key, value in self.attr.items():
                xml += f'{key}="{value}" '
        xml += ">"
        if self.content and self.child_elements:
            raise XmlElemFormatError('content and children cannot exist in an element at the same time')
        elif self.content:
            xml += self.content
        else:
            for i in self.child_elements:
                xml += i.get_xml()
        xml += f"<{self.name}/>"
        return xml


class Document:
    def __init__(self, path: str, name: str, main_elem: str, attr: dict):
        self.path = path
        self.name = name
        self.main_elem = main_elem
        self.attr = attr
        self.xml = f'<{main_elem} '
        for k, v in self.attr.items():
            self.xml += f'{k}="{v}" '
        self.xml += ">"
        with open(f'{self.path}{self.name}', "w", encoding='utf8') as wf:
            wf.write(self.xml)

    def close_document(self):
        with open(f'{self.path}{self.name}', "a", encoding='utf8') as wf:
            wf.write(f'<{self.main_elem}/>')

    def add_elem(self, elem: Elem):
        self.xml = elem.get_xml()
        with open(f'{self.path}{self.name}', "a", encoding='utf8') as wf:
            wf.write(self.xml)
