import numpy as np
from PIL import Image

import matplotlib.pyplot as plt

# gray_img = Image.open('data_images_train_2/images/0.png').convert("LA")#밝기와 알파값을 이용해서 Grayscale로 변환
# gray_img.show()#grayscale로 변환된 흑백 이미지를 출력
gray_img = Image.open('../images/0.png')
row = gray_img.size[0] # 이미지의 가로 픽셀 수 출력
col = gray_img.size[1] # 세로 픽셀 수 출력
thr_img = Image.new("1", (row, col))#새 이진 이미지를 생성.
for x in range(1 , row):
    for y in range(1, col):
        # if gray_img.getpixel((x,y))[0] > 128:#RGB 전부 같음 따라서 R값만 임계값과 비교
        if gray_img.getpixel((x, y))[0] > 85:  # RGB 전부 같음 따라서 R값만 임계값과 비교
            print("x:",x,"/y:", y)
            thr_img.putpixel((x,y),1)
        else:
            thr_img.putpixel((x,y),0)
thr_img.show()#이진화 이미지 출력

# y = gray_img.histogram()
# y = y[0:256]
# x = np.arange(len(y))
# plt.title("original hist")
# plt.bar(x, y)
# plt.show()

# y = thr_img.histogram()
# y = y[0:2]
# x = np.arange(len(y))
# plt.title("binary hist")
# plt.bar(x, y)
# plt.show()