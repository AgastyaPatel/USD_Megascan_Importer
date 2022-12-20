import hou

class MS_Asset():
    """
    This Class only returns the path of the MS Asset Geometry(s), MS Asset Material or Number of Variants
    """
    def __init__(self):
            self.ms_asset = hou.selectedNodes()[0]

    def __str__(self):
        return str(self.ms_asset)

    #--------- Asset Name---------#
    def get_MS_name(self):
        return str(self.ms_asset)
    
    #--------- Asset Path---------#
    def get_MS_Path(self):
        return self.ms_asset.path()

    #--------- Get MS Asset Single Geo Node ---------#
    def get_SingleMeshAssetGeo(self):
        """Return the Geo Node inside MS asset Subnet"""
        for child in self.ms_asset.children():
            if child.name() == "Asset_Geometry":
                return child.path()

    #--------- Get MS Asset Mat Node ---------#
    def get_AssetMat(self):
        """Return the Mat Node inside MS asset Subnet"""
        for child in self.ms_asset.children():
            if child.name() == "Asset_Material":
                return child.children()[0].path()
    
    #--------- Get MS Asset Single Geo Node ---------#
    def get_SOPVariantMeshesGeo(self):
        """Return the inside MS asset Subnet's SOP based LOD0 variants"""

        newChildrenList = []    # LOD0 SOPS meshes are added in this list
        children = self.ms_asset.children()
        
        for i in range(len(children)):
            if str(children[i]).rfind("_LOD0") != -1:   # -1 if not found
                newChildrenList.append(children[i])
        
        return len(newChildrenList)
                
    #--------- Get MS Asset Single Geo Node ---------#
    def get_SubSOPVariantMeshesGeo(self):
        """Returns the number of subSop LOD0 variants"""

        newChildrenList = []    # _LOD0 nulls from _LOD0 SOP meshes are added in this list
        children = hou.node(self.ms_asset.path() + "/lod0").children()

        for i in range(len(children)):
            if str(children[i]).rfind("_LOD0") != -1:   # -1 if not found
                newChildrenList.append(children[i])
        return len(newChildrenList)
        

class MS_Asset_Data(MS_Asset):
    def __init__(self):
        super().__init__()


    def Check_is_MS_Asset(self):
        if self.get_AssetMat() == None:
            check = False
        else:
            check = True

        return check
        
    def SingleMeshData(self):
        """Returns (AssetName, Asset_Geo_Path, Asset_Mat_Path)"""
        
        self.MS_Name = self.get_MS_name()
        self.MS_GeoPath = self.get_SingleMeshAssetGeo()
        self.MS_MatPath = self.get_AssetMat()

        return(self.MS_Name, self.MS_GeoPath, self.MS_MatPath)
    
    def SOPvariantsData(self):
        """Returns (AssetName, Asset_Geo_Path, Asset_Mat_Path, IterationRange)"""
        
        self.MS_Name = self.get_MS_name()
        self.MS_GeoPath = self.get_MS_Path()
        self.MS_MatPath = self.get_AssetMat()
        self.IterationRange = self.get_SOPVariantMeshesGeo()

        return(self.MS_Name, self.MS_GeoPath, self.MS_MatPath, self.IterationRange)

    def SubSOPvariantsData(self):
        """Returns (AssetName, Asset_Geo_Path, Asset_Mat_Path, IterationRange)"""
        
        self.MS_Name = self.get_MS_name()
        self.MS_GeoPath = self.get_MS_Path() + "/lod0"
        self.MS_MatPath = self.get_AssetMat()
        self.IterationRange = self.get_SubSOPVariantMeshesGeo()

        return(self.MS_Name, self.MS_GeoPath, self.MS_MatPath, self.IterationRange)


# print(MS_Asset_Data().Check_is_MS_Asset())