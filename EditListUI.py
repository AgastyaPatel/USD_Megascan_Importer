from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QLineEdit
import os, sys
from pathlib import Path
scripts = os.getenv('HOUDINI_SCRIPT_PATH')
SRC_PATH = str(scripts + '/USD_Megascan_Importer')
# SRC_PATH = "M:\\Notes\\Tools\\USD_Megascan_Importer"

class ExportPathVarUI(QWidget):
    def __init__(self, parentWidget):
        super().__init__()
        self._parent = parentWidget
        self._ui()

    def _ui(self):
        self.setWindowTitle("Path Variable")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setMaximumWidth()

        vbox = QVBoxLayout(self)
        self.listWidget = QListWidget()
        self.addVarLine = QLineEdit("Add Export Path Here")
        RemoveSelected = QPushButton("Remove Selected")
        Reset = QPushButton("Reset")
        Add = QPushButton("Add")
        Save = QPushButton("Save")
        
        RemoveSelected.clicked.connect(self.Remove_was_clicked)
        Reset.clicked.connect(self.Reset_was_clicked)
        Save.clicked.connect(self.Save_was_clicked)
        Add.clicked.connect(self.Add_was_clicked)

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox1.addWidget(self.addVarLine)
        hbox1.addWidget(Add)
        hbox2.addWidget(RemoveSelected)
        hbox2.addWidget(Reset)
        hbox2.addWidget(Save)

        self.listWidget.addItems(self._getList())       ## Reading all items

        self.listWidget.itemDoubleClicked.connect(self.onClicked)

        vbox.addWidget(self.listWidget)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

    def Reset_was_clicked(self):
        self.listWidget.clear()
        self.listWidget.addItem("$HIP/usd/assets")
    
    def Save_was_clicked(self, parentWidget):
        if self.listWidget.count() == 0:
            QMessageBox.critical(self, "Need atleast one Variable", "Export Path Variable list should atleast contain one variable. Reset if you want to continue with default path ($HIP/usd)")
        
        self._parent.SetPathPrefixCombo.clear() # clearing the combobox
        with open(self.exportPathPresetFile, "w") as file:
            for i in range(self.listWidget.count()):
                file.write((self.listWidget.item(i).text()) + ",")
                print(self.listWidget.item(i).text())
                self._parent.SetPathPrefixCombo.addItem(self.listWidget.item(i).text())
    
        print (self._parent.SetPathPrefixCombo.itemText(2))
        # # parentWidget.SetPathPrefixSelection.addItems(self._getList())

        self.close()

    def Remove_was_clicked(self):
        for i in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(i))

    def Add_was_clicked(self):
        if self.addVarLine.text() != "Add Export Path Here" and self.addVarLine.text().rstrip() != "":
            self.listWidget.addItem(self.addVarLine.text().strip())

    def onClicked(self, item):
        QMessageBox.information(self, "Info", item.text())

    def _getList(self):
        if not os.path.exists(SRC_PATH + "\\bin"):
            os.makedirs(SRC_PATH + "\\bin")
        if not os.path.exists(SRC_PATH + "\\bin\\preset"):
            os.makedirs(SRC_PATH + "\\bin\\preset")

        ## Create a default file if it doesn't exists
        self.exportPathPresetFile = SRC_PATH + "\\bin\\preset\\exportpath.csv"
        if not os.path.exists(self.exportPathPresetFile):
            print("it not exist")
            with open(self.exportPathPresetFile, "w") as file:
                file.write("$HIP/usd/assets,")
                # file.write("$JIP/USD,")

        ## Get List
        with open(self.exportPathPresetFile, "r") as file:
            for line in file:
                return line.split(",")[:-1]


def main():
    app = QApplication(sys.argv)
    ex = ExportPathVarUI()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()