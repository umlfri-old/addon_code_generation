'''
Created on 13.4.2010

@author: kubincam
'''
from generator.Generator import CGenerator
from generator.Factory import CLanguageFactory

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
        sm.AddMenuItem('test', self.generateCodeFormularCallback, -1, 'Generate');
        
    def generateCodeFormularCallback(self, widget):
        buffer = [];
        buffer.append(widget);
       
        print "buffer callback content: ", buffer
        
        clan = CLanguageFactory;
        clan.__Load('../codeTemplate/cplusplus_template.xml')
        clan.__Load('../codeTemplate/delphi_template.xml')
        clan.__Load('../codeTemplate/html_documentation.xml')
        clan.__Load('../codeTemplate/python_temlate.xml')
        # path where to save generate code
        gen = CGenerator(clan.GetType(''), 'C:\Users\kubincam\Desktop')
        
                     