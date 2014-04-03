import cv2
import numpy as np
from matplotlib import pyplot as plt
#################### AUTO CAR ####################


#################### FIRST TEST ####################
#edges = cv2.Canny(img,100,200)
#
# surf = cv2.SURF(400,1,1,True,0)
# kp, des = surf.detectAndCompute(img,None)
# len(kp)
#surf.hessianThreshold = 50000
#kp, des = surf.detectAndCompute(img,None)
# img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)

# #
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# #
# plt.imshow(img2),plt.show()
# #
# plt.show()

#################### SECOND TEST ####################

#surf_params = {"_hessianThreshold":500,"_nOctaves":1, "_nOctaveLayers":1, "_extended":1, "_upright":0}

surf = cv2.SURF(10000,1,1,0,0)
image = cv2.imread('uparrow.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
keypoints = surf.detect(image)

for keypoint in keypoints:
    #x,y = keypoint.pt
    #size = keypoint.size 
    orientation = keypoint.angle
    #response = keypoint.response 
    #octave = keypoint.octave
    #class_id = keypoint.class_id
    print orientation
    #print (x,y), size, orientation

image2 = cv2.drawKeypoints(image,keypoints,None,(255,0,0),4)
edges = cv2.Canny(image,200,400)
plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Orientation'), plt.xticks([]), plt.yticks([])
#
plt.imshow(image2),plt.show()
#
plt.show()

