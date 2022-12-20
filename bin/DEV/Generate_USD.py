
"""
    STATUS: v01_01 Working
    Feature/Purpose: Should create texture nodes based on the dict
    
"""

import hou
ASSET_NAME = "Test"
ASSET_PATH = "/obj/geo1"
EXPORT_PATH = "$HIP/usd/assets"

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
asset_compGeo = Asset_Stager.createNode("componentgeometry", ASSET_NAME + "componentGeometry")
asset_compMat = Asset_Stager.createNode("componentmaterial", ASSET_NAME + "componentMaterial")
asset_matLib = Asset_Stager.createNode("materiallibrary", ASSET_NAME + "componentLibrary")
asset_compOut = Asset_Stager.createNode("componentoutput", ASSET_NAME + "componentoutput")

asset_compMat.setFirstInput(asset_compGeo)
asset_compMat.setNextInput(asset_matLib)
asset_compOut.setNextInput(asset_compMat)

Asset_Stager.layoutChildren()

box = Asset_Stager.createNetworkBox(ASSET_NAME)
box.setComment(ASSET_NAME)
box.addItem(asset_compGeo)
box.addItem(asset_compMat)
box.addItem(asset_matLib)
box.addItem(asset_compOut)
box.fitAroundContents()

i+=1
box.setPosition(hou.Vector2((i%5)*6,-(i//5)*5))
Asset_Stager.setUserData("nodeinfo_boxPos", str(i))

# Component Geometry
asset_compGeo_Inner = hou.node(asset_compGeo.path() + "/sopnet/geo")

obj_merge = asset_compGeo_Inner.createNode("object_merge")
obj_merge.parm("objpath1").set(ASSET_PATH)
hou.node(asset_compGeo.path() + "/sopnet/geo" + "/default").setNextInput(obj_merge)
polyreduce = obj_merge.createOutputNode("polyreduce::2.0")
polyreduce.parm("percentage").set(10)
hou.node(asset_compGeo.path() + "/sopnet/geo" + "/proxy").setNextInput(polyreduce)
hou.node(asset_compGeo.path() + "/sopnet/geo" + "/simproxy").setNextInput(polyreduce)

asset_compGeo_Inner.layoutChildren()

# Setting Component Output Parameters 
asset_compOut.parm("rootprim").set("/" + ASSET_NAME)
asset_compOut.parm("lopoutput").set(EXPORT_PATH + "/" + ASSET_NAME + "/" + asset_compOut.parm("filename").eval())
