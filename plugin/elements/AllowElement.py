from CodeObject import CCodeObject
from CodeContainer import CCodeContainer

class CAllowElement(CCodeContainer):
    
    def __init__(self, id):
        CCodeContainer.__init__(self)
        self.id = id
    
    def Generate(self, elementObject, path, fil = None):
        ret = [True, ""]
        id = 0
        for id, i in enumerate(self.GetNodeSpecifyElements(elementObject, self.id, False)):
            root = self.GetRoot()
            template = root.GetTemplate(i.type.identity)
            if  template is not None:
                id += 1
                ret = self.JoinReturnValue(ret, template.Generate(root.GetTemplates(), i.GetObject(), path))
        
        if id == 0:
            return [False, ""]
            
        return ret

    def GetNodeSpecifyElements(self, elementObject, elements, recursive = True):
        List = []
        def Rekurzia(elementObject):
            for i in elementObject.children:
                if i.type.name in elements or elements == "All":
                    List.append(i)
                    if recursive and i.children and i.type.name == 'Package':
                        Rekurzia(i)

        Rekurzia(elementObject)
        for i in List:
            yield i