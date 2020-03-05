import cv2

img = cv2.imread('../images/0.png')
height = img.shape[0]
width = img.shape[1]

remove_range = 500

for y in range(0,remove_range):
    for x in range(0,remove_range):
        print(img[y,x])

        # print("y:",y,"x:",x)
        # 검은 색으로 세팅
        # img.itemset(y, x, 0, 0)
        # img.itemset(y, x, 1, 0)
        # img.itemset(y, x, 2, 0)
        
        # 흰 색으로 세팅
        # img.itemset(y, x, 0, 255)
        # img.itemset(y, x, 1, 255)
        # img.itemset(y, x, 2, 255)


# for x in range(0,width):
    # img.itemset(50, x, 0, 255)
    # img.itemset(50, x, 1, 255)
    # img.itemset(50, x, 2, 255)

cv2.imshow('win', img)
cv2.waitKey(0)

# print(img[y,x])
# print(x)

# 픽셀값은 [blue, green, red] 값으로 구성되어 있는데 blue가 가장 크기 때문에 이미지에서 파란색으로 보입니다.
# print(img[50,50])

# for y in range(len(y)):
    # print(str(img[x, y]))

# 흰색으로 변경하면 아래 결과 영상처럼 파란색 사각형의 왼쪽 아래에 흰점이 출력됩니다.
# img[50,50] = [255,255,255]
# print(img[50,50])

# cv.imshow('win', img)

# cv.waitKey(0)