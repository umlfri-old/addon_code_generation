import gtk

"""
Class to define code generating window.
"""
class CodeGeneratingWindow:
    """
    Initializes new window.
    @param interface: API interface
    """
    def __init__(self, interface):
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
        # Assign events.
        self.__gtkBuilder.get_object("cancelButton").connect("clicked",lambda x:self.cancelButtonClicked())
        self.__gtkBuilder.get_object("generateButton").connect("clicked",lambda x:self.generateButtonClicked())
        self.__gtkBuilder.get_object("selectAll").connect("clicked",lambda x:self.selectAllClicked())
        self.__gtkBuilder.get_object("includeChildPackages").connect("clicked",lambda x:self.includeChildrenClicked())

    """
    Shows code generating window.
    """
    def show(self):
        self.__window.show_all()

    """
    Loads data (visual elements in diagram) to object list.
    @param includeChildren: True if child elements should be included in the list
    """
    def loadData(self):
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

    """
    Loads child elements for the given element.
    @param element: child elements of this element object will be loaded to the list
    @param level: level of the element (elements in former diagram are level 0, children of those elements are level 1,
                  their children level 2 etc), used to compute indent
    @param elementList: list of the elements where children will be added
    @param lastIndex: next index to be assigned to the child element in list
    @return value of the next index to be used
    """
    def loadChildren(self, element, level, elementList, nextIndex):
        indent = ""
        for i in range(0, level):
            indent += "     "
        for child in element.children:
            elementList.append([indent+child.name, child.type.name, nextIndex])
            self.__elements.append(child)
            nextIndex += 1
            nextIndex = self.loadChildren(child, level+1, elementList, nextIndex)
        return nextIndex

    """
    Button to generate code was clicked.
    """
    def generateButtonClicked(self):
        elementList = self.__gtkBuilder.get_object("objectView")
        (model, paths) = elementList.get_selection().get_selected_rows()
        selectedElements = []
        for path in paths:
            index = model.get_value(model.get_iter(path),2)
            selectedElements.append(self.__elements[index])
        # TODO: generating logic, remove following lines, they are just for testing of selection
        testText = "";
        for item in selectedElements:
            testText += item.name + "\n"
        md = gtk.MessageDialog(self.__window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, testText)
        md.set_keep_above(True)
        md.run()
        md.destroy()

    """
    Closes window with no changes.
    """
    def cancelButtonClicked(self):
        self.__window.hide()

    """
    Selects all elements in list.
    """
    def selectAllClicked(self):
        if self.selectAll():
            self.__gtkBuilder.get_object("objectView").get_selection().select_all()
        else:
            self.__gtkBuilder.get_object("objectView").get_selection().unselect_all()

    """
    Checks if "select all" check box is checked.
    @return True if it is selected, False otherwise
    """
    def selectAll(self):
        return self.__gtkBuilder.get_object("selectAll").get_active()

    """
    Checks if "Include all child packages" check button is checked.
    @return True if it is checked
    """
    def includeChildren(self):
        return self.__gtkBuilder.get_object("includeChildPackages").get_active()

    """
    Include child elements in list of objects.
    """
    def includeChildrenClicked(self):
        self.loadData()