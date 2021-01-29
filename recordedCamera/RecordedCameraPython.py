import Sofa
import os
import math
#path = os.path.dirname(os.path.abspath(__file__))+'/mesh/'


def createScene(rootNode):
                
                rootNode.findData('dt').value = 0.1
                rootNode.findData('gravity').value='0 0 0'
                # Adding the Soft-Robotics Plugin and the SofaPython  plugin
                rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
                rootNode.createObject('RequiredPlugin', name='SofaPython')
                rootNode.createObject('RequiredPlugin', name='SofaMiscCollision')
                rootNode.createObject('DefaultPipeline', name="DefaultCollisionPipeline", verbose="0", draw="0", depth="6")
                rootNode.createObject('BruteForceDetection', name="Detection")
                rootNode.createObject('DefaultContactManager', response="default", name="collision response")
                rootNode.createObject('PythonScriptController', filename="CameraControllerORB.py", classname="controller")
                rootNode.createObject('MinProximityIntersection', name="Proximity", alarmDistance="0.8", contactDistance="0.64")
                rootNode.createObject('TreeCollisionGroupManager', name="Group")
#                rootNode.createObject('OglSceneFrame', style="1")
#                rootNode.createObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels showCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')
                rootNode.createObject('BackgroundSetting', color='0.2 0.2 0.2')
#                rootNode.createObject('RecordedCamera', name='recCamera', rotationLookAt="0 0 0", rotationStartPoint="0 6 -6", rotationCenter="0 6 0", listening="true", endTime="50", drawRotation="1", rotationMode="1")
                rootNode.createObject('RecordedCamera', name='recCamera', rotationLookAt="0 0 5", rotationStartPoint="0 0 0", rotationCenter="1 1 0", listening="true", endTime="50", drawRotation="0", rotationMode="1", rotationAxis="0 0 1",cameraUp = "0 -1 0")


                visu = rootNode.createChild('visu')
                #Using material contained in liver-smooth.obj
                visu.createObject('MeshSTLLoader', name="meshLoader_0", filename="../mesh/blender_ellipsoid.stl", scale="1", translation="0 0 5", rotation = "0 0 0")
#                                , handleSeams="1", scaleTex="100 100"
                visu.createObject('OglModel', name="VisualModel", src="@meshLoader_0", texturename="../mesh/haushalt_2_edited2.jpeg", scale ="1")
                #visu.createObject('BarycentricMapping', input="@..", output="@VisualModel", name="visual mapping")
                

                
                
#                floor = rootNode.createChild('floor')
#                floor.createObject('MeshObjLoader', name="meshLoader_1", filename="../mesh/floor.obj", handleSeams="1", scaleTex="0.05 0.05", scale3d="1 1 1", translation="0 0 100")
#                floor.createObject('OglModel', name="VisualModel", src="@meshLoader_1", texturename="../mesh/cubemap_bk.bmp")



                
                return rootNode
