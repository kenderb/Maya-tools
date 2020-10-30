from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TableExampleDialog(QtWidgets.QDialog):
    ATTR_ROLE = QtCore.Qt.UserRole
    VALUE_ROLE = QtCore.Qt.UserRole + 1

    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = TableExampleDialog()
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(TableExampleDialog, self).__init__(parent)

        self.setWindowTitle("Table Example")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(500)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        # Inner table creation widgets
        self.table_wdg = QtWidgets.QTableWidget()
        self.table_wdg.setColumnCount(5)
        self.table_wdg.setColumnWidth(0, 22)
        self.table_wdg.setColumnWidth(2, 70)
        self.table_wdg.setColumnWidth(3, 70)
        self.table_wdg.setColumnWidth(4, 70)
        self.table_wdg.setHorizontalHeaderLabels(["", "Name", "TansX", "TransY", "TransZ"])
        header_view = self.table_wdg.horizontalHeader()
        header_view.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        #buttons Creation widgets
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.table_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close)
    
    def showEvent(self, e):
        super(TableExampleDialog, self).showEvent(e)
        self.refresh_table()

    def refresh_table(self):
        self.table_wdg.setRowCount(0)

        meshes = cmds.ls(type="mesh")
        for i in range(len(meshes)):
            transform_name = cmds.listRelatives(meshes[i], parent=True)[0]
            translation = cmds.getAttr("{0}.translate".format(transform_name))[0]
            visible = cmds.getAttr("{0}.visibility".format(transform_name))

            self.table_wdg.insertRow(i)
            self.insert_item(i, 0, "", "Visibility", visible, True)
            self.insert_item(i, 1, transform_name, None, transform_name, False)
            self.insert_item(i, 2, self.float_to_string(translation[0]), "tx", translation[0], False)
            self.insert_item(i, 3, self.float_to_string(translation[1]), "ty", translation[1], False)
            self.insert_item(i, 4, self.float_to_string(translation[2]), "tz", translation[2], False)
    
    def insert_item(self, row, colum, text, attr, value, is_boolean):
        item = QtWidgets.QTableWidgetItem(text)
        self.set_item_attr(item, attr)
        self.set_item_value(item, value)
        if is_boolean:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.set_item_checked(item, value)

        self.table_wdg.setItem(row, colum, item) 
    
    def set_item_text(self, item, text):
        item.setText(text)
    
    def get_item_tex(self, item):
        return item.text()
    
    def set_item_checked(self, item, checked):
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)
    
    def is_item_checked(self, item):
        return item.checkState() == QtCore.Qt.Checked
    
    def set_item_attr(self, item, attr):
        item.setData(self.ATTR_ROLE, attr)
    
    def get_item_attr(self, item):
        return item.data(self.ATTR_ROLE)
    
    def set_item_value(self, item, value):
        item.setData(self.VALUE_ROLE, value)
    
    def get_item_value(self, item):
        return item.data(self.VALUE_ROLE)

    def float_to_string(self, value):
        return "{0:.4f}".format(value)



if __name__ == "__main__":

    try:
        table_example_dialog.close() # pylint: disable=E0601
        table_example_dialog.deleteLater()
    except:
        pass

    table_example_dialog = TableExampleDialog()
    table_example_dialog.show()
