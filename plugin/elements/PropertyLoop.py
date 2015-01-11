
from CodeContainer import CCodeContainer
from Property import CProperty
from CodeCondition import CCodeCondition

class CPropertyLoop(CCodeContainer):
    
    def __init__(self, id, separator = "", parse = None):
        CCodeContainer.__init__(self)
        self.collection = id
        self.separator = separator
        self.parse = parse
        self.item = None
    
    def GetItem(self):
        return self.item
    
    def __GetItemFromParentLoop(self):
        parent = self.GetParent()
        
        while parent.GetParent() is not None:
            if isinstance(parent, CPropertyLoop):
                return parent.GetItem()
            parent = parent.GetParent()
        return None
    
    def Generate(self, elementObject, path, fil = None):        
        root = self.GetRoot()
        ret = [True, ""]
        retFlag = False
        separatorFlag = False
        if self.parse is not None: # TODO: this "if" could be part of separate class which would iterate over list inside some loopvar parameter
            if self.collection == "@parameters":
                parameters = elementObject.__LOOPVARS__[self.parse]
                if parameters is None or len(parameters) == 0:
                    return [False, ""]
                i = 0;
                for parameter in parameters:
                    for ch in self.childs:
                        elementObject.__LOOPVARS__ = parameter
                        genList = ch.Generate(elementObject, path, fil)
                        ret = self.JoinReturnValue(ret, genList)
                        if isinstance(ch, (CCodeContainer)) and genList[0]:
                            retFlag = True
                    if i < len(parameters) - 1:
                        ret[1] += self.separator
                    i += 1
        else:
            if elementObject.values[self.collection] is None or len(elementObject.values[self.collection]) == 0:
                return [False,""]
            for item in eval(elementObject.values[self.collection]): # TODO: Eval has to be removed after API is fixed
                self.item = item
                for i in self.childs:
                    elementObject.__LOOPVARS__ = item
                    genList = i.Generate(elementObject, path, fil)
                    ret = self.JoinReturnValue(ret, genList)
                    if isinstance(i, (CCodeContainer)) and genList[0]:
                        retFlag = True
                        separatorFlag = True
                    #~ del elementObject.__LOOPVARS__
                if separatorFlag:
                    ret[1] += '\n'
                    root.SetNewLine(True)
                    separatorFlag = False
        
        item = self.__GetItemFromParentLoop()
        if item is not None:
            elementObject.__LOOPVARS__ = item 
        
        if retFlag:
            ret[0] = True
            
        return ret