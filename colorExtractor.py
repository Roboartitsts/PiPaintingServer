'''
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
'''

#import cv2
import numpy as np
from math import hypot
import pygame
import pygame.camera

pygame.init()
pygame.camera.init()

#screen = pygame.display.set_mode((640,480),0)

cam_list = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(cam_list[0], (640, 480))
webcam.start()

def show_webcam(mirror=False):
	#cam = cv2.VideoCapture(0)
        
	prevColor = np.array([0,0,0])
	while True:
                camimg = webcam.get_image()
                
                imgdisp = camimg.get_buffer()
                imgtemp = pygame.surfarray.array3d(camimg)
                img = np.array(imgtemp)
                del imgtemp
		#ret_val, img = cam.read()
		#if mirror: 
		#	img = cv2.flip(img, 1)

		# print img.shape
		rows, cols, colors = img.shape
                print rows, cols, colors
		cx = cols // 2
		cy = rows // 2
		r = 200
		# circlemask = np.zeros(rows,cols)
		x,y = np.ogrid[:rows,:cols]
		r2 = (x-cy)**2 + (y-cx)**2
		circlemask = r2 <= r**2
		circlemask[circlemask > 0] = 1
		circlemaskfinal = np.dstack([circlemask,circlemask,circlemask])
		img = np.multiply(circlemaskfinal, img)
		avgColor = getMeanColor(img)
		img[~circlemask] = avgColor


                imgdisp.write(img.tostring(),0)
                del img
                del imgdisp
                screen.blit(camimg,(0,0))
                pygame.display.update()
                
		# circlemask()
		# numpixels = 0
		# avgColor = np.array([0,0,0])
		# for i in range(cols):
		# 	for j in range(rows):
		# 		if hypot(i-cx, j-cy) > r:
		# 			numpixels += 1
		# 			avgColor[0] += img[j,i,0]
		# 			avgColor[1] += img[j,i,1]
		# 			avgColor[2] += img[j,i,2]
		# 			# img[j,i] = img[j,i]*0.3
		# 			img[j,i] = prevColor

		# avgColor = avgColor/numpixels
		# prevColor = avgColor
		# print(avgColor)

		


                
		#cv2.imshow('my webcam', img)
		#if cv2.waitKey(1) == 27: 
	#		break  # esc to quit
	#cv2.destroyAllWindows()
def captureImg():
        camimg = webcam.get_image()
                
        imgdisp = camimg.get_buffer()
        imgtemp = pygame.surfarray.array3d(camimg)
        img = np.array(imgtemp)
#        del imgtemp
#        del imgdisp
        return img


def getMeanColor(img):
        
	rows, cols, colors = img.shape
	cx = cols // 2
	cy = rows // 2
	r = 200

	x,y = np.ogrid[:rows,:cols]
	r2 = (x-cy)**2 + (y-cx)**2
	circlemask = r2 <= r**2
	circlemask[circlemask > 0] = 1

	count = np.sum(circlemask>0)
	colors = np.sum(img, axis=1)
	colors = np.sum(colors, axis=0) / count
	colors2 = colors
	temp = colors[0]
	temp2 = colors[2]
	#colors[0] = temp2
	#colors[2] = temp
	print np.sum(circlemask)
	print 'imgsum',	colors

	numpixels = 0
	avgColor = np.array([0,0,0])
        
	
	# for i in range(cols):
	# 	for j in range(rows):
	# 		if hypot(i-x, j-y) > r:
	# 			numpixels += 1
	# 			avgColor[0] += img[j,i,0]
	# 			avgColor[1] += img[j,i,1]
	# 			avgColor[2] += img[j,i,2]
	# 			# img[j,i] = img[j,i]*0.3

	# avgColor = avgColor/numpixels
	return colors

def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()
