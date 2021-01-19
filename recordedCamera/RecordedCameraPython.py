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
#                rootNode.createObject('OglSceneFrame', style="2")
#                rootNode.createObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels showCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')
                rootNode.createObject('BackgroundSetting', color='0.2 0.2 0.2')
                rootNode.createObject('RecordedCamera', name="cam", rotationLookAt="0 0 0", rotationStartPoint="0 6 -6", rotationCenter="0 6 0", listening="true", endTime="50", drawRotation="0", rotationMode="1")
#                rootNode.createObject('RecordedCamera', cameraPositions='6.09723 0.245606 10.51377 8.09723 1.245606 15.51377 8.09723 -1.245606 5.51377 6.09723 0.245606 10.51377 11.2328 3.82765 1.21452', cameraOrientations='-0.129003 -0.330287 -0.0526663 -0.933539 -0.129003 -0.330287 -0.0526663 -0.933539 -0.129003 -0.330287 -0.0526663 -0.933539 -0.129003 -0.330287 -0.0526663 -0.933539 -0.055733 -0.704027 -0.110098 -0.69937', name='recordedCamera0', listening='1', projectionType='0', navigationMode='1')

                visu = rootNode.createChild('visu')
                #Using material contained in liver-smooth.obj
                visu.createObject('MeshSTLLoader', name="meshLoader_0", filename="../mesh/blender_ellipsoid.stl", scale="1", translation="0 0 0", rotation = "90 0 0")
#                                , handleSeams="1", scaleTex="100 100"
                visu.createObject('OglModel', name="VisualModel", src="@meshLoader_0", texturename="../mesh/haushalt_2_edited.jpeg", scale ="1")
                #visu.createObject('BarycentricMapping', input="@..", output="@VisualModel", name="visual mapping")
                

                
                
#                floor = rootNode.createChild('floor')
#                floor.createObject('MeshObjLoader', name="meshLoader_1", filename="../mesh/floor.obj", handleSeams="1", scaleTex="0.05 0.05", scale3d="1 1 1", translation="0 0 100")
#                floor.createObject('OglModel', name="VisualModel", src="@meshLoader_1", texturename="../mesh/cubemap_bk.bmp")



                
                return rootNode
