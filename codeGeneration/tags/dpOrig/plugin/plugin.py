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
        
        self.app = interface.GetAdapter();
        self.guiMan = self.app.GetGuiManager();
        self.m = self.guiMan.GetMainMenu();
        for t in self.m.GetItems():
            if t.GetGuiId() == 'mItemProject':
                break;
        self.sm = t.GetSubmenu();
        self.sm.AddMenuItem('test', self.generateCodeFormularCallback, -1, 'Generate');
        
    def generateCodeFormularCallback(self, widget):
        buffer = [];
        buffer.append(widget);
       
#        print "buffer callback content: ", buffer
        
        self.Storage = open_storage(ROOT_PATH)
        self.CodeEngineering = CLanguageFactory(self.Storage,SOURCECODE_PATH)
        gen = CGenerator(self.CodeEngineering.GetType('Delphi'), '/home/janik/tmp/aqw')
        # TODO get selected element as Object 
        elementObj = self.app.GetCurrentDiagram().GetSelectedElements()[0].GetObject()
        
        gen.GenerateElement(elementObj)
                           