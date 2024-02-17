import hou
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton
from PySide2.QtGui import QIcon

import os, sys, webbrowser
scripts = os.getenv('HOUDINI_SCRIPT_PATH')
SRC_PATH = str(scripts + '/USD_Megascan_Importer')

class HelpUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help/Support")
        layout = QVBoxLayout()

        self.setWindowTitle("Help - Megascan USD Asset Converter")
        self.setWindowIcon(QIcon(SRC_PATH + "\\bin\\icons\\help.png"))
        
        label1 = QLabel("Kindly support the creator by giving Star ⭐ to the repository")
        self.docBtn = QPushButton('Open Documentation')
        self.support = QPushButton('Give Star ⭐')
        contact = QLabel('AgastyaPatel on LinkedIn/Github\n Email: contact2agastya@gmail.com')
        
        self.docBtn.clicked.connect(self.open_doc)
        self.support.clicked.connect(self.support_exec)
        
        layout.addWidget(label1)
        layout.addWidget(self.docBtn)
        layout.addWidget(self.support)
        layout.addSpacing(20)
        layout.addWidget(contact)
        self.setLayout(layout)
        
    def open_doc(self):
        webbrowser.open('https://agastyapatel.github.io/USD_Megascan_Importer/')

    def support_exec(self):
        webbrowser.open('https://github.com/AgastyaPatel/USD_Megascan_Importer')
        
def main():
    dialog = HelpUI()
    dialog.show()
