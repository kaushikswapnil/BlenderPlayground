import bpy
import os
import sys

#specify script to execute
scriptFile = "metaballs.py"

#check if script is executed in blender and get the absolute path 
#of current folder
#filesDir = os.path.dirname(os.path.abspath(__file__))
#filesDir = os.getcwd();
#filesDir = os.path.dirname(bpy.context.space_data.text.filepath)
filepath = bpy.data.filepath
filesDir = os.path.dirname(filepath)
#print(filesDir)

#get current scripts folder
#filesDir = os.path.realpath(filesDir)
#cwd = filesDir
cwd = os.path.join(filesDir, "scripts")
#print(cwd)
#cwd = cwd.replace("//", "")
#print(cwd)
#set this as search path for modules
sys.path.append(cwd)
#print(cwd)
#change current working directory
os.chdir(cwd)

#compile and execute script
file = os.path.join(cwd, scriptFile)
exec(compile(open(file).read(), scriptFile, 'exec'))