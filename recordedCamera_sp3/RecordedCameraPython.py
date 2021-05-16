import Sofa
import Sofa.Gui
import Sofa.Core
import Sofa.Simulation

import os
import math
#path = os.path.dirname(os.path.abspath(__file__))+'/mesh/'

#from CameraControllerP3 import controller

def createScene(rootNode):
#                Sofa.Gui.GUIManager.Init("simple_scene", "qtviewer")
                rootNode.findData('dt').value = 0.1
                rootNode.findData('gravity').value= [0, 0, 0]
                rootNode.addObject('RequiredPlugin', name="SofaPython3", printLog=False)
                rootNode.addObject('RequiredPlugin', name='SofaOpenglVisual')
                rootNode.addObject('RequiredPlugin', pluginName = 'SofaGeneralVisual')
                rootNode.addObject('RequiredPlugin', name='SofaMiscCollision')
                rootNode.addObject('LightManager')
                rootNode.addObject('DefaultPipeline', name="DefaultCollisionPipeline", verbose=0, draw=0, depth=6)
                rootNode.addObject('BruteForceDetection', name="Detection")
                rootNode.addObject('DefaultContactManager', response="default", name="collision response")
                rootNode.addObject('MinProximityIntersection', name="Proximity", alarmDistance=0.8, contactDistance=0.64)
                rootNode.addObject('TreeCollisionGroupManager', name="Group")
                rootNode.addObject('BackgroundSetting', color = [0,0,0])
                #rootNode.addObject('RecordedCamera', name='camera', rotationLookAt="0 0 5",
                    #                rotationStartPoint="0 0 0", rotationCenter="1 1 0", listening="true",
                      #              endTime="50", drawRotation="0", rotationMode="1", rotationAxis="0 0 1",
                        #            cameraUp="0 -1 0")
                rootNode.addObject('RecordedCamera', name='camera', rotationLookAt=[0, 0, 5],
                                    rotationStartPoint=[0, 0, 0], rotationCenter=[1, 1, 0], listening="true",
                                    endTime=50, drawRotation=0, rotationMode=1, rotationAxis=[0, 0, 1],
                                    cameraUp=[0, -1, 0])
                                    

#                rootNode.addObject(controller(name="CameraController", node=rootNode))




                translation = [0, 0, 5]
                rotation = [0, 0, 0]
                
                ellipsoid = rootNode.addChild('ellipsoid')
                ellipsoid.addObject('EulerImplicit', name='odesolver', rayleighStiffness=0.1, rayleighMass=0.1)
                ellipsoid.addObject('SparseLDLSolver', name='directSolver')
                ellipsoid.addObject('MeshVTKLoader', name='loader', filename='../mesh/blender_ellipsoid.vtk')
                ellipsoid.addObject('Mesh', src='@loader', name='container')
                ellipsoid.addObject('MechanicalObject', name='tetras', template='Vec3d', showObject='false', showObjectScale=1,translation=translation, rotation =rotation)
                ellipsoid.addObject('UniformMass', totalMass=0.01)
                ellipsoid.addObject('LinearSolverConstraintCorrection', solverName='directSolver')
                
                
                ### TetrahedronFEMForceField:
                ### By using this component you choose hyperelastic model
                ### Here you can set the youngModulus to adapt the stiffness of the deformable structurepoissonRatio = 0.2
                youngModulus = 3000
                poissonRatio = 0.4
                #bellow.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio=poissonRatio,  youngModulus=youngModulus, drawAsEdges="true")

                ###StVenantKirchhoff
                mu_ = youngModulus / (2 * (1 + poissonRatio))
                lambda_ = youngModulus * poissonRatio / ((1 - 2 * poissonRatio) * (1 + poissonRatio))
                ellipsoid.addObject('TetrahedronHyperelasticityFEMForceField', materialName="StVenantKirchhoff", ParameterSet=[mu_, lambda_])
                
                #### Collision
                modelCollis = ellipsoid.addChild('collisionEllipsoid')
                modelCollis.addObject('MeshSTLLoader', name='loader', filename='../mesh/blender_ellipsoid.stl')
                modelCollis.addObject('Mesh', src='@loader', name='topo')
                modelCollis.addObject('MechanicalObject', name='collisMech', translation=translation, rotation = rotation)
                modelCollis.addObject('Triangle', selfCollision="false")
                modelCollis.addObject('Line',selfCollision="false")
                modelCollis.addObject('Point', selfCollision="false")
                modelCollis.addObject('BarycentricMapping')


                #### Visualization
                modelVisu = ellipsoid.addChild('visu')
                modelVisu.addObject('MeshSTLLoader', name="visuLoader", filename="../mesh/blender_ellipsoid.stl", scale=1, translation=translation, rotation = rotation)
                modelVisu.addObject('OglModel', name="VisualModel", src="@visuLoader", texturename="../mesh/suchbild.dds", scale =1)
                modelVisu.addObject('BarycentricMapping')
                
                
                ellipsoid.addObject('BoxROI', name='boxROI_fix', box='-1.5 -1.5 4.5 1.5 1.5 5.5', drawBoxes=True)
                ellipsoid.addObject('FixedConstraint',  name="FixedConstraint", indices="@boxROI_fix.indices")
                ellipsoid.addObject('BoxROI', name='boxROI', box='-0.1 0.3 3.5 1.0 1.5 4.5', drawBoxes=True)
#                print(ellipsoid.getObject('boxROI').findData('pointInROI').value)
#                p = root["ellipsoid.boxROI.indices"]
#                print(rootNode["ellipsoid.boxROI.indices"])
#                print(rootNode.ellipsoid.boxROI.findData("nbIndices").value)      ## Ffast access
                forces = []
                # fix hard code -> number of indices in boxROI
                for i in range(1,29):
                    forces.append([0,0,0])
                ellipsoid.addObject('ConstantForceField', name="CFF", indices="@boxROI.indices", forces=forces) # , showArrowSize=0.1)
            
                rootNode.addObject("DirectionalLight", direction=[0, 1, 1])
                rootNode.addObject("DirectionalLight", direction=[0, -1, -1])
                # rootNode.addObject("DirectionalLight", direction=[1, 0, 5])
                # rootNode.addObject("DirectionalLight", direction=[0, 0, 5])
            
            
                return rootNode
