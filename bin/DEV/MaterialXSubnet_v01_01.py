"""
    STATUS: V01_01 Working
    Feature/Purpose: Creates Mtlx Subnet with Basic Texture Connection
"""
import hou
print("----------------------------")
hou.node("/obj").deleteItems(hou.node("/obj").children())



#-----------------------------------------------------------#
# Create MaterialX Subnet

def create_MTLX_Subnet(matcontext):
    """
    :param matContext: Dest Path for creating materialX subnet
    :type matContext: matnet

    :raise TypeError: if not a matnet object
    :rtype: Boolean
    """
    if matcontext.type().name() != "matnet":
        print("create_MTLX_Subnet requires Matnet Object as input")
        return False

    mtlxSubnet = matcontext.createNode("subnet", matcontext.type().name() + "_materialX")
    print("Material X subnet Created")

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
    albedo = mtlxSubnet.createNode(IMG_TEX_NODE, "Albedo")
    mtlxStandard.setNamedInput("base_color", albedo, "out")

    # Roughness
    roughness = mtlxSubnet.createNode(IMG_TEX_NODE, "Roughness")
    roughness.parm("signature").set("float")
    mtlxStandard.setNamedInput("specular_roughness", roughness, "out")

    # Metallic
    metallic = mtlxSubnet.createNode(IMG_TEX_NODE, "Metallic")
    metallic.parm("signature").set("float")
    mtlxStandard.setNamedInput("metalness", metallic, "out")

    # SPECULAR
    specular = mtlxSubnet.createNode(IMG_TEX_NODE, "Specular")
    specular.parm("signature").set("float")
    mtlxStandard.setNamedInput("specular", specular, "out")

    #OPACITY 
    opacity = mtlxSubnet.createNode(IMG_TEX_NODE, "Opacity")
    mtlxStandard.setNamedInput("opacity", opacity, "out")

    # Normals
    normal = mtlxSubnet.createNode(IMG_TEX_NODE, "Normals")
    normal_map = mtlxSubnet.createNode("mtlxnormalmap")
    normal_map.setNamedInput("in", normal, "out")
    mtlxStandard.setNamedInput("normal", normal_map, "out")

    # Displacement
    displacement_tex = mtlxSubnet.createNode(IMG_TEX_NODE, "Displacement")
    displacement_tex.parm("signature").set("float")
    displacement_remap = mtlxSubnet.createNode("mtlxremap")
    displacement = mtlxSubnet.createNode("mtlxdisplacement")

    displacementOutput.setNamedInput("suboutput", displacement, "out")
    displacement.setNamedInput("displacement", displacement_remap, "out")
    displacement_remap.setNamedInput("in", displacement_tex, "out")

    displacement_remap.parm("outlow").set(-0.5)
    displacement_remap.parm("outhigh").set(0.5)
    displacement.parm("scale").set(0.1)

    # LAYOUT
    mtlxSubnet.layoutChildren()
    return True
#-----------------------------------------------------------#

def main():

    MTLX_DEST = hou.node("/obj").createNode("matnet")
    create_MTLX_Subnet(MTLX_DEST)
   
main()