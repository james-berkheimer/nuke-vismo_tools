#################################################################
#															    #
#                    Gizmos VISMO menu.py                       #
#                                                               #
#################################################################

import nuke

#import source_target_match
nuke.tprint ('...nuke-Gizmos menu.py')

# Initialize VISMO menu
VISMO_Menu = nuke.menu('Nodes').addMenu('Viscira','viscira.png')

#Image Stuff
VISMO_Menu.addCommand('Image/VISMO Write',"nuke.createNode('VISMO_Write.gizmo')", icon='Write.png')

