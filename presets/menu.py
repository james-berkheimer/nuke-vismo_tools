#################################################################
#															    #
#                     Presets VISMO menu.py                     #
#                                                               #
#################################################################

import os
import sys

import nuke
import nukescripts
import nodeTools

import user_presets
import cam_presets
import reformat_presets

#import source_target_match
nuke.tprint ('...nuke-Presets menu.py')

nuke.root()['format'].setValue("HD_1080")

# Camera presets
cam_presets.nodePresetCamera()

# Reformat presets
reformat_presets.nodePresetReformat()

# Node Defaults
nuke.addAutolabel( nodeTools.showFocal, nodeClass='Camera2' )
nuke.addOnUserCreate( nodeTools.addFovKnob, nodeClass='Camera2' )
nuke.addKnobChanged( nodeTools.fovCB, nodeClass='Camera2' )

# Knob Defaults
nuke.knobDefault('EXPTool.mode', '0')
nuke.knobDefault('EXPTool.label', '[value mode]')
nuke.knobDefault('Shuffle.label', '[knob in]')
#nuke.knobDefault('Shuffle.postage_stamp', '1')

# Default Project Settings
nuke.knobDefault("Root.format", "HD_1080")
latlong = '2000 1000 LatLong_2k'
nuke.addFormat(latlong)
HD720 = '1280 720 HD_720'
nuke.addFormat(HD720)
RetinaDisplay = '2048 1536 Retina_Display'
nuke.addFormat(RetinaDisplay)
iPadDisplay = '1024 768 iPad_Display'
nuke.addFormat(iPadDisplay)