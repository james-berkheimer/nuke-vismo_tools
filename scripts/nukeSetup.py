#!/usr/bin/env python

import nuke
import nukescripts
import random
import math
import re
import string
import time
import os
import string
from re import findall
from nukeTools import *
from nukeSequenceDict import *

tools = NukeTools()
getDict = NukeSequenceDict()

############

print("SetUp Class")

class NukeSetup(object):    
    def __init__(self):
        #Global Vars
        self.tmp = ""
        self.hasPasses = False
        self.check = 0
    
            
    def importLocalFolderSeqs(self):
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++ In importLocalFolderSeqs! ++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        
        # Checking for Modo or Maya sequences
        default_dir = None
        rootDir = nuke.getClipname("Read folder recursively...", default=default_dir, multiple=False)
        # rootDir = rootDir.replace(" ", "_")
        subDir = os.listdir(rootDir)
        renderLayerName = rootDir.split('/')[-2]
        mayaPath = False
        if "MAYA_" in rootDir:
            print ("----------- Maya frames -----------")
            mayaPath = True
            tools.importSeqeunces(tools.getImageSeqList(subDir, rootDir, mayaPath), renderLayerName,self.hasPasses, mayaPath)
            
        else:
            print ("----------- Modo frames -----------")
            alphaDict, finalColorDict, basicDict, driverDict, geometryDict, lightingDict, materialsDict, particlesDict, shadingDict, volumeDict = getDict.makeRenderoutDict(tools.getImageSeqList(subDir, rootDir))
            self.hasPasses = tools.checkForPasses(finalColorDict)
                
    
            tools.importSeqeunces(shadingDict, 'Shading',self.hasPasses, mayaPath)
            tools.importSeqeunces(materialsDict, 'Materials',self.hasPasses, mayaPath)
            tools.importSeqeunces(basicDict, 'Basic', self.hasPasses, mayaPath, 'Final Color')
            tools.importSeqeunces(lightingDict, 'Lighting',self.hasPasses, mayaPath)
            tools.importSeqeunces(geometryDict, 'Geometry',self.hasPasses, mayaPath)
            tools.importSeqeunces(particlesDict, 'Particles',self.hasPasses, mayaPath)
            tools.importSeqeunces(volumeDict, 'Volumetric',self.hasPasses, mayaPath)
            tools.importSeqeunces(driverDict, 'Driver',self.hasPasses, mayaPath)
            tools.importSeqeunces(alphaDict, 'Alpha',self.hasPasses, mayaPath)
                
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++ Leaving importLocalFolderSeqs! +++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
            
            
    def makeComp(self):
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++ In makeComp! +++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        if self.check < 6:
            print("Final Color")
            tools.arrangeNodesUtility(-600, -1000)
            tools.arrangeNodesAlpha(-1000, -700)
            tools.arrangeNodesColor('Final Color', self.hasPasses, -600, -700, True)
            
            for node in nuke.allNodes('Grade'):
                if node['name'].value() == 'Grade1':
                    node['selected'].setValue(1)
                
        else:
            print("Shading")
            tools.arrangeNodesUtility(-600, -1000)
            tools.arrangeNodesAlpha(-1000, -700)
            tools.arrangeNodesColor('Shading', self.hasPasses, -600, -700)
        
            for node in nuke.allNodes('Merge2'):
                if node['name'].value() == 'Merge1':
                    node['selected'].setValue(1)
                
        nukescripts.connect_selected_to_viewer(0)
        
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++ Leaving makeComp! ++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
            
            
            
    def setRenderDir(self):
        print("Hello")
        scenePath = tools.getScenePath()
        sceneName = tools.getSceneName()
        sceneVersion = tools.getSceneVersion()
        writeNodes = tools.RecursiveFindNodes( "Write", nuke.Root() )
        
        if writeNodes > 1:
            print("You have more than 1 write node in your scene")
        
        # Make new comp dir
        renderPath = scenePath.replace("compositions", "frames") + sceneVersion
        
        #check if path exists
        dirCheck = os.path.exists(renderPath)
        if dirCheck == True:
            print("Directory Exists")
            
        else:
            os.makedirs(renderPath)
        
        
        
        
            