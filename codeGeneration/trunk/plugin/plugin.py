'''
Created on 13.4.2010

@author: kubincam
'''
from generator.Generator import CGenerator
from generator.Factory import CLanguageFactory
from generator.storage import open_storage
import os

from generator.consts import ROOT_PATH, VERSIONS_PATH, DIAGRAMS_PATH, ELEMENTS_PATH, CONNECTIONS_PATH, DATATYPE_PATH, SOURCECODE_PATH

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
        
        # TODO find path
        self.Storage = open_storage(os.path.join(ROOT_PATH, 'etc', 'uml'))
        self.CodeEngineering = CLanguageFactory(self.Storage,SOURCECODE_PATH)
#        clan = CLanguageFactory(storage, path);
        #clan = CLanguageFactory();
#        clan.Load('generator/codeTemplate/cplusplus_template.xml')
#        clan.Load('generator/codeTemplate/delphi_template.xml')
#        clan.Load('generator/codeTemplate/html_documentation.xml')
#        clan.Load('generator/codeTemplate/python_temlate.xml')
        # path where to save generate code
        gen = CGenerator(self.application.GetProject().GetCodeEngineering().GetType(self.cbTargetLanguage.get_active_text()), 'C:\Users\kubincam\Desktop')
#        gen = CGenerator(clan.GetType(''), 'C:\Users\kubincam\Desktop')
        
                     