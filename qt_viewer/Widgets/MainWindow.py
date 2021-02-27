from qtpy.QtCore import *
from qtpy.QtWidgets import *
from .SofaGLViewer import SofaGLViewer
from .SofaSim import SofaSim
from .QXBoxViewController import QXBoxViewController
from .QSofaViewKeyboardController import QSofaViewKeyboardController
from .engineORB import EngineORB
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sofa_sim = SofaSim()  # class to hold the scene
        self.sofa_sim.init_sim()  # initialize the scene

        # create an opengl view to display a node from sofa and control a camera
        self.sofa_view = SofaGLViewer(sofa_visuals_node=self.sofa_sim.root, camera=self.sofa_sim.root.camera)

        # set the view to be the main widget of the window. In the future, this should be done in a layout
        self.setCentralWidget(self.sofa_view)

        self.sofa_sim.animation_end.connect(self.sofa_view.update)  # set a qt signal to update the view after sim step

        # Add a class to control a view's camera using an xbox controller
        # self.view_control = QXBoxViewController(dead_zone=0.3, translate_rate_limit=1.5, rotate_rate_limit=20)
        # self.view_control.set_viewer(self.sofa_view)  # set the active view to control
        self.view_control = QSofaViewKeyboardController(translate_rate_limit=1.5, rotate_rate_limit=5, update_rate=20)
        self.view_control.set_viewer(self.sofa_view)

        # draw the scene at a constant update rate. This is done so the scene is drawn even if nothing is being animated
        self.view_control.start_auto_update()
                
        # initialize matlab engine
        self.current_dir = os.path.dirname(__file__)
        self.mat_dir = os.path.join(self.current_dir,'../../orb_slam_matlab_for_qt_viewer')
        self.mat_engine = EngineORB(mat_dir=self.mat_dir, n_init_images=10, skip_images_init = 4, skip_images_main = 2)
        self.mat_engine.set_viewer(self.sofa_view)
        self.mat_engine.set_sim(self.sofa_sim)



    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Space:
            if self.sofa_sim.is_animating:
                self.sofa_sim.stop_sim()
            else:
                self.sofa_sim.start_sim()
                self.sofa_sim.animation_start.connect(self.mat_engine.get_camera_position)
                self.sofa_sim.animation_end.connect(self.mat_engine.get_camera_orientation)
        
               
            
                
                

                