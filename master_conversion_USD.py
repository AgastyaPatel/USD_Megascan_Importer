import os, sys
from pathlib import Path
scripts = os.getenv('HOUDINI_SCRIPT_PATH')
SRC_PATH = str(scripts + '/USD_Megascan_Importer')
# varPath = "M:\\Notes\\Tools\\USD_Megascan_Importer"

from Get_Bridge_Asset_2 import MS_Asset_Data
from Get_Maps_v01_02 import Texture_Files
from MaterialXSubnet_v01_02 import create_MTLX_Subnet
from Generate_USD_02_Variant_Asset import USD_Asset_Builder


def mainSingle():   # Working

    if len(hou.selectedNodes()) == 0:
        hou.ui.displayMessage("Select a Megascan Imported Asset Subnet")
    else:
        if not MS_Asset_Data().Check_is_MS_Asset():
            hou.ui.displayMessage("Select a Megascan Imported Asset Subnet")
        else:
            ASSET_NAME, ASSET_PATH, ASSET_MAT_PATH =  MS_Asset_Data().SingleMeshData()
        
            prinShader = hou.node(ASSET_MAT_PATH)
            maps = Texture_Files().GetMapsFromNode(prinShader)
            
            MS = USD_Asset_Builder(ASSET_NAME, ASSET_PATH)
            MS.singleGeoImport()

            create_MTLX_Subnet(MS.asset_matLib, maps, ASSET_NAME)
            MS.setMeshExport()


def SOPVariants():  # 

    print(MS_Asset_Data().SOPvariantsData())
    if len(hou.selectedNodes()) == 0:
        hou.ui.displayMessage("Select a Megascan Imported Asset Subnet")
    else:
        if not MS_Asset_Data().Check_is_MS_Asset():
            hou.ui.displayMessage("Select a Megascan Imported Asset Subnet")
        else:
            ASSET_NAME, ASSET_PATH, ASSET_MAT_PATH, ASSET_ITER_RANGE =  MS_Asset_Data().SOPvariantsData()
            # l = MS_Asset_Data().SOPvariantsData()
            # print (l)
            
            prinShader = hou.node(ASSET_MAT_PATH)
            maps = Texture_Files().GetMapsFromNode(prinShader)

            MS = USD_Asset_Builder(ASSET_NAME, ASSET_PATH)
            MS.variantSOPsGeoImport(ASSET_ITER_RANGE)
            
            create_MTLX_Subnet(MS.asset_matLib, maps, ASSET_NAME)
            MS.setMeshExport()

def subSOPVariants():

    if len(hou.selectedNodes()) == 0:
        hou.ui.displayMessage("Select a Megascan Imported Asset Subnet")
    else:
        if not MS_Asset_Data().Check_is_MS_Asset():
            hou.ui.displayMessage("Select a Megascan Imported Asset Subnet")
        else:
            ASSET_NAME, ASSET_PATH, ASSET_MAT_PATH, ASSET_ITER_RANGE =  MS_Asset_Data().SubSOPvariantsData()
            print(ASSET_PATH)
            prinShader = hou.node(ASSET_MAT_PATH)
            maps = Texture_Files().GetMapsFromNode(prinShader)

            MS = USD_Asset_Builder(ASSET_NAME, ASSET_PATH)
            MS.variantSub_SOPGeoImport(ASSET_ITER_RANGE - 1)
            
            create_MTLX_Subnet(MS.asset_matLib, maps, ASSET_NAME)
            MS.setMeshExport()
