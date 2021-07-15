# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 23:03:31 2021

@author: yun_z
"""

import cv2
import imutils
import boundary_detection as BD

# Window name in which image is displayed
window_name = 'Image'

# font
font = cv2.FONT_HERSHEY_SIMPLEX

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# threshold for radius search
threshold = 30
lockout_counter = 0

cap = cv2.VideoCapture('walking_lowres.mp4')
count = 0
notFirst = False
previous = None
while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()
    if ret:
        image = imutils.resize(image, width=min(600, image.shape[1]))

        image = BD.draw_boundaries(image)
        # Detecting all the regions
        # in the Image that has a
        # pedestrians inside it
        (regions, _) = hog.detectMultiScale(image,
                                            winStride=(4, 4),
                                            padding=(8, 8),
                                            scale=1.05)

        # print(regions)

        # Drawing the regions in the
        # Image

        # regions = np.array([[x, y, x + w, y + h] for (x, y, w, h) in regions])
        # filtered_regions = NMS.non_max_suppression(regions, overlapThresh=0.65)
        i = 0
        person = 0
        vectors = []
        centers = []
        for x, y, w, h in regions:
            center = (x + round(w / 2), y + round(h / 2))
            if notFirst:
                for a, b, c, d in previous:
                    oldcenter = (a + round(c / 2), b + round(d / 2))
                    vector = (center[0] - oldcenter[0], center[1] - oldcenter[1])
                    mag = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
                    if mag <= threshold:
                        # we found a point to associate!!
                        cv2.arrowedLine(image, oldcenter, (center[0] + 3 * vector[0], center[1] + 3 * vector[1]),
                                        (255, 0, 255), 1)
                        vectors.append(vector)
                        centers.append(center)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(image, center, 2, (0, 0, 255), 2)
            cv2.putText(image, 'person', (x + 10, y + 20), font, 0.5, (0, 0, 255), 1)
            person += 1
        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people

        # draw the final bounding boxes
        # for (xA, yA, xB, yB) in pick:
        # cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 255), 2)

        cv2.putText(image, 'Current Count: ' + str(count), (20, 40), font, 0.6, (255, 255, 255), 2)
        # cv2.putText(image, f'Total Persons : {person - 1}', (20, 70), font, 0.6, (255, 255, 255), 2)
        previous = regions
        notFirst = True

        if lockout_counter <= 0:
            crossing = BD.detect_crossing(centers, vectors)
            if (crossing):
                count += crossing
                lockout_counter = 30
        lockout_counter -= 1

        # Showing the output Image
        cv2.imshow("Image", image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
