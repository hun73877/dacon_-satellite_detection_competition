import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../images/0.png')
rows, cols, ch = img.shape



"""
1. (pts1 변수) 원본 이미지에 세 개의 좌표 포인트 찍기 [x, y]
2. (1)좌 (2)우 (3)하 순서로 좌표가 찍힘
"""
pts1 = np.float32([[200,200],[2800,200],[200,2800]])

"""
1. pts1에서 이동할 좌표
"""
pts2 = np.float32([[200,250],[2800,200],[200,2800]])

# pts1 = np.float32([[100,100],[2900,2900],[100,2900]])
# pts2 = np.float32([[20,20],[2980,2980],[20,2980]])

# pts1의 좌표에 표시. Affine 변환 후 이동 점 확인 (x, y) (b,g,r)
cv2.circle(img, (200,200), 10, (255,0,0),-1) # 블루_좌
cv2.circle(img, (2800,200), 10, (0,255,0),-1) # 그린_우
cv2.circle(img, (200,2800), 10, (0,0,255),-1) # 레드_하



M = cv2.getAffineTransform(pts1, pts2)

dst = cv2.warpAffine(img, M, (cols,rows))

cv2.imwrite("affine_before.png", img)
cv2.imwrite("affine_result.png", dst)

# plt.subplot(121),plt.imshow(img),plt.title('image')
# plt.subplot(122),plt.imshow(dst),plt.title('Affine')
# plt.show()

