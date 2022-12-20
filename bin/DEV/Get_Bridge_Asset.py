import hou

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
