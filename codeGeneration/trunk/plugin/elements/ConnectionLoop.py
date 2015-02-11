
from CodeContainer import CCodeContainer
from Property import CProperty
from PropertyLoop import CPropertyLoop

class CConnectionLoop(CCodeContainer):
    
    def __init__(self, id, value, separator=""):
        CCodeContainer.__init__(self)
        self.collection = id
        self.separator = separator
        self.value = value
    
    def __GetItemFromParentLoop(self):
        parent = self.GetParent()
        
        while parent.GetParent() is not None:
            if isinstance(parent, CPropertyLoop):
                return parent.GetItem()
            parent = parent.GetParent()
        return None
    
    def Generate(self, elementObject, path, fil = None):
        ret = [True, ""]
        retFlag = False
        separatorFlag = False
        for id, item in enumerate(elementObject.connections):
            if item.type.name == self.value or self.value == "All":
                continue #TODO: Should be reviewed and fixed so connections are looped properly
                for i in self.childs:
                    elementObject.__LOOPVARS__ = item
                    genList = i.Generate(elementObject, path, fil)
                    ret = self.JoinReturnValue(ret, genList)
                    if isinstance(i, CProperty) and genList[0]:
                        retFlag = True
                        separatorFlag = True
                    del elementObject.__LOOPVARS__
                if separatorFlag:
                    ret[1] += self.separator
                separatorFlag = False
        
        if ret[1].find(self.separator, -1) == -1:
            ret[1] = ret[1][:-len(self.separator)]
               
        ret[0] = retFlag
            
        return ret