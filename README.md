# unreal-project-archiver
Intelligently batch archive UE Project folders with Python.

I am sure I am not the first to do this, but I made a project archival tool with Python. I keep running out of disk space and I use this to zip projects to my Archival volume. Hope it helps others too. I may make a dev tutorial on this and share it out, simply shows how to take internal UE stuff and wrap it simply with python. This could be way more sophisticated, but it serves my simple purposes today. 

It will take additional directories with self.extraDirs to package in the script itself.

```
projectPacker.py: Simple batch archive using built in Unreal Engine ZipProjectUp with Python directory parsing.

Takes a path to a root directory containing many uproject folders and user defined environment in the __init__.
Iterates through each root directory, checking for a matching .uproject to determine what should be packaged. 
Checks for the destination to ensure no other project zips with the same daily time stamp exist. 
```
