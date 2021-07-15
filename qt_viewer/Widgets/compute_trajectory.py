#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 14:50:11 2021

@author: jona
"""
def compute_trajectory(self):
    # if not self.sim_step % 250:
    #     print(self.sofa_sim.root.camera.position.value)
    #     print(self.sofa_sim.root.camera.orientation.value)
        # print(self.viewer.get_intrinsic_parameters())
        # print(self.viewer.get_viewer_size())
        # print(self.sofa_sim.root.camera.lookAt.value)
        # print(self.sofa_sim.root.camera.distance.value)
        # print(self.sofa_sim.root.camera.zNear.value)
        # print(self.sofa_sim.root.camera.zFar.value)
        # print(self.sofa_sim.root.camera.fieldOfView.value)
    if self.sim_step <= 100:
        self.sofa_sim.root.camera.position += [0.01, 0., 0.]
    elif self.sim_step <= 500:
        x_pos = math.cos(2*math.pi*(self.sim_step-100)/400) * math.cos(2*math.pi*(self.sim_step-100)/1600)
        y_pos = math.sin(2*math.pi*(self.sim_step-100)/400) * math.cos(2*math.pi*(self.sim_step-100)/1600)
        self.sofa_sim.root.camera.position.value = [x_pos, y_pos, 5.0]
    elif self.sim_step <= 900:
        y_pos = 5*math.sin(2*math.pi*(self.sim_step-500)/800)
        z_pos = 5*math.cos(2*math.pi*(self.sim_step-500)/800)
        self.sofa_sim.root.camera.position.value = [0.0, y_pos, z_pos]
        q_1 = -1.0 * math.sin(2*math.pi*(self.sim_step-500)/1600)
        q_2 = 0.0
        q_3 = 0.0
        q_4 = 1.0 * math.cos(2*math.pi*(self.sim_step-500)/1600)
        norm_q = q_1**2+q_2**2+q_3**2+q_4**2
        q_1 = q_1/norm_q
        q_2 = q_2/norm_q
        q_3 = q_3/norm_q
        q_4 = q_4/norm_q
        self.sofa_sim.root.camera.orientation.value = [q_1, q_2, q_3, q_4]
    elif self.sim_step <= 1000:
        self.sofa_sim.root.camera.position += [0.01, 0., 0.]
    elif self.sim_step <= 1400:
        x_pos = math.cos(2*math.pi*(self.sim_step-1000)/400) * math.cos(2*math.pi*(self.sim_step-1000)/1600)
        y_pos = math.sin(2*math.pi*(self.sim_step-1000)/400)
        self.sofa_sim.root.camera.position.value = [x_pos, y_pos, -5.0]
        # 0, 0, -5 at the end
    elif self.sim_step <= 1800:
        y_pos = 5*math.sin(2*math.pi*(self.sim_step-1000)/800)
        z_pos = 5*math.cos(2*math.pi*(self.sim_step-1000)/800)
        self.sofa_sim.root.camera.position.value = [0.0, y_pos, z_pos]
        q_1 = -1.0 * math.sin(2*math.pi*(self.sim_step-1000)/1600)
        q_2 = 0.0
        q_3 = 0.0
        q_4 = 1.0 * math.cos(2*math.pi*(self.sim_step-1000)/1600)
        norm_q = q_1**2+q_2**2+q_3**2+q_4**2
        q_1 = q_1/norm_q
        q_2 = q_2/norm_q
        q_3 = q_3/norm_q
        q_4 = q_4/norm_q
        self.sofa_sim.root.camera.orientation.value = [q_1, q_2, q_3, q_4]
        # 0, 0, 5 at the end
    elif self.sim_step <= 2200:
        x_pos = 1.5*math.cos(2*math.pi*(self.sim_step-1800)/400) * math.sin(2*math.pi*(self.sim_step-1800)/1600)
        y_pos = -1.5*math.sin(2*math.pi*(self.sim_step-1800)/400) * math.sin(2*math.pi*(self.sim_step-1800)/1600)
        self.sofa_sim.root.camera.position.value = [x_pos, y_pos, 5.0]
        # 1.5, 0, 5 at the end
    elif self.sim_step <= 2350:
        self.sofa_sim.root.camera.position -= [0.01, 0., 0.]
        # 0, 0, 5 at the end
    elif self.sim_step <= 3100:
        x_pos = 5*math.sin(2*math.pi*(self.sim_step-2350)/1000)
        z_pos = 5*math.cos(2*math.pi*(self.sim_step-2350)/1000)
        self.sofa_sim.root.camera.position.value = [x_pos, 0.0, z_pos]
        q_1 = 0.0
        q_2 = -1.0 * math.sin(2*math.pi*(self.sim_step-2350)/2000)
        q_3 = 0.0
        q_4 = -1.0 * math.cos(2*math.pi*(self.sim_step-2350)/2000)
        norm_q = q_1**2+q_2**2+q_3**2+q_4**2
        q_1 = q_1/norm_q
        q_2 = q_2/norm_q
        q_3 = q_3/norm_q
        q_4 = q_4/norm_q
        self.sofa_sim.root.camera.orientation.value = [q_1, q_2, q_3, q_4]
        # -5, 0, 0 at the end
    elif self.sim_step <= 4100:
        x_pos = -5*math.cos(2*math.pi*(self.sim_step-3100)/1000)
        y_pos = -5*math.sin(2*math.pi*(self.sim_step-3100)/1000)
        self.sofa_sim.root.camera.position.value = [x_pos, y_pos, 0.0]
        q_1 = (1/math.sqrt(2)) * math.sin(2*math.pi*(self.sim_step-3100)/2000)
        q_2 = -(1/math.sqrt(2)) * math.cos(2*math.pi*(self.sim_step-3100)/2000)
        q_3 = (1/math.sqrt(2)) * math.sin(2*math.pi*(self.sim_step-3100)/2000)
        q_4 = (1/math.sqrt(2)) * math.cos(2*math.pi*(self.sim_step-3100)/2000)
        norm_q = q_1**2+q_2**2+q_3**2+q_4**2
        q_1 = q_1/norm_q
        q_2 = q_2/norm_q
        q_3 = q_3/norm_q
        q_4 = q_4/norm_q
        self.sofa_sim.root.camera.orientation.value = [q_1, q_2, q_3, q_4]
        # at 0:      0,         -1/sqrt(2),   0,         1/sqrt(2) 
        # after 250: 0.5,       -0.5,         0.5,       0.5
        # after 500: 1/sqrt(2),  0,           1/sqrt(2), 0 
        # after 750: 0.5,        0.5,         0.5,      -0.5
        # after 1000: 0,         1/sqrt(2),   0,        -1/sqrt(2)
        # -5, 0, 0 at the end
    elif self.sim_step <= 4350:
        x_pos = 5*math.sin(2*math.pi*(self.sim_step-3350)/1000)
        z_pos = 5*math.cos(2*math.pi*(self.sim_step-3350)/1000)
        self.sofa_sim.root.camera.position.value = [x_pos, 0.0, z_pos]
        q_1 = 0.0
        q_2 = 1.0 * math.sin(2*math.pi*(self.sim_step-3350)/2000)
        q_3 = 0.0
        q_4 = 1.0 * math.cos(2*math.pi*(self.sim_step-3350)/2000)
        norm_q = q_1**2+q_2**2+q_3**2+q_4**2
        q_1 = q_1/norm_q
        q_2 = q_2/norm_q
        q_3 = q_3/norm_q
        q_4 = q_4/norm_q
        self.sofa_sim.root.camera.orientation.value = [q_1, q_2, q_3, q_4]
        # 0, 0, 5 at the end