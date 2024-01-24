import os, sys, subprocess, traceback
import nuke, nukescripts
from nukeTools import *
nukeTools = NukeTools()

def GetRepositoryRoot():
    print("------ In GetRepositoryRoot ------")    
    # On OSX, we look for the DEADLINE_PATH file. On other platforms, we use the environment variable.
    if os.path.exists( "/Users/Shared/Thinkbox/DEADLINE_PATH" ):
        with open( "/Users/Shared/Thinkbox/DEADLINE_PATH" ) as f: deadlineBin = f.read().strip()
        deadlineCommand = deadlineBin + "/deadlinecommand"
    else:
        try:
            deadlineBin = os.environ['DEADLINE_PATH']
        except KeyError:
            return ""
    
        if os.name == 'nt':
            deadlineCommand = deadlineBin + "\\deadlinecommand.exe"
        else:
            deadlineCommand = deadlineBin + "/deadlinecommand"
    
    startupinfo = None
    if os.name == 'nt' and hasattr( subprocess, 'STARTF_USESHOWWINDOW' ): #not all python versions have this
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    proc = subprocess.Popen([deadlineCommand, "-root"], cwd=deadlineBin, stdout=subprocess.PIPE, startupinfo=startupinfo)
    
    root = proc.stdout.read()
    root = root.replace("\n","").replace("\r","")
    return root

    print("------ Out GetRepositoryRoot ------ \n")
    
    

def main():
    print("------------------------ In DeadlineNukeClient.py ------------------------")
    print("------ In main ------")
    
    #### Sanity Name Check ####
    sceneName = nukeTools.getSceneName()
    if sceneName.count('_') != 3:
        nuke.message('You scene has name issues.\nPlease check your namespaces.')
        
    else:    
        #### Request for versioning up ####
        userResponse = False
        if nuke.ask('Do you want to render a new version of your comp?'):
            print("Making new version of the comp scene and render")
            nukescripts.script_version_up()
            nukeTools.setNewWriteOutPath()
            nuke.scriptSave("")
            
        else:
            nukeTools.setNewWriteOutPath()
            nuke.scriptSave
        
        
        # Get the repository root
        path = GetRepositoryRoot()
        if path != "":
            #path += "/submission/Nuke/Main/VISMO"
            path += "/custom/scripts/submission/Nuke"
            path = path.replace( "\\", "/" )
            
            # Add the path to the system path
            if path not in sys.path :
                print("Appending \"" + path + "\" to system path to import VISMO_SubmitNukeToDeadline module")
                #print "Appending \"" + path + "\" to system path to import DEV_SubmitNukeToDeadline module"
                sys.path.append( path )
            else:
                print(( "\"%s\" is already in the system path" % path ))
    
            # Import the script and call the main() function
            try:
                import VISMO_SubmitNukeToDeadline
                #import DEV_SubmitNukeToDeadline
                # VISMO_SubmitNukeToDeadline.SubmitToDeadline( path )
                #DEV_SubmitNukeToDeadline.SubmitToDeadline( path )
                VISMO_SubmitNukeToDeadline.SubmitToDeadline()
            except:
                print(traceback.format_exc())
                nuke.message( "The VISMO_SubmitNukeToDeadline.py script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is set in the DEADLINE_PATH environment variable, and that the Deadline Client has been configured to point to a valid Repository." )
                #nuke.message( "The DEV_SubmitNukeToDeadline.py script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is set in the DEADLINE_PATH environment variable, and that the Deadline Client has been configured to point to a valid Repository." )
        else:
            nuke.message( "The VISMO_SubmitNukeToDeadline.py script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is set in the DEADLINE_PATH environment variable, and that the Deadline Client has been configured to point to a valid Repository." )
            #nuke.message( "The DEV_SubmitNukeToDeadline.py script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is set in the DEADLINE_PATH environment variable, and that the Deadline Client has been configured to point to a valid Repository." )

    print("------ Out main ------ \n")