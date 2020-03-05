import cv2
import numpy as np

img= cv2.imread('_1210.png')
# cv2.imshow('Original',img)

kernel_sharpen_1 = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]) #정규화를 하지 않은 이유는 모든 값을 다 더하면 1이되기때문에 1로 나눈것과 같은 효과
kernel_sharpen_2 = np.array([[1,1,1],[1,-7,1],[1,1,1]]) #이것도 마찬가지
kernel_sharpen_3 = np.array([[-1,-1,-1,-1,-1],[-1,2,2,2,-1],[-1,2,8,2,-1],[-1,2,2,2,-1],[-1,-1,-1,-1,-1]])/8.0 #정규화위해 8로나눔

#applying different kernels to the input image
output_1 = cv2.filter2D(img,-1,kernel_sharpen_1)
output_2 = cv2.filter2D(img,-1,kernel_sharpen_2)
output_3 = cv2.filter2D(img,-1,kernel_sharpen_3)

cv2.imwrite("a. Sharpening.png", output_1)
cv2.imwrite("b. Excessive_Sharpening.png", output_2)
cv2.imwrite("c. Edge_Enhancement.png", output_3)


# cv2.imshow('Sharpening',output_1)
# cv2.imshow('Excessive_Sharpening',output_2)
# cv2.imshow('Edge_Enhancement',output_3)
# cv2.waitKey()