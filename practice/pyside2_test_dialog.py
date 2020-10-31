from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        #create the window
        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        #Create calls Methods
        self.create_widget()
        self.create_layouts()
        self.create_conections()


    def create_widget(self):
    	self.lineedit = QtWidgets.QLineEdit()
    	self.checkbox1 = QtWidgets.QCheckBox()
    	self.checkbox2 = QtWidgets.QCheckBox()
    	self.ok_btn = QtWidgets.QPushButton("OK")
    	self.cancel_btn = QtWidgets.QPushButton("Cancel")


    def create_layouts(self):
        #form layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('Name: ',self.lineedit)
        form_layout.addRow('Hidde: ',self.checkbox1)
        form_layout.addRow('Locked: ',self.checkbox2)

        #buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)

        #main layout
    	main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
    

    def create_conections(self):
        self.lineedit.editingFinished.connect(self.print_hello_name)
        self.checkbox1.toggled.connect(self.print_is_hidden)
        self.cancel_btn.clicked.connect(self.close)
    

    def print_hello_name(self):
        name = self.lineedit.text()
        print('Hello, {0}'.format(name))


    def print_is_hidden(self):
        hidden = self.checkbox1.isChecked()
        if hidden:
            print("Hidden")
        else:
            print("Visible")
        


if __name__ == "__main__":

    try:
        test_dialog.close() #pylint: disable = E0601
        test_dialog.deleteLater()
    except:
        pass
    
    test_dialog = TestDialog()
    test_dialog.show()
   	