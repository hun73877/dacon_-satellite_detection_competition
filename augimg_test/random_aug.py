""" Random Augmentation
임의의 각도, 비율, 필터가 사용되며 이미지 증강
"""
import os
import cv2
import math
import json
import random
import argparse
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageFilter
from _collections import OrderedDict


def rotate_image_with_box(img_path, box_coord, ang, ratio, input_image=None):
    """ 이미지 및 박스 회전
    :param img_path: 이미지 경로(경로로 부터 읽어올 경우)
    :param box_coord: 박스 좌표(문자열)
    :param ang: 회전시킬 각도
    :param ratio: output 이미지의 원본대비 비율(이미지가 잘리지 않도록 하기 위해)
    :param input_image: cv 이미지(직접 input을 넣어줄 경우)
    :return: 회전된 이미지, 박스좌표 문자열
    """

    # 경로로 부터 이미지를 읽어온다
    img = cv2.imread(img_path)
    # input 이미지가 있다면 input 이미지를 읽어온다
    if input_image is not None:
        img = input_image

    # input 이미지의 가로, 세로 길이
    height, width = img.shape[:2]

    # 좌표(문자열)을 변수에 나눠서 입력한다
    coord = box_coord.split(",")
    p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(coord[0]), float(coord[1]), float(coord[2]), \
                                             float(coord[3]), float(coord[4]), float(coord[5]), \
                                             float(coord[6]), float(coord[7])

    # 각도 변환
    angle = 180 / ang
    degree = math.pi / angle

    # 이미지 중심의 좌표
    img_yc = height / 2
    img_xc = width / 2

    # 좌표를 이미지 중심으로 변환한다(회전은 이미지 중심을 원점으로 하므로), 이때 비율을 곱하여 준다
    new_coord = [(p1x - img_xc) * ratio, (img_yc - p1y) * ratio, (p2x - img_xc) * ratio, (img_yc - p2y) * ratio,
                 (p3x - img_xc) * ratio, (img_yc - p3y) * ratio, (p4x - img_xc) * ratio, (img_yc - p4y) * ratio]

    # 변환된 좌표를 회전시킨다
    r_p1x = new_coord[0] * math.cos(degree) - new_coord[1] * math.sin(degree)
    r_p1y = new_coord[0] * math.sin(degree) + new_coord[1] * math.cos(degree)
    r_p2x = new_coord[2] * math.cos(degree) - new_coord[3] * math.sin(degree)
    r_p2y = new_coord[2] * math.sin(degree) + new_coord[3] * math.cos(degree)
    r_p3x = new_coord[4] * math.cos(degree) - new_coord[5] * math.sin(degree)
    r_p3y = new_coord[4] * math.sin(degree) + new_coord[5] * math.cos(degree)
    r_p4x = new_coord[6] * math.cos(degree) - new_coord[7] * math.sin(degree)
    r_p4y = new_coord[6] * math.sin(degree) + new_coord[7] * math.cos(degree)

    # 원본의 원점기준으로 변환
    rr_p1x = r_p1x + img_xc
    rr_p1y = img_yc - r_p1y
    rr_p2x = r_p2x + img_xc
    rr_p2y = img_yc - r_p2y
    rr_p3x = r_p3x + img_xc
    rr_p3y = img_yc - r_p3y
    rr_p4x = r_p4x + img_xc
    rr_p4y = img_yc - r_p4y

    # 이미지 회전
    rotate_m = cv2.getRotationMatrix2D(center=(img_xc, img_yc), angle=ang, scale=ratio)
    r_img = cv2.warpAffine(src=img, M=rotate_m, dsize=(width, height), borderMode=cv2.BORDER_CONSTANT)

    # cv2.line(r_img, (int(rr_p1x), int(rr_p1y)), (int(rr_p2x), int(rr_p2y)), (255, 255, 0), 6)
    # cv2.line(r_img, (int(rr_p2x), int(rr_p2y)), (int(rr_p3x), int(rr_p3y)), (255, 255, 0), 6)
    # cv2.line(r_img, (int(rr_p3x), int(rr_p3y)), (int(rr_p4x), int(rr_p4y)), (255, 255, 0), 6)
    # cv2.line(r_img, (int(rr_p4x), int(rr_p4y)), (int(rr_p1x), int(rr_p1y)), (255, 255, 0), 6)

    # cv2_img = cv2.cvtColor(r_img, cv2.COLOR_RGB2BGR)
    # p_en_img = Image.fromarray(cv2_img).filter(ImageFilter.EDGE_ENHANCE)
    # cv_en_img = cv2.cvtColor(np.array(p_en_img), cv2.COLOR_RGB2BGR)
    # cv2.imwrite("test.png", r_img)

    # 좌표 문자열로 복원
    rotation_box_coord = str(rr_p1x) + "," + str(rr_p1y) + "," + \
                         str(rr_p2x) + "," + str(rr_p2y) + "," + \
                         str(rr_p3x) + "," + str(rr_p3y) + "," + \
                         str(rr_p4x) + "," + str(rr_p4y)
    # print(rotation_box_coord)

    return r_img, rotation_box_coord


def rotate_box_3000x3000(object_image, box_coord, ang, ratio):
    """ 박스만 회전용  3000x3000이미지 기준
    :param object_image: 객체가 포함된 이미지
    :param box_coord: 박스좌표(문자열)
    :param ang: 회전시킬 각도
    :param ratio: 적용할 비율(0~1)
    :return: 회전된 좌표
    """

    # input 이미지의 가로, 세로 길이
    height, width = object_image.shape[0:2]

    # 좌표(문자열)을 변수에 나눠서 입력한다
    coord = box_coord.split(",")
    p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(coord[0]), float(coord[1]), float(coord[2]), \
                                             float(coord[3]), float(coord[4]), float(coord[5]), \
                                             float(coord[6]), float(coord[7])

    # 각도 변환
    angle = 180 / ang
    degree = math.pi / angle

    # 이미지 중심의 좌표
    img_yc = height / 2
    img_xc = width / 2

    # 좌표를 이미지 중심으로 변환한다(회전은 이미지 중심을 원점으로 하므로), 이때 비율을 곱하여 준다
    new_coord = [(p1x - img_xc) * ratio, (img_yc - p1y) * ratio, (p2x - img_xc) * ratio, (img_yc - p2y) * ratio,
                 (p3x - img_xc) * ratio, (img_yc - p3y) * ratio, (p4x - img_xc) * ratio, (img_yc - p4y) * ratio]

    # 변환된 좌표를 회전시킨다
    r_p1x = new_coord[0] * math.cos(degree) - new_coord[1] * math.sin(degree)
    r_p1y = new_coord[0] * math.sin(degree) + new_coord[1] * math.cos(degree)
    r_p2x = new_coord[2] * math.cos(degree) - new_coord[3] * math.sin(degree)
    r_p2y = new_coord[2] * math.sin(degree) + new_coord[3] * math.cos(degree)
    r_p3x = new_coord[4] * math.cos(degree) - new_coord[5] * math.sin(degree)
    r_p3y = new_coord[4] * math.sin(degree) + new_coord[5] * math.cos(degree)
    r_p4x = new_coord[6] * math.cos(degree) - new_coord[7] * math.sin(degree)
    r_p4y = new_coord[6] * math.sin(degree) + new_coord[7] * math.cos(degree)

    # 원본의 원점기준으로 변환
    rr_p1x = r_p1x + img_xc
    rr_p1y = img_yc - r_p1y
    rr_p2x = r_p2x + img_xc
    rr_p2y = img_yc - r_p2y
    rr_p3x = r_p3x + img_xc
    rr_p3y = img_yc - r_p3y
    rr_p4x = r_p4x + img_xc
    rr_p4y = img_yc - r_p4y

    # 좌표 문자열로 복원
    rotation_box_coord = str(rr_p1x) + "," + str(rr_p1y) + "," + \
                         str(rr_p2x) + "," + str(rr_p2y) + "," + \
                         str(rr_p3x) + "," + str(rr_p3y) + "," + \
                         str(rr_p4x) + "," + str(rr_p4y)

    return rotation_box_coord


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


def posterize_image(input_image):
    """ image posterizing
    :param input_image: input cv image
    :return: posterized image
    """

    # Number of levels of quantization
    n = 4

    # List of all colors
    indices = np.arange(0, 256)
    # we get a divider
    divider = np.linspace(0, 255, n + 1)[1]
    # we get quantization colors
    quantiz = np.int0(np.linspace(0, 255, n))

    # color levels 0,1,2..
    color_levels = np.clip(np.int0(indices / divider), 0, n - 1)

    # Creating the palette
    palette = quantiz[color_levels]

    # Applying palette on image
    im2 = palette[input_image]

    # Converting image back to uint8
    posterized_img = cv2.convertScaleAbs(im2)

    return posterized_img


def sharpen_image(input_image):
    """ sharpen image
    :param input_image: cv image
    :return: sharpened image
    """
    kernel_sharpen = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # kernel_sharpen_2 = np.array(
    #     [[-1, -1, -1, -1, -1], [-1, 2, 2, 2, -1], [-1, 2, 8, 2, -1], [-1, 2, 2, 2, -1], [-1, -1, -1, -1, -1]]) / 8.0
    sharpened_image = cv2.filter2D(input_image, -1, kernel_sharpen)

    return sharpened_image


def motion_blur_image(input_image):
    """ motion blur
    :param input_image: cv image
    :return: motion blurred image
    """
    size = 5

    motion_blur = np.zeros((size, size))
    motion_blur[int((size - 1) / 2), :] = np.ones(size)
    motion_blur = motion_blur / size

    motion_blurred_image = cv2.filter2D(input_image, -1, motion_blur)

    return motion_blurred_image


def biliteral_blur_image(input_image):
    """ biliteral blur
    :param input_image: cv image
    :return: biliteral blurred image
    """
    biliteral_blurred_image = cv2.bilateralFilter(input_image, 9, 75, 75)

    return biliteral_blurred_image


def median_blur_image(input_image):
    """ median blur
    :param input_image: cv image
    :return: median blurred image
    """
    median_blurred_image = cv2.medianBlur(input_image, 5)

    return median_blurred_image


def rgb_to_bgr_image(input_image):
    """ rgb to bgr image
    :param input_image: cv image
    :return: bgr image
    """

    bgr_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)

    return bgr_image


def random_box_shift(coord_str, type_id):
    """ 박스 좌표를 랜덤하게 움직인다
    :param coord_str: 좌표(문자열)
    :param type_id: 좌표(객체)의 타입
    :return: 변환된 좌표(문자열)
    """
    random_shift_list = [1., 3., 5., -1., -3., -5.]

    if type_id == 1:
        random_shift_list = [1., 3., -1., -3., 0., 0.]
    elif type_id == 2:
        random_shift_list = [1., 3., -1., -3., 0., 0.]
    elif type_id == 3:
        random_shift_list = [3., 6., 9., -3., -6., -9., 0., 0.]
    elif type_id == 4:
        random_shift_list = [1., -1., 0., 0.]

    shift_x = random.choice(random_shift_list)
    shift_y = random.choice(random_shift_list)

    # 좌표 분리
    coord = coord_str.split(",")
    p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(coord[0]) + shift_x, float(coord[1]) + shift_y, \
                                             float(coord[2]) + shift_x, float(coord[3]) + shift_y, \
                                             float(coord[4]) + shift_x, float(coord[5]) + shift_y, \
                                             float(coord[6]) + shift_x, float(coord[7]) + shift_y

    # shifted coord
    shifted_coord = str(p1x) + "," + str(p1y) + "," + \
                    str(p2x) + "," + str(p2y) + "," + \
                    str(p3x) + "," + str(p3y) + "," + \
                    str(p4x) + "," + str(p4y)

    return shifted_coord


def random_aug_image(input_image, ratio):
    """ random filtering image
    :param input_image: cv image
    :param ratio: if ratio < 0.7, filter(like blur) too damage to image
    :return: random filtered image
    """
    augmented_image = input_image
    random_number = random.randrange(0, 10)
    if ratio < 0.7:
        random_number = random.randrange(3, 10)

    if random_number == 0:
        augmented_image = motion_blur_image(input_image)

    elif random_number == 1:
        augmented_image = biliteral_blur_image(input_image)

    elif random_number == 2:
        augmented_image = median_blur_image(input_image)

    elif random_number == 3:
        augmented_image = equalize_image(input_image)

    elif random_number == 4:
        augmented_image = sharpen_image(input_image)

    elif random_number == 5:
        augmented_image = edge_enhance_image(input_image)

    elif random_number == 6:
        augmented_image = edge_enhance_image(input_image)

    elif random_number == 7:
        augmented_image = rgb_to_bgr_image(input_image)

    else:
        pass

    return augmented_image


def delete_box_to_json(criterion=50):
    """ features_list에서 크기가 50x50(px)미만 박스 제거
    :return: None
    """
    with open('labels_new.json') as json_file:
        json_data = json.load(json_file)
        features = json_data["features"]

    new_features = []

    original_object_number = len(features)
    object_num = 0

    for feature in features:
        box_points = feature['properties']['bounds_imcoords'].split(",")
        p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(box_points[0]), float(box_points[1]), float(box_points[2]), \
                                                 float(box_points[3]), float(box_points[4]), float(box_points[5]), \
                                                 float(box_points[6]), float(box_points[7])

        # x_length = p2x - p1x
        # y_length = p2y - p1y
        #
        # box_length_1 = math.sqrt((x_length * x_length) + (y_length * y_length))
        # box_length_2 = math.sqrt((x_length * x_length) + (y_length * y_length))
        #
        # WH_list = [box_length_1, box_length_2].sort()
        # width, height = WH_list[0], WH_list[1]

        x_points = [p1x, p2x, p3x, p4x]
        x_points.sort()
        y_points = [p1y, p2y, p3y, p4y]
        y_points.sort()

        if x_points[3] - x_points[0] < criterion and y_points[3] - y_points[0] < criterion:
            try:
                print('feature_id:', feature['properties']['feature_id'], 'is delete(',
                      feature['properties']['image_id'],
                      'class:', feature['properties']['type_name'], ')')
            except KeyError:
                print('feature_id:', '[ there is no feature_id!!! ]', 'is delete(', feature['properties']['image_id'],
                      'class:', feature['properties']['type_name'], ')')
        else:
            properties_object = OrderedDict()
            properties = OrderedDict()

            properties_object['bounds_imcoords'] = feature['properties']['bounds_imcoords']
            properties_object['image_id'] = feature['properties']['image_id']
            properties_object['type_id'] = feature['properties']['type_id']
            properties_object['type_name'] = feature['properties']['type_name']

            properties['properties'] = properties_object
            new_features.append(properties)

            object_num += 1

        # criterion = 100
        #
        # if feature['properties']['type_id'] == 3 and \
        #         x_points[3] - x_points[0] < criterion and y_points[3] - y_points[0] < criterion:
        #     try:
        #         print('feature_id:', feature['properties']['feature_id'], 'is delete(', feature['properties']['image_id'],
        #               'class:', feature['properties']['type_name'], ')')
        #     except KeyError:
        #         print('feature_id:', '[ there is no feature_id!!! ]', 'is delete(', feature['properties']['image_id'],
        #               'class:', feature['properties']['type_name'], ')')

    features = OrderedDict()
    features['features'] = new_features

    with open('labels_new.json', 'w', encoding='utf-8') as make_file:
        json.dump(features, make_file, indent=4)

    type_1_list = []
    type_2_list = []
    type_3_list = []
    type_4_list = []

    for feature in new_features:
        if feature['properties']['type_id'] == 1:
            type_1_list.append(feature)
        elif feature['properties']['type_id'] == 2:
            type_2_list.append(feature)
        elif feature['properties']['type_id'] == 3:
            type_3_list.append(feature)
        else:
            type_4_list.append(feature)

    print('current object count: ', object_num)
    print('deleted object count:', original_object_number - object_num)
    print('container:', len(type_1_list), '(', str((len(type_1_list)/object_num)*100)[:4], '% )')
    print('oil tanker:', len(type_2_list), '(', str((len(type_2_list)/object_num)*100)[:4], '% )')
    print('aircraft carrier:', len(type_3_list), '(', str((len(type_3_list)/object_num)*100)[:4], '% )')
    print('maritime vessles:', len(type_4_list), '(', str((len(type_4_list)/object_num)*100)[:4], '% )')
    print('saved \'labels_new.json\'')


parser = argparse.ArgumentParser(description='Create random augmentation image with new geojson')
parser.add_argument('--root_path', type=str, required=True, metavar='DIR', help='Root directory to geojson and images')
parser.add_argument('--initial_number', type=int, required=True, metavar='INT', help='Initial image file number')

args = parser.parse_args()
new_image_number = args.initial_number

# read list to image path
try:
    image_root_path = args.root_path + 'images/'
    image_file_list = os.listdir(image_root_path)
    image_file_list.sort()
except BaseException:
    print('there is no path, images/ in root path')
    exit()

# read json file
try:
    with open(args.root_path + 'labels.json') as json_file:
        json_data = json.load(json_file)
        features = json_data["features"]
except BaseException:
    print('there is no json, labels.json in root path')
    exit()

coords_list = []
image_id_list = []
type_id_list = []
type_name_list = []
new_geojson_list = []
last_image_number = 0

for i in range(len(features)):
    new_geojson_list.append(features[i])

for i in range(len(image_file_list)):
    image_id = image_file_list[i]

    for j in range(len(features)):
        if features[j]['properties']['image_id'] == image_id:
            coords_list.append(features[j]['properties']['bounds_imcoords'])
            image_id_list.append(features[j]['properties']['image_id'])
            type_id_list.append(features[j]['properties']['type_id'])
            type_name_list.append(features[j]['properties']['type_name'])

angle_list = [15, 30, 45, 60, 75, 90,
              105, 120, 135, 150, 165,
              180, 195, 210, 225, 240,
              255, 270, 285, 300, 315, 330, 345]

ratio_list = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.65, 0.65, 0.6]
ratio_2_list = [0.8, 0.85, 0.9, 0.95, 1]

angle = random.choice(angle_list)
ratio = random.choice(ratio_list)
if angle == 90 or angle == 180 or angle == 270:
    ratio = random.choice(ratio_2_list)

for i in tqdm(range(len(coords_list))):
    coord_str = coords_list[i]
    image_id = image_id_list[i]
    type_id = type_id_list[i]
    type_name = type_name_list[i]

    total_path = image_root_path + image_id
    cur_image = cv2.imread(total_path)

    rotated_coord = rotate_box_3000x3000(cur_image, coord_str, angle, ratio)
    random_shifted_coord = random_box_shift(rotated_coord, type_id)

    properties_object = OrderedDict()
    properties = OrderedDict()

    properties_object['bounds_imcoords'] = random_shifted_coord
    properties_object['image_id'] = str(new_image_number) + '.png'
    properties_object['type_id'] = type_id
    properties_object['type_name'] = type_name

    properties['properties'] = properties_object
    new_geojson_list.append(properties)

    try:
        if image_id_list[i] != image_id_list[i + 1]:
            ori_img = cv2.imread(total_path)
            result = rotate_image_with_box(total_path, coord_str, angle, ratio=ratio, input_image=ori_img)
            cv2.imwrite(image_root_path + str(new_image_number) + '.png', random_aug_image(result[0], ratio))

            new_image_number += 1

            angle = random.choice(angle_list)
            ratio = random.choice(ratio_list)
            if angle == 90 or angle == 180 or angle == 270:
                ratio = random.choice(ratio_2_list)

    except BaseException:
        ori_img = cv2.imread(total_path)
        result = rotate_image_with_box(total_path, coord_str, angle, ratio=ratio, input_image=ori_img)
        cv2.imwrite(image_root_path + str(new_image_number) + '.png', random_aug_image(result[0], ratio))

features = OrderedDict()
features['features'] = new_geojson_list

with open('labels_new.json', 'w', encoding='utf-8') as make_file:
    json.dump(features, make_file, indent=4)

delete_box_to_json(60)
