from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from create_mtl import CreateShadingNodes

import maya.OpenMaya as om
import maya.OpenMayaUI as oumi
import maya.cmds as cmds

def maya_main_window():
    """
    Retur the Maya main Window Widget as a Python Object
    """
    main_window_ptr = oumi.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class CreateMaterialDialog(QtWidgets.QDialog):

    FILE_FITERS = "png (*.png);;jpg (*.jpg);;exr (*.exr);;tif (*.tif);;All Files (*.*)"

    selected_filter = "image (*.jpg *.png *.tif *.exr)"

    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = CreateMaterialDialog()
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(CreateMaterialDialog, self).__init__(parent)

        self.setWindowTitle("Create Material")
        self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.filepath_le = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton()
        self.select_file_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.select_file_path_btn.setToolTip("Open folder")

        self.apply_btn = QtWidgets.QPushButton('Create')
        self.close_btn = QtWidgets.QPushButton('Close')
    
    def create_layout(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filepath_le)
        file_path_layout.addWidget(self.select_file_path_btn)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('Folder:', file_path_layout)
 
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)             
    
    def create_connections(self):
        self.select_file_path_btn.clicked.connect(self.show_file_select_dialog)

        self.apply_btn.clicked.connect(self.load_file)
        self.close_btn.clicked.connect(self.close)
    
    def show_file_select_dialog(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", self.FILE_FITERS, self.selected_filter )
        
        if file_path:
            self.filepath_le.setText(file_path)

    def load_file(self):
        file_path = self.filepath_le.text()
        if file_path:
            status_mode = CreateShadingNodes.createmtl(file_path)
            print(status_mode)
        else:
            print ("ERROR: Select a image file")

        file_info = QtCore.QFileInfo(file_path)
        
if __name__ == "__main__":
    try:
        open_import_dialog.close() #pylint: disable=E0601
        open_import_dialog.deleteLater()
    except:
        pass    
    open_import_dialog = CreateMaterialDialog()
    open_import_dialog.show()