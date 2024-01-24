import os
import re

VERSION_REGEX = re.compile(r'file_._v(\d+)\.nk')

def getNukeScripts(currentDir):
    print("----- In getNukeScripts -----")
    inUseScripts = []
    oldScripts = []
    inUseScriptsDict = {}
    oldScriptsDict = {}
    nukePath = currentDir
    for dirpath, dirnames, filenames in os.walk(nukePath):
        if filenames:
            print ("Filenames: %s" % (filenames))
            filteredScripts = [s for s in filenames if not (s[-1] == "~" or s[-9:] == ".autosave" or s == ".DS_Store")]
            print ("Filtered Scripts: %s" % (filteredScripts))
            try:
##                print (sorted(filteredScripts)[-1])
##                inUseScripts = sorted(filteredScripts)[-1]
                inUseScripts = mostRecentFiles(filteredScripts)
                print("In Use Scripts: %s" % (inUseScripts))
            except:
                print ("No valid files --- %s" % (filteredScripts))
                pass
            oldScripts = [x for x in filenames if x not in inUseScripts]            
            inUseScriptsDict[dirpath] = inUseScripts
            oldScriptsDict[dirpath] = oldScripts
    print(inUseScriptsDict)
    print("----- Out getNukeScripts -----\n")
    return inUseScriptsDict, oldScriptsDict


def getFramesUsedInNukeScripts(nukeScript):
    print("----- In getFramesUsedInNukeScripts -----")
    print ("Nuke Script: %s" % (nukeScript))
    filePaths = []
    foundRead = False
    openFile = open(nukeScript, 'r')
    for line in openFile:
        if foundRead == False:
            if "Read {" in line:
                foundRead = True
        else:
            if "file " in line:
                if "/Animation/" not in line:
                    print ("!!!!! Found Alien File !!!!!")
                    print("   Line: %s" % (line))
                else:
                    print("Line: %s" % (line))
                    filePaths.append(line.split(" ")[-1])
                    foundRead = False
    print("----- Out getFramesUsedInNukeScripts -----\n")
    return filePaths

def moveAlienFiles(line, nukeScript):
    filepath = line.split(" ")[-1]

def getUsedShots(usedScriptsDict):
    print("----- In getUsedShots -----")
    shotsToBeArchived = {}
    shotDir = []
##    for dirpath, script in list(usedScriptsDict.items()):
    for dirpath, script in usedScriptsDict.items():
        for frame in sorted(getFramesUsedInNukeScripts(os.path.join(dirpath, script))):
            print("Frame: %s" % (frame))
            pathInfo = frame.split('/')
            if "MODO_" or "MAYA_" in frame:
                if "\\".join(pathInfo[0:-4]) in shotsToBeArchived:
                    shotsToBeArchived["\\".join(pathInfo[0:-4])].append("\\".join(pathInfo[0:-3]))
                else:
                    shotsToBeArchived["\\".join(pathInfo[0:-4])] = ["\\".join(pathInfo[0:-3])]
    print("----- Out getUsedShots -----\n")
    return shotsToBeArchived

def archiveShotFrames(usedScriptsDict):
    print("----- In archiveShotFrames -----")
    print(str("Archiving Unused Frames"))
    for dirpath, framePaths in list(getUsedShots(usedScriptsDict).items()):
        shotDirList = []
        for path in getImmediateSubdirectories(dirpath):
            shotDirList.append(dirpath + "\\" + path)
        for dirpath in [x for x in shotDirList if x not in uniqifyList(framePaths)]:
            if "_archive" not in dirpath:
                pathInfo = dirpath.split("\\")
                dest = "\\".join(pathInfo[0:-1]) + "\\_archive\\" + pathInfo[-1]
                print(str("    Moving..... " + dirpath))
                print(str("    To..... " + dest + "\n"))
                # shutil.move(dirpath, dest)
    print("----- Out archiveShotFrames -----\n")
            
def archiveNukeScripts(oldScriptsDict):
    print("----- In archiveNukeScripts -----")
    print(str("Archiving Nuke Scripts"))
    for dirpath, scripts in list(oldScriptsDict.items()):
        archivePath = dirpath + "\\_archive"
        if not os.path.exists(archivePath):
            print(str("    Making: " + archivePath))
            # os.makedirs(archivePath)
        for script in scripts:
            print(str("    Moving..... " + dirpath + "\\" + script))
            print(str("    To..... " + archivePath + "\\" + script + "\n"))
            # shutil.move(dirpath + "\\" + script, archivePath + "\\" + script)
    print("----- Out archiveNukeScripts -----\n")

def getImmediateSubdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def mostRecentFiles(files):    
    fileDict = {}
    recent = []
    files.sort()
    for file in files:
        fileInfo = file.split('_')
        fileKey = '_'.join(fileInfo[0:2])        
        fileDict[fileKey] = []
        fileDict[fileKey].append(fileInfo[-2])
        fileOwner = fileInfo[-1].split('.')[0]
        fileExtention = '.' + fileInfo[-1].split('.')[1]
    for key, value in fileDict.items():
        tmp = [key, value[0], fileOwner]
        recent.append('_'.join(tmp) + fileExtention)
    return recent

def uniqifyList(seq):
    # not order preserving
    set = {}
    list(map(set.__setitem__, seq, []))
    return list(set.keys())

##path = "O:\Clients\Argenx\MG\ARGMG_MOD_19-6180\Animation\ARGMG_NUKE"
path = "O:\Clients\Argenx\MG\ARGMG_MOD_19-6180\Animation\ARGMG_NUKE\FINAL\ARGMG_02"
usedScriptsDict, oldScriptsDict = getNukeScripts(path)
##archiveNukeScripts(oldScriptsDict)
##archiveShotFrames(usedScriptsDict)
shotsToBeArchived = getUsedShots(usedScriptsDict)

for i in shotsToBeArchived:
    print(i)
