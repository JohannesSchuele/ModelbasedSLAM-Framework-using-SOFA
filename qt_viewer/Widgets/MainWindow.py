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
        self.mat_engine = EngineORB(mat_dir=self.mat_dir, skip_images=4)

        
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Space:
            if self.sofa_sim.is_animating:
                self.sofa_sim.stop_sim()
                if self.mat_engine.is_mapping:
                    self.mat_engine.stop_slam()
            else:
                self.sofa_sim.start_sim()
                
        if QKeyEvent.key() == Qt.Key_G: # G for GO
            if self.mat_engine.is_mapping:
                self.mat_engine.stop_slam()
            elif self.sofa_sim.is_animating:
                self.mat_engine.is_mapping = True
                self.sofa_sim.animation_end.connect(self.update_slam) # set a qt signal to update slam after sim step
                self.mat_engine.viewer_info(viewer_size=self.sofa_view.get_viewer_size(), intrinsics=self.sofa_view.get_intrinsic_parameters())

                
    def update_slam(self):
        if self.mat_engine.skip_counter == self.mat_engine.skip_images:
            self.mat_engine.skip_counter = 0
            if self.mat_engine.is_initialized:
                self.mat_engine.main_slam(image=self.sofa_view.get_screen_shot())
            else:
                self.mat_engine.initialize_slam(image=self.sofa_view.get_screen_shot())
        else:
            self.mat_engine.skip_counter += 1
               
            
                
                

                