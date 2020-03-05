import os
import cv2
import json
import math
from PIL import Image, ImageFilter
from _collections import OrderedDict
import numpy as np

" ############ 이미지 준비 ################################### "


# input_image_name = '400'= 87
# input_image_name = '29' = 140
# input_image_name = '30' = 155
# input_image_name = '32' = 69
# input_image_name = '33' = 38
# input_image_name = '41' = 64

input_image_name = '41'

# input_image_name = '44' = 33
# input_image_name = '46' = 50
# input_image_name = '47' = 30
# input_image_name = '48' = 106

# input_image_name = '49' = 107
# input_image_name = '50' = 158
# input_image_name = '51' = 180
# input_image_name = '52' = 35
# input_image_name = '105' = 13

# input_image_name = '142' = 87
# input_image_name = '160' = 70
# input_image_name = '161' = 82
# input_image_name = '163' = 41

# input_image_name = ''

# input_image_name = ''
# input_image_name = ''
# input_image_name = ''
# input_image_name = ''
# input_image_name = ''
# input_image_name = ''


# 이미지 경로
image_path = "../images/"

# 원본 이미지
# img_original = cv2.imread(image_path + input_image_name + ".png")

# 픽셀 수 구할 이미지
# count_pixel = Image.open(image_path + input_image_name + '.png')

"############ (끝) 이미지 준비 ###################################"



"############ 이미지 이진화 함수 ###################################"
def remove_background(coords_str, img):
    """
        :param coords_str: 객체의 좌표
        :param img: cv2.imread로 불러온 이미지
        
        :param bright_op: 이진화 하기전에 밝기 옵션.
        :param bright_deg: 옵션 사용법은 아래 참고
        
        (밝기 옵션 bright_op)

            up: 밝기 증가
            down: 밝기 감소

       (밝기 옵션 bright_deg)

            밝기 적용 정도를 0 ~ 100 사이로 조정하기

        :return: 객체의 배경이 제거된 이미지
    """

    # 밝기 조절
    def bright(bright_img, bright_option, bright_degree):
        if bright_option is 'up':
            M = np.ones(bright_img.shape, dtype="uint8") * bright_degree
            result_bright = cv2.add(bright_img, M)

        elif bright_option is 'down':
            M = np.ones(bright_img.shape, dtype="uint8") * bright_degree
            result_bright = cv2.subtract(bright_img, M)

        return result_bright

    # 이진화
    def binary(binary_img, binary_weight):
        # 그레이 스케일 하기
        gray_scale = cv2.cvtColor(binary_img, cv2.COLOR_BGR2GRAY)

        # 이진화 적용
        # ret, result_binary = cv2.threshold(gray_scale, 100, 255, cv2.THRESH_BINARY)

        # 노이즈 제거 + 이진화 적용
        img_blur = cv2.GaussianBlur(gray_scale, (5, 5), 0)
        ret, result_binary = cv2.threshold(img_blur, binary_weight, 255, cv2.THRESH_BINARY)

        return result_binary

    # 배경 제거
    def cut_background(coords, binary_img, origin_img):
        # 이미지의 가로, 세로 픽셀 수 구하기
        # width, height = ref_img.shape
        # = ref_img.shape
        before_perspective_coords = coords.split(",")

        # 객체 영역 구하기
        # 바운딩박스의 중심점 구하기.
        point_x_list = []
        point_y_list = []

        # 객체가 3000 X 3000 범위를 벗어날 경우
        # 0 or 3000 안에 있는것으로 예외처리 해주기
        for i in range(len(before_perspective_coords)):
            if i is 0 or i is 2 or i is 4 or i is 6:
                x = str(before_perspective_coords[i]).split(".")

                if 3000 < int(x[0]):
                    point_x_list.append(int(3000))
                elif 0 > int(x[0]):
                    point_x_list.append(int(0))
                else:
                    point_x_list.append(int(x[0]))
            else:
                y = str(before_perspective_coords[i]).split(".")
                if 3000 < int(y[0]):
                    point_x_list.append(int(3000))
                elif 0 > int(y[0]):
                    point_y_list.append(int(0))
                else:
                    point_y_list.append(int(y[0]))

        point_x_list.sort()
        point_y_list.sort()

        # 바운딩 박스 안의 배경만 제거하기
        for y in range(point_y_list[0], point_y_list[3]):
            for x in range(point_x_list[0], point_x_list[3]):
                if binary_img[y][x] == 0:
                    origin_img[y, x] = [0, 0, 0]  # black

        return origin_img

    # 객체와 객체 주변의 픽셀 평균 밝기 구하기
    def getImageBrightAverage(coords, img):
        """
        :param img: 밝기 평균을 구할 이미지
        :param range_start: 밝기 평균을 구할 영역 시작점
        :param range_end: 밝기를 평균을 구할 영역 끝점
        :return: 밝기 증,감 여부 ('up' or 'down'), 밝기 조절 정도 (0 ~ 100)
        """
        before_perspective_coords = coords.split(",")
        point_x_list = []
        point_y_list = []

        # 모든 픽셀의 평균 밝기를 저장하는 리스트
        pixel_average = []

        # 최종 밝기를 구한 후 밝기를 up or down 할지 여부
        bright_op = str

        # 밝기 조절 (0~100)
        bright_degree = int
        # down일 경우 숫자가 높을 수록 어두워짐
        # up일 경우 숫자가 높을 수록 밝아짐

        #  객체의 범위가 3000 or 0을 벗어나지 않게 예외처리
        for i in range(len(before_perspective_coords)):
            if i is 0 or i is 2 or i is 4 or i is 6:
                x = str(before_perspective_coords[i]).split(".")
                if 3000 < int(x[0]):
                    point_x_list.append(int(3000))
                elif 0 > int(x[0]):
                    point_x_list.append(int(0))
                else:
                    point_x_list.append(int(x[0]))
            else:
                y = str(before_perspective_coords[i]).split(".")
                if 3000 < int(y[0]):
                    point_x_list.append(int(3000))
                elif 0 > int(y[0]):
                    point_y_list.append(int(0))
                else:
                    point_y_list.append(int(y[0]))

        point_x_list.sort()
        point_y_list.sort()

        # 모든 픽셀의 평균 값을 구해서 리스트에 담기 (평균 값은 0 ~ 255 사이 값이 되어야 함)
        for y in range(point_y_list[0], point_y_list[3]):
            for x in range(point_x_list[0], point_x_list[3]):
                b, g, r = img[y][x]
                average = (int(b) + int(g) + int(r)) / 3
                pixel_average.append(average)

        # 리스트에 담긴 모든 픽셀을 더해서 최종 평균 값 구하기
        size_pixel_average = len(pixel_average)
        total_average = sum(pixel_average) / size_pixel_average
        total_average = int(total_average)

        print("평균 밝기 값:",total_average)

        # 최종 평균값을 참고해서 밝기 조절 여부를 정하기
        if 130 <= total_average:
            bright_op = 'down'
            bright_degree = int(40)
            print("매우 밝음. 밝기 감소",bright_degree)

        elif 100 <= total_average and 129 >= total_average:

            bright_op = 'down'
            bright_degree = int(9)
            print("밝음. 밝기 감소",bright_degree)

        elif 70 <= total_average and 99 >= total_average:

            # 밝기 조정이 필요 없을 경우
            bright_op = 'up'
            bright_degree = int(60)
            print("약간 어두움. 밝기 증가",bright_degree)

        elif 40 <= total_average and 69 >= total_average:

            bright_op = 'up'
            bright_degree = int(60)
            print("어두움. 밝기 증가",bright_degree)

        elif 39 >= total_average:

            bright_op = 'up'
            bright_degree = int(70)
            print("매우 어두움. 밝기 증가",bright_degree)

        # print("bright_op:",bright_op,"/ bright_degree:",bright_degree)
        return bright_op, bright_degree

    """ (선택) 1. 히스토그램 평활화 """
    # img_processing1 = equalize_image(img)
    # cv2.imwrite("result/" + str(i) + ". 2. result_equalize.png", img_processing1)

    get_bright_op, get_bright_degree = getImageBrightAverage(coords=coords_str, img=img)

    """ (선택) 1. 밝기 조절 bright_option='up' or 'down' """
    img_processing1 = bright(bright_img=img, bright_option=get_bright_op, bright_degree=get_bright_degree)
    # cv2.imwrite("result/" + str(i) + ". 2. result_bright.png", img_processing1)

    """ 2. 이진화 """
    img_processing2 = binary(binary_img=img_processing1, binary_weight=100)
    cv2.imwrite("400_binary.png", img_processing2)
    # cv2.imwrite("result/" + str(i) + ". 3. result_binary.png", img_processing2)

    """ 3. 배경 제거 """
    img_processing3 = cut_background(coords=coords_str, binary_img=img_processing2, origin_img=img)
    # cv2.imwrite("result/" + str(i) + ". 4. cut_result.png", img_processing3)
    # cv2.imwrite("result/" + str(i) + ". 5. edge_enhance_image.png", edge_enhance_image(img_processing3))
    # cv2.imwrite("result/" + str(i) + ". 6. equalize_image.png", equalize_image(img_processing3))

    result_remove_background = img_processing3

    return result_remove_background

def edge_enhance_image(input_image):
    """ cv 이미지를 받아서 PIL.EDGE_ENHANCE 적용 후 다시 cv 이미지 반환
    :param input_image: input cv image
    :return: edge enhanced cv image
    """
    cv_img = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
    PIL_EE_img = Image.fromarray(cv_img).filter(ImageFilter.EDGE_ENHANCE)
    cv_EE_img = cv2.cvtColor(np.array(PIL_EE_img), cv2.COLOR_RGB2BGR)

    return cv_EE_img

def equalize_image(input_image):
    """ image equalizing
    :param input_image: input cv image
    :return: equalized image
    """
    # hsv 컬러 형태로 변형
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    # h, s, v로 컬러 영상을 분리
    h, s, v = cv2.split(hsv)
    # v값으로 히스토그램 평활화
    equalizedV = cv2.equalizeHist(v)
    # h,s,equalizedV를 합쳐서 새로운 hsv 이미지 생성
    hsv2 = cv2.merge([h, s, equalizedV])
    # hsv2를 다시 BGR 형태로 변경
    hsvDst_img = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)

    return hsvDst_img

"############ (끝) 이미지 이진화 함수 ###################################"

"############ 이미지 필터 적용, 저장하기 ###################################"
# image_root_path = "../images/"
# image_file_list = os.listdir(image_root_path)
# image_file_list.sort()

with open('labels.json') as json_file:
    json_data = json.load(json_file)
    features = json_data["features"]

img = None
for i in range(len(features)):
    if features[int(i)]['properties']['image_id'] == input_image_name + '.png':

        # maritime 을 제외한 객체만 배경 제거
        if features[int(i)]['properties']['type_id'] is not 4:

            # 모든 객체의 배경 제거가 끝나면 다음 이미지 배경 제거 처리로 넘어가기
            if img is None:
                img = cv2.imread(image_path + input_image_name + '.png')

            elif img is not img:
                img = cv2.imread(image_path + input_image_name + '.png')

            # 민간 선박을 제외한 선박들만 배경 제거하기
            # if features[int(i)]['properties']['type_id'] is not 4:
            print(i, features[int(i)]['properties']['type_id'], features[int(i)]['properties']['type_name'])
            
            """객체의 배경 제거하기"""
            # result_remove_back = remove_background(coords_str=features[int(i)]['properties']['bounds_imcoords'], img=img, bright_op='down', bright_deg=30)
            # remove_background(coords_str=features[int(i)]['properties']['bounds_imcoords'], img=img)
            result_remove_back = remove_background(coords_str=features[int(i)]['properties']['bounds_imcoords'], img=img)
            cv2.imwrite(features[int(i)]['properties']['image_id'], result_remove_back)

            print("save done:",features[int(i)]['properties']['image_id'])

"############ (끝) 이미지 필터 적용, 저장하기 ###################################"
