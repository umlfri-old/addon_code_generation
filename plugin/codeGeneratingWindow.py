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

    """
    Shows code generating window.
    """
    def show(self):
        self.__window.show_all()

    """
    Loads data (visual elements in diagram) to object list.
    """
    def loadData(self):
        self.__gtkBuilder.get_object("objectView").get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        elementList = self.__gtkBuilder.get_object("objectView").get_model()
        elementList.clear()
        self.__elements = []
        index = 0
        for element in self.__i.current_diagram.elements:
            elementList.append([element.object.name, element.object.type.name, index])
            index += 1
            self.__elements.append(element.object)

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