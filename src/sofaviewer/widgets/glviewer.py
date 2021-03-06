from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import Sofa.SofaGL as SGL
import Sofa
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from typing import List
from PIL import Image


def quaternion_rotation_matrix(Q):
    """
    https://automaticaddison.com/how-to-convert-a-quaternion-to-a-rotation-matrix/
    Covert a quaternion into a full three-dimensional rotation matrix.
    Input
    :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3)
    Output
    :return: A 3x3 element matrix representing the full 3D rotation matrix.
             This rotation matrix converts a point in the local reference
             frame to a point in the global reference frame.
    """
    # Extract the values from Q
    q0 = Q[0]
    q1 = Q[1]
    q2 = Q[2]
    q3 = Q[3]

    # First row of the rotation matrix
    r00 = 2 * (q0 * q0 + q1 * q1) - 1
    r01 = 2 * (q1 * q2 - q0 * q3)
    r02 = 2 * (q1 * q3 + q0 * q2)

    # Second row of the rotation matrix
    r10 = 2 * (q1 * q2 + q0 * q3)
    r11 = 2 * (q0 * q0 + q2 * q2) - 1
    r12 = 2 * (q2 * q3 - q0 * q1)

    # Third row of the rotation matrix
    r20 = 2 * (q1 * q3 - q0 * q2)
    r21 = 2 * (q2 * q3 + q0 * q1)
    r22 = 2 * (q0 * q0 + q3 * q3) - 1

    # 3x3 rotate matrix <-- These values are tweaked to match the results obtained from scipy.spatial.transform.Rotation
    rot_matrix = np.array([[r22, -r12, r02], [r21, -r11, r01], [-r20, r10, -r00]])
    return rot_matrix


class SofaGLViewer(QOpenGLWidget):
    key_pressed = Signal(QKeyEvent)
    key_released = Signal(QKeyEvent)
    scroll_event = Signal(QWheelEvent)
    resizedGL = Signal(float, float)  # width, height

    def __init__(
        self,
        sofa_visuals_node,
        camera,  # Sofa.Core.BaseCamera
    ):

        super(SofaGLViewer, self).__init__()
        self.visuals_node = sofa_visuals_node
        self.camera = camera
        self.z_far = (
            camera.zFar
        )  # get these values using self.z***.value because they are sofa Data objects
        self.z_near = camera.zNear
        self.setFocusPolicy(Qt.StrongFocus)
        self.background_color = [25 / 255, 35 / 255, 45 / 255, 1]
        self.spheres = []

    def make_viewer_transparent(self, make_transparent=True):
        """This will only make the background of the viewer transparent if the background_color alpha is set to 0"""
        self.setAttribute(Qt.WA_TranslucentBackground, make_transparent)
        self.setAttribute(Qt.WA_AlwaysStackOnTop, make_transparent)

    def set_background_color(self, color):
        """
        :param color: [r, g, b, alpha] alpha determines opacity. Use 0 to save images with a transparent background
        """
        self.background_color = color

    def get_intrinsic_parameters(self):
        # https://github.com/opencv/opencv_contrib/blob/master/modules/viz/src/types.cpp
        pm = glGetFloatv(GL_PROJECTION_MATRIX)
        pm = np.transpose(pm)  # openGL is column-major
        near = self.z_near.value
        left = (near * (pm[0][2] - 1)) / pm[0][0]
        right = 2 * near / pm[0][0] + left
        bottom = near * (pm[1][2] - 1) / pm[1][1]
        top = 2.0 * near / pm[1][1] + bottom
        width, height = self.width(), self.height()
        # _, _, width, height = glGetIntegerv(GL_VIEWPORT)
        # height = height//2
        # width = width//2
        cx = (left * width) / (left - right)
        cy = (top * height) / (top - bottom)
        fx = -near * cx / left
        fy = near * cy / top
        return fx, fy, cx, cy

    def get_transform_to_global_coord(self):
        transformation = np.zeros((4, 4))
        transformation[:3, -1] = self.camera.position.array()
        transformation[-1, -1] = 1
        transformation[:3, :3] = quaternion_rotation_matrix(
            self.camera.orientation.array()
        )
        return transformation

    def initializeGL(self):
        glViewport(0, 0, self.width(), self.height())
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        SGL.glewInit()
        Sofa.Simulation.initVisual(self.visuals_node)
        Sofa.Simulation.initTextures(self.visuals_node)

    def paintGL(self):
        self.makeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*self.background_color)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(
            self.camera.findData("fieldOfView").value,
            (self.width() / self.height()),
            self.z_near.value,
            self.z_far.value,
        )
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera_mvm = self.camera.getOpenGLModelViewMatrix()
        glMultMatrixd(camera_mvm)
        SGL.draw(self.visuals_node)

    def resizeGL(self, w: int, h: int) -> None:
        self.camera.widthViewport = self.width()
        self.camera.heightViewport = self.height()
        glViewport(0, 0, w, h)
        self.resizedGL.emit(w, h)

    def get_depth_image(self, scaled_for_viewing=True, return_type=np.uint16):
        """ " Get the depth map as an array for displaying"""
        depth_image = self.get_depth_map()
        depth_image = (depth_image - depth_image.min()) / (
            depth_image.max() - depth_image.min()
        )
        if scaled_for_viewing:
            indices = depth_image.nonzero()
            actual_image_pixels = depth_image[indices[0][:], indices[1][:]]
            actual_image_pixels = (actual_image_pixels - actual_image_pixels.min()) / (
                actual_image_pixels.max() - actual_image_pixels.min()
            )
            depth_image[indices] = actual_image_pixels

        depth_image = depth_image * np.iinfo(return_type).max
        return depth_image.astype(return_type)

    def get_depth_map(self):
        """Get the depth value for each pixel in image"""
        self.makeCurrent()
        width, height = self.width(), self.height()
        buff = glReadPixels(0, 0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)
        image = np.frombuffer(buff, dtype=np.float32)
        image = image.reshape(height, width)
        image = np.flipud(image)  # <-- image is now a numpy array you can use
        far, near = self.z_far.value, self.z_near.value
        return -far * near / (far + image * (near - far))

    def get_screen_shot(self, return_with_alpha=False):
        """Returns the RGB image array for the current view"""
        self.makeCurrent()
        # the height and width functions are kinda buggy when using a mac, because the screen ratio is so weird
        # TODO get this more robust on a mac
        _, _, width, height = glGetIntegerv(GL_VIEWPORT)
        # width, height = self.width(), self.height()
        if return_with_alpha:
            buff = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
            image = np.frombuffer(buff, dtype=np.uint8)
            return np.flipud(image.reshape(height, width, 4))
        else:
            buff = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
            image = np.frombuffer(buff, dtype=np.uint8)
            return np.flipud(image.reshape(height, width, 3))

    def get_sofa_screen_shot(self):
        """Returns the RGB image array for the current view"""
        _, _, width, height = glGetIntegerv(GL_VIEWPORT)
        height = height // 2
        width = width // 2
        buff = glReadPixels(0, height, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = np.frombuffer(buff, dtype=np.uint8)
        return np.flipud(image.reshape(height, width, 3))

    def save_image(self, filename):
        """
        Save image to file
        :param filename: name of file to save image to. extension determines file type (i.e. "pic.png")
        """
        image = self.get_screen_shot(return_with_alpha=True)
        img = Image.fromarray(image)
        img.save(filename)

    def get_screen_locations(self, points: List[List[float]]):
        """
        :param points: list of 3D world coordinate points
        :return: (x, y, z) positions in the screen coordinates
        """
        points = np.asarray(points)
        screen_positions = np.zeros((len(points), 3))
        for i in range(len(points)):
            screen_positions[i] = gluProject(points[i][0], points[i][1], points[i][2])
        return screen_positions

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        self.key_pressed.emit(a0)
        super(SofaGLViewer, self).keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        self.key_released.emit(a0)
        super(SofaGLViewer, self).keyReleaseEvent(a0)

    def wheelEvent(self, a0: QWheelEvent) -> None:
        self.scroll_event.emit(a0)
        super(SofaGLViewer, self).wheelEvent(a0)

    def draw_spheres(self, positions, radii, colors, clear_existing=True):
        """
        :param clear_existing: whether or not to clear other spheres from the scene
        :param positions: list of x,y,z positions
        :param radii: list of radii for each sphere
        :param colors: list of colors [r, g, b] for each sphere
        """
        if clear_existing:
            self.clear_spheres()
        for i in range(len(positions)):
            new_node = self.visuals_node.addChild("sphere" + str(i))
            self.spheres.append(new_node)
            new_node.addObject(
                "MeshObjLoader",
                name="loader" + str(i),
                filename="mesh/sphere.obj",
                scale=radii[i],
                translation=positions[i],
            )
            new_node.addObject(
                "OglModel", name="i" + str(i), src="@loader" + str(i), color=colors[i]
            )
        Sofa.Simulation.initVisual(self.visuals_node)
        Sofa.Simulation.initTextures(self.visuals_node)

    def clear_spheres(self):
        """
        clear all spheres from scene
        """
        [x.detachFromGraph() for x in self.spheres]

    def get_viewer_size(self):
        self.makeCurrent()
        _, _, width, height = glGetIntegerv(GL_VIEWPORT)
        # width, height = self.width(), self.height()
        return width, height
