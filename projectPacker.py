#!/usr/bin/env python

"""projectPacker.py: Simple batch archive using built in Unreal Engine ZipProjectUp with Python directory parsing.

Takes a path to a root directory containing many uproject folders and user defined environment in the __init__.
Iterates through each root directory, checking for a matching .uproject to determine what should be packaged. 
Checks for the destination to ensure no other project zips with the same daily time stamp exist. 
"""

from logging import warning
import os
import sys
import datetime
import subprocess
import zipfile
import warnings
import pathlib

__author__      = "Mike Weiss"
__version__     = "2022.10.25"
__status__      = "Intial Testing"


class projectPacker:
    def __init__(self, dirPath, extraDirs=None):
        self.dirPath = dirPath
        self.debug = True
        self.dryrun = False
        self.UEInstallPath = 'C:\\Program Files\\Epic Games\\UE_5.0'
        self.outputZipRootPath = "E:/"
        self.extraDirs = ["Datasmith", "CAD", "WebControl", "WebInterface"] # Case matters
        
        warnings.simplefilter('default', UserWarning)
        
        self.logPath = os.path.abspath(os.getenv('APPDATA') + "\\Unreal Engine\\AutomationTool\\Logs\\" + self.UEInstallPath.replace(":", "").replace("\\", "+").replace(" ", "+") +"\\Log.txt")
        if self.debug: 
            # Example logpath: 
            # C:\Users\MikeWeiss\AppData\Roaming\Unreal Engine\AutomationTool\Logs\C+Program+Files+Epic+Games+UE_5.0\Log.txt
            print(self.logPath)
        

    def makezip(self):
        # Example formatting: cmd.exe /c ""C:/Program Files/Epic Games/UE_5.0/Engine/Build/BatchFiles/RunUAT.bat" ZipProjectUp -nocompileeditor -project="D:/UEProjects/MRQCommandLine/" -install="D:/UEProjects/MRQCommandLine/MRQCommandLine.zip"" -nocompile
        self.cmd = 'cmd.exe /c \"\"' + os.path.abspath(os.path.join(self.UEInstallPath + '/Engine/Build/BatchFiles/RunUAT.bat')).replace("\\", "\\\\") + '\" ZipProjectUp -nocompileeditor -project=' + self.projectDir.replace("\\", "/") + '/ -install=' + self.outputZipPath.replace("\\", "/") + ' -nocompile "'
        if self.debug: print(self.cmd) 
        if not self.dryrun:
            subprocess.check_call(self.cmd)


    def appendToZip(self):
        
        with zipfile.ZipFile(self.outputZipPath, "a") as archive:
            archive.write(self.logPath, arcname="Log.txt")
            for dirs in self.extraDirs:
                extradir = os.path.join(self.projectDir, dirs)
                if self.debug: print("Looking for", extradir)
                if os.path.exists(extradir):
                    if self.debug: print("Found the following extra directory!", extradir)
                    directory = pathlib.Path(extradir)
                    for file_path in directory.rglob("*"):
                        if self.debug: print("Appending to zip:", file_path)
                        archive.write(
                        file_path,
                        arcname=file_path.relative_to(self.projectDir)
                        )

    def main(self):
        for dir in os.listdir(self.dirPath):
            if self.debug: print(dir)
            self.cmd = "" # Clear if prior
            self.projectDir = os.path.join(self.dirPath, dir)
            self.projectName = os.path.split(self.projectDir)[-1] # Get the last one since standard is to match .uproject to folder name.
            self.datestamp = datetime.date.today()
            self.outputZipName = self.projectName + "_" + str(self.datestamp) + '.zip'
            self.projectPath = os.path.abspath(os.path.join(self.projectDir, self.projectName + ".uproject"))
            self.outputZipPath = os.path.join(self.outputZipRootPath ,self.outputZipName)
            if os.path.exists(self.projectPath):
                if os.path.exists(self.outputZipPath): # Destination zip conflict.
                    #TODO: Handle zip clashes with some logic defined by the user, skip or overwrite. 
                    warnings.warn("There is a clash for the zip destination. Please clear the destination file " + os.path.abspath(self.outputZipPath))
                else: # No Zip Conflict
                    if self.debug:
                        print("projectPath", self.projectPath)
                        print("DateTimestamp", self.datestamp)
                        print("projectName", self.projectName)
                        print("projectDir:", self.projectDir)
                        print("outputZipName", self.outputZipName)
                        print("outputZipRootPath", self.outputZipRootPath)
                        print("outputZipPath", self.outputZipPath)
                    #TODO: Add logic to determine if content is updated since last archive. 
                    self.makezip()
                self.appendToZip()
                

if __name__ == "__main__":
    #Usage: Python3 path\to\projectPacker.py path\to\UEProjectsDirRoot
    myPacker = projectPacker(sys.argv[1])
    myPacker.main()


