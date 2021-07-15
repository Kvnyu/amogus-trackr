# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 19:56:03 2021

@author: yun_z
"""
import numpy as np
import cv2

# defined exits/entraces (x0,y0) and type
# boundary = np.array([[30,20],[30,320],[70,300],[70,60]])
boundary = np.array([[100,0],[100,350],[170,300],[170,40]])
boundary_direction = 0

def draw_boundaries(image):
    height = image.shape[0]
    boundary[1][1] = height
    boundary[2][1] = height - 50
    overlay = image.copy()
    cv2.fillPoly(overlay, [boundary], (0,0,255,0.4))
    cv2.addWeighted(overlay,0.5,image,0.5,0,image)
    return image

def detect_crossing(positions, vectors):
    min_x = boundary[0][0]
    max_x = boundary[3][0]
    crossings = 0
    counter = 0
    max_angle = boundary_direction + 90
    min_angle = boundary_direction - 90
    for (x,y) in positions:
        if ( max_x > x > min_x):
            vector = vectors[counter]
            angle = np.rad2deg(np.arctan2(vector[1],vector[0]));
            # print(angle)
            if (max_angle > angle > min_angle):
                # print("exit")
                crossings -= 1
            else:
                # print("entry")
                crossings += 1
            
        counter += 1
    return crossings