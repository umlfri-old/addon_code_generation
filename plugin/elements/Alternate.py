
from CodeContainer import CCodeContainer


class CAlternate(CCodeContainer):
    
    def __init__(self):
        CCodeContainer.__init__(self)
    
    
    def Generate(self, elementObject, path, fil = None):
        ret = [False, ""]
 
        for i in self.childs:
            genList = i.Generate(elementObject, path, fil)
            if isinstance(i, CCodeContainer):
                ret = [ret[0] | genList[0], ret[1] + genList[1]]
            else:
                ret = [ret[0], ret[1] + genList[1]]
        
        return ret
            