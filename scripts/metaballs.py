import bpy
import random
from mathutils import Vector
import utils

def CreateMetaball(origin = (0, 0, 0), n = 8, r0 = 4, r1 = 2.5):
    metaball = bpy.data.metaballs.new('Metaball')
    obj = bpy.data.objects.new('MetaballObject', metaball)
    bpy.context.scene.collection.objects.link(obj)
    
    metaball.resolution = 0.3
    metaball.render_resolution = 0.05
    
    for i in range(n):
        location = Vector(origin) + Vector(random.uniform(-r0, r0) for i in range(3))
        
        element = metaball.elements.new()
        element.co = location
        element.radius = r1
        
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
    metaball = CreateMetaball()
    
    #bpy.app.handlers.frame_change_pre.append(FrameUpdateHandler)

    #render scene
    utils.RenderToFolder('rendering', 'metaballs', 500, 500)