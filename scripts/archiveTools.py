import os, re, shutil
import math


def getNukeScripts(currentDir):
    print("\n>>> In getNukeScripts")
    inUseScripts = []
    oldScripts = []
    inUseScriptsDict = {}
    oldScriptsDict = {}
    if "_NUKE" in currentDir:
        for dirpath, dirnames, filenames in os.walk(currentDir):
            if filenames:
                filteredScripts = [s for s in filenames if (s[-3:] == ".nk")]
                print ("   Filtered Scripts: %s" % (filteredScripts))
                try:
                    inUseScripts = mostRecentFiles(filteredScripts)
                    print("   In Use Scripts: %s" % (inUseScripts))
                except:
                    print ("   No valid files %s" % (filteredScripts))
                    pass
                oldScripts = [x for x in filenames if x not in inUseScripts]            
                inUseScriptsDict[dirpath.replace('\\', '/')] = inUseScripts
                oldScriptsDict[dirpath.replace('\\', '/')] = oldScripts
    else:
        print(" !!!! NOT A NUKE PATH.  PLEASE SPECIFY A PATH TO NUKE SCRIPTS !!!!")
    print(inUseScriptsDict)
    print("<<< Out getNukeScripts \n")
    return inUseScriptsDict, oldScriptsDict

def mostRecentFiles(files):
    print("\n>>> In mostRecentFiles")
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
    print("   Most Recent: %s" % (recent))
    print("<<< Out mostRecentFiles \n")
    return recent

def getShotsToBeArchived(usedScriptsDict):
    print("\n>>> In getShotsToBeArchived")
    shotsToBeArchived = {}
    shotDir = []
    for dirpath, scripts in list(usedScriptsDict.items()):
        for script in scripts:
            frames = sorted(getFramesUsedInNukeScript('/'.join((dirpath, script))))
            print("   Dirpath: %s" % (dirpath))
            print("   Script: %s\n" % (script))
            for frame in frames:
                frame = frame.rstrip().strip('"').replace('//', '/')                
                pathInfo = frame.split('/')
                if "MODO_" in frame:
                    print("   *** Modo Frame ***")
                    print("   Frame: %s\n" % (frame))
                    if "/".join(pathInfo[0:-4]) in shotsToBeArchived:
                        shotsToBeArchived["/".join(pathInfo[0:-4])].append("/".join(pathInfo[0:-3]))
                    else:
                        shotsToBeArchived["/".join(pathInfo[0:-4])] = ["/".join(pathInfo[0:-3])]
                elif "MAYA_" in frame:
                    print("   *** Maya Frame ***")
                    print("   Frame: %s\n" % (frame))
                    if "/".join(pathInfo[0:-4]) in shotsToBeArchived:
                        shotsToBeArchived["/".join(pathInfo[0:-4])].append("/".join(pathInfo[0:-3]))
                    else:
                        shotsToBeArchived["/".join(pathInfo[0:-4])] = ["/".join(pathInfo[0:-3])]
                elif "frames/NK_" in frame:
                    print("   *** Nuke Frame ***")
                    print("   Frame: %s" % (frame))
                    print("   !! Not Archiving !!\n")
                elif "images/" or "movies/" in frame:
                    print("   *** Comp Asset ***")
                    print("   Frame: %s" % (frame))
                    print("   !! Not Archiving !!\n")
                else:
                    print("   *** Unknown Frame ***")
                    print("   Frame: %s" % (frame))
                    print("   !! Not Archiving !!\n")
    print("<<< Out getShotsToBeArchived \n")
    return shotsToBeArchived 


def getFramesUsedInNukeScript(nukescript):
    print("\n>>> In getFramesUsedInNukeScript")
    print ("   Nuke Script: %s" % (nukescript))
    usedFrames = []
    lines_to_edit = []
    foundRead = False
    openFile = open(nukescript, 'r')
    for line in openFile:
        if foundRead == False:
            if "Read {" in line:
                foundRead = True
        else:
            if "file " in line:
                if "/Animation/" not in line:
                   print ("   !!!!! Found Alien File !!!!!")
                   print("   Line: %s" % (line))
                   lines_to_edit.append(line)
                else:
                   print("   Line: %s" % (line))
                   print("      Appending: %s" % (line.split("file ")[-1]))
                   usedFrames.append(line.split("file ")[-1])
                   foundRead = False
    if lines_to_edit:
        print("   Updating file to fix alien file location")        
        for line in lines_to_edit:
            replacement_text = " file " + moveAlienFiles(line, nukescript)
            editScript(nukescript, line, replacement_text)
    print("<<< Out getFramesUsedInNukeScript \n")
    return usedFrames

def moveAlienFiles(line, nukeScript):
    print("\n>>> In moveAlienFiles")    
    oldpath = line.split('file ')[1].rstrip()
    filename = line.split('/')[-1].replace(' ', '_').rstrip()
    script = nukeScript.replace('\\', '/')
    moviespath = (script.split('Animation'))[0] + 'Animation/images/Comp_Assets/'
    newpath = '/'.join((moviespath, filename))
##    shutil.move(oldpath,newpath)
    print("   Moved: %s to %s" % (filename, moviespath))
    print("<<< Out moveAlienFiles \n")
    return newpath

def editScript(filename, text_to_search, replacement_text):
    print("\n>>> In editScript")
    print("   Reading in file: %s" % (filename))
##    with open(filename, 'r') as file :
##      filedata = file.read()
    print("   Searching for: %s" % (text_to_search))
    print("   Replacing with: %s" % (replacement_text))
##    filedata = filedata.replace(text_to_search, replacement_text)
    print("   Making backup of: %s" % (filename))
##    shutil.copy2(filename,filename + '.bak')
    print("   Writing out changes to: %s" % (filename))
##    with open(filename, 'w') as file:
##      file.write(filedata)
    print("<<< Out editScript \n")
    

def archiveShotFrames(usedScriptsDict):
    print("\n>>> In archiveShotFrames")
    for dirpath, framePaths in list(getShotsToBeArchived(usedScriptsDict).items()):
        shotDirList = []
        for path in getImmediateSubdirectories(dirpath):
            print("   subDir: %s" % (path))
            shotDirList.append(dirpath + "/" + path)
        for dirpath in [x for x in shotDirList if x not in uniqifyList(framePaths)]:
            if "_archive" not in dirpath:
                pathInfo = dirpath.split("/")
                dest = "/".join(pathInfo[0:-1]) + "/_archive/" + pathInfo[-1]
                print(str("    Moving..... " + dirpath))
                print(str("    To..... " + dest + "\n"))
                # shutil.move(dirpath, dest)
        print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print("<<< Out archiveShotFrames \n")
            
def archiveNukeScripts(oldScriptsDict):
    print("\n>>> In archiveNukeScripts")
    print(str("   Archiving Nuke Scripts"))
    for dirpath, scripts in list(oldScriptsDict.items()):
        archivePath = dirpath + "/_archive"
        if not os.path.exists(archivePath):
            print(str("    Making: " + archivePath))
            # os.makedirs(archivePath)
        for script in scripts:
            print(str("    Moving..... " + dirpath + "/" + script))
            print(str("    To..... " + archivePath + "/" + script + "\n"))
            # shutil.move(dirpath + "/" + script, archivePath + "/" + script)
    print("<<< Out archiveNukeScripts")


# Utils
def getImmediateSubdirectories(a_dir):
    print("\n>>> In getImmediateSubdirectories")
    print("   a_dir: %s" % (a_dir))
    print("<<< Out getImmediateSubdirectories \n")
    return [name for name in os.listdir(a_dir) if os.path.isdir('/'.join((a_dir, name)))]

def uniqifyList(seq):
    # not order preserving
    set = {}
    list(map(set.__setitem__, seq, []))
    return list(set.keys())

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])



# shotsToBeArchived = getShotsToBeArchived(usedScriptsDict)

for shot, versions in shotsToBeArchived.items():
    print(shot)
    for version in uniqifyList(versions):
        print("   --> %s (%s)" % (version.split('/')[-1], convert_size(get_size(version))))
    print("\n")