import bpy
import random
from mathutils import Vector
from math import sqrt, pi, sin, ceil
from random import TWOPI
import utils
import numpy as np

def CreateMetaball(origin = (0, 0, 0), n = 8, r0 = 4, r1 = 2.5, r2 = 4.5):
    if r2 < r1:
        r2 = r1

    #animation & keyframe
    keyFrameCount = 150

    originVector = Vector(origin)

    frameRange = bpy.context.scene.frame_end - bpy.context.scene.frame_start
    if frameRange == 0:
        bpy.context.scene.frame_end = 150
        bpy.context.scene.frame_start = 0
        frameRange = 150
    else:
        keyFrameCount = frameRange #to return to start pos

    invKeyFrameCount = 1.0 / (keyFrameCount - 1)
        
    fIncr = ceil(frameRange * invKeyFrameCount)

    metaball = bpy.data.metaballs.new('Metaball')
    obj = bpy.data.objects.new('MetaballObject', metaball)
    bpy.context.scene.collection.objects.link(obj)
    
    metaball.resolution = 0.3
    metaball.render_resolution = 0.05
    
    for i in range(n):
        location = originVector + Vector(random.uniform(-r0, r0) for i in range(3))
        
        element = metaball.elements.new()
        element.co = location
        element.radius = (np.random.rand() * (r2 - r1)) + r1

    for element in metaball.elements:
        #add key frames
        aIncr = 8 * TWOPI * invKeyFrameCount * ((r1+r2)/2) * (1/element.radius)

        curFrame = bpy.context.scene.frame_start;
        #print("-----ELEMENT-----")
        for keyFrameIter in range(0, keyFrameCount, 1):
            #convert keyframe into angle

            curPosVector = element.co - originVector

            sight = curPosVector.copy()
            sight.normalize()

            horizon = Vector((1, 0, 0))
            banking = sight.cross(horizon)

            if banking.length < 0.1:
                horizon = Vector((0, 1, 0))
                banking = sight.cross(horizon)

            banking.normalize()
            horizon = banking.cross(sight);
            horizon.normalize()

            #print("----New Frame----")

            layer = bpy.context.view_layer
            layer.update()
            
            #print(element.co)
            #print(horizon)
            #print(banking)
            #print(curPosVector.length)
            newPosVector = utils.GetRotatedVector(curPosVector, horizon, aIncr)
            element.co = originVector + Vector(newPosVector)
            #print(element.co)

            #set scene to current frame
            #bpy.context.scene.frame_set(curFrame)
            #insert key frame for scale property
            element.keyframe_insert(data_path='co', frame = curFrame)
            
            curFrame += fIncr
        
    return metaball

if __name__ == '__main__':
    #remove elements
    utils.RemoveAllElements();
    
    #create camera
    target = utils.CreateNewTarget()
    camera = utils.CreateNewCamera((-10, -10, 10), target)
    
    #create lights
    utils.AddRainbowLights(7, 300, 3, 8.0)
    
    #create metaball
    metaball = CreateMetaball(n = 18, r0 = 3.8, r1 = 0.8, r2 = 3.5)
    
    #bpy.app.handlers.frame_change_pre.append(FrameUpdateHandler)

    #render scene
    #utils.RenderToFolder('rendering', 'metaballs', 500, 500, 100, animation = True, frame_end = 50)