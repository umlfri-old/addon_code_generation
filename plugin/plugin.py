#!/usr/bin/python

from org.umlfri.api.mainLoops import GtkMainLoop
import gtk

"""
Main class of the plugin, it defines what happens during its loading and basic functionality.
"""
class pluginMain:

    """
    Constructor.
    @param interface: API adapter object
    """
    def __init__(self, interface):
        self.__i = interface
        self.__i.set_main_loop(GtkMainLoop())
        self.__gtkBuilder = gtk.Builder()
        self.createMenu()

    """
    Creates menu item for plugin.
    """
    def createMenu(self):
        # Generates menu item for code engineering, unless it is already there (placed there by another plugin to generate diagram from source code).
        if self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.items["mItemCodeEngineering"] is None:
            codeEngineeringMenu = self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.add_menu_item("mItemCodeEngineering", None, 0, "_Code engineering", True, None)
            codeEngineeringMenu.enabled = False
        self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.items["mItemCodeEngineering"].add_submenu()
        self.__i.gui_manager.main_menu.items["mItemDiagram"].submenu.items["mItemCodeEngineering"].submenu.add_menu_item("mItemGenerateCode", self.openCodeGeneratingWindow, 0, "_Generate code", True, None)

    def openCodeGeneratingWindow(self, widget):
        self.__gtkBuilder.add_from_file("share\\addons\\codeGenerator\\plugin\\generateCodeWindow.glade")
        self.__codeGeneratingWindow = self.__gtkBuilder.get_object("generateSourceCodeWindow")
        self.__codeGeneratingWindow.set_keep_above(True)
        self.__codeGeneratingWindow.set_modal(True)
        self.__codeGeneratingWindow.set_transient_for(None)
        self.__codeGeneratingWindow.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.__codeGeneratingWindow.show_all()