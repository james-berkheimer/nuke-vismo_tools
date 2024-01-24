
import nuke
import nukescripts

nuke.tprint ('O:/Assets/Animation_Share/VISMO_Tools/Nuke/nuke-vismo_tools/init.py')

nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./plugins')
nuke.pluginAddPath('./presets')
nuke.pluginAddPath('./scripts')
nuke.pluginAddPath('./toolsets')


if not nuke.GUI:
    nuke.tprint('\n\n')
    for i in nuke.pluginPath():
        nuke.tprint(i)
        nuke.tprint('\n\n')
        