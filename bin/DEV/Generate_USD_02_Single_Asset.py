
"""
    STATUS: v01_01 Working
    Feature/Purpose: Should create texture nodes based on the dict
    
"""

import hou, sys
varPath = "M:\\Notes\\Tools\\USD_Megascan_Importer"
sys.path.append(varPath)

from MaterialXSubnet_v01_02 import create_MTLX_Subnet
from Get_Maps_v01_02 import Texture_Files
#-----------------------------------------------------------#
# Get Bridge Asset
def get_AssetGeo(asset):
    for child in asset_name.children():
        if child.name() == "Asset_Geometry":
            return child

def get_AssetMat(asset):
    for child in asset_name.children():
        if child.name() == "Asset_Material":
            return child

if len(hou.selectedNodes())==0:
    hou.ui.displayMessage("Please Select a MS Subnet")
else:
    asset_name = hou.selectedNodes()[0]
    ms_geo = get_AssetGeo(asset_name)
    ms_shader = get_AssetMat(asset_name).children()
    
    print(ms_geo, ms_geo.path(), ms_shader[0])

    ASSET_NAME = str(asset_name)
    ASSET_PATH = ms_geo.path()
    tx = Texture_Files()
    maps = tx.GetMapsFromNode(ms_shader[0])
#-----------------------------------------------------------#    

# ASSET_NAME = "Test"
# ASSET_PATH = "/obj/pig"
EXPORT_PATH = "$HIP/usd/assets"

class USD_Asset_Builder():
    def __init__(self):
    ## Check if the asset Stager Exists and use it if it does
        if hou.node("/stage/MS_Asset_USD_Processor") == None:
            Asset_Stager = hou.node("/stage").createNode("lopnet", "MS_Asset_USD_Processor")
            Asset_Stager.setUserData("nodeinfo_boxPos", "0")
            i = int(Asset_Stager.userData("nodeinfo_boxPos"))
            print("i = ", i)
        else:
            print("Asset is being imported in /stage/MS_Asset_USD_Processor")
            Asset_Stager = hou.node("/stage/MS_Asset_USD_Processor")
            i = int(Asset_Stager.userData("nodeinfo_boxPos"))
            print("i = ", i)

        ## Create a basic component builder
        self.asset_compGeo = Asset_Stager.createNode("componentgeometry", ASSET_NAME + "_cGeo")
        self.asset_compMat = Asset_Stager.createNode("componentmaterial", ASSET_NAME + "_cMat")
        self.asset_matLib = Asset_Stager.createNode("materiallibrary", ASSET_NAME + "_cMLib")
        self.asset_compOut = Asset_Stager.createNode("componentoutput", ASSET_NAME + "_cOut")

        self.asset_compMat.setFirstInput(self.asset_compGeo)
        self.asset_compMat.setNextInput(self.asset_matLib)
        self.asset_compOut.setNextInput(self.asset_compMat)
        self.asset_compMat.setGenericFlag(hou.nodeFlag.Display, True)
        # time.sleep(3)
        self.asset_compOut.setGenericFlag(hou.nodeFlag.Display, True)

        
        # Global Component Output Settings
        self.asset_matLib.parm("matpathprefix").set("/ASSET/mtl/")
        self.asset_compMat.parm("variantname").set("Default_MS_Mat")
        self.asset_compMat.parm("primpattern1").set("*")
        self.asset_compOut.parm("thumbnailmode").set(2)
        self.asset_compOut.parm("res1").set(256)
        self.asset_compOut.parm("res2").set(256)
        self.asset_compOut.parm("autothumbnail").set(True)

        Asset_Stager.layoutChildren()

        ## Set Network Box
        box = Asset_Stager.createNetworkBox(ASSET_NAME)
        box.setComment(ASSET_NAME)
        box.addItem(self.asset_compGeo)
        box.addItem(self.asset_compMat)
        box.addItem(self.asset_matLib)
        box.addItem(self.asset_compOut)
        box.fitAroundContents()

        i+=1
        box.setPosition(hou.Vector2((i%5)*6,-(i//5)*5))
        Asset_Stager.setUserData("nodeinfo_boxPos", str(i))
        
    #-----------------------------------------------------------#    
    # Sets the Object import into the Component Geometry
    def singleGeoImport(self):  
        # Component Geometry
        asset_compGeo_Inner = hou.node(self.asset_compGeo.path() + "/sopnet/geo")

        obj_merge = asset_compGeo_Inner.createNode("object_merge")
        obj_merge.parm("objpath1").set(ASSET_PATH)
        hou.node(self.asset_compGeo.path() + "/sopnet/geo" + "/default").setNextInput(obj_merge)
        polyreduce = obj_merge.createOutputNode("polyreduce::2.0")
        polyreduce.parm("percentage").set(10)
        hou.node(self.asset_compGeo.path() + "/sopnet/geo" + "/proxy").setNextInput(polyreduce)
        hou.node(self.asset_compGeo.path() + "/sopnet/geo" + "/simproxy").setNextInput(polyreduce)

        asset_compGeo_Inner.layoutChildren()
    
    #-----------------------------------------------------------#
    # Set Single Mesh Export
    def setSingleMeshExport(self):
        # Setting Component Output Parameters 
        self.asset_compOut.parm("rootprim").set("/" + ASSET_NAME)
        self.asset_compOut.parm("lopoutput").set(EXPORT_PATH + "/" + ASSET_NAME + "/" + self.asset_compOut.parm("filename").eval())
        # time.sleep(1)
        buttonPath = self.asset_compOut.path() + "/execute"
        hou.parm(buttonPath).pressButton()
        # time.sleep(1)
        buttonPath = self.asset_compOut.path() + "/addtogallery"
        hou.parm(buttonPath).pressButton()
        self.asset_compOut.parm("loadfromdisk").set(True)

MS = USD_Asset_Builder()
MS.singleGeoImport()
create_MTLX_Subnet(MS.asset_matLib, maps, ASSET_NAME)
MS.setSingleMeshExport()
