import os, sys
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import (QComboBox, QFrame, QHBoxLayout, QLabel,
                               QLineEdit, QListWidget, QMainWindow,
                               QMessageBox, QPushButton, QRadioButton,
                               QStatusBar, QVBoxLayout, QWidget, QCheckBox, QApplication)

SRC_PATH = "M:\\Notes\\Tools\\USD_Megascan_Importer"

sys.path.append(SRC_PATH)
from EditListUI import ExportPathVarUI
from Help_UI import HelpUI
import master_conversion_USD 

class USD_UI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Megascan USD Asset Converter")
        
        self.setWindowIcon(QIcon(SRC_PATH + "\\bin\\icons\\main.png"))
        self.LightGreyFont = QFont("Courier", 8)
        self._UI_ImportSection()
        self._createUI()

    #--------- UI MAIN ---------#       
    def _createUI(self):
        self.setStatusBar(QStatusBar(self))
        # Step 1
        PathPrefixLabel = QLabel("Set a Default Path Prefix for Asset Export Path")
        PathPrefixLabel.setStyleSheet( "font-size : 10pt; color: lightgrey; font-weight:bold;")

        self.SetPathPrefixCombo = QComboBox()
        self.SetPathPrefixCombo.setFixedWidth(200)
        self.EditPathWindow = ExportPathVarUI(self)

        self.SetPathPrefixCombo.addItems(self.EditPathWindow._getList())
        
        EditPathSet = QPushButton("Edit List")
        EditPathSet.clicked.connect(self.EditList_was_clicked)

        PathPrefixLabel2 = QLabel("Default $HIP/usd/assets would be good if you need to move around your Project")
        PathPrefixLabel2.setWordWrap(True)
        PathPrefixLabel2.setFont(self.LightGreyFont)

        # Step 2
        HLine = QFrame()
        HLine.setFrameShape(QFrame.HLine)
        Frame1 = QFrame()
        Frame1.setFrameShape(QFrame.Box)

        self.convert = QPushButton("Convert into USD")
        self.convert.setStyleSheet("color: rgb(0, 255, 155);")
        self.help = QPushButton("Help")
        self.help.setStyleSheet("color: rgb(255, 80, 80);")
        self.help.clicked.connect(self.help_was_clicked)
        self.convert.clicked.connect(self.convert_was_clicked)

        ## Path Layout
        LayHor1 = QHBoxLayout()
        LayHor1.addStretch()
        LayHor1.addWidget(self.SetPathPrefixCombo)
        LayHor1.addStretch()
        LayHor1.addWidget(EditPathSet)
        LayHor1.addStretch()
        
    
        ## Final Layout
        FinalLayout = QHBoxLayout()
        FinalLayout.addWidget(self.help)
        FinalLayout.addWidget(self.convert)
        FinalLayout.setAlignment(self.help, Qt.AlignHCenter)
        FinalLayout.setAlignment(self.convert, Qt.AlignHCenter)

        ## Core Layout
        CoreLayout = QVBoxLayout()
        CoreLayout.addWidget(PathPrefixLabel)
        CoreLayout.addLayout(LayHor1)
        CoreLayout.addWidget(PathPrefixLabel2)
        CoreLayout.addWidget(HLine)
        CoreLayout.addSpacing(20)
        CoreLayout.addLayout(self.ImportLayout)
        CoreLayout.addSpacing(20)
        CoreLayout.addLayout(FinalLayout)
        CoreLayout.addStretch()

        Container = QWidget()
        Container.setLayout(CoreLayout)

        self.setCentralWidget(Container)
    
    #--------- UI Import Section ---------#   
    def _UI_ImportSection(self):

        label1 = QLabel("1. Import Megascan Asset Using Bridge and MSPlugin and select the *Asset Subnet*.")
        ImportHeading = QLabel("Import Settings")
        ImportHeading.setStyleSheet( "font-size : 10pt; color: lightgrey; font-weight:bold;")
        label2 = QLabel("2. Select One of the Import Method.")

        self.Single = QRadioButton ("Single Mesh")
        self.Variant = QRadioButton ("Multiple Variant Mesh LOD0 SOPS")
        self.Split = QRadioButton ("Sub-Split Variant Meshes inside LOD0")
        self.Single.toggled.connect(self._updateImportMethod)
        self.Variant.toggled.connect(self._updateImportMethod)
        self.Split.toggled.connect(self._updateImportMethod)
        self.Single.setStatusTip("Creates Single Asset for Single Mesh")
        self.Variant.setStatusTip("Creates Individual Asset for each of the collection Items of Single Meshes.")
        self.Split.setStatusTip("Creates Single Asset containing all variant of each collection items.")

        ## Method Radio Buttons
        ButtonLayout = QHBoxLayout()
        ButtonLayout.addStretch()
        ButtonLayout.addWidget(self.Single)
        ButtonLayout.addWidget(self.Variant)
        ButtonLayout.addWidget(self.Split)
        ButtonLayout.addStretch()
        
        self.RenderVariantLayers = QCheckBox("Render Variants Individually?")
        
        self.ImportLayout = QVBoxLayout()
        self.ImportLayout.addWidget(ImportHeading)
        self.ImportLayout.setAlignment(ImportHeading, Qt.AlignHCenter)
        self.ImportLayout.addSpacing(10)
        self.ImportLayout.addWidget(label1)
        self.ImportLayout.addSpacing(10)
        self.ImportLayout.addWidget(label2)
        self.ImportLayout.addLayout(ButtonLayout)
        self.ImportLayout.addSpacing(10)
        self.ImportLayout.addWidget(self.RenderVariantLayers)
        self.ImportLayout.setAlignment(self.RenderVariantLayers, Qt.AlignHCenter)


    #--------- Choose Import Method ---------#
    def _updateImportMethod(self, data):
        if self.Single.isChecked():
            self.RenderVariantLayers.setEnabled(False)
            self.RenderVariantLayers.setChecked(False)
        elif self.Variant.isChecked():
            self.RenderVariantLayers.setEnabled(True)
        elif self.Split.isChecked():
            self.RenderVariantLayers.setEnabled(True)

    #--------- Help ---------#
    def convert_was_clicked(self):
        rnderVariants = self.RenderVariantLayers.isChecked()
        
        ExportPrefix = self.SetPathPrefixCombo.currentText()

        if self.Single.isChecked():
            master_conversion_USD.mainSingle(ExportPrefix)
            print("single")
        elif self.Variant.isChecked():
            master_conversion_USD.SOPVariants(ExportPrefix, rnderVariants)
            print("Variant")
        elif self.Split.isChecked():
            master_conversion_USD.subSOPVariants(ExportPrefix, rnderVariants)
            print("Split")
    
    #--------- Help ---------#
    def help_was_clicked(self):
        print("help")
        self.H = HelpUI()
        self.H.show()
    
    def EditList_was_clicked(self):
        self.EditPathWindow.show()


def main():
    # app = QApplication()
    A = USD_UI()
    A.show()
    # app.exec_()

# if __name__ == '__main__':
#     main()

main()