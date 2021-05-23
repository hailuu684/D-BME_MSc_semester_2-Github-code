import numpy as np
import cv2
import math
from scipy import ndimage

def distanceTo(x1,x2,y1,y2):
    distance = np.sqrt((x2-x1)**2+(y2-y1)**2)
    return distance

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

filepath = 'D:/BME_MSc_semester_2/rqim-luuhaitung-master/images/188729603_267553585152759_1752710080305516995_n.jpg'
image = cv2.imread(filepath)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow('hello',image)
edges = cv2.Canny(gray,50,50,L2gradient=True)
lines = cv2.HoughLinesP(edges,rho = 1,theta = np.pi/180,threshold = 50,minLineLength = 45,maxLineGap = 4.8)
circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,10,param1=5,param2=10,minRadius=20,maxRadius=100)
line1 = []
line2 = []
for i in range(len(lines)-1):
    x1_i, y1_i, x2_i, y2_i = lines[i][0]
    x1_j, y1_j, x2_j, y2_j = lines[i+1][0]
    distance = distanceTo(x1_i,x1_j,y1_i,y1_j)
    # print(distance)
    if distance<40:
        cv2.line(image, (x1_i, y1_i), (x2_i, y2_i), (255, 0, 0), 3)
        cv2.line(image, (x1_j, y1_j), (x2_j, y2_j), (255, 0, 0), 3)
        line1.append([x1_i, y1_i, x2_i, y2_i])
        line2.append([x1_j, y1_j, x2_j, y2_j])
        angle = math.atan(y2_i-y1_i/x2_i-x1_i)

        # print('angle = ',angle*180/np.pi)

center = None
if circles is not None:
    x, y, radius = circles[0][0]
    center = (x, y)
    cv2.circle(image, center, int(radius), (0, 255, 0), 2)
    # cv2.circle(frame, center, 2, (0, 255, 0), -1, 8, 0);
    print('center = ：{}, {}'.format(x, y))
center_blank = (int((x1_i+x1_j)/2),int((y1_i+y1_j)/2))
cv2.line(image,center,center_blank,(255,255,0),2)
angle_middle = math.atan2(center[0]-center_blank[0],center[1]-center_blank[1])
rotate_image = ndimage.rotate(image,-angle_middle*180/np.pi-90)
cv2.imshow('rotated',rotate_image)
cv2.imshow('lines detected',image)


cv2.waitKey(0)
cv2.destroyAllWindows()



