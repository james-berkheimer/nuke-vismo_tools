#!/usr/bin/env python

import os, sys
import time
import collections
import shutil
import math
import logging
import nuke
from PySide import QtGui, QtCore
execGui = None


class ArchiveTask(QtCore.QThread):
    #--------------------------------------------------------------------------
    # Establish Signal variables
    #--------------------------------------------------------------------------
    taskFinished = QtCore.Signal()
    printConsole = QtCore.Signal(str)

    #--------------------------------------------------------------------------
    # Initialize function
    #--------------------------------------------------------------------------
    def __init__(self, parent=None):
        super(ArchiveTask, self).__init__(parent)
        animroot, nukeroot = self.getRootDirs()
        self._animroot = animroot
        self._nukeroot = nukeroot
        self._collectData_layout = QtGui.QHBoxLayout()
        self._filepath_layout = QtGui.QHBoxLayout()
        # self._archivebutton_layout = QtGui.QHBoxLayout()
        self.create_dropMenus()
        self.create_collectData_button()
        self.create_filepath()
        # self.create_archive_button()
        self.populate_phasesbox()
        self.populate_shotsbox()
        self.populate_filepath()
        self._usedScriptsDict = []
        self._oldScriptsDict = []
        self._shotsToBeArchived = []

    #--------------------------------------------------------------------------
    # Slot/Signal functions
    #--------------------------------------------------------------------------
    # @QtCore.Slot()
    # def on_button_clicked(self):
    #     # Start the task
    #     print("Start Archive")
    #     self.myArchiveTask.start()
    #     # ArchiveTask.run()

    #--------------------------------------------------------------------------
    # UI Functions (To be sent to Task UI)
    #--------------------------------------------------------------------------
    def create_collectData_button(self):
        self._collectdata_label = QtGui.QLabel("Shots to Archive: ")
        self._collectdata = self.createButton("Collect Shots",
                                              self.collectData)
        self._collectdata.setMinimumWidth(100)
        self._collectData_layout.addWidget(self._collectdata, 1)

    def createButton(self, text, member, icon=""):
        if icon:
            button = QtGui.QPushButton(QtGui.QIcon(icon), text)
        else:
            button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def create_dropMenus(self):
        self._phases_label = QtGui.QLabel("Shot Phases: ")
        self._phasesbox = QtGui.QComboBox()
        self._shots_label = QtGui.QLabel("Shots: ")
        self._shotsbox = QtGui.QComboBox()

        self._phasesbox.activated[str].connect(self.populate_shotsbox)
        self._phasesbox.activated[str].connect(self.populate_filepath)
        self._shotsbox.activated[str].connect(self.populate_filepath)

        self._collectData_layout.addWidget(self._phases_label)
        self._collectData_layout.addWidget(self._phasesbox, 1)
        self._collectData_layout.addWidget(self._shots_label)
        self._collectData_layout.addWidget(self._shotsbox, 1)

    def create_filepath(self):
        self._filepath_lineedit = QtGui.QLineEdit()
        self._filepath_layout.addWidget(self._filepath_lineedit, 1)

    def populate_phasesbox(self):
        keys = self.getShots().keys()
        self._phasesbox.addItem('ALL')
        for key in keys:
            self._phasesbox.addItem(key)
        self._phasesbox.setCurrentIndex(0)

    def populate_shotsbox(self):
        self._shotsbox.clear()
        shots = self.getShots()
        currentPhase = self._phasesbox.currentText()
        self._shotsbox.addItem('ALL')
        for key, values in shots.items():
            if key == currentPhase:
                for value in values:
                    self._shotsbox.addItem(str(value))

    def populate_filepath(self):
        currentPhase = self._phasesbox.currentText()
        currentShot = self._shotsbox.currentText()
        if currentPhase == 'ALL':
            self._filepath_lineedit.setText(self._nukeroot)
        else:
            if currentShot == 'ALL':
                self._filepath_lineedit.setText('/'.join(
                    (self._nukeroot, currentPhase)))
            else:
                self._filepath_lineedit.setText('/'.join(
                    (self._nukeroot, currentPhase, currentShot)))

    # def create_archive_button(self):
    #     self._archive_button = self.createButton("Archive", self.on_button_clicked)

    #     self._unarchive_checkbox = QtGui.QCheckBox("Unarchive")
    #     self._unarchive_checkbox.setChecked(False)
    #     self._unarchive_checkbox.stateChanged.connect(lambda:self.btnstate(self._unarchive_checkbox))

    #     self._archivebutton_layout.addWidget(self._archive_button)
    #     self._archivebutton_layout.addWidget(self._unarchive_checkbox)

    # def create_unarchive_checkbox(self):
    #     self._unarchive_checkbox = QtGui.QCheckBox("Unarchive", self)
    #     self._unarchive_checkbox.setChecked(False)
    #     self._unarchive_checkbox.stateChanged.connect(lambda:self.btnstate(self.b1))
    #     self._archivebutton_layout.addWidget(self._unarchive_checkbox)

    # def btnstate(self, b):
    #     if self._unarchive_checkbox.isChecked() == True:
    #         self._archive_button.setText("Unarchive")
    #     if self._unarchive_checkbox.isChecked() == False:
    #         self._archive_button.setText("Archive")

    #--------------------------------------------------------------------------
    # Run the task
    #--------------------------------------------------------------------------
    def run(self):
        logfile = open(self._animroot + "/.archiveDATA", "a")
        if self._oldScriptsDict:
            self.archiveNukeScripts(self._oldScriptsDict, logfile)
        if self._usedScriptsDict:
            self.archiveShotFrames(self._shotsToBeArchived, logfile)
        self.taskFinished.emit()
        logfile.close()

    #--------------------------------------------------------------------------
    # Test functions
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # Get functions
    #--------------------------------------------------------------------------
    def collectData(self):
        print("----- In collectData -----")
        try:
            # nukeroot = self.getRootDirs()
            self._usedScriptsDict, self._oldScriptsDict = self.getNukeScripts(
                self._filepath_lineedit.text())
            self._shotsToBeArchived = self.getShotsToBeArchived(
                self._usedScriptsDict)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        self.taskFinished.emit()
        print("----- Out collectData -----")

    def getRootDirs(self):
        scriptPath = nuke.root()['name'].value()
        projectRoot = scriptPath.split('Animation')[0]
        animRoot = projectRoot + 'Animation/'
        nukeRoot = animRoot + scriptPath.split('Animation')[1].split('/')[1]
        return animRoot, nukeRoot

    def getNukeScripts(self, currentDir):
        print("\n>>> In getNukeScripts")
        inUseScripts = []
        oldScripts = []
        inUseScriptsDict = {}
        oldScriptsDict = {}
        if "_NUKE" in currentDir:
            for dirpath, dirnames, filenames in os.walk(currentDir,
                                                        topdown=True):
                dirnames[:] = [d for d in dirnames if d not in "_archive"]
                if filenames:
                    filteredScripts = [
                        s for s in filenames if (s[-3:] == ".nk")
                    ]
                    print("   Filtered Scripts: %s" % (filteredScripts))
                    try:
                        inUseScripts = self.mostRecentFiles(filteredScripts)
                        print("   In Use Scripts: %s" % (inUseScripts))
                    except:
                        print("   No valid files %s" % (filteredScripts))
                        pass
                    oldScripts = [
                        x for x in filenames if x not in inUseScripts
                    ]
                    inUseScriptsDict[dirpath.replace('\\', '/')] = inUseScripts
                    oldScriptsDict[dirpath.replace('\\', '/')] = oldScripts
        else:
            print(
                " !!!! NOT A NUKE PATH.  PLEASE SPECIFY A PATH TO NUKE SCRIPTS !!!!"
            )
        print(inUseScriptsDict)
        print("<<< Out getNukeScripts \n")
        return inUseScriptsDict, oldScriptsDict

    def mostRecentFiles(self, files):
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

    def getShots(self):
        # animroot, nukeroot = self.getRootDirs()
        print("self._nukeroot: %s" % (self._nukeroot))
        shotsDict = {}
        for directory in os.listdir(self._nukeroot):
            shotsDict[directory] = os.listdir(
                os.path.join(self._nukeroot, directory))
        return shotsDict

    def getShotsToBeArchived(self, usedScriptsDict):
        print("\n>>> In getShotsToBeArchived")
        shotsToBeArchived = {}
        shotDir = []
        for dirpath, scripts in list(usedScriptsDict.items()):
            for script in scripts:
                frames = sorted(
                    self.getFramesUsedInNukeScript('/'.join(
                        (dirpath, script))))
                print("   Dirpath: %s" % (dirpath))
                print("   Script: %s\n" % (script))
                for frame in frames:
                    frame = frame.rstrip().strip('"').replace('//', '/')
                    pathInfo = frame.split('/')
                    if "MODO_" in frame:
                        print("   *** Modo Frame ***")
                        print("   Frame: %s\n" % (frame))
                        if "/".join(pathInfo[0:-4]) in shotsToBeArchived:
                            shotsToBeArchived["/".join(pathInfo[0:-4])].append(
                                "/".join(pathInfo[0:-3]))
                        else:
                            shotsToBeArchived["/".join(
                                pathInfo[0:-4])] = ["/".join(pathInfo[0:-3])]
                    elif "MAYA_" in frame:
                        print("   *** Maya Frame ***")
                        print("   Frame: %s\n" % (frame))
                        if "/".join(pathInfo[0:-4]) in shotsToBeArchived:
                            shotsToBeArchived["/".join(pathInfo[0:-4])].append(
                                "/".join(pathInfo[0:-3]))
                        else:
                            shotsToBeArchived["/".join(
                                pathInfo[0:-4])] = ["/".join(pathInfo[0:-3])]
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
        totalShotSize = 0
        self.printConsole.emit(str("\n"))
        self.printConsole.emit(str("SHOTS TO BE ARCHIVED:"))
        for shot, versions in shotsToBeArchived.items():
            self.printConsole.emit(str(shot))
            for version in self.uniqifyList(versions):
                shotsize = self.get_size(version)
                totalShotSize += shotsize
                self.printConsole.emit(
                    str("----- %s (%s)" %
                        (version.split('/')[-1], self.convert_size(shotsize))))
            self.printConsole.emit(str("\n"))
            self.taskFinished.emit()
        self.printConsole.emit(
            str("\nTOTAL ARCHIVE SIZE: %s" %
                (self.convert_size(totalShotSize))))
        self.printConsole.emit(str("___________________________________\n"))
        print("<<< Out getShotsToBeArchived \n")
        return shotsToBeArchived

    def getFramesUsedInNukeScript(self, nukescript):
        print("\n>>> In getFramesUsedInNukeScript")
        print("   Nuke Script: %s" % (nukescript))
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
                        print("   !!!!! Found Alien File !!!!!")
                        print("   Line: %s" % (line))
                        lines_to_edit.append(line)
                    else:
                        print("   Line: %s" % (line))
                        print("      Appending: %s" %
                              (line.split("file ")[-1]))
                        usedFrames.append(line.split("file ")[-1])
                        foundRead = False
        if lines_to_edit:
            print("   Updating file to fix alien file location")
            for line in lines_to_edit:
                self.printConsole.emit(
                    str("FILE FOUND OUTSIDE OF ANIMATION DIRECTORY"))
                self.printConsole.emit(
                    str("   %s" % (line.split('file ')[1].rstrip())))
                # replacement_text = " file " + self.moveAlienFiles(line, nukescript)
                # self.editScript(nukescript, line, replacement_text)
                # self.printConsole.emit(str("\n"))
                self.printConsole.emit(str("\n"))
                self.taskFinished.emit()
        print("<<< Out getFramesUsedInNukeScript \n")
        return usedFrames

    def moveAlienFiles(self, line, nukeScript):
        print("\n>>> In moveAlienFiles")
        self.printConsole.emit(str("!!!!! Found Alien File !!!!!"))
        oldpath = line.split('file ')[1].rstrip()
        filename = line.split('/')[-1].replace(' ', '_').rstrip()
        script = nukeScript.replace('\\', '/')
        moviespath = (
            script.split('Animation'))[0] + 'Animation/images/Comp_Assets/'
        newpath = '/'.join((moviespath, filename))
        shutil.move(oldpath, newpath)  ### Comment to turn off
        print("   Moved: %s to %s" % (filename, moviespath))
        self.printConsole.emit(
            str("   Moving File: %s -- to -- %s" % (filename, moviespath)))
        self.taskFinished.emit()
        print("<<< Out moveAlienFiles \n")
        return newpath

    def editScript(self, filename, text_to_search, replacement_text):
        print("\n>>> In editScript")
        print("   Reading in file: %s" % (filename))
        with open(filename, 'r') as file:  ### Comment to turn off
            filedata = file.read()
        print("   Searching for: %s" % (text_to_search))
        print("   Replacing with: %s" % (replacement_text))
        filedata = filedata.replace(text_to_search,
                                    replacement_text)  ### Comment to turn off
        print("   Making backup of: %s" % (filename))
        self.printConsole.emit(str("   Making backup of: %s" % (filename)))
        shutil.copy2(filename, filename + '.bak')  ### Comment to turn off
        print("   Writing out changes to: %s" % (filename))
        with open(filename, 'w') as file:  ### Comment to turn off
            file.write(filedata)
        self.printConsole.emit(str("   Editing: %s" % (filename)))
        self.taskFinished.emit()
        print("<<< Out editScript \n")

    #--------------------------------------------------------------------------
    # Action functions
    #--------------------------------------------------------------------------
    def archiveShotFrames(self, shotsToBeArchived, logfile):
        print("\n>>> In archiveShotFrames")
        self.printConsole.emit(str("\n\n"))
        self.printConsole.emit(str("Archiving Frames"))
        for dirpath, framePaths in list(shotsToBeArchived.items()):
            shotDirList = []
            for path in self.getImmediateSubdirectories(dirpath):
                print("   subDir: %s" % (path))
                shotDirList.append(dirpath + "/" + path)
            for dirpath in [
                    x for x in shotDirList
                    if x not in self.uniqifyList(framePaths)
            ]:
                if "_archive" not in dirpath:
                    pathInfo = dirpath.split("/")
                    archivePath = "/".join(
                        pathInfo[0:-1]) + "/_archive/" + pathInfo[-1]
                    self.printConsole.emit(str("    Moving..... " + dirpath))
                    self.printConsole.emit(
                        str("    To..... " + archivePath + "\n"))
                    logfile.write(archivePath + "\n")
                    shutil.move(dirpath, archivePath)  ### Comment to turn off
                    self.taskFinished.emit()
            print(
                "\n---------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            )
        # logging.shutdown()
        print("<<< Out archiveShotFrames \n")

    def archiveNukeScripts(self, oldScriptsDict, logfile):
        print("\n>>> In archiveNukeScripts")
        print(str("   Archiving Nuke Scripts"))
        self.printConsole.emit(str("Archiving Nuke Scripts"))
        for dirpath, scripts in list(oldScriptsDict.items()):
            archivePath = dirpath + "/_archive"
            if not os.path.exists(archivePath):
                print(str("    Making: " + archivePath))
                os.makedirs(archivePath)  ### Comment to turn off
            for script in scripts:
                self.printConsole.emit(
                    str("    Moving..... " + dirpath + "\\" + script))
                self.printConsole.emit(
                    str("    To..... " + archivePath + "\\" + script + "\n"))
                logfile.write(archivePath + "\n")
                shutil.move(dirpath + "/" + script, archivePath + "/" +
                            script)  ### Comment to turn off
                self.taskFinished.emit()
        print("<<< Out archiveNukeScripts")

    def getImmediateSubdirectories(self, a_dir):
        print("\n>>> In getImmediateSubdirectories")
        print("   a_dir: %s" % (a_dir))
        print("<<< Out getImmediateSubdirectories \n")
        return [
            name for name in os.listdir(a_dir)
            if os.path.isdir('/'.join((a_dir, name)))
        ]

    def uniqifyList(self, seq):
        # not order preserving
        set = {}
        list(map(set.__setitem__, seq, []))
        return list(set.keys())

    def get_size(self, start_path='.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def collectArchiveData(self):
        print("\n>>> In collectArchiveData")
        logfile = open(self._animroot + "/.archiveDATA")
        lines = logfile.readlines()
        archivedata = self.uniqifyList(lines)
        archivedata.sort()
        print("<<< Out collectArchiveData")
        return archivedata

    def joinUnixPaths(self, root, *args):
        output = root
        for arg in args:
            output += ("/" + arg)
        return output


#############################


class ArchiveUI(QtGui.QWidget):
    #--------------------------------------------------------------------------
    # Set Signals
    #--------------------------------------------------------------------------
    taskStart = QtCore.Signal(str)

    #--------------------------------------------------------------------------
    # Set Init
    #--------------------------------------------------------------------------
    def __init__(self, parent=None):
        super(ArchiveUI, self).__init__(parent)
        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle('Frames Archive Tool v0.1.1')
        #--------------------------------------------------------------------------
        # Create ArchiveTask object
        #--------------------------------------------------------------------------
        self.myArchiveTask = ArchiveTask()

        #--------------------------------------------------------------------------
        # Set layouts
        #--------------------------------------------------------------------------
        self._mainlayout = QtGui.QVBoxLayout()
        self._progressbar_layout = QtGui.QHBoxLayout()
        self._console_layout = QtGui.QVBoxLayout()
        self._archivebutton_layout = QtGui.QHBoxLayout()

        #--------------------------------------------------------------------------
        # Creating Widget Items
        #--------------------------------------------------------------------------
        self.create_progressbar()
        self.create_message_box()
        self.create_archive_button()
        # self.create_unarchive_checkbox()

        #--------------------------------------------------------------------------
        # Populate main layout
        #--------------------------------------------------------------------------
        self._mainlayout.addLayout(self.myArchiveTask._collectData_layout)
        self._mainlayout.addLayout(self.myArchiveTask._filepath_layout)
        self._mainlayout.addLayout(self._progressbar_layout)
        self._mainlayout.addLayout(self._console_layout)
        self._mainlayout.addLayout(self._archivebutton_layout)
        self.setLayout(self._mainlayout)

        # Init signal emitter
        self.taskStart.connect(self.onStart)

        # Call progress loop
        self.myArchiveTask.taskFinished.connect(self.onFinished)
        self.myArchiveTask.printConsole.connect(self.printToConsole)

    #--------------------------------------------------------------------------
    # Slot/Signal functions
    #--------------------------------------------------------------------------
    @QtCore.Slot(str)
    def printToConsole(self, message):
        self.taskStart.emit(message)

    @QtCore.Slot(str)
    def onStart(self, message):
        # Start pulsation and print to console
        self._console.append(message)
        self._progressBar.setRange(0, 0)

    @QtCore.Slot()
    def on_button_clicked(self):
        # Start the task
        print("Start Archive")
        self.myArchiveTask.start()

    @QtCore.Slot()
    def onFinished(self):
        # Stop the pulsation
        self._progressBar.setRange(0, 1)
        self._progressBar.setValue(1)

    #--------------------------------------------------------------------------
    # Main layout functions
    #--------------------------------------------------------------------------
    def create_progressbar(self):
        self._progressBar = QtGui.QProgressBar(self)
        self._progressBar.setRange(0, 1)
        self._progressbar_layout.addWidget(self._progressBar)

    def create_archive_button(self):
        _archive_button = self.createButton("Archive", self.on_button_clicked)
        self._archivebutton_layout.addWidget(_archive_button)

    def create_message_box(self):
        self._console = QtGui.QTextBrowser()
        self._console_layout.addWidget(self._console)

    def createButton(self, text, member, icon=""):
        if icon:
            button = QtGui.QPushButton(QtGui.QIcon(icon), text)
        else:
            button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button


def launch_gui():
    global execGui
    execGui = ArchiveUI()
    execGui.resize(1200, 650)
    execGui.show()


# if __name__ == "__main__":
#     # app = QtGui.QApplication(sys.argv)
#     window = ArchiveUI()
#     window.resize(1200, 650)
#     window.show()
#     # sys.exit(app.exec_())
