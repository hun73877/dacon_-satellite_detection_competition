import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../images/0.png')

"""
원근감 옵션
0: 상
1: 하
2: 좌
3: 우
"""
option_perspective = 1

# 좌표점은 좌상->좌하->우상->우하
# default: [200,200],[200,2800],[2800,200],[2800,2800]
perspective_direction_list = [
    [[225,200],[175,2800],[2775,200],[2825,2800]],
    [[175,200],[225,2800],[2825,200],[2785,2800]],
    [[200,225],[200,2775],[2800,175],[2800,2825]],
    [[200,175],[200,2825],[2800,225],[2800,2775]]
]

pts1 = np.float32([[200,200],[200,2800],
                   [2800,200],[2800,2800]])

# 원근감 적용하기
pts2 = np.float32(perspective_direction_list[option_perspective])

# 중앙 점찍기
cv2.circle(img, (1500,1500), 10, (0,0,255),-1)

# 전체 점 찍기
countY = 0
countX = 0
for y in range(0, 3000):
    countY += 1
    if countY is 100:
        countY = 0
        for x in range(0, 3000):
            countX += 1
            if countX is 100:
                if y is not 2999 or x is not 2999:
                    print("y:",y,"/ x:",x)
                    cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
                    countX = 0

# cv2.circle(img, (200,400), 10, (0,0,255),-1)
# cv2.circle(img, (200,600), 10, (0,0,255),-1)
# cv2.circle(img, (200,800), 10, (0,0,255),-1)
# cv2.circle(img, (200,1000), 10, (0,0,255),-1)
#
# cv2.circle(img, (200,1200), 10, (0,0,255),-1)
# cv2.circle(img, (200,1400), 10, (0,0,255),-1)
# cv2.circle(img, (200,1600), 10, (0,0,255),-1)
# cv2.circle(img, (200,1800), 10, (0,0,255),-1)
# cv2.circle(img, (200,2000), 10, (0,0,255),-1)
#
# cv2.circle(img, (200,2200), 10, (0,0,255),-1)
# cv2.circle(img, (200,2400), 10, (0,0,255),-1)
# cv2.circle(img, (200,2600), 10, (0,0,255),-1)
# cv2.circle(img, (200,2800), 10, (0,0,255),-1)
# cv2.circle(img, (200,3000), 10, (0,0,255),-1)
#
# # 좌측 2열
# cv2.circle(img, (200,200), 10, (0,0,255),-1)
# cv2.circle(img, (200,2800), 10, (0,0,255),-1)
#
#
# cv2.circle(img, (400,400), 10, (0,0,255),-1)
# cv2.circle(img, (400,2600), 10, (0,0,255),-1)
#
# # 우측 상
# cv2.circle(img, (2800,200), 10, (0,0,255),-1)
# cv2.circle(img, (2800,2800), 10, (0,0,255),-1)
#
# # 우측 중
#
# # 우측 하
# cv2.circle(img, (2600,400), 10, (0,0,255),-1)
# cv2.circle(img, (2600,2600), 10, (0,0,255),-1)




M = cv2.getPerspectiveTransform(pts1, pts2)


dst = cv2.warpPerspective(img, M, (3000,3000))

cv2.imwrite("perspective_before.png", img)
cv2.imwrite("perspective_result.png", dst)

# plt.subplot(121),plt.imshow(img),plt.title('image')
# plt.subplot(122),plt.imshow(dst),plt.title('Perspective')
# plt.show()