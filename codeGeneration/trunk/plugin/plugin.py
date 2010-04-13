'''
Created on 13.4.2010

@author: kubincam
'''
from compiler.ast import For

class pluginMain(object):
    '''
    classdocs
    '''

    def __init__(self, interface):
        '''
        Constructor
        '''
        
        app = interface.GetAdapter();
        guiMan = app.GetGuiManager();
        m = guiMan.GetMainMenu();
        for t in m.GetItems():
            if t.GetGuiId() == 'mItemProject':
                break;
        sm = t.GetSubmenu();
        sm.AddMenuItem('test', self.generateCodeFormularCallback, -1, 'Test');
        
    def generateCodeFormularCallback(self, *widget):
        buffer = [];
        buffer.append(widget);               