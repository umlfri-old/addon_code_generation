from CodeContainer import CCodeContainer
from lib.lib import ToBool

class CProperty(CCodeContainer):
    def __init__(self, id, value="", newLine="", default="", prefix="", sufix="", recursive="0"):
        CCodeContainer.__init__(self)
        self.id = id
        self.value = value
        self.newLine = newLine
        self.default = default
        self.prefix = prefix
        self.sufix = sufix
        self.recursive = ToBool(recursive)

    def Generate(self, element, path, fil=None):
        ret = [True, self.prefix]
        text, = self.GetVariables(element, 'id')

        # If the result is string
        if isinstance(text, basestring):
            textList = text.splitlines()

            if len(text) == 0:
                if self.default != "":
                    ret = [True, self.GetRoot().GetNewLineIndent() + self.default]
                    return ret
                else:
                    return [False, ""]

            for id, i in enumerate(textList):
                ret[1] += self.GetRoot().GetNewLineIndent() + self.newLine + i
                if id < len(textList) - 1:
                    ret[1] += '\n'
                    self.GetRoot().SetNewLine(True)

            for i in self.childs:
                ret = self.JoinReturnValue(ret, i.Generate(element, path, fil))

        # Else it is ElementObject
        else:
            if not self.recursive:
                if text is not element:
                    for i in self.childs:
                        ret = self.JoinReturnValue(ret, i.Generate(text, path, fil))
                else:
                    return [False, ""]
            else:
                for i in self.childs:
                    ret = self.JoinReturnValue(ret, i.Generate(text, path, fil))

        ret[1] += self.sufix
        return ret