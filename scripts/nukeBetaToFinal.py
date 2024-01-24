import os
import nuke
nroot = nuke.root()


class Beta_to_Final(object):
    def __init__(self):
        print("In Beta_to_Final")

    def get_immediate_subdirectories(self, a_dir):
        try:
            return [
                name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))
            ]
        except:
            nuke.message(
                "!!! Problem with paths.  Please check that the Finals frames exist !!!"
            )
            exit

    def updateFilePath(self):
        nodes = nuke.selectedNodes()
        if nodes:
            for node in nodes:
                if node.Class() == "Read":
                    print(node.name())
                    filePath = node['file'].value()
                    newFilePath = filePath.replace("_BETA", "_FINAL")
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
            nuke.message('Files switched to final')

        else:
            nuke.message('No read nodes selected')
