# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 23:03:31 2021

@author: yun_z
"""

import cv2
import imutils
import non_max_suppression as NMS
import numpy as np

# Window name in which image is displayed
window_name = 'Image'
  
# text
text = 'GeeksforGeeks'
  
# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# fontScale
fontScale = 0.8
   
# Red color in BGR
color = (0, 0, 255)
  
# Line thickness of 2 px
thickness = 1
   


# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture('people.mp4')


while cap.isOpened():
	# Reading the video stream
	ret, image = cap.read()
	if ret:
		image = imutils.resize(image,width=min(600, image.shape[1]))

		# Detecting all the regions
		# in the Image that has a
		# pedestrians inside it
		(regions, _) = hog.detectMultiScale(image,
											winStride=(4, 4),
											padding=(8, 8),
											scale=1.05)

		# Drawing the regions in the
		# Image
		person = 1
			
		for x,y,w,h in regions:
			cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
			cv2.circle(image,(x+round(w/2),y+round(h/2)), 2, (0,0,255), 2)
			cv2.putText(image, f'person {person}', (x+10,y+20), font, 0.5, (0,0,255), 1)
			person += 1

		# apply non-maxima suppression to the bounding boxes using a
		# fairly large overlap threshold to try to maintain overlapping
		# boxes that are still people
		regions = np.array([[x, y, x + w, y + h] for (x, y, w, h) in regions])
		pick = NMS.non_max_suppression(regions, overlapThresh=0.65)
		
		# draw the final bounding boxes
		#for (xA, yA, xB, yB) in pick:
		#cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 255), 2)
	    	
		cv2.putText(image, 'Status : Detecting ', (20,40), font , 0.6, (255,255,255), 2)
		cv2.putText(image, f'Total Persons : {person-1}', (20,70), font , 0.6 , (255,255,255), 2)
		
		# Showing the output Image
		cv2.imshow("Image", image)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break
	else:
		break

cap.release()
cv2.destroyAllWindows()
