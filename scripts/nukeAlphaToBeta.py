import os
import nuke
nroot = nuke.root()


class Alpha_to_Beta(object):
    def __init__(self):
        print("In Alpha_to_Beta")

    def get_immediate_subdirectories(self, a_dir):
        return [
            name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))
        ]

    def updateFilePath(self):
        nodes = nuke.selectedNodes()
        if nodes:
            for node in nodes:
                if node.Class() == "Read":
                    print(node.name())
                    filePath = node['file'].value()
                    newFilePath = filePath.replace("_ALPHA", "_BETA")
                    shotPath = "/".join(newFilePath.split('/')[:-4])
                    shotVersion = newFilePath.split('/')[-4].split('_')[-1]
                    currentShot = node['file'].value().split('/')[-4][:-3]
                    print("shotPath: " + shotPath)
                    print("shotVersion: " + shotVersion)
                    print("currentShot: " + currentShot)
                    versionHolder = []
                    for n in self.get_immediate_subdirectories(shotPath):
                        print("Shot: " + n)
                        if currentShot in n:
                            version = n.split('_')[-1]
                            print("Version: " + str(version))
                            # print(int(list(filter(str.isdigit, version))))
                            print(int(filter(str.isdigit, version)))
                            versionHolder.append(
                                int(filter(str.isdigit, version)))
                    print("newVersion: " + "v" + "%03d" % max(versionHolder))
                    newVersion = "v" + "%03d" % max(versionHolder)
                    print(shotVersion)
                    print(newVersion)
                    newFilePath = newFilePath.replace(shotVersion, newVersion)
                    print(newFilePath)
                    node['file'].setValue(newFilePath)
                else:
                    print("No Read Nodes")
            nuke.message('Files switched to beta')

        else:
            nuke.message('No read nodes selected')
