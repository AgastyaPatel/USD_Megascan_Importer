"""
    STATUS: V01_02 Working
    Feature/Purpose: Should create texture nodes based on the dict
    
"""
import hou
# print("----------------------------")
# hou.node("/obj").deleteItems(hou.node("/obj").children())


#-----------------------------------------------------------#
# Create MaterialX Subnet

def create_MTLX_Subnet(matcontext, mapsDict, matXName = "Converted"):
    """
    :param matContext: Dest Path for creating materialX subnet
    :type matContext: matnet

    :param mapsDict: Dest Path for creating materialX subnet
    :type mapsDict: Dictionary

    :raise TypeError: if not a matnet object
    :rtype: Boolean
    """

    # Removing any whitespaces characters
    for tex in mapsDict:
       mapsDict[tex] = mapsDict[tex].strip()
    #    print(mapsDict[tex])
    
    print("matcontex : " + matcontext.type().name())
    if (matcontext.type().name() != "matnet" and matcontext.type().name() != "materiallibrary" and matcontext.type().name() != "assignmaterial" and matcontext.type().name() != "editmaterial"):
        print("ERROR :create_MTLX_Subnet requires Matnet/ materiallibrary/ assignmaterial/ editmaterial Object as input for create_MTLX_Subnet")
        return False

    mtlxSubnet = matcontext.createNode("subnet", matXName + "_materialX")

    children = mtlxSubnet.allSubChildren()
    mtlxSubnet.deleteItems(children)
    
    # Define Outer Surface
    surfaceOutput = mtlxSubnet.createNode("subnetconnector")
    surfaceOutput.setName("Surface_Output")
    surfaceOutput.parm("connectorkind").set("output")
    surfaceOutput.parm("parmname").set("surface")
    surfaceOutput.parm("parmlabel").set("surface")
    surfaceOutput.parm("parmtype").set("surface")
    

    # Discplacement Output
    displacementOutput = mtlxSubnet.createNode("subnetconnector")
    displacementOutput.setName("Displacement_Output")
    displacementOutput.parm("connectorkind").set("output")
    displacementOutput.parm("parmname").set("Displacement")
    displacementOutput.parm("parmlabel").set("Displacement")
    displacementOutput.parm("parmtype").set("displacement")
    
    # Mtlx_Standard_Surface
    mtlxStandard = mtlxSubnet.createNode("mtlxstandard_surface")
    surfaceOutput.setInput(0, mtlxStandard)

    IMG_TEX_NODE = "mtlximage"


    # Albedo
    if len(mapsDict["alb"]) > 0:
        albedo = mtlxSubnet.createNode(IMG_TEX_NODE, "Albedo")
        albedo.parm("file").set(mapsDict["alb"])
        mtlxStandard.setNamedInput("base_color", albedo, "out")

    # Roughness
    if len(mapsDict["rough"]) > 0:
        roughness = mtlxSubnet.createNode(IMG_TEX_NODE, "Roughness")
        roughness.parm("signature").set("float")
        roughness.parm("file").set(mapsDict["rough"])
        mtlxStandard.setNamedInput("specular_roughness", roughness, "out")

    # Metallic
    if len(mapsDict["metal"]) > 0:
        metallic = mtlxSubnet.createNode(IMG_TEX_NODE, "Metallic")
        metallic.parm("signature").set("float")
        metallic.parm("file").set(mapsDict["metal"])
        mtlxStandard.setNamedInput("metalness", metallic, "out")

    # SPECULAR
    if len(mapsDict["spec"]) > 0:
        specular = mtlxSubnet.createNode(IMG_TEX_NODE, "Specular")
        specular.parm("signature").set("float")
        specular.parm("file").set(mapsDict["spec"])
        mtlxStandard.setNamedInput("specular", specular, "out")

    #OPACITY 
    if len(mapsDict["opac"]) > 0:
        opacity = mtlxSubnet.createNode(IMG_TEX_NODE, "Opacity")
        opacity.parm("file").set(mapsDict["opac"])
        mtlxStandard.setNamedInput("opacity", opacity, "out")

    # Normals
    if len(mapsDict["nrml"]) > 0:
        normal = mtlxSubnet.createNode(IMG_TEX_NODE, "Normals")
        normal.parm("file").set(mapsDict["nrml"])
        normal_map = mtlxSubnet.createNode("mtlxnormalmap")
        normal_map.setNamedInput("in", normal, "out")
        mtlxStandard.setNamedInput("normal", normal_map, "out")

    # Displacement
    if len(mapsDict["disp"]) > 0:
        displacement_tex = mtlxSubnet.createNode(IMG_TEX_NODE, "Displacement")
        displacement_tex.parm("signature").set("float")
        displacement_tex.parm("file").set(mapsDict["disp"])
        displacement_remap = mtlxSubnet.createNode("mtlxremap")
        displacement = mtlxSubnet.createNode("mtlxdisplacement")

        displacementOutput.setNamedInput("suboutput", displacement, "out")
        displacement.setNamedInput("displacement", displacement_remap, "out")
        displacement_remap.setNamedInput("in", displacement_tex, "out")

        displacement_remap.parm("outlow").set(-0.7)
        displacement_remap.parm("outhigh").set(0.3)
        displacement.parm("scale").set(0.05)

    # LAYOUT
    mtlxSubnet.layoutChildren()
    mtlxSubnet.setGenericFlag(hou.nodeFlag.Material, True)
    return True
#-----------------------------------------------------------#

def Test():
    maps = {
        "alb" : "M:/Megascans Library/Downloaded/3dplant/plants_3d_rbtnZ/Textures/Atlas/pjxvi_4K_Albedo.jpg",
        "rough" : "M:/Megascans Library/Downloaded/3dplant/plants_3d_rbtnZ/Textures/Atlas/pjxvi_4K_Roughness.jpg",
        "metal" : "M:/Megascans Library/Downloaded/3dplant/plants_3d_rbtnZ/Textures/Atlas/pjxvi_4K_Roughness.jpg",
        "spec" : "M:/Megascans Library/Downloaded/3dplant/plants_3d_rbtnZ/Textures/Atlas/pjxvi_4K_Roughness.jpg",
        "opac" : "M:/Megascans Library/Downloaded/3dplant/plants_3d_rbtnZ/Textures/Atlas/pjxvi_4K_Opacity.jpg",
        "nrml" : "M:/Megascans Library/Downloaded/3dplant/plants_3d_rbtnZ/Textures/Atlas/pjxvi_4K_Normal.jpg",
        "disp" : "M:/Megascans Library/Downloaded/3dplant/plants_3d_rbtnZ/Textures/Atlas/pjxvi_4K_Displacement.exr"
    }

    no_map = {
        "alb" : "",
        "rough" : "",
        "metal" : "",
        "spec" : "",
        "opac" :"",
        "nrml" : "",
        "disp" : "",
    }

    map1 = {
    'alb': 'M:/Megascans Library/Downloaded/3d/nature_rock_vcljbb1iw/vcljbb1iw_4K_Albedo.jpg', 
    'rough': 'M:/Megascans Library/Downloaded/3d/nature_rock_vcljbb1iw/vcljbb1iw_4K_Roughness.jpg', 
    'metal': '',
    'spec': '',
    'opac': '',
    'nrml': 'M:/Megascans Library/Downloaded/3d/nature_rock_vcljbb1iw/vcljbb1iw_4K_Normal_LOD0.jpg',
    'disp': 'M:/Megascans Library/Downloaded/3d/nature_rock_vcljbb1iw/vcljbb1iw_4K_Displacement.exr'
    }
    test_map = maps
    MTLX_DEST = hou.node("/obj").createNode("matnet")
    Geo_DEST = hou.node("/obj").createNode("geo")
    create_MTLX_Subnet(MTLX_DEST, map1)

# Test()