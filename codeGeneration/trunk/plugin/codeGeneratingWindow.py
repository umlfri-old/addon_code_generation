import gtk
from os import listdir
from os.path import expanduser, isdir, isfile, join
import xml.dom.minidom as xml
from Generator import CGenerator
from Type import CLanguageType

class CodeGeneratingWindow:
    """
    Class to define code generating window.
    """

    def __init__(self, interface):
        """
        Initializes new window.
        @param interface: API interface
        """
        self.__i = interface
        self.__gtkBuilder = gtk.Builder()
        self.__gtkBuilder.add_from_file("share\\addons\\codeGeneration\\plugin\\generateCodeWindow.glade")
        self.__elements = []
        self.__window = self.__gtkBuilder.get_object("generateSourceCodeWindow")
        # Sets window properties.
        self.__window.set_keep_above(True)
        self.__window.set_modal(True)
        self.__window.set_transient_for(None)
        self.__window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        # Hide check button which sets if children elements should be shown
        # (they are currently generated automatically if parent element is generated)
        self.__gtkBuilder.get_object("mainContainer").remove(self.__gtkBuilder.get_object("includeChildPackages"))
        # Assign events.
        self.__gtkBuilder.get_object("selectFolderButton").connect("clicked",lambda x:self.selectFolderButtonClicked())
        self.__gtkBuilder.get_object("cancelButton").connect("clicked",lambda x:self.cancelButtonClicked())
        self.__gtkBuilder.get_object("generateButton").connect("clicked",lambda x:self.generateButtonClicked())
        self.__gtkBuilder.get_object("selectAll").connect("clicked",lambda x:self.selectAllClicked())
        self.__gtkBuilder.get_object("includeChildPackages").connect("clicked",lambda x:self.includeChildrenClicked())

    def show(self):
        """
        Shows code generating window.
        """
        self.__window.show_all()

    def loadData(self):
        """
        Loads data (visual elements in diagram) to object list.
        @param includeChildren: True if child elements should be included in the list
        """
        self.loadConverters()
        self.__gtkBuilder.get_object("objectView").get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        elementList = self.__gtkBuilder.get_object("objectView").get_model()
        elementList.clear()
        self.__elements = []
        index = 0
        for element in self.__i.current_diagram.elements:
            elementList.append([element.object.name, element.object.type.name, index])
            self.__elements.append(element.object)
            index += 1
            if (self.includeChildren()):
                index = self.loadChildren(element.object, 1, elementList, index)
        if self.selectAll():
            self.selectAllClicked()

    def loadChildren(self, element, level, elementList, nextIndex):
        """
        Loads child elements for the given element.
        @param element: child elements of this element object will be loaded to the list
        @param level: level of the element (elements in former diagram are level 0, children of those elements are level 1,
                      their children level 2 etc), used to compute indent
        @param elementList: list of the elements where children will be added
        @param lastIndex: next index to be assigned to the child element in list
        @return value of the next index to be used
        """
        indent = ""
        for i in range(0, level):
            indent += "     "
        for child in element.children:
            elementList.append([indent+child.name, child.type.name, nextIndex])
            self.__elements.append(child)
            nextIndex += 1
            nextIndex = self.loadChildren(child, level+1, elementList, nextIndex)
        return nextIndex

    def generateButtonClicked(self):
        """
        Button to generate code was clicked.
        """
        # TODO: check form
        elementList = self.__gtkBuilder.get_object("objectView")
        converterCB = self.__gtkBuilder.get_object("converters")
        (model, paths) = elementList.get_selection().get_selected_rows()
        selectedElements = []
        for path in paths:
            index = model.get_value(model.get_iter(path),2)
            selectedElements.append(self.__elements[index])
        converterIter = converterCB.get_active_iter()
        selectedConverterRoot = self.__converterRoots[converterCB.get_model().get_value(converterIter, 1)]

        path = self.__gtkBuilder.get_object("targetFolder").get_text()
        gen = CGenerator(CLanguageType(selectedConverterRoot), path)
        for item in selectedElements:
            gen.GenerateElement(item)
        message = gtk.MessageDialog(parent=self.__window, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
        message.set_markup("Code generation completed.")
        message.set_keep_above(True)
        message.run()
        self.__window.hide()

    def cancelButtonClicked(self):
        """
        Closes window with no changes.
        """
        self.__window.hide()

    def selectAllClicked(self):
        """
        Selects all elements in list.
        """
        if self.selectAll():
            self.__gtkBuilder.get_object("objectView").get_selection().select_all()
        else:
            self.__gtkBuilder.get_object("objectView").get_selection().unselect_all()

    def selectAll(self):
        """
        Checks if "select all" check box is checked.
        @return True if it is selected, False otherwise
        """
        return self.__gtkBuilder.get_object("selectAll").get_active()

    def includeChildren(self):
        """
        Checks if "Include all child packages" check button is checked.
        @return True if it is checked
        """
        return self.__gtkBuilder.get_object("includeChildPackages").get_active()

    def includeChildrenClicked(self):
        """
        Include child elements in list of objects.
        """
        self.loadData()

    def selectFolderButtonClicked(self):
        """
        Opens window to selected target folder and processes result.
        """
        folderEntry = self.__gtkBuilder.get_object("targetFolder")
        chooser = gtk.FileChooserDialog(title="Select target folder", parent=self.__window, action = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_keep_above(True)
        if folderEntry.get_text().strip() == "" or not isdir(folderEntry.get_text()):
            chooser.set_current_folder(expanduser("~"))
        else:
            chooser.set_current_folder(folderEntry.get_text())
        chooser.set_default_response(gtk.RESPONSE_OK)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            folderEntry.set_text(chooser.get_filename())
        chooser.destroy()

    def loadConverters(self):
        """
        Loads information about available converters.
        """
        dir = "share/addons/codeGeneration/converters"
        converters = [ f for f in listdir(dir) if isfile(join(dir,f)) ]
        converterList = self.__gtkBuilder.get_object("converters").get_model()
        converterList.clear()
        diagramName = self.__i.current_diagram.type.name.lower()
        id = 0
        self.__converterRoots = []
        for converter in converters:
            converterXML = xml.parse(join(dir, converter))
            root = converterXML.documentElement
            if root.tagName == 'Template' and root.hasAttribute("diagram") and root.hasAttribute("name") and root.hasAttribute("type"):
                if root.getAttribute("diagram").lower() == diagramName or root.getAttribute("diagram").lower() == "all":
                    converterList.append([root.getAttribute("name") + " (" + root.getAttribute("type") + ")", id])
                    self.__converterRoots.append(root)
                    id += 1