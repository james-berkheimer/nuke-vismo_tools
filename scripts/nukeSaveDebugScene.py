import os
import nuke
from nukeTools import *
tools = NukeTools()

class SaveDebugScene(object):
    def __init__(self):
        print("In SaveDebugScene")       
        
    def save(self):
        rootDir = "O:/Clients"
        newRootDir = str()
        # filename = modo.Scene().filename
        currSceneName = tools.getSceneName()
        currScenePath = tools.getScenePath()
        currUser = tools.getUserInitials()
        newUserInitials = txt = nuke.getInput('Get new initials', 'new initial')
        newRootDir = nuke.getFilename('Select destination directory', default='O:/Users/jBerkheimer/Clients/')
            
        # Make new file name and file path
        newScenePath = currScenePath.replace(rootDir, newRootDir)
        newSceneName = currSceneName.replace("_" + currUser, "_" + newUserInitials)
        newScenePathFull = newScenePath + "\\" + newSceneName
        
        # set new write file path
        writeNodes = tools.getWriteNodes()
        for node in writeNodes:
            newWritePath = node['file'].value().replace(rootDir, newRootDir)
            node['file'].setValue(newWritePath)
            os.makedirs('/'.join(newWritePath.split('/')[:-1]))
               
        # Create new directory structure and copy over file with new name    
        try:
            os.makedirs(newScenePath)            
        except:
            print("Path exists!")            
        
        try:
            nuke.scriptSaveAs(newScenePathFull)
        except:
            print("Failed to copy scene file")
    
        print(("Debug scene moved to: %s" % (newScenePathFull)))
        
                
