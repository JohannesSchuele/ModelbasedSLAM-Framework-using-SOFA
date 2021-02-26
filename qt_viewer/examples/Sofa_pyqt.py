from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtOpenGL import *

import Sofa
import SofaRuntime
import Sofa.Gui
import Sofa.Simulation as sim
import os
#sofa_directory = os.environ['SOFA_ROOT']
sofa_directory = '/Users/jona/sofa_20.12/build_20.12'
from OpenGL.GL import *
from OpenGL.GLU import *


"""
With something like this setup, we can use Sofa with our own GUI and not have to give over control of the main thread.
Simple pyqt signals can be added to manually rotate the view with the mouse (could be a tedious task to get it to
be intuitive).
"""

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sofa_sim = SofaSim()
        self.sofa_sim.init_sim()
        self.sofa_view = glSofaWidget(self.sofa_sim.visuals)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.sofa_view)
        self.setLayout(mainLayout)
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.step_sim)
        self.simulation_timer.setInterval(self.sofa_sim.root.getDt())
        self.simulation_timer.start()

    def step_sim(self):
        self.sofa_sim.step_sim()
        self.sofa_view.update()


class glSofaWidget(QGLWidget):
    def __init__(self, sofa_visuals_node):
        QGLWidget.__init__(self)
        self.visuals_node = sofa_visuals_node
        self.setMinimumSize(800, 600)

    def initializeGL(self):
        glViewport(0,0, self.width(), self.height())
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        Sofa.Simulation.glewInit()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width() / self.height()), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glViewport(0,0, self.width(), self.height())
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width()/ self.height()), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        cameraMVM = self.visuals_node.camera.getOpenGLModelViewMatrix()
        glMultMatrixd(cameraMVM)

        sim.draw(self.visuals_node)


class SofaSim():
    def __init__(self):
        # Register all the common component in the factory.
#        SofaRuntime.PluginRepository.addFirstPath(os.path.join(sofa_directory, 'bin'))
        SofaRuntime.PluginRepository.addFirstPath('/Users/jona/sofa_20.12/build_20.12/install/plugins')
        SofaRuntime.importPlugin('SofaOpenglVisual')
        SofaRuntime.importPlugin("SofaComponentAll")
        SofaRuntime.importPlugin("SofaGeneralLoader")
        SofaRuntime.importPlugin("SofaImplicitOdeSolver")
        SofaRuntime.importPlugin("SofaLoader")
        SofaRuntime.importPlugin("SofaSimpleFem")
        SofaRuntime.importPlugin("SofaBoundaryCondition")
        SofaRuntime.importPlugin("SofaMiscForceField")
        self.root = Sofa.Core.Node("Root")
        root = self.root
        root.gravity = [0, -1., 0]
        root.addObject("VisualStyle", displayFlags="showBehaviorModels showAll showVisual")
        root.addObject("MeshGmshLoader", name="meshLoaderCoarse",
                       filename="mesh/liver.msh")
        root.addObject("MeshObjLoader", name="meshLoaderFine",
                       filename="mesh/liver-smooth.obj")

        root.addObject("EulerImplicitSolver")
        root.addObject("CGLinearSolver", iterations="200",
                       tolerance="1e-09", threshold="1e-09")

        liver = root.addChild("liver")

        liver.addObject("TetrahedronSetTopologyContainer",
                        name="topo", src="@../meshLoaderCoarse")
        liver.addObject("TetrahedronSetGeometryAlgorithms",
                        template="Vec3d", name="GeomAlgo")
        liver.addObject("MechanicalObject",
                        template="Vec3d",
                        name="MechanicalModel", showObject="1", showObjectScale="3")

        liver.addObject("TetrahedronFEMForceField", name="fem", youngModulus="1000",
                        poissonRatio="0.4", method="large")

        liver.addObject("MeshMatrixMass", massDensity="1")
        liver.addObject("FixedConstraint", indices="2 3 50")

        # place light and a camera
        self.visuals = root.addChild('visuals')
        self.visuals.addObject("LightManager")
        self.visuals.addObject("SpotLight", position=[0, 10, 0], direction=[0, -1, 0])
        self.visuals.addObject("InteractiveCamera", name="camera", position=[0, 10, 0],
                               lookAt=[0, 0, 0], distance=37,
                               fieldOfView=45, zNear=0.63, zFar=55.69)

    def init_sim(self):
        # start the simulator
        Sofa.Simulation.init(self.root)

    def step_sim(self):
        self.visuals.camera.position = self.visuals.camera.position + [-0.0002, 0, 0]
        Sofa.Simulation.animate(self.root, self.root.getDt())  # uncomment to animated sim


if __name__ == '__main__':
    app = QApplication(['Yo'])
    window = MainWindow()
    window.show()
    app.exec_()
