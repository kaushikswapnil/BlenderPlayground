import bpy
import colorsys
from math import sqrt, pi, sin, ceil
from random import TWOPI
import utils

#grid & cube
numCubes = 16
invCubeCount = 1.0 / (numCubes - 1)

gridSize = 8.0

cubePadding = 0

cubeSize = (gridSize / numCubes) - cubePadding
minCubeSize = cubeSize * 0.25
maxCubeSize = cubeSize * gridSize
cubeSizeRange = maxCubeSize - minCubeSize

jprc = 0.0
kprc = 0.0

diffGridSize = gridSize * 2;

posX = 0.0
posY = 0.0

origin = (0, 0, 0)

rise = 0.0
run = 0.0
normDist = 0.0
maxDist = sqrt(2 * gridSize * gridSize)

#animation & keyframe
curFrame = 0

keyFrameCount = 150
invKeyFrameCount = 1.0 / (keyFrameCount - 1)

frameRange = bpy.context.scene.frame_end - bpy.context.scene.frame_start
if frameRange == 0:
    bpy.context.scene.frame_end = 150
    bpy.context.scene.frame_start = 0
    frameRange = 150
else:
    keyFrameCount = frameRange; #to return to start pos
    
fIncr = ceil(frameRange * invKeyFrameCount)

#wave
offset = 0.0
angle = 0.0

#remove elements
utils.RemoveAllElements();

#create camera
target = utils.CreateNewTarget()
camera = utils.CreateNewCamera((-30, -10, 15), target)

for cubeIterX in range(0, numCubes, 1):
    jprc = cubeIterX * invCubeCount
    posY = -gridSize + jprc * diffGridSize;
    
    rise = posY - origin[1]
    rise *= rise
    
    for cubeIterY in range(0, numCubes, 1):
        kprc = cubeIterY * invCubeCount
        posX = -gridSize + kprc * diffGridSize
        
        run = posX - origin[0]
        run *= run
        
        normDist = sqrt(rise + run) / maxDist
        offset = -TWOPI * normDist + pi
        
        bpy.ops.mesh.primitive_cube_add(location = (origin[0] + posX, origin[1] + posY, origin[2]), size = 2*cubeSize)
        
        current = bpy.context.object
        current.name = 'Cube ({0:0>2d}, {1:0>2d})'.format(cubeIterX, cubeIterY)
        current.data.name = 'Mesh ({0:0>2d}, {1:0>2d})'.format(cubeIterX, cubeIterY)
        
        #create and add new material
        mat = bpy.data.materials.new(name = 'Material ({0:0>2d}, {1:0>2d})'.format(cubeIterX, cubeIterY))
        rgb = colorsys.hsv_to_rgb(normDist, 0.875, 1.0);
        mat.diffuse_color = (rgb[0], rgb[1], rgb[2], 1)
        current.data.materials.append(mat)
        
        #add key frames
        curFrame = bpy.context.scene.frame_start;
        for keyFrameIter in range(0, keyFrameCount, 1):
            #convert keyframe into angle
            fprc = keyFrameIter * invKeyFrameCount
            angle = TWOPI * fprc
            
            #set scene to current frame
            bpy.context.scene.frame_set(curFrame)
            
            #change scale
            current.scale[2] = minCubeSize + (sin(offset + angle)) * cubeSizeRange
            
            #insert key frame for scale property
            current.keyframe_insert(data_path='scale', index = 2)
            
            curFrame += fIncr
