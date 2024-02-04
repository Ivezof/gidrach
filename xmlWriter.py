from typing import Union


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
    def __init__(self, name: str, attr: dict = None, content: str = None, parent_elem=None):
        self.name = name
        self.attr = attr
        self.child_elements = []
        self.content = content
        if parent_elem:
            parent_elem.add_child(self)

    def add_child(self, elem):
        if self.content:
            raise XmlElemFormatError('content and children cannot exist in an element at the same time')
        self.child_elements.append(elem)

    def set_content(self, content: Union[str, int]):
        if self.child_elements:
            raise XmlElemFormatError('content and children cannot exist in an element at the same time')
        self.content = str(content)

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
        xml += f"</{self.name}>"
        return xml


class Document:
    def __init__(self, path: str, name: str, main_elem: str, attr: dict):
        self.__path = path
        self.__name = name
        self.__main_elem = main_elem
        self.__attr = attr
        self.__xml = f'<{main_elem} '
        for k, v in self.__attr.items():
            self.__xml += f'{k}="{v}" '
        self.__xml += ">"
        with open(f'{self.__path}{self.__name}', "w", encoding='utf8') as wf:
            wf.write(self.__xml)

    def close_document(self):
        with open(f'{self.__path}{self.__name}', "a", encoding='utf8') as wf:
            wf.write(f'</{self.__main_elem}>')

    def add_elem(self, elem: Elem):
        self.__xml = elem.get_xml()
        with open(f'{self.__path}{self.__name}', "a", encoding='utf8') as wf:
            wf.write(self.__xml)
