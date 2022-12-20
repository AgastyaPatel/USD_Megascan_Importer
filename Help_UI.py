from PySide2.QtWidgets import QWidget, QLabel, QApplication
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

SRC_PATH = "M:\\Notes\\Tools\\USD_Megascan_Importer"

class HelpUI(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Help - Megascan USD Asset Converter")
        self.setWindowIcon(QIcon(SRC_PATH + "\\bin\\icons\\main.png"))

        self.setText("[TIP] You can set a $VAR = /MS_USD_Path and use it as a common USD Library Directory for Export")
