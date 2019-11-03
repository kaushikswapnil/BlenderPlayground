import bpy
import colorsys
import os
from math import sin, cos, pi
import math
import numpy as np 

tau = 2*pi

def RemoveAllElements(type = None):
	if type:
		bpy.ops.object.select_all(action = 'DESELECT')
		bpy.ops.object.select_by_type(type = type)
		bpy.obs.object.delete()
	else:
		#remove all elements in scene
		#bpy.ops.object.select_by_layer()
		#bpy.ops.object.delete(use_global = False)
		bpy.ops.object.select_all(action = 'SELECT')
		bpy.ops.object.delete()

#Camera and targets

def CreateNewTarget(origin = (0, 0, 0)):
	target = bpy.data.objects.new('Target', None)
	bpy.context.scene.collection.objects.link(target)
	target.location = origin

	return target

def CreateNewCamera(origin, target = None, lens = 35, clip_start = 0.1, clip_end = 200, type = 'PERSP', ortho_scale = 6):
	camera = bpy.data.cameras.new("Camera")
	camera.lens = lens
	camera.clip_start = clip_start
	camera.clip_end = clip_end
	camera.type = type
	if (type == 'ORTHO'):
		camera.ortho_scale = ortho_scale

	#link obj to scene
	cameraObj = bpy.data.objects.new("CameraObj", camera)
	cameraObj.location = origin
	bpy.context.scene.collection.objects.link(cameraObj)
	bpy.context.scene.camera = cameraObj #making it the default camera

	if target:
		AddTrackToConstraint(cameraObj, target)

	return cameraObj

def AddTrackToConstraint(obj, target):
	constraint = obj.constraints.new('TRACK_TO')
	constraint.target = target
	constraint.track_axis = 'TRACK_NEGATIVE_Z'
	constraint.up_axis = 'UP_Y'

	return constraint

#End of camera and targets

def AddRainbowLights(r = 5, n = 100, freq = 2, energy = 0.1):
	for i in range(n):
		t = float(i)/float(n)
		pos = (r*sin(tau*t), r*cos(tau*t), r*sin(freq*tau*t))

		#create lamp
		#bpy.ops.object.add(type='LAMP', location = pos)
		#obj = bpy.context.object
		#obj.data.type = 'POINT'

		#apply gamma correction for blender
		color = tuple(pow(c, 2.2) for c in colorsys.hsv_to_rgb(t, 0.8, 1))

		#set hsv color & lamp enery
		#obj.data.color = color
		#obj.data.energy = energy 
		lightData = bpy.data.lights.new(name = "Light", type = 'POINT')
		lightData.energy = energy
		lightData.color = color;

		lightObj = bpy.data.objects.new(name = "Light", object_data=lightData)
		bpy.context.scene.collection.objects.link(lightObj)
		bpy.context.view_layer.objects.active = lightObj
		lightObj.location = pos

def RenderToFolder(renderFolder = 'rendering', renderName = 'render', resX = 800, resY = 800, resPercentage = 100, animation = False, frame_end = None):
	print('RenderToFolder called')
	scn = bpy.context.scene
	scn.render.resolution_x = resX
	scn.render.resolution_y = resY
	scn.render.resolution_percentage = resPercentage

	if frame_end:
		scn.frame_end = frame_end

	#print(bpy.context.space_data)

	#check if script is executed in blender
	if bpy.context.space_data is not None:
	#specify folder to save rendering and check if it exists
		render_folder = os.path.join(os.getcwd(), renderFolder)
		#print(render_folder)
		if (not os.path.exists(render_folder)):
			os.mkdir(render_folder)

		if animation:
			scn.render.filepath = os.path.join(render_folder, renderName)
			bpy.ops.render.render(animation = True)
		else:
		#render still frame
			scn.render.filepath = os.path.join(render_folder, renderName + '.png')
			bpy.ops.render.render(write_still = True)

def GetRotationMatrix(axis, angle):
	axis = np.asarray(axis)
	axis = axis/math.sqrt(np.dot(axis, axis))
	a = math.cos(angle / 2.0)
	b, c, d = -axis * math.sin(angle/2.0)
	aa, bb, cc, dd = a*a, b*b, c*c, d*d
	bc, ad, ac, ab, bd, cd = b *c, a * d, a * c, a * b, b * d, c * d
	return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def GetRotatedVector(vectorToRotate, rotationAxis, angle):
	rMatrix = GetRotationMatrix(rotationAxis, angle)
	return rMatrix.dot(vectorToRotate)