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

# H, _ = cv2.findHomography(pts1, pts2)
# print(H)

# 전체 점 찍기
# countY = 0
# countX = 0
# for y in range(0, 3000):
#     countY += 1
#     if countY is 100:
#         countY = 0
#         for x in range(0, 3000):
#             countX += 1
#             if countX is 100:
#                 if y is not 2999 or x is not 2999:
#                     # print("y:",y,"/ x:",x)
#                     # cv2.circle(img, (x, y), 5, (255, 255, 255), -1) # white
#                     cv2.circle(img, (x, y), 5, (0, 0, 255), -1) # red
#                     countX = 0

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (3000,3000))

print(M[0,0])

#
# cv2.imshow("Draw matches", img_draw_matches)
# cv2.waitKey(0)
#
cv2.imwrite("perspective_before.png", img)
cv2.imwrite("perspective_result.png", dst)