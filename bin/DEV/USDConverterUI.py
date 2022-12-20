from PySide2.QtWidgets import QMainWindow, QWidget, QStatusBar, QListWidget, QRadioButton, QFrame, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
import hou

class USD_UI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Megascan USD Asset Converter")
        self.LightGreyFont = QFont("Courier", 8)
        self._UI_ImportSection()
        self._createUI()

    #--------- UI MAIN ---------#       
    def _createUI(self):
        self.setStatusBar(QStatusBar(self))
        # Step 1
        PathPrefixLabel = QLabel("Set a Default Path Prefix for Asset Export Path")
        PathPrefixLabel.setStyleSheet( "font-size : 10pt; color: lightgrey; font-weight:bold;")
        self.SetPathPrefix = QLineEdit("$HIP/usd")
        self.SetPathPrefix.echoMode()
        self.SetPathPrefix.setAlignment(Qt.AlignHCenter)
        # pathPrefixVarSet = QListWidget("Edit List")

        PathPrefixLabel2 = QLabel("Default $HIP/usd would be good if you need to move around your Project.\n[TIP] You can set a $VAR = /MS_USD_Path and use it as a common USD Library Directory for Export")
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

        ## Path Layout
        LayHor1 = QHBoxLayout()
        LayHor1.addWidget(PathPrefixLabel)
        LayHor1.addStretch()
        LayHor1.addWidget(self.SetPathPrefix)
        # LayHor1.addWidget(pathPrefixVarSet)
    
        ## Final Layout
        FinalLayout = QHBoxLayout()
        FinalLayout.addWidget(self.help)
        FinalLayout.addWidget(self.convert)
        FinalLayout.setAlignment(self.help, Qt.AlignHCenter)
        FinalLayout.setAlignment(self.convert, Qt.AlignHCenter)

        ## Core Layout
        CoreLayout = QVBoxLayout()
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
        self.Variant = QRadioButton ("Variant Mesh")
        self.Split = QRadioButton ("Split Variant Mesh")
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
        
        
        self.ImportLayout = QVBoxLayout()
        self.ImportLayout.addWidget(ImportHeading)
        self.ImportLayout.setAlignment(ImportHeading, Qt.AlignHCenter)
        self.ImportLayout.addSpacing(10)
        self.ImportLayout.addWidget(label1)
        self.ImportLayout.addSpacing(10)
        self.ImportLayout.addWidget(label2)
        self.ImportLayout.addLayout(ButtonLayout)


    #--------- Choose Import Method ---------#
    def _updateImportMethod(self, data):
        if self.Single.isChecked():
            print("single")
        elif self.Variant.isChecked():
            print("Variant")
        elif self.Split.isChecked():
            print("Split")

    #--------- Help ---------#
    def help_was_clicked(self):
        print("help")
        self.H = HelpUI()
        self.H.show()

#--------- Help Widget Class---------#
class HelpUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Help - Megascan USD Asset Converter")

A = USD_UI()
A.show()