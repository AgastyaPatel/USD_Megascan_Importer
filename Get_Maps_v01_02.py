"""
    STATUS: V01_02 In Progress
    Feature/Purpose: Created Textures class which returns dict object
 """   

import hou, os

class Texture_Files():
    def __init__(self):
        self.tex_maps = {
        "alb" : "",
        "rough" : "",
        "metal" : "",
        "spec" : "",
        "opac" :"",
        "nrml" : "",
        "disp" : "",
        }

    def __str__(self) -> str:
        string = ""
        for tex in self.tex_maps:
             string += tex + " = " + self.tex_maps[tex] + "\n"
        return string

    def extractMaps(self):
        return self.tex_maps

    #-----------------------------------------------------------#
    # Get Maps From Node
    
    def GetMapsFromNode(self, prinMatShader):
        """
        :param prinMatShader: Dest Path for creating materialX subnet
        :type prinMatShader: matnet

        :raise TypeError: if folderPath not str
        :rtype: dictionary
        """

        if prinMatShader.type().name() != "principledshader::2.0":
            print("Not a principle shader")
            return None
        
        self.tex_maps["alb"] = prinMatShader.parm("basecolor_texture").eval()
        self.tex_maps["rough"] = prinMatShader.parm("rough_texture").eval()
        self.tex_maps["metal"] = prinMatShader.parm("metallic_texture").eval()
        self.tex_maps["spec"] = prinMatShader.parm("reflect_texture").eval()
        self.tex_maps["opac"] = prinMatShader.parm("opaccolor_texture").eval()
        self.tex_maps["nrml"] = prinMatShader.parm("baseNormal_texture").eval()
        self.tex_maps["disp"] = prinMatShader.parm("dispTex_texture").eval()

        # safety strip
        for tex in self.tex_maps:
            self.tex_maps[tex] = self.tex_maps[tex].strip()
            # print(self.tex_maps[tex])

        return self.tex_maps


def main():
    
    shader = hou.selectedNodes()[0]
    texture = Texture_Files()
    texture.GetMapsFromNode(shader)
    print(texture.extractMaps())
    print(texture)

