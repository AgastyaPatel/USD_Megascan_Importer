"""
    STATUS: V01_01 Completed
    Feature/Purpose: Should Return Dict object with maps
    tex_maps = {
        "alb" : "",
        "rough" : "",
        "metal" : "",
        "spec" : "",
        "opac" :"",
        "nrml" : "",
        "disp" : "",
    }
 """   

import hou, os

tex_maps = {
        "alb" : "",
        "rough" : "",
        "metal" : "",
        "spec" : "",
        "opac" :"",
        "nrml" : "",
        "disp" : "",
    }

#-----------------------------------------------------------#
# Get Maps From Folder

def GetMapsFromFolder(folderPath):
    """
    :param folderPath: Dest Path for creating materialX subnet
    :type folderPath: matnet

    :raise TypeError: if folderPath not str
    :rtype: dictionary
    """
    MegaScanLib = "M:\\Megascans Library"
    path = MegaScanLib + "\\Downloaded\\3d\\3d_other_ufokciifa"

    dir_list = os.listdir(path)
    print(dir_list)
    




#-----------------------------------------------------------#
# Get Maps From Node
    
def GetMapsFromNode(prinMatShader):
    """
    :param prinMatShader: Dest Path for creating materialX subnet
    :type prinMatShader: matnet

    :raise TypeError: if folderPath not str
    :rtype: dictionary
    """
    global tex_maps

    if prinMatShader.type().name() != "principledshader::2.0":
        print("Not a principle shader")
        return tex_maps
    
    tex_maps["alb"] = prinMatShader.parm("basecolor_texture").eval()
    tex_maps["rough"] = prinMatShader.parm("rough_texture").eval()
    tex_maps["metal"] = prinMatShader.parm("metallic_texture").eval()
    tex_maps["spec"] = prinMatShader.parm("reflect_texture").eval()
    tex_maps["opac"] = prinMatShader.parm("opaccolor_texture").eval()
    tex_maps["nrml"] = prinMatShader.parm("baseNormal_texture").eval()
    tex_maps["disp"] = prinMatShader.parm("dispTex_texture").eval()

    # safety strip
    for tex in tex_maps:
       tex_maps[tex] = tex_maps[tex].strip()
       print(tex_maps[tex])

    return tex_maps

def main():
    

    shader = hou.selectedNodes()[0]
    print(GetMapsFromNode(shader))