#!/usr/bin/env python

import nuke
import random
import math
import re
import string
import time
import os
from re import findall


class NukeSequenceDict(object):
    def __init__(self):
        print("In NukeSequenceDict")
        
#myList = ["Alpha1", "Alpha2", "Color1", "Color2", "SubSurface1", "SubSurface2"]
    
    def makeRenderoutDict(self, sequenceList):
        print("________________ In makeRenderoutDict! ____________________\n")
        basicOutputsDict = dict()
        finalColorOutputsDicts = dict()
        alphaOutputsDict = dict()
        driverOutputsDict = dict()
        geometryOutputsDict = dict()
        lightingOutputsDict = dict()
        materialOutputsDict = dict()
        patricleOutputsDict = dict()
        shadingOutputsDict = dict()
        volumeOutputsDict = dict()        
        
#### Render Output arrays ####

############### Basic ###############################
    #Alpha  
        alpha = []
    #Depth  
        depth = []
    #Final Color  
        beauty = []
    #Motion Vector 
        motion = []

############### Driver ##############################
    #Driver A        
        driverA = []
    #Driver B
        driverB = []
    #Driver C
        driverC = []
    #Driver D
        driverD = []

############### Geometry ############################
    #Object Coordinates 
        objCoord = []
    #Shading Incidence 
        inc = []
    #Shading Normal 
        norm = []
    #UV Coordinates 
        uVCoord = []
    #World Coordinates 
        worldCoord = []  

############### Lighting ############################
    #Ambient Occlusion 
        ambientOcclusion = []
    #Illumination (Direct) 
        illumDirect = []
    #Illumination (Indirect) 
        illumIndir = []
    #Illumination (Total) 
        illumTotal = []
    #Illumination (Unshadowed) 
        illumUnshdw = []
    #Reflection Occlusion 
        reflecOcc = []
    #Shadow Density 
        shadDen = []

############### Material ############################
    #Diffuse Amount 
        diffAmt = []
    #Diffuse Coeficient 
        diffCoef = []
    #Diffuse Color 
        diffClr = []
    #Diffuse Energy Conservation 
        diffEn = []
    #Diffuse Roughness
        diffRgh = []
    #Reflection Coefficient 
        reflecCoef = []
    #Roughness 
        roughness = []
    #Specular Coefficient 
        specCoef = []
    #Subsurface Amount 
        subSurfAmt = []
    #Subsurface Color
        subSurfClr = []
    #Transparent Amount  
        transAmt = []
    #Transparent Color
        transClr = []

############### Particle Effects ####################
    #Particle Age
        patricleAge = []
    #Particle ID
        patricleID = []
    #Particle Velocity
        patricleVel = []

############### Shading #############################
    #Diffuse Shading (Direct) 
        diffDirect = []
    #Diffuse Shading (Indirect) 
        diffIndirect = []
    #Diffuse Shading (Total) 
        diffTotal = []
    #Diffuse Shading (Unshadowed) 
        diffUnshdw = []
    #Luminous Shading  
        lumShading = []
    #Reflection Shading 
        reflec = []
    #Specular Shading
        spec = []
    #Subsurface Shading
        sss = []
    #Transparent Shading 
        transShading = []

############### Volume ##############################
    #Volumetric Depth 
        volDepth = []
    #Volumetric Opacity 
        volOpac = []
    #Volumetric Scattering 
        volScat = []
        
##############################################################################        
        
############### Basic ###############################
        for i in sequenceList:
            if "_alp_" in i:
                print("Putting in Alpha")
                alpha.append(i)
            if "_dep_" in i:
                print("Putting in Depth")
                depth.append(i)
            if "_col_" in i:
                print("Putting in Final Color")
                beauty.append(i)
            if "_mot_" in i:
                print("Putting in Motion Vector")
                motion.append(i)

############### Driver ##############################
            if "_drvrAt_" in i:
                print("Putting in Driver A")
                driverA.append(i)
            if "_drvrB_" in i:
                print("Putting in Driver B")
                driverB.append(i)
            if "_drvrC_" in i:
                print("Putting in Driver C")
                driverC.append(i)
            if "_drvrD_" in i:
                print("Putting in Driver D")
                driverD.append(i)

############### Geometry ############################
            if "_objc_" in i:
                print("Putting in Object Coord")
                objCoord.append(i)
            if "_inc_" in i:
                print("Putting in Shading Incidence")
                inc.append(i)
            if "_nrm_" in i:
                print("Putting in Shading Normal")
                norm.append(i)
            if "_uvc_" in i:
                print("Putting in UV Coordinates")
                uVCoord.append(i)
            if "_wcd_" in i:
                print("Putting in World Coordinates")
                worldCoord.append(i)

############### Lighting ############################
            if "_aoc_" in i:
                print("Putting in ambientOcclusion")
                ambientOcclusion.append(i)
            if "_ild_" in i:
                print("Putting in illumination Direct")
                illumDirect.append(i)
            if "_ili_" in i:
                print("Putting in illumination Indirect")
                illumIndir.append(i)
            if "_ilt_" in i:
                print("Putting in illumination Total")
                illumTotal.append(i)
            if "_ilu_" in i:
                print("Putting in illumimination Unshdowed")
                illumUnshdw.append(i)
            if "_rfc_" in i:
                print("Putting in Reflection Coefficient")
                reflecCoef.append(i)
            if "_shd_" in i:
                print("Putting in Shadow Density")
                shadDen.append(i)

############### Material ############################
            if "_dfAm_" in i:
                print("Putting in Diffuse Amount")
                diffAmt.append(i)
            if "_dfc_" in i:
                print("Putting in Diffuse Coeficiant")
                diffCoef.append(i)
            if "_dfClr_" in i:
                print("Putting in Diffuse Color")
                diffClr.append(i)
            if "_dfEn_" in i:
                print("Putting in Diffuse Energy Conservation")
                diffEn.append(i)
            if "_dfRgh_" in i:
                print("Putting in Diffuse Roughness")
                diffRgh.append(i)
            if "_rfo_" in i:
                print("Putting in Reflection Occlusion")
                reflecOcc.append(i)
            if "_rgh_" in i:
                print("Putting in Roughness")
                roughness.append(i)
            if "_spcoef_" in i:
                print("Putting in Specular Coefficient")
                specCoef.append(i)
            if "_ssAmt_" in i:
                print("Putting in Subsurface Amount")
                subSurfAmt.append(i)
            if "_ssClr_" in i:
                print("Putting in Subsurface Color")
                subSurfClr.append(i)
            if "_trAmt_" in i:
                print("Putting in Transparent Amount")
                transAmt.append(i)
            if "_trClr_" in i:
                print("Putting in Transparent Color")
                transClr.append(i)

############### Particle Effects ####################
            if "_ptAge_" in i:
                print("Putting in Particle Age")
                patricleAge.append(i)
            if "_ptID_" in i:
                print("Putting in Particle ID")
                patricleID.append(i)
            if "_ptVel_" in i:
                print("Putting in Particle Velocity")
                patricleVel.append(i)

############### Shading #############################
            if "_dfd_" in i:
                print("Putting in Diffuse Direct")
                diffDirect.append(i)
            if "_dfi_" in i:
                print("Putting in Diffuse Indirect")
                diffIndirect.append(i)
            if "_dft_" in i:
                print("Putting in Diffuse Total")
                diffTotal.append(i)
            if "_dfu_" in i:
                print("Putting in Diffuse Unshadowed")
                diffUnshdw.append(i)  
            if "_lum_" in i:
                print("Putting in Luminosity")
                lumShading.append(i)
            if "_rfl_" in i:
                print("Putting in Reflection")
                reflec.append(i)
            if "_spc_" in i:
                print("Putting in Specular")
                spec.append(i)
            if "_sss_" in i:
                print("Putting in Subsurface")
                sss.append(i)
            if "_tran_" in i:
                print("Putting in Transparent")
                transShading.append(i)

############### Volume ##############################
            if "_voldp_" in i:
                print("Putting in Volumetric Depth")
                volDepth.append(i)
            if "_volop_" in i:
                print("Putting in Volumetric Opacity")
                volOpac.append(i)
            if "_volsc_" in i:
                print("Putting in Volumetric Scattering")
                volScat.append(i)
                
##############################################################################
              
############### Basic ###############################
        if not alpha:
            print("None")
        else:
            alphaOutputsDict ['Alpha'] = alpha
        if not depth:
            print("None")
        else:
            basicOutputsDict ['Depth'] = depth
        if not beauty:
            print("None")
        else:
            finalColorOutputsDicts ['Final Color'] = beauty
        if not motion:
            print("None")
        else:
            basicOutputsDict ['Motion Vector'] = motion

############### Driver ##############################
        if not driverA:
            print("None")
        else:
            driverOutputsDict ['Driver A'] = driverA
        if not driverB:
            print("None")
        else:
            driverOutputsDict ['Driver B'] = driverB
        if not driverC:
            print("None")
        else:
            driverOutputsDict ['Driver C'] = driverC
        if not driverD:
            print("None")
        else:
            driverOutputsDict ['Driver D'] = driverD

############### Geometry ############################
        if not objCoord:
            print("None")
        else:
            geometryOutputsDict ['Object Coordinates'] = objCoord
        if not inc:
            print("None")
        else:
            geometryOutputsDict ['Incidence'] = inc
        if not norm:
            print("None")
        else:
            geometryOutputsDict ['Normals'] = norm
        if not uVCoord:
            print("None")
        else:
            geometryOutputsDict ['UV Coordinates'] = uVCoord
        if not worldCoord:
            print("None")
        else:
            geometryOutputsDict ['World Coordinates'] = worldCoord

############### Lighting ############################
        if not ambientOcclusion:
            print("None")
        else:
            lightingOutputsDict ['Ambient Occlusion'] = ambientOcclusion
        if not illumDirect:
            print("None")
        else:
            lightingOutputsDict ['Illumination Direct'] = illumDirect
        if not illumIndir:
            print("None")
        else:
            lightingOutputsDict ['Illumination Indirect'] = illumIndir
        if not illumTotal:
            print("None")
        else:
            lightingOutputsDict ['Illumination Total'] = illumTotal
        if not illumUnshdw:
            print("None")
        else:
            lightingOutputsDict ['Illumination Unshadowed'] = illumUnshdw
        if not reflecOcc: 
            print("None")
        else:   
            lightingOutputsDict ['Reflection Occlusion'] = reflecOcc
        if not shadDen:
            print("None")
        else:
            lightingOutputsDict ['Shadow Density'] = shadDen

############### Material ############################
        if not diffAmt:
            print("None")
        else:
            materialOutputsDict ['Diffuse Amount'] = diffAmt
        if not diffCoef:
            print("None")
        else:
            materialOutputsDict ['Diffuse Coefficient'] = diffCoef
        if not diffClr:
            print("None")
        else:
            materialOutputsDict ['Diffuse Color'] = diffClr
        if not diffEn:
            print("None")
        else:
            materialOutputsDict ['Diffuse Energy'] = diffEn
        if not diffRgh:
            print("None")
        else:
            materialOutputsDict ['Diffuse Roughness'] = diffRgh
        if not reflecCoef:
            print("None")
        else:
            materialOutputsDict ['Reflection Coefficient'] = reflecCoef
        if not roughness:
            print("None")
        else:
            materialOutputsDict ['Roughness'] = roughness
        if not specCoef:
            print("None")
        else:
            materialOutputsDict ['Specular Coefficient'] = specCoef
        if not subSurfAmt:
            print("None")
        else:
            materialOutputsDict ['Subsurface Amount'] = subSurfAmt
        if not subSurfClr:
            print("None")
        else:
            materialOutputsDict ['Subsurface Color'] = subSurfClr
        if not transAmt:
            print("None")
        else:
            materialOutputsDict ['Trasnparent Amount'] = transAmt
        if not transClr:
            print("None")
        else:
            materialOutputsDict ['Transparent Color'] = transClr        

############### Particle Effects ####################
        if not patricleAge:
            print("None")
        else:
            patricleOutputsDict ['Particle Age'] = patricleAge
        if not patricleID:
            print("None")
        else:
            patricleOutputsDict ['Particle ID'] = patricleID
        if not patricleVel:
            print("None")
        else:
            patricleOutputsDict ['Particle Velocity'] = patricleVel

############### Shading #############################
        if not diffDirect:
            print("None")
        else:
            shadingOutputsDict ['Diffuse Direct'] = diffDirect
        if not diffIndirect:
            print("None")
        else:
            shadingOutputsDict ['Diffuse Indirect'] = diffIndirect
        if not diffTotal:
            print("None")
        else:
            shadingOutputsDict ['Diffuse Total'] = diffTotal
        if not diffUnshdw:
            print("None")
        else:
            shadingOutputsDict ['Diffuse Unshadowed'] = diffUnshdw
        if not lumShading:
            print("None")
        else:
            shadingOutputsDict ['Luminosity'] = lumShading
        if not reflec:
            print("None")
        else:
            shadingOutputsDict ['Reflection'] = reflec
        if not spec:
            print("None")
        else:
            print("Putting in Spec")
            shadingOutputsDict ['Specular'] = spec
        if not sss:
            print("None")
        else:
            #print sss
            print("Putting in SSS")
            shadingOutputsDict ['Subsurface'] = sss
        if not transShading:
            print("None")
        else:
            shadingOutputsDict ['Transparent'] = transShading

############### Volume ##############################  
        if not volDepth:
            print("None")
        else:
            volumeOutputsDict ['Volume Depth'] = volDepth
        if not volOpac:
            print("None")
        else:
            volumeOutputsDict ['Volume Opacity'] = volOpac
        if not volScat:
            print("None")
        else:
            volumeOutputsDict ['Volume Scattering'] = volScat
        
        print("________________ In makeRenderoutDict! ____________________\n")
        
        return (alphaOutputsDict, finalColorOutputsDicts, basicOutputsDict, driverOutputsDict, geometryOutputsDict,
                lightingOutputsDict, materialOutputsDict, patricleOutputsDict,
                shadingOutputsDict, volumeOutputsDict)
    
    print("Out NukeSequenceDict")
