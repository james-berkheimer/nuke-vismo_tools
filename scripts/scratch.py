
import os
import os, shutil
import string
from re import findall
import nuke


rootDir = "O:/Clients/Revance/RHA_Collection/REVRH_Multi_media_20-6622/Animation/frames/MODO_REVRH_FINAL/REVRH_SCS/REVRH_SkinCrossSection_v051"
subDir = os.listdir(rootDir)


def getImageSeqList(subDir, rootDir, Maya=False):
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx In getImageSeqList xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    seqList = []
    start = "{"
    end = "}"
    subDirPaths = []
    for d in subDir:
        subDirPaths.append(os.path.join(rootDir,d))        
    print("subDirPaths: %s\n" % (subDirPaths))
    if Maya == False:
        print("Running on a Modo Path")
        tmpDirPath = []
        for subdir in subDirPaths:
            print("----------------------- In loop 1 ------------------------") 
            print("subdir: %s\n" % (subdir))
            subsubdirs = os.listdir(subdir)
            print("subsubdirs: %s\n" (subsubdirs))
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
        print("Raw: ", raw)
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
    
    
seqs = getImageSeqList(subDir, rootDir, Maya=False)