import numpy as np
import cv2

# 원본 이미지 불러오기
img_source = cv2.imread('../images/0.png')

"""
x축 이동 방향: 음수: 좌 / 양수: 우
y축 이동 방향: 음수: 상 / 양수: 하
np.float32([[1, 0, '이동할 x축 입력'], [0, 1, '이동할 y축 입력']])
"""
height, width = img_source.shape[:2]
M = np.float32([[1, 0, -700], [0, 1, 1500]])
img_translation = cv2.warpAffine(img_source, M, (width,height))

# 이미지 저장하기
# cv2.imwrite("저장할 경로/파일명", "편집된 이미지")
cv2.imwrite("2769.png", img_translation)

# cv2.imshow("translation", img_translation)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




