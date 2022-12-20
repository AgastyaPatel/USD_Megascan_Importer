import hou

class USD_Asset_Builder():
    def __init__(self, asset_name, asset_path, export_prefix= "$HIP/usd/assets"):
        self.ASSET_NAME = asset_name
        self.ASSET_PATH = asset_path
        self.EXPORT_PATH = export_prefix
        # self.ASSET_NAME = ASSET_NAME
    ## Check if the asset Stager Exists and use it if it does
        if hou.node("/stage/MS_Asset_USD_Processor") == None:
            Asset_Stager = hou.node("/stage").createNode("lopnet", "MS_Asset_USD_Processor")
            Asset_Stager.setUserData("nodeinfo_boxPos", "0")
            self.i = int(Asset_Stager.userData("nodeinfo_boxPos"))
            print("i = ", self.i)
        else:
            print("Asset is being imported in /stage/MS_Asset_USD_Processor")
            Asset_Stager = hou.node("/stage/MS_Asset_USD_Processor")
            self.i = int(Asset_Stager.userData("nodeinfo_boxPos"))
            print("i = ", self.i)
        
        self.Stager = Asset_Stager

        ## Create a basic component builder
        self.asset_compGeo = Asset_Stager.createNode("componentgeometry", self.ASSET_NAME + "_cGeo")
        self.asset_compMat = Asset_Stager.createNode("componentmaterial", self.ASSET_NAME + "_cMat")
        self.asset_matLib = Asset_Stager.createNode("materiallibrary", self.ASSET_NAME + "_cMLib")
        self.asset_compOut = Asset_Stager.createNode("componentoutput", self.ASSET_NAME + "_cOut")

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

        self.Stager_nodes = [self.asset_compGeo, self.asset_compMat, self.asset_compOut, self.asset_matLib]
        
        

        ## Set Network Box
    def _create_netBox(self, *args):
        self.Stager.layoutChildren()

        self.netbox = self.Stager.createNetworkBox(self.ASSET_NAME)
        self.netbox.setComment(self.ASSET_NAME)
        
        for arg in args:
            self.netbox.addItem(arg)

        self.netbox.fitAroundContents()

        self.i+=1
        self.netbox.setPosition(hou.Vector2((self.i%5)*8,-(self.i//5)*8))
        self.Stager.setUserData("nodeinfo_boxPos", str(self.i))
        
    #-----------------------------------------------------------#
    # Set Single Mesh Export
    def setMeshExport(self, IndividualVarLayer = False):
        """Class Method sets file paths for exports and runs the export commands
        IndividualVarLayer creates individual variant Layers for LAG 
        """
        if IndividualVarLayer:
            self.asset_compOut.parm("variantlayers").set(True)

        # Setting Component Output Parameters 
        self.asset_compOut.parm("rootprim").set("/" + self.ASSET_NAME)
        self.asset_compOut.parm("lopoutput").set(self.EXPORT_PATH + "/" + self.ASSET_NAME + "/" + self.asset_compOut.parm("filename").eval())
        
        buttonPath = self.asset_compOut.path() + "/execute"
        hou.parm(buttonPath).pressButton()
        
        buttonPath = self.asset_compOut.path() + "/addtogallery"
        hou.parm(buttonPath).pressButton()
        self.asset_compOut.parm("loadfromdisk").set(True)
    
    #-----------------------------------------------------------#    
    # Sets the Object import into the Component Geometry
    def singleGeoImport(self, meshPath = None, asst_comp_geo = None, polyreducepercent = 10, netbox = True):
        """
        asst_comp_geo by default is set to Stager compGeo1
        meshPath by default set to self.ASSET_PATH
        polyreducepercent = 10
        netBox = True : Creates a netbox by default.
        """  
        if asst_comp_geo is None:
            asst_comp_geo = self.asset_compGeo

        if meshPath is None:
            meshPath = self.ASSET_PATH
            
        # Component Geometry
        asset_compGeo_Inner = hou.node(asst_comp_geo.path() + "/sopnet/geo")

        obj_merge = asset_compGeo_Inner.createNode("object_merge")
        obj_merge.parm("objpath1").set(meshPath)
        hou.node(asst_comp_geo.path() + "/sopnet/geo" + "/default").setNextInput(obj_merge)
        polyreduce = obj_merge.createOutputNode("polyreduce::2.0")
        polyreduce.parm("percentage").set(polyreducepercent)
        hou.node(asst_comp_geo.path() + "/sopnet/geo" + "/proxy").setNextInput(polyreduce)
        hou.node(asst_comp_geo.path() + "/sopnet/geo" + "/simproxy").setNextInput(polyreduce)

        asset_compGeo_Inner.layoutChildren()
        if netbox:
            self._create_netBox(*self.Stager_nodes)
    

    def variantSOPsGeoImport(self, iterLength):
        """Mesh with Multiple LOD0 SOP"""
        for_start = self.asset_compGeo.createOutputNode("begincontextoptionsblock", self.ASSET_NAME + "_forStart")
        asset_compGeo2 = self.Stager.createNode("componentgeometry", self.ASSET_NAME + "_cGeoVarImports")
        compGeoVariants = for_start.createOutputNode("componentgeometryvariants", self.ASSET_NAME + "_cGeoVar")
        compGeoVariants.setNextInput(asset_compGeo2)
        for_end = self.Stager.createNode("foreach", self.ASSET_NAME + "_forEnd")
        for_end.setInput(2, compGeoVariants)
        setVariant = for_end.createOutputNode("setvariant")
        setVariant.setGenericFlag(hou.nodeFlag.Bypass, True)
        self.asset_compMat.insertInput(0, setVariant)
        
        self.asset_compGeo.parm("geovariantname").set("Var1")
        asset_compGeo2.parm("geovariantname").set("Var`@ITERATIONVALUE`")
        
        for_end.parm("iterations").set(100)
        for_end.parm("iterrange").set("range")
        for_end.parm("firstiteration").set(2)
        for_end.parm("lastiteration").set(iterLength)

        self.Stager_nodes.extend([for_start, asset_compGeo2, compGeoVariants, for_end, setVariant])

        # Setting the compGeo1
        self.singleGeoImport(meshPath = (self.ASSET_PATH + "/Var1_LOD0"), netbox= False)
        # Setting the compGeo1

        self.singleGeoImport((self.ASSET_PATH + "/`chsop(\"../../../geovariantname\")`_LOD0"), asset_compGeo2)
    
    def variantSub_SOPGeoImport(self, iterLength):
        """Mesh with Multiple LOD0 SOP"""
        for_start = self.asset_compGeo.createOutputNode("begincontextoptionsblock", self.ASSET_NAME + "_forStart")
        asset_compGeo2 = self.Stager.createNode("componentgeometry", self.ASSET_NAME + "_cGeoVarImports")
        compGeoVariants = for_start.createOutputNode("componentgeometryvariants", self.ASSET_NAME + "_cGeoVar")
        compGeoVariants.setNextInput(asset_compGeo2)
        for_end = self.Stager.createNode("foreach", self.ASSET_NAME + "_forEnd")
        for_end.setInput(2, compGeoVariants)
        setVariant = for_end.createOutputNode("setvariant")
        setVariant.setGenericFlag(hou.nodeFlag.Bypass, True)
        self.asset_compMat.insertInput(0, setVariant)
        
        self.asset_compGeo.parm("geovariantname").set("Var1")
        asset_compGeo2.parm("geovariantname").set("Var`@ITERATIONVALUE`")
        
        for_end.parm("iterations").set(100)
        for_end.parm("iterrange").set("range")
        for_end.parm("firstiteration").set(0)
        for_end.parm("lastiteration").set(iterLength)

        self.Stager_nodes.extend([for_start, asset_compGeo2, compGeoVariants, for_end, setVariant])

        # Setting the compGeo1
        self.singleGeoImport(meshPath = (self.ASSET_PATH + "/*_00_LOD0"), netbox= False)
        # Setting the compGeo1

        self.singleGeoImport((self.ASSET_PATH + "/*_`padzero(2, @ITERATIONVALUE)`_LOD0"), asset_compGeo2)
