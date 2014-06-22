import xml.dom.minidom as xml
from elements import CODEALL

class CLanguageType:
    #def __init__(self, language, type):
    #    self.language = language
    #    self.type = type
    #    self.elements = {}

    def __init__(self, root):
        self.language = root.getAttribute("name")
        self.type = root.getAttribute("type")
        self.elements = {}
        for i in root.childNodes:
            if i.nodeType not in (xml.Node.ELEMENT_NODE, xml.Node.DOCUMENT_NODE):
                continue
            if i.tagName == 'Element':
                if not i.hasAttribute('id'):
                    # TODO: add UMLException (how to do it in plug in?)
                    #raise UMLException("XMLError", ('ElementType', 'id'))
                    pass
                #obj.AddElement(i.getAttribute('id'),self.__LoadElement(i))
                self.elements[i.getAttribute('id')] = self.__LoadElement(i)
    
    def GetType(self):
        return self.type
    
    def GetLanguage(self):
        return self.language
    
    def SetLanguage(self, language):
        self.language = language
        
    #def AddElement(self, id, element):
    #    self.elements[id] = element
    
    def GetElement(self, id):
        return self.elements[id]
    
    def GetElements(self):
        return self.elements

    def __LoadElement(self, root):
        if root.tagName in CODEALL:
            cls = CODEALL[root.tagName]
            params = {}
            for i in root.attributes.values():
                params[str(i.name)] = i.nodeValue
            obj = cls(**params)
        else:
            obj = CODEALL['None']()

        for i in root.childNodes:
            if i.nodeType not in (xml.Node.ELEMENT_NODE, xml.Node.DOCUMENT_NODE):
                if i.nodeType is xml.Node.TEXT_NODE:
                    for k in i.nodeValue.splitlines():
                        if len(k.expandtabs(1).strip(' ')) > 0:
                            obj.AppendChild(CODEALL['Text'](k.expandtabs(1).strip(' ')))
                continue
            if obj is not None:
                a = self.__LoadElement(i)
                if a is not None:
                    obj.AppendChild(a)
            else:
                self.__LoadElement(i)

        return obj