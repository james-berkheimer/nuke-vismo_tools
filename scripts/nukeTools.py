#!/usr/bin/env python

import math
import os
import random
import re
import shutil
import string
import time
from re import findall

import nuke
from autoBackdrop import *

backDrop = BackDrop()

############

print("Tools Class")

class NukeTools(object):
    def __init__(self):
        #Global Vars
######################################
        
        self.node = nuke.thisNode()
        self.knob = nuke.thisKnob()
        
        

    def testing(self):
        outputTypes = ['Driver','Volumetric','Particles','Geometry','Materials','Lighting', 'Basic']
        for node in nuke.allNodes('Read'):
            for ot in outputTypes:
                if ot in node['label'].value():
                    node['selected'].setValue(1)
            


############ Notes ############################
#
# print nuke.filename(nuke.thisNode(), nuke.REPLACE)
#
#
###############################################

##############################################################################
##              Checks                                                      ##
##############################################################################

    def checkForPasses(self, seqDict):
        print("========================= In CheckForPasses =========================")
        print("")
        try:
            passCheck = len(seqDict['Final Color'])
        except:
            passCheck = 2
            
        if passCheck > 1:
            hasPasses = True
            print("HasPasses is True")
        else:
            hasPasses = False
            print("HasPasses is False")
            
        return hasPasses
        print("")
        print("========================= Leaving CheckForPasses =========================")
                
            
    
    def colorCheck(self, seqDict):
        print(".................... In colorCheck ........................\n")
        check = 0
        checkList = ['Diffuse Total', 'Transparent', 'Reflection', 'Specular', 'Subsurface', 'Luminosity']
        for k, v in list(seqDict.items()):
            #print k
            if k in checkList:
                print(k)
                check = check+1
                print(check)
                
        return check
        print(".................... Leaving colorCheck ........................\n")
        
    
##############################################################################
##              Gets                                                        ##
##############################################################################

    def getAlphaName(self, i, name):
        print("---------------- In getAlphaName! -------------------\n")
        newName = ""
        print("Render output type coming in: " + name)
        tmp = i.split('/')
        fileName =  tmp[-1]
        underScoreCount = fileName.count('_')
        if underScoreCount > 5:
            print("Hass passes")
            fileComponents = fileName.split('_')
            print("Pass name: " + fileComponents[-2])
            alphaName = "_" + fileComponents[-4] + "_" + fileComponents[-2]
        else:
            print("No passes")
            fileComponents = fileName.split('_')
            #print "Pass name: " + fileComponents[-3]
            alphaName = "_" + fileComponents[-3]
        print("Alpha Name is: " + alphaName)
        return alphaName
        print("---------------- Leaving getAlphaName! -------------------\n")
        
    def getFileInfo(self):        
        print("----------------- In getFileInfo --------------------------")        
        print(("File Name: " + self.getSceneName()))
        fileInfo = self.getSceneName().split("_")
        print("----------------- Leaving getFileInfo --------------------------")
        return fileInfo 
    
    def getFilePath(self, path):
        print("---------------- In getFilePath! -------------------\n")
        filePath = ""
        for i in path.split('/')[:-1]:
            filePath = filePath + i + '/'
        print("---------------- Leaving getScenePath! -------------------\n")
        return filePath
    
    def getFramesPath(self):
        fileInfo = self.getFileInfo()
        pathInfo = self.getScenePath().split('Animation')
        framesPath = pathInfo[0] + 'Animation/frames/'
        phase = pathInfo[1].split('/')[2]
        phaseFolder = 'NK_' + fileInfo[0] + '_' + phase + '/'
        shotFolder = fileInfo[0] + '_' + fileInfo[1] + '/'
        return framesPath + phaseFolder + shotFolder
    
    def getImageSeqList(self, subDir, rootDir, Maya=False):
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx In getImageSeqList xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        seqList = []
        start = "{"
        end = "}"
        subDirPaths = []
        for d in subDir:
            tmp = os.path.join(rootDir,d)
            print("Appending....." + tmp.strip('\n'))
            subDirPaths.append(os.path.join(rootDir,d))        
        # print("subDirPaths: %s\n" % (subDirPaths))
        if Maya == False:
            print("Running on a Modo Path")
            tmpDirPath = []
            for subdir in subDirPaths:
                print("----------------------- In loop 1 ------------------------") 
                print("subdir: %s\n" % (subdir))
                subsubdirs = os.listdir(subdir)
                print("subsubdirs: ", (subsubdirs))
                for d in subsubdirs:
                    newpath = os.path.join(subdir, d)        
                    print("newpath: %s" % (newpath))
                    tmpDirPath.append(newpath)        
            subDirPaths = tmpDirPath
        
        print("\n........................................................\n")
        
        for subdir in subDirPaths:
            print("----------------------- In loop 2 ------------------------")
            subdir = subdir.replace('\\','/')
            print("SubDirPath: %s" % (subdir))
            raw = nuke.tcl('filename_list -compress "' + subdir + '"')
            print("Raw: %s" % (raw))
            print("")            
            if raw == None:
                print("RAW is NONE")
                continue
            else:
                print("IS RAW")
            seqCount = raw.count('{')
            print("Number of sequences: %s" % (str(seqCount)))
            if seqCount > 1:
                ###### Look for Passes here?? ######
                print("I need to solve for more than one sequence")
                multSeq = findall("{(.*?)}", raw)
                print("multSeq: %s" % (multSeq))
                for seq in multSeq:
                    seq = '/' + seq
                    seq = seq.replace('%04d','####')
                    print("seq 1: %s" % (seq))
                    seq = subdir + seq
                    print("seq 2: %s" % (seq))               
                    seqList.append(seq)               
            elif seqCount == 0:
                print("I need to solve for single images")
                singleImages = []
                tmp = raw.split()    
                print(tmp)
                for t in tmp:
                    if ".png" in t or ".exr" in t:
                        print("Found: " + t)
                        singleImages.append(t)                      
                for s in singleImages:
                    s = '/' + s
                    print(s)
                    s = subdir + s
                    print(s)
                    seqList.append(s)               
            elif seqCount == 1:
                print("I need to solve for only one sequence")
                singleSeq = findall("{(.*?)}", raw)
                singleSeq = ''.join(singleSeq)
                print("singleSeq 1: %s" % (singleSeq))
                singleSeq = '/' + singleSeq
                singleSeq = singleSeq.replace('%04d','####')
                print("singleSeq 2: %s" % (singleSeq))
                singleSeq = subdir + singleSeq
                print("singleSeq 3: %s" % (singleSeq))               
                seqList.append(singleSeq)           
                
        return seqList
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Leaving getImageSeqList xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")        

    def getPassName(self, i, name):
        print("---------------- In getPassName! -------------------\n")
        newName = ""
        print("Render output type coming in: " + name)
        tmp = i.split('/')
        fileName =  tmp[-1]
        underScoreCount = fileName.count('_')
        if underScoreCount > 5:
            fileComponents = fileName.split('_')
            print("Pass name: " + fileComponents[-2])
            passName = "_" + fileComponents[-2]
            return passName
        print("---------------- Leaving getPassName! -------------------\n")
        
        
    def getScenePath(self):
        print("---------------- In getScenePath! -------------------\n")
        path = nuke.Root()['name'].getValue()  
        scenePath = ""
        for i in path.split('/')[:-1]:
            scenePath = scenePath + i + '/'
        print("---------------- Leaving getScenePath! -------------------\n")
        return scenePath
    
    def getSceneName(self):
        print("---------------- In getSceneName! -------------------\n")
        path = nuke.Root()['name'].getValue()
        sceneName = path.split('/')[-1]
        print("---------------- Leaving getSceneName! -------------------\n")
        return sceneName
    
    def getSceneVersion(self):
        print("---------------- In getSceneVersion! -------------------\n")
        path = nuke.Root()['name'].getValue()  
        sceneName = path.split('/')[-1]
        sceneVersion = sceneName.split('_')[-2]
        print("---------------- Leaving getSceneVersion! -------------------\n")     
        return sceneVersion
   
    def getPassTypeSet(self):
        print("________________ In getPassTypeSet! ____________________\n")
        passSet = set()
        for node in nuke.allNodes('Read'):
            tmp = node['name'].value()
            tmp = tmp.split('_')
            print("Pass type is: " + tmp[-1])
            passSet.add(tmp[-1])
        print("________________ Leaving getPassTypeSet! ____________________\n")
        return passSet    

    def getWriteNodes(self):        
        nodes = nuke.allNodes()
        writeNodes = []
        for node in nodes:
            #print node['name'].value()    
            if node.Class() == "Write":
                writeNodes.append(node)
        if len(writeNodes) < 1:
            nuke.message("No Write Nodes in scene \n Please make sure only write node exists in your scene.") 
            exit
            
        else:
            print("I'm still standin!!!")
            return writeNodes    
    
    def getReadVersionInfo(self, node, down=False):
        print("________________ In getReadVersionInfo! ____________________\n")
        path = node['file'].value()
        print(path)
        pathInfo = path.split('/')
        print(pathInfo[-1])
        fileInfo = pathInfo[-1].split('_')
        if len(fileInfo) < 6:
            version = "empty"
            newVersion = "empty"
        else:
            version = fileInfo[2]
            #print version
            versionNum = version[1:]
            #print versionNum
            if down == False:
                newVersionNum = int(versionNum) + 1
            else:
                newVersionNum = int(versionNum) - 1
            newVersionNum = "%03d" % int(newVersionNum)
            #print newVersionNum
            newVersion = "v" + str(newVersionNum)
            #print newVersion
        print("________________ Leaving getReadVersionInfo! ____________________\n")
        return (version, newVersion)
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def getNewWriteVersionInfo(self, node, up=False):
        print("________________ In getNewWriteVersionInfo! ____________________\n")
        path = node['file'].value()     
        sceneVersion = self.getSceneVersion()
        print(path)
        pathInfo = path.split('/')
        print(pathInfo[-1])
        fileInfo = pathInfo[-1].split('_')
        if len(fileInfo) < 4:
            version = "empty"
            newVersion = "empty"
        else:
            version = fileInfo[2]
            versionNum = sceneVersion[1:]

            print("VersionNum: " + str(versionNum))
            if up == True:
                newVersionNum = int(versionNum) + 1
            else:
                newVersionNum = int(versionNum)
            newVersionNum = "%03d" % int(newVersionNum)
            newVersion = "v" + str(newVersionNum)
        print("________________ Leaving getNewWriteVersionInfo! ____________________\n")
        return (version, newVersion)
    
    def getUserInitials(self):        
        print("----------------- In getUserInitials --------------------------")
        fileInfo = self.getFileInfo()
        userName = fileInfo[-1]
        userInitials = userName.split('.')[0].upper()
        print("----------------- Leaving getUserInitials --------------------------")
        return userInitials  
        
        
##############################################################################
##              Sets                                                        ##
##############################################################################

    def setFrameRange(self):
        ret = nuke.getFramesAndViews('New frame range', '1-100')
        if ret:
            range = ret[0]
            first = int(range.split('-')[0])
            last = int(range.split('-')[1])     
            nodes = nuke.selectedNodes()
            for node in nodes:
                if node.Class() == "Read":
                    node['first'].setValue(first)
                    print(node['first'].value())
                    node['last'].setValue(last)
                    print(node['last'].value())
                
    def setLinearColorspace(self):
        nodes = nuke.selectedNodes()
        for node in nodes:
            if node.Class() == "Read":
                print(node['colorspace'].value())
                node['colorspace'].setValue('linear')
                print(node['colorspace'].value())
                
                
    def setNewWriteOutPath(self):
        writeNodes = self.getWriteNodes()
        for writeNode in writeNodes:
            filePath = writeNode['file'].value()
            oldVersion, newVersion = self.getNewWriteVersionInfo(writeNode)
            if oldVersion == "empty":
                exit
            print(oldVersion)
            print(newVersion)
            print(filePath)
            newPath = filePath.replace(oldVersion, newVersion)
            writeNode['file'].setValue(newPath)
            pathWOFilename = ""
            
            #get the file path without the file name
            pathWOFilename = self.getFilePath(newPath)          
            #make the new directory
            dirCheck = os.path.exists(pathWOFilename)
            if not dirCheck:
                print("making new directories: " + pathWOFilename)
                os.makedirs(pathWOFilename)


##############################################################################
##              Tasks                                                       ##
##############################################################################

    def archiveOldVersions(self):
        framesPath = self.getFramesPath()
        # get directories in framesPath
        dirs = []
        for (dirpath, dirnames, filenames) in os.walk(framesPath):
            dirs.extend(dirnames)
            sorted(dirs)
            dirs.remove('_revs')
            break
        
        # make _revs directory
        revsPath = framesPath + '_revs'
        if not os.path.isdir(revsPath):
            os.mkdir(revsPath)
            
        # move older directories but leave the last in the list
        movedDirs = []
        for d in dirs:
            if d != dirs[-1]:
                movedDirs.append(d)
                print(("moving " + d))
                shutil.move(framesPath + d, framesPath + '_revs/' + d)                
        s = " "
        nuke.message("Moved " + s.join(movedDirs))
                

    def arrangeNodesAlpha(self, x = 0, y = 0):
        print("________________ In arrangeNodesAlpha! ____________________\n")
        for node in nuke.allNodes('Read'): 
            if 'Alpha' in node['label'].value():
                print(node['name'].value())
                node['selected'].setValue(1)
                node['xpos'].setValue(x)
                node['ypos'].setValue(y)
                node['selected'].setValue(1)
                y = y+125
                
        backDrop.autoBackdrop(50,40,25,'Alphas')
        nodes = nuke.selectedNodes()
        #time.sleep(1)
        for node in nodes:
            node['selected'].setValue(0)
        print("________________ Leaving arrangeNodesAlpha! ____________________\n")
        
        
    def arrangeNodesUtility(self, x = 0, y = 0):
        print("________________ In arrangeNodesUtility! ____________________\n")
        outputTypes = ['Driver','Volumetric','Particles','Geometry','Materials','Lighting', 'Basic']
        for node in nuke.allNodes('Read'):
            for ot in outputTypes:
                #print ot
                if ot != 'Final Color':                 
                    if ot in node['label'].value():
                        print(node['name'].value())
                        node['selected'].setValue(1)
                        node['xpos'].setValue(x)
                        node['ypos'].setValue(y)
                        node['selected'].setValue(1)        
                        x = x+125
                    
        nodes = nuke.selectedNodes()
        if len(nodes) == 0:
            print("No Utilities")
        else:
            for node in nodes:
                print("I am selecting this node: " + node.name())
                node['selected'].setValue(1)
            backDrop.autoBackdrop(50,40,25,'Utilities')
            #nodes = nuke.selectedNodes()        
            for node in nodes:
                print("I am Deselecting this node: " + node.name())
                node['selected'].setValue(0)
        print("________________ Leaving arrangeNodesUtility! ____________________\n")
        
        
    def arrangeNodesColor(self, name, hasPasses, x = 0, y = 0, finalColor = False):
        print("________________ In arrangeNodesColor! ____________________\n")
        
        print("Has Passes: " + str(hasPasses))
        if hasPasses == True:
            for p in self.getPassTypeSet():
                print("in Pass Loop")
                print("I'm looking for pass: " + p)
                print("Creating node at x: " + str(x))
                if self.imagesInPass(name, p) == True:
                    if finalColor == False:
                        x = self.arrangeUtilColor(name, False, x, y, p)
                    else:
                        x = self.arrangeUtilColor(name, True, x, y, p)
                    x = x+200               
                    nodes = nuke.selectedNodes()
                    for node in nodes:
                                print("Printing selected Nodes" + node.name())
                                node['selected'].setValue(0)
                    
        else:
            print("No passes")
            if finalColor == False:
                x = self.arrangeUtilColor(name, False, x, y)
            else:
                x = self.arrangeUtilColor(name, True, x, y)
            x = x+200
            nodes = nuke.selectedNodes()
            for node in nodes:
                print("Printing selected Nodes" + node.name())
                node['selected'].setValue(0)
        print("________________ Leaving arrangeNodesColor! ____________________\n")
        

    def arrangeUtilColor(self, name, finalColor = True, x=0, y=0, p = ""):
        print("________________ In arrangeUtilColor! ____________________\n")
        selectedNodes = []
        i = 0
        print("X is :" + str(x))
        print("P is: " + p)
        print("Name is: " + name)
        # Looking for a a Final Color node
        if finalColor == False:
            print("Creating Merge")
            m = nuke.nodes.Merge2()
            m['ypos'].setValue(y+450)
            m['xpos'].setValue(x+440)           
            for node in nuke.allNodes('Read'):
                print('In node loop 1\n')
                print("if " + p + " in " + node['name'].value())
                if p is None:
                    p = 'Final Color'
                    #x, i = self.moveNode(name, p, node, x, y, i, m)
                    if name in node['label'].value():
                        print("*** Found a render out type match ***")                       
                        print("Selecting: " + p + " " + node['name'].value())
                        print("")
                        node['selected'].setValue(1)
                        node['xpos'].setValue(x)
                        node['ypos'].setValue(y)
                        g = nuke.nodes.Grade()
                        g['ypos'].setValue(y+300)
                        g.setInput(0,node)
                        if m is not None:
                            m.setInput(i,g)
                            m['operation'].setValue('plus')
                            m['selected'].setValue(1)
                        node['selected'].setValue(1)
                        x = x+150
                        i = i+1
                    
                else:                   
                    if p in node['name'].value():
                        print("!!!!! Found a pass match !!!")
                        print("if " + name + " in " + node['label'].value())
                        print("")
                        #x, i = self.moveNode(name, p, node, x, y, i, m)
                        if name in node['label'].value():
                            print("*** Found a render out type match ***")                       
                            print("Selecting: " + p + " " + node['name'].value())
                            print("")
                            node['selected'].setValue(1)
                            node['xpos'].setValue(x)
                            node['ypos'].setValue(y)
                            g = nuke.nodes.Grade()
                            g['ypos'].setValue(y+300)
                            g.setInput(0,node)
                            if m is not None:
                                m.setInput(i,g)
                                m['operation'].setValue('plus')
                                m['selected'].setValue(1)
                            node['selected'].setValue(1)
                            x = x+150
                            i = i+1
                        
                print("X is :" + str(x))
            backDrop.autoBackdrop(50,40,50,p)
        
        else:
            for node in nuke.allNodes('Read'):
                print('In node loop 2')
                print("if " + p + " in " + node['name'].value())
                if p is None:
                    p = 'Final Color'
                    #x, i = self.moveNode(name, p, node, x, y, i)
                    if name in node['label'].value():
                        print("*** Found a render out type match ***")                       
                        print("Selecting: " + p + " " + node['name'].value())
                        print("")
                        node['selected'].setValue(1)
                        node['xpos'].setValue(x)
                        node['ypos'].setValue(y)
                        g = nuke.nodes.Grade()
                        g['ypos'].setValue(y+300)
                        g.setInput(0,node)
                        g['selected'].setValue(1)
                        node['selected'].setValue(1)
                        x = x+150
                        i = i+1
                    
                else:
                    if p in node['name'].value():
                        print("!!!!! Found a pass match !!!")
                        print("if " + name + " in " + node['label'].value())
                        print("")
                        #x, i = self.moveNode(name, p, node, x, y, i)
                        if name in node['label'].value():
                            print("*** Found a render out type match ***")                       
                            print("Selecting: " + p + " " + node['name'].value())
                            print("")
                            node['selected'].setValue(1)
                            node['xpos'].setValue(x)
                            node['ypos'].setValue(y)
                            g = nuke.nodes.Grade()
                            g['ypos'].setValue(y+300)
                            g.setInput(0,node)
                            g['selected'].setValue(1)
                            node['selected'].setValue(1)
                            x = x+150
                            i = i+1

            #backDrop.autoBackdrop(50,40,50,p)
                    
        #return selectedNodes
        print("________________ Leaving arrangeUtilColor! ____________________\n")
        return x

    def deleteUnconnectedReadNodes(self):
        for node in nuke.allNodes('Read'):
            children = nuke.toNode(node.name()).dependent( nuke.INPUTS | nuke.EXPRESSIONS )
            if children:
                print("Connected nodes, passing")
            else:
                print("No connections, deleting: ", node.name())
                nuke.delete(node)
    
    def imagesInPass(self, name, p):
        goodToGo = False
        for node in nuke.allNodes('Read'):
            if p in node['name'].value():
                if name in node['label'].value():
                    goodToGo = True
        return goodToGo
    

    def importSeqeunces(self, sequences, name, hasPasses, Maya, exclude = None):
        print("***************** In importSeqeunces *********************\n")
        print("Render output name going in: " + name)
        ingoingName = name
        newName = ""
        print("Ingoing Name: " + ingoingName)
        #if exclude is None:
        #print "... Exclude is None ..."
        if Maya == True:
            print ("Maya Sequences")
            for seq in sequences:
                lbl = "-----------------\n" + name
                self.makeReadNode(seq, lbl)
        else:
            for k,v in list(sequences.items()):
                lbl = "-----------------\n" + name
                print("k: " + k)
                if k == "Alpha":
                    print("Is an Alpha Pass")
                    for i in v:
                        if hasPasses is True:
                            print("Has Passes")
                            newName = k + self.getAlphaName(i, ingoingName)
                            self.makeReadNode(i, lbl,newName)
                        else:
                            print("No Passes")
                            newName = k + self.getAlphaName(i, ingoingName)
                            self.makeReadNode(i, lbl,newName)
                    print("Alpha Name is: " + newName)
                else:
                    print("Not an Alpha Pass")
                    print("k: " + k)
                    for i in v:
                        if hasPasses is True:
                            print("Has Passes")
                            newName = str(k) + str(self.getPassName(i, ingoingName))
                            self.makeReadNode(i, lbl,newName)
                        else:
                            self.makeReadNode(i, lbl,k)
                        print("Node Name is: " + newName)                    
                        
        print("***************** Leaving importSeqeunces *********************\n")

        
    def makeReadNode(self, i, lbl, name=""):
        print("________________ In makeReadNode! ____________________\n")
        print("File name is: " + i)
        fileInfo = i.split()
        filePath = ""
        if len(fileInfo) > 2:
            myTuple = (fileInfo[0], fileInfo[1])
            filePath = ' '.join(myTuple)
        else:
            filePath = fileInfo[0]
        frameFirst = ""
        frameLast = ""
        if name == "":
            name = filePath.split('/')[-2]
        if len(fileInfo) == 1:
            frameFirst = "1"
            frameLast = "1"
        else:
            print("Frames: " + str(fileInfo))
            frameList = fileInfo[-1].split('-')
            print("Frame first: " + str(frameList[0]))
            print("Frame last: " + str(frameList[1]))
            #frameLast = frameLast.split('-')
            frameFirst = frameList[0]
            frameLast = frameList[1]
            
        print("First frame: " + str(frameFirst))
        print("Last frame: " + str(frameLast))
        nuke.nodes.Read(file=filePath, first=frameFirst, last=frameLast, label=lbl, name=name)
        
        print("Node Created \n")
        print("________________ Leaving makeReadNode! ____________________\n")
        
    
    def makeWriteNode(self):
        sceneName = self.getSceneName()
        u = '_'
        tmp = sceneName.split('_')[0:2]
        filename = u.join(tmp) + '_v001_%04d.png'
        newFramesPath = self.getFramesPath() + 'v001/' + filename        
        selected = ""
        
        try:
            selected = nuke.selectedNode()
        except:
            print ("No node selected")

        if selected:
            nuke.nodes.Write(file=newFramesPath, file_type='png', inputs=[selected])
        else:
            nuke.nodes.Write(file=newFramesPath, file_type='png')        

    
    def moveNode(self, name, p, node, x , y, i, m = ""):
        if name in node['label'].value():
            print("*** Found a render out type match ***")                       
            print("Selecting: " + p + " " + node['name'].value())
            print("")
            node['selected'].setValue(1)
            node['xpos'].setValue(x)
            node['ypos'].setValue(y)
            g = nuke.nodes.Grade()
            g['ypos'].setValue(y+300)
            g.setInput(0,node)
            #g['ypos'].setValue(y+100)
            if m is not None:
                m.setInput(i,g)
                m['operation'].setValue('plus')
                m['selected'].setValue(1)
            node['selected'].setValue(1)
            x = x+150
            i = i+1
            return x, i
        
        
    def RecursiveFindNodes(self, nodeClass, startNode):
        #print "------ In RecursiveFindNodes ------"
        nodeList = []
        
        if startNode != None:
            if startNode.Class() == nodeClass:
                nodeList = [startNode]
            elif isinstance(startNode, nuke.Group):
                for child in startNode.nodes():
                    nodeList.extend( self.RecursiveFindNodes(nodeClass, child) )
                    
        #print "------ Leaving RecursiveFindNodes ------"
        return nodeList
        
    
    def saveNewSceneVersion(self):
        scenePath = self.getScenePath()
        sceneName = self.getSceneName()
        sceneVersion = self.getSceneVersion()
        
        #increasing up the version number
        versionNumber = sceneVersion[1:]
        versionNumber = int(versionNumber) + 1
        version = "%03d" % int(versionNumber)
        version = "v" + str(version)
        
        #updating scene file name with new version
        #nukescripts.script_version_up()        
        if sceneName.count("_") == 3:
            print("Legal Name")
            nameInfo = sceneName.split('_')
            newSceneName = nameInfo[0] + '_' +  nameInfo[1] + '_' + newVersion + '_' + nameInfo[3]      
        newScenePath = scenePath + newSceneName
                
    def setToArchivePath(self):
        scriptPath = nuke.root().knob('name').value() 
        rootPath = scriptPath.split("Clients")[0]        
        for node in nuke.allNodes('Read'):
            node['file'].setValue(node['file'].value().replace("O:/", rootPath))        
                
    def uniqifyList(self, seq):
        # not order preserving
        set = {}
        list(map(set.__setitem__, seq, []))
        return list(set.keys())
        
##############################################################################
##              Dialogs                                                     ##
##############################################################################
        
    def initialsDialog(self):
        userInput = ""
        try:
            print ("Setting new user initials")
            print ("user.defNew user.initials life:{momentary}")
            print(("user.def user.initials dialogname {%s}" % ("Enter user initials")))
            print ("user.value user.initials")
            userInput = lx.eval("user.value user.initials ?")
        except:
            print("!! Failed at get user initials !!")
            exit()
        return userInput
        
        
        
        
        
        
                
        
    
