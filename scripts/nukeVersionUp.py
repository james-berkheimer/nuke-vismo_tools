from nukeTools import *
tools = NukeTools()


class VersionUp(object):
    def __init__(self):
        print("In VersionUp")

    def versionReadsUp(self):
        for node in nuke.selectedNodes():
            if node.Class() == "Read":
                oldVersion, newVersion = tools.getReadVersionInfo(node)
                if oldVersion == "empty":
                    continue
                print(oldVersion)
                print(newVersion)
                path = node['file'].value()
                print(path)
                newPath = path.replace(oldVersion, newVersion)
                print(newPath)
                node['file'].setValue(newPath)
            
    def versionReadsDown(self):
        for node in nuke.selectedNodes():
            if node.Class() == "Read":
                oldVersion, newVersion = tools.getReadVersionInfo(node, True)
                if oldVersion == "empty":
                    continue
                print(oldVersion)
                print(newVersion)
                path = node['file'].value()
                print(path)
                newPath = path.replace(oldVersion, newVersion)
                print(newPath)
                node['file'].setValue(newPath)