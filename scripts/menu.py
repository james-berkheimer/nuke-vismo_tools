#################################################################
#															    #
#                        VISMO Scripts menu.py                  #
#                                                               #
#################################################################

import os
import sys

import nuke
import nukescripts

import nodeTools
import VISMO_DeadlineNukeClient

import newautoBackdrop
import collectFiles
import camAim

from nukeSaveDebugScene import *
from nukeSetup import *
from nukeVersionUp import *
from nukeAlphaToBeta import *
from nukeBetaToFinal import *
from nukeTools import *
import nukeArchiveProjectShots
# import archiveProject

#import source_target_match
nuke.tprint ('...nuke-Scripts menu.py')


#---- Variables ----
nukeTools = NukeTools()
setup = NukeSetup()
versionUp = VersionUp()
a2b = Alpha_to_Beta()
b2f = Beta_to_Final()
sds = SaveDebugScene()

##### Custom Menu Stuff #####
# Variables
menuBar = nuke.menu( 'Nuke' )
vismo = menuBar.addMenu('VISMO Tools')

## Adding Shortcut Editor
try:
    import shortcuteditor
    shortcuteditor.nuke_setup()
except Exception:
    import traceback
    traceback.print_exc()


######################### Submit to Deadline #########################
tbmenu = menubar.addMenu("&Thinkbox")
tbmenu.addCommand("Submit Nuke To Deadline", VISMO_DeadlineNukeClient.main, 'shift+d')

########################### Gonzo Tools ##################################



################### Nuke VISMO Menu ###################
#---- Set Archive Tool UI ----
vismo.addCommand('Archive Test', 'archiveProject.getProjectRoot()')
vismo.addCommand('Alpha to Beta', 'a2b.updateFilePath()', 'alt+a')
vismo.addCommand('Beta to Final', 'b2f.updateFilePath()')
vismo.addCommand('Archive Project Shots', 'nukeArchiveProjectShots.launch_gui()', 'ctrl+shift+a')
vismo.addCommand('AutoBackDrop', lambda: newautoBackdrop.newautoBackdrop(), 'alt+b')
vismo.addCommand("&Camera with Aim", camAim.camAim,"")
vismo.addCommand('Collect Files', 'collectFiles.collectFiles()')
vismo.addCommand('Delete Unconnected Read Nodes', 'nukeTools.deleteUnconnectedReadNodes()', 'ctrl+alt+d')
vismo.addCommand('Load Shot Images', 'setup.importLocalFolderSeqs()', 'alt+r')
vismo.addCommand('Rev Old Shot Versions', 'nukeTools.archiveOldVersions()', 'alt+/')
vismo.addCommand('Save Debug Script', 'sds.save()', 'alt+d')
vismo.addCommand('Set To Archive Path', 'nukeTools.setToArchivePath()')
vismo.addCommand('Set Alpha Colorspace to Linear', 'nukeTools.setLinearColorspace()', 'alt+l')
vismo.addCommand('Set Read Node Frame Range', 'nukeTools.setFrameRange()', 'alt+f')
vismo.addCommand('Set New Write Node', 'nukeTools.makeWriteNode()', 'alt+w')
vismo.addCommand('Version Read Node Up', 'versionUp.versionReadsUp()', 'ctrl+up')
vismo.addCommand('Version Read Node Down', 'versionUp.versionReadsDown()', 'ctrl+down')
