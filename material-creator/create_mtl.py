import maya.cmds as cmds
import maya.mel as mel
from os import walk

class CreateShadingNodes(object):
    """
    Create an Arnold material with basic connectios

    """
    @classmethod
    def createmtl(cls, file_path):
        selection_obj = cmds.ls(selection=True)
        if selection_obj:
            texture_path = cls.getfiles(file_path)
            
            material_node = cmds.shadingNode("aiStandardSurface", name="{0}_Arnold_mtl".format(selection_obj[0]), asShader=True)
            blinn_material = cmds.shadingNode("blinn", name="{0}_blinn_mtl".format(selection_obj[0]), asShader=True)
            
            shading_node = cmds.sets(r=True, noSurfaceShader=True, name="{0}_ShaderG".format(selection_obj[0]))
            cmds.select(selection_obj[0])
            cmds.sets(e=True, forceElement=shading_node)
            cmds.connectAttr('{0}.outColor'.format(material_node), '{0}.aiSurfaceShader'.format(shading_node))
            cmds.connectAttr('{0}.outColor'.format(blinn_material), '{0}.surfaceShader'.format(shading_node))
            file_node = cls.file_node(blinn_material, material_node, shading_node, texture_path[0], texture_path[1], texture_path[2])
            mel.eval("MLdeleteUnused;")
            return "Material Created!"
        else:
            print("Please select an object")
    
    @classmethod
    def getfiles(cls, file_path):
        file_list = []
        file_format=""
        final_path =""
        split_path = file_path.split("/")
        split_format = split_path[-1].split(".")
        file_format = split_format[-1]
        final_path ="/".join(split_path[:-1])

        for(dirpath, dirnames, filenames) in walk(final_path):
            file_list.extend(filenames)
            break
        return [file_list, file_format, final_path]
    
    @classmethod
    def file_node(cls, blinn_material, material_node, shading_node, texture_path, file_format, final_path):       
        placement = cmds.shadingNode('place2dTexture',asUtility=1, name ='place2DTexture')
        for item in texture_path:
            print(item)
            if (item.find("Albedo.{0}".format(file_format))>=1):
                file_node = cls.create_file_node("Albedo", item, placement, final_path)
                color_correct = cmds.shadingNode("aiColorCorrect", name="Albedo_ColorCorrect", asShader=True)
                cmds.connectAttr('{0}.outColor'.format(file_node), '{0}.input'.format(color_correct))
                cmds.connectAttr('{0}.outColor'.format(color_correct), '{0}.baseColor'.format(material_node))
                cmds.connectAttr('{0}.outColor'.format(file_node), '{0}.color'.format(blinn_material))

            elif (item.find("Roughness.{0}".format(file_format))>=1):
                file_node = cls.create_file_node("Roughness", item, placement, final_path)
                range_node = cmds.shadingNode("aiRange", name="Roughness_aiRange", asShader=True)
                cmds.setAttr("{0}.colorSpace".format(file_node), "Utility - Raw", type="string")
                cmds.connectAttr('{0}.outColor'.format(file_node), '{0}.input'.format(range_node))
                cmds.connectAttr('{0}.outColorR'.format(range_node), '{0}.specularRoughness'.format(material_node))

            elif (item.find("Normal.{0}".format(file_format))>=1):
                file_node = cls.create_file_node("Normal", item, placement, final_path)
                normal_node = cmds.shadingNode("aiNormalMap", name="Normal_aiNormalMap1", asShader=True)
                cmds.setAttr("{0}.colorSpace".format(file_node), "Utility - Raw", type="string")
                cmds.connectAttr('{0}.outColor'.format(file_node), '{0}.input'.format(normal_node))
                cmds.connectAttr('{0}.outValue'.format(normal_node), '{0}.normalCamera'.format(material_node))

            elif (item.find("Displacement.exr")>=1):
                file_node = cls.create_file_node("Displacement", item, placement, final_path)
                cmds.setAttr("{0}.colorSpace".format(file_node), "Utility - Raw", type="string")
                displacement_shader = cmds.shadingNode("displacementShader", name="{0}_file".format("Displacement"), asShader=True)
                cmds.setAttr("{0}.aiDisplacementPadding".format(displacement_shader), 1.0)
                cmds.setAttr("{0}.scale".format(displacement_shader), 0.050)
                cmds.connectAttr('{0}.outColorR'.format(file_node), '{0}.displacement'.format(displacement_shader))
                cmds.connectAttr('{0}.displacement'.format(displacement_shader), '{0}.displacementShader'.format(shading_node))

            elif (item.find("Specular.{0}".format(file_format))>=1):
                file_node = cls.create_file_node("Specular", item, placement, final_path)
                range_node = cmds.shadingNode("aiRange", name="Specular_aiRange", asShader=True)
                cmds.setAttr("{0}.colorSpace".format(file_node), "Utility - Raw", type="string")
                cmds.connectAttr('{0}.outColor'.format(file_node), '{0}.input'.format(range_node))
                cmds.connectAttr('{0}.outColorR'.format(range_node), '{0}.specular'.format(material_node))

        return file_node

    @classmethod
    def create_file_node(cls, name, file_name, placement, final_path):
        file1 = cmds.shadingNode("file", name="{0}_file".format(name), asTexture=True)
        cmds.setAttr("{0}.ignoreColorSpaceFileRules".format(file1), True)
        cmds.setAttr("{0}.fileTextureName".format(file1), "{0}/{1}".format(final_path, file_name), type='string')
        cmds.connectAttr( placement+'.coverage',  file1+'.coverage')
        cmds.connectAttr( placement+'.translateFrame',  file1+'.translateFrame')
        cmds.connectAttr( placement+'.rotateFrame',  file1+'.rotateFrame')
        cmds.connectAttr( placement+'.mirrorU',  file1+'.mirrorU')
        cmds.connectAttr( placement+'.mirrorV',  file1+'.mirrorV')
        cmds.connectAttr( placement+'.stagger',  file1+'.stagger')
        cmds.connectAttr( placement+'.wrapU',  file1+'.wrapU')
        cmds.connectAttr( placement+'.wrapV',  file1+'.wrapV')
        cmds.connectAttr( placement+'.repeatUV',  file1+'.repeatUV')
        cmds.connectAttr( placement+'.offset',  file1+'.offset')
        cmds.connectAttr( placement+'.rotateUV',  file1+'.rotateUV')
        cmds.connectAttr( placement+'.noiseUV',  file1+'.noiseUV')
        cmds.connectAttr( placement+'.vertexUvOne',  file1+'.vertexUvOne')
        cmds.connectAttr( placement+'.vertexUvTwo',  file1+'.vertexUvTwo')
        cmds.connectAttr( placement+'.vertexUvThree',  file1+'.vertexUvThree')
        cmds.connectAttr( placement+'.vertexCameraOne',  file1+'.vertexCameraOne')
        cmds.connectAttr( placement+'.outUV', file1+'.uv')
        cmds.connectAttr( placement+'.outUvFilterSize',  file1+'.uvFilterSize')
        return file1