import hou
import os, sys
from pathlib import Path
scripts = os.getenv('HOUDINI_SCRIPT_PATH')
SRC_PATH = str(scripts + '/USD_Megascan_Importer')

panel_file_path = SRC_PATH + "/pref/MS_USD_Converter.pypanel"
hou.pypanel.installFile(panel_file_path)