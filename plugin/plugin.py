#!/usr/bin/python

from org.umlfri.api.mainLoops import GtkMainLoop
import gtk
from codeGeneratingWindow import CodeGeneratingWindow

class pluginMain:
    """
    Main class of the plugin, it defines what happens during its loading and basic functionality.
    """

    def __init__(self, interface):
        """
        Constructor.
        @param interface: API adapter object
        """
        self.__i = interface
        self.__i.set_main_loop(GtkMainLoop())
        self.createMenu()

    def createMenu(self):
        """
        Creates menu item for plugin.
        """
        # Generates menu item for code engineering, unless it is already there (placed there by another plugin to generate diagram from source code).
        if self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.items["mItemCodeEngineering"] is None:
            codeEngineeringMenu = self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.add_menu_item("mItemCodeEngineering", None, 0, "_Code engineering", True, None)
            codeEngineeringMenu.enabled = False
        self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.items["mItemCodeEngineering"].add_submenu()
        self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.items["mItemCodeEngineering"].submenu.add_menu_item("mItemGenerateCode", self.openCodeGenerationWindow, 0, "_Generate code", True, None)

    def openCodeGenerationWindow(self, widget):
        """
        Opens window to set up code generation.
        @param widget
        """
        if not hasattr(self, '__codeGeneratingWindow') or self.__codeGeneratingWindow is None:
            self.__codeGeneratingWindow = CodeGeneratingWindow(self.__i)
        self.__codeGeneratingWindow.loadData()
        self.__codeGeneratingWindow.show()