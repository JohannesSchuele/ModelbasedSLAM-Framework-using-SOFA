import Sofa
import os
import math
#path = os.path.dirname(os.path.abspath(__file__))+'/mesh/'


def createScene(rootNode):
                
                rootNode.findData('dt').value = 0.1
                rootNode.findData('gravity').value='0 0 -9.81'
                # Adding the Soft-Robotics Plugin and the SofaPython  plugin
                rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
                rootNode.createObject('RequiredPlugin', name='SofaPython')
                rootNode.createObject('RequiredPlugin', name='SofaMiscCollision')
                rootNode.createObject('DefaultPipeline', name="DefaultCollisionPipeline", verbose="0", draw="0", depth="6")
                rootNode.createObject('BruteForceDetection', name="Detection")
                rootNode.createObject('DefaultContactManager', response="default", name="collision response")
                rootNode.createObject('PythonScriptController', filename="CameraController_groundTruth.py", classname="controller")
                rootNode.createObject('MinProximityIntersection', name="Proximity", alarmDistance="0.8", contactDistance="0.64")
                rootNode.createObject('TreeCollisionGroupManager', name="Group")
#                rootNode.createObject('OglSceneFrame', style="1")
                rootNode.createObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels hideCollisionModels hideBoundingCollisionModels hideForceFields hideInteractionForceFields hideWireframe')
                rootNode.createObject('BackgroundSetting', color='0.2 0.2 0.2')
#                rootNode.createObject('RecordedCamera', name='recCamera', rotationLookAt="0 0 0", rotationStartPoint="0 6 -6", rotationCenter="0 6 0", listening="true", endTime="50", drawRotation="1", rotationMode="1")
                rootNode.createObject('RecordedCamera', name='recCamera', rotationLookAt="0 0 5", rotationStartPoint="0 0 0", rotationCenter="1 1 0", listening="true", endTime="50", drawRotation="0", rotationMode="1", rotationAxis="0 0 1",cameraUp = "0 -1 0")

                
                translation = "0 0 5"
                rotation = "0 0 0"
                
                ellipsoid = rootNode.createChild('ellipsoid')
                ellipsoid.createObject('EulerImplicit', name='odesolver', rayleighStiffness='0.1', rayleighMass='0.1')
                ellipsoid.createObject('SparseLDLSolver', name='directSolver')
                ellipsoid.createObject('MeshVTKLoader', name='loader', filename='../mesh/blender_ellipsoid.vtk')
                ellipsoid.createObject('Mesh', src='@loader', name='container')
                ellipsoid.createObject('MechanicalObject', name='tetras', template='Vec3d', showObject='false', showObjectScale='1',translation=translation, rotation =rotation)
                ellipsoid.createObject('UniformMass', totalMass='0.01')
                ellipsoid.createObject('LinearSolverConstraintCorrection', solverName='directSolver')
                
                
                ### TetrahedronFEMForceField:
                ### By using this component you choose hyperelastic model
                ### Here you can set the youngModulus to adapt the stiffness of the deformable structurepoissonRatio = 0.2
                youngModulus = 3000
                poissonRatio = 0.4
                #bellow.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio=poissonRatio,  youngModulus=youngModulus, drawAsEdges="true")

                ###StVenantKirchhoff
                mu_ = youngModulus / (2 * (1 + poissonRatio))
                lambda_ = youngModulus * poissonRatio / ((1 - 2 * poissonRatio) * (1 + poissonRatio))
                ellipsoid.createObject('TetrahedronHyperelasticityFEMForceField', materialName="StVenantKirchhoff", ParameterSet=str(mu_) + " " + str(lambda_))
                
                #### Collision
                modelCollis = ellipsoid.createChild('collisionEllipsoid')
                modelCollis.createObject('MeshSTLLoader', name='loader', filename='../mesh/blender_ellipsoid.stl')
                modelCollis.createObject('Mesh', src='@loader', name='topo')
                modelCollis.createObject('MechanicalObject', name='collisMech', translation=translation, rotation = rotation)
                modelCollis.createObject('Triangle', selfCollision="false")
                modelCollis.createObject('Line',selfCollision="false")
                modelCollis.createObject('Point', selfCollision="false")
                modelCollis.createObject('BarycentricMapping')


                #### Visualization
                modelVisu = ellipsoid.createChild('visu')
                modelVisu.createObject('MeshSTLLoader', name="visuLoader", filename="../mesh/blender_ellipsoid.stl", scale="1", translation=translation, rotation = rotation)
                modelVisu.createObject('OglModel', name="VisualModel", src="@visuLoader", texturename="../mesh/haushalt_2_edited2.jpeg", scale ="1")
                modelVisu.createObject('BarycentricMapping')
                
                
                ellipsoid.createObject('BoxROI', name='boxROI_fix', box='-1.5 -1.5 4.5 1.5 1.5 5.5', drawBoxes=True)
                ellipsoid.createObject('FixedConstraint',  name="FixedConstraint", indices="@boxROI_fix.indices")
                ellipsoid.createObject('BoxROI', name='boxROI', box='-0.1 0.3 3.5 1.0 1.5 4.5', drawBoxes=True)
#                print(ellipsoid.getObject('boxROI').findData('pointInROI').value)
                forces = ""
                # fix hard code -> number of indices in boxROI
                for i in range(1,29):
                    forces = forces + "0 0 0 "
                ellipsoid.createObject('ConstantForceField', name="CFF", indices="@boxROI.indices", forces=forces, showArrowSize="0.01")
                
                
                return rootNode
