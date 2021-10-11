import Sofa
import Sofa.Gui
import Sofa.Core
import Sofa.Simulation

import os
import math
#path = os.path.dirname(os.path.abspath(__file__))+'/mesh/'
from CameraControllerP3 import controller
def createScene(root):
#                Sofa.Gui.GUIManager.Init("simple_scene", "qtviewer")
#        root = self.root
        root.gravity = [0, -1., 0]
        root.addObject("VisualStyle", displayFlags="showBehaviorModels showVisual")
        root.addObject("MeshVTKLoader", name="meshVTK",
                       filename="../mesh/blender_ellipsoid.vtk")
#        root.addObject("MeshSTLLoader", name="meshSTL",
#                       filename="../../../mesh/blender_ellipsoid.stl")

        root.addObject("EulerImplicitSolver")
        root.addObject("CGLinearSolver", iterations="200",
                       tolerance="1e-09", threshold="1e-09")

        translation = [0, 0, 0]
        rotation = [0, 0, 0]
        stlFilename = "../mesh/blender_ellipsoid.stl"
        textureFilename = "../mesh/haushalt_2_edited2.dds"
        ellipsoid = root.addChild("ellipsoid")

#        ellipsoid.addObject("TetrahedronSetTopologyContainer",
#                        name="topo", src="@../meshVTK")
#        ellipsoid.addObject("TetrahedronSetGeometryAlgorithms",
#                        template="Vec3d", name="GeomAlgo")
        ellipsoid.addObject("Mesh", src='@../meshVTK', name="container")
        ellipsoid.addObject("MechanicalObject",
                        template="Vec3d",
                        name="MechanicalModel", showObject="0", showObjectScale="1",
                        translation=translation, rotation=rotation)
        ellipsoid.addObject("UniformMass", totalMass=0.01)
#        ellipsoid.addObject("LinearSolverConstraintCorrection", solverName="directSolver")

        ellipsoid.addObject("TetrahedronFEMForceField", name="fem", youngModulus="1000",
                        poissonRatio="0.4", method="large")

#        ellipsoid.addObject("MeshMatrixMass", massDensity="1")
        ellipsoid.addObject("BoxROI", name='boxROI_fix', box='-1.5 -1.5 -0.5 1.5 1.5 0.5', drawBoxes=True)
        ellipsoid.addObject("FixedConstraint",  name="FixedConstraint", indices="@boxROI_fix.indices")
        # Visual
        visual = ellipsoid.addChild("visual")
        visual.addObject('MeshSTLLoader', name="meshLoader_0", filename=stlFilename, translation=translation, rotation=rotation)
        visual.addObject('OglModel', name="VisualModel", src="@meshLoader_0", texturename=textureFilename, scale =1)
        visual.addObject('BarycentricMapping', input="@..", output="@VisualModel", name="visual mapping")
#        # Collision
        collision = ellipsoid.addChild("collision")
        collision.addObject("MeshSTLLoader", name="meshLoader_1",  filename=stlFilename)
        collision.addObject('Mesh', src='@meshLoader_1', name='topo')
        collision.addObject('MechanicalObject', name='collisMech', translation=translation, rotation = rotation)
        collision.addObject('Triangle', selfCollision="false")
        collision.addObject('Line',selfCollision="false")
        collision.addObject('Point', selfCollision="false")
        collision.addObject('BarycentricMapping', input="@..", output="@collisMech", name="visual mapping")
        forces = []
#        for i in range(1,32):
#            forces.append([0,0,0])
        ellipsoid.addObject('BoxROI', name='boxROI', box='-0.1 0.3 0.5 1.0 1.5 1.5', drawBoxes=True)
        ellipsoid.addObject('ConstantForceField', name="CFF", indices=[1], forces=[0,0,0], showArrowSize="0.01")
        
        # place light and a camera
        root.addObject("LightManager")
        root.addObject("DirectionalLight", direction=[0, 1, 0])
        root.addObject("Camera", name = "camera", position=[0, 0, 5],
                            lookAt=[0, 0, 0], distance=5,
                            fieldOfView=45, zNear=0.160738, zFar=9.209)
            
        # add controller
        root.addObject(controller(name="CameraControllerP3", node=root))
        return root
