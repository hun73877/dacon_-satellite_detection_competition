import os
import cv2
import json
import math
import tqdm
from _collections import OrderedDict


def crop_leftup(coords_str, image_id, x_shift=0, y_shift=0, cv2_image=None):
    """
    선박 크롭 및 패딩, 좌표 변환

    :param coords_str: 원본 박스 좌표(문자열)
    :param image_id: 이미지 파일 이름
    :param x_shift: 박스 가로축 이동
    :param y_shift: 박스 세로축 이동
    :param cv2_image: 이미지 객체(기본값 비어있음)
    :return: 크롭된 이미지, 변환된 박스 좌표(문자열)
    """

    coords = coords_str.split(",")
    p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3]), \
                                             float(coords[4]), float(coords[5]), float(coords[6]), float(coords[7])

    coord_list = [p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y]

    x_coord_list = [coord_list[0], coord_list[2], coord_list[4], coord_list[6]]
    x_coord_list.sort()

    y_coord_list = [coord_list[1], coord_list[3], coord_list[5], coord_list[7]]
    y_coord_list.sort()

    x_min = int(x_coord_list[0])
    if x_min < 0:
        x_min = 0

    y_min = int(y_coord_list[0])
    if y_min < 0:
        y_min = 0

    x_max = int(x_coord_list[3])
    if x_max > 3000:
        x_max = 3000

    y_max = int(y_coord_list[3])
    if y_max > 3000:
        y_max = 3000

    x_size = x_max - x_min
    y_size = y_max - y_min
    x_pad_size = 3000 - x_size
    y_pad_size = 3000 - y_size

    original_img = cv2.imread(image_root_path + image_id)
    copy_img = original_img.copy()

    if cv2_image is not None:
        copy_img = cv2_image

    crop_img = copy_img[y_min:y_max, x_min:x_max]

    crop_y, crop_x = crop_img.shape[:2]

    if x_size > crop_x:
        x_pad_size += (x_size - crop_x)
    if y_size > crop_y:
        y_pad_size += (y_size - crop_y)

    padadd_img = cv2.copyMakeBorder(crop_img, 0, y_pad_size, 0, x_pad_size, borderType=cv2.BORDER_CONSTANT)
    result_img = padadd_img

    xx1 = p1x - x_min + x_shift
    yy1 = p1y - y_min + y_shift
    xx2 = p2x - x_min + x_shift
    yy2 = p2y - y_min + y_shift
    xx3 = p3x - x_min + x_shift
    yy3 = p3y - y_min + y_shift
    xx4 = p4x - x_min + x_shift
    yy4 = p4y - y_min + y_shift

    coords_str = str(xx1) + "," + str(yy1) + "," + \
                 str(xx2) + "," + str(yy2) + "," + \
                 str(xx3) + "," + str(yy3) + "," + \
                 str(xx4) + "," + str(yy4)

    return result_img, coords_str


def rotate_image_coord(coords_str, image_id, ang, cv2_image=None):
    """
    이미지 및 박스 좌표 회전

    :param coords_str: 원본 박스 좌표(문자열)
    :param image_id: 이미지 파일 이름
    :param ang: 회전시킬 각도
    :param cv2_image: 이미지 객체(기본값 비어있음)
    :return: 회전된 이미지, 회전된 박스 좌표(문자열)
    """

    original_img = cv2.imread(image_root_path + image_id)
    copy_img = original_img.copy()

    if cv2_image is not None:
        copy_img = cv2_image

    height, width = copy_img.shape[:2]
    """이미지를 읽어와서 가로, 세로의 길이를 받는다"""

    coord_list = coords_str.split(",")
    """좌표를 ,으로 분리하여 8개의 변수에 나눠 넣는다"""
    p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(coord_list[0]), float(coord_list[1]), float(coord_list[2]), \
                                             float(coord_list[3]), float(coord_list[4]), float(coord_list[5]), \
                                             float(coord_list[6]), float(coord_list[7])

    angle = 180 / ang
    degree = math.pi / angle
    """각도 변환"""

    img_yc = height / 2
    img_xc = width / 2
    """이미지의 중심 좌표"""

    new_coord_list = [p1x - img_xc, img_yc - p1y, p2x - img_xc, img_yc - p2y,
                      p3x - img_xc, img_yc - p3y, p4x - img_xc, img_yc - p4y]
    """좌표를 이미지 중심 기준으로 바꿔준다"""

    r_p1x = new_coord_list[0] * math.cos(degree) - new_coord_list[1] * math.sin(degree)
    r_p1y = new_coord_list[0] * math.sin(degree) + new_coord_list[1] * math.cos(degree)
    r_p2x = new_coord_list[2] * math.cos(degree) - new_coord_list[3] * math.sin(degree)
    r_p2y = new_coord_list[2] * math.sin(degree) + new_coord_list[3] * math.cos(degree)
    r_p3x = new_coord_list[4] * math.cos(degree) - new_coord_list[5] * math.sin(degree)
    r_p3y = new_coord_list[4] * math.sin(degree) + new_coord_list[5] * math.cos(degree)
    r_p4x = new_coord_list[6] * math.cos(degree) - new_coord_list[7] * math.sin(degree)
    r_p4y = new_coord_list[6] * math.sin(degree) + new_coord_list[7] * math.cos(degree)
    """이미지 중심기준으로 바뀐 좌표를 회전시킨다"""

    rr_p1x = r_p1x + img_xc
    rr_p1y = img_yc - r_p1y
    rr_p2x = r_p2x + img_xc
    rr_p2y = img_yc - r_p2y
    rr_p3x = r_p3x + img_xc
    rr_p3y = img_yc - r_p3y
    rr_p4x = r_p4x + img_xc
    rr_p4y = img_yc - r_p4y
    """다시 원래 기준으로 좌표를 복원한다"""

    rotate_m = cv2.getRotationMatrix2D((img_xc, img_yc), ang, 1)
    r_img = cv2.warpAffine(copy_img, rotate_m, (width, height))
    """이미지를 회전시킨다"""

    # cv2.line(r_img, (int(rr_p1x), int(rr_p1y)), (int(rr_p2x), int(rr_p2y)), (255, 255, 0), 6)
    # cv2.line(r_img, (int(rr_p2x), int(rr_p2y)), (int(rr_p3x), int(rr_p3y)), (255, 255, 0), 6)
    # cv2.line(r_img, (int(rr_p3x), int(rr_p3y)), (int(rr_p4x), int(rr_p4y)), (255, 255, 0), 6)
    # cv2.line(r_img, (int(rr_p4x), int(rr_p4y)), (int(rr_p1x), int(rr_p1y)), (255, 255, 0), 6)
    #
    # cv2.imwrite("test.png", r_img)
    #
    rotation_box_coords = str(rr_p1x) + "," + str(rr_p1y) + "," + \
                          str(rr_p2x) + "," + str(rr_p2y) + "," + \
                          str(rr_p3x) + "," + str(rr_p3y) + "," + \
                          str(rr_p4x) + "," + str(rr_p4y)
    # print(rotation_box_coords)
    """회전된 좌표들을 JSON에 들어있던 형식의 문자열로 다시 합치고 출력"""

    return r_img, rotation_box_coords


def resize_image_coord(coords_str, image_id, ratio, cv2_image=None):
    """
    이미지 리사이즈

    :param coords_str: 원본 박스 좌표(문자열)
    :param image_id: 이미지 파일 이름
    :param ratio: 리사이즈 비율(0~1)
    :param cv2_image: 이미지 객체(기본값 비어있음)
    :return: 리사이즈된 이미지, 변경된 박스 좌표 문자열
    """

    coord_list = coords_str.split(",")
    """좌표를 ,으로 분리하여 8개의 변수에 나눠 넣는다"""
    p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(coord_list[0]), float(coord_list[1]), float(coord_list[2]), \
                                             float(coord_list[3]), float(coord_list[4]), float(coord_list[5]), \
                                             float(coord_list[6]), float(coord_list[7])

    original_img = cv2.imread(image_root_path + image_id)
    copy_img = original_img.copy()

    if cv2_image is not None:
        copy_img = cv2_image

    resize_img = cv2.resize(copy_img, dsize=(0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
    """입력된 비율로 이미지를 리사이즈하고 변경된 크롭사이즈로 이미지를 크롭한다"""

    r_p1x = p1x * ratio
    r_p1y = p1y * ratio
    r_p2x = p2x * ratio
    r_p2y = p2y * ratio
    r_p3x = p3x * ratio
    r_p3y = p3y * ratio
    r_p4x = p4x * ratio
    r_p4y = p4y * ratio
    """변경된 좌표 계산"""

    # cv2.line(resize_img, (new_p1x, new_p1y), (new_p2x, new_p2y), (255, 255, 0), 4)
    # cv2.line(resize_img, (new_p2x, new_p2y), (new_p3x, new_p3y), (255, 255, 0), 4)
    # cv2.line(resize_img, (new_p3x, new_p3y), (new_p4x, new_p4y), (255, 255, 0), 4)
    # cv2.line(resize_img, (new_p4x, new_p4y), (new_p1x, new_p1y), (255, 255, 0), 4)
    #
    # cv2.imshow("test.png", resize_img)
    # cv2.waitKey(0)
    """확인용으로 박스를 그려서 표시"""

    modify_box_coords = str(r_p1x) + "," + str(r_p1y) + "," + \
                        str(r_p2x) + "," + str(r_p2y) + "," + \
                        str(r_p3x) + "," + str(r_p3y) + "," + \
                        str(r_p4x) + "," + str(r_p4y)
    """변경된 좌표들을 JSON에 들어있던 형식의 문자열로 다시 합치고 출력"""

    return resize_img, modify_box_coords


def save_image_json(result, filter_var=0):
    f_image = result[0]
    if filter_var is 1:
        f_image = cv2.bilateralFilter(result[0], 9, 75, 75)
    elif filter_var is 2:
        f_image = cv2.GaussianBlur(result[0], (5, 5), 0)
    elif filter_var is 3:
        f_image = cv2.medianBlur(result[0], 5)
    elif filter_var is 4:  # Todo 필터 추가...
        print("필터 추가")

    cv2.imwrite(str(new_image_number) + ".png", f_image)

    properties_object = OrderedDict()
    properties = OrderedDict()

    properties_object['bounds_imcoords'] = result[1]
    properties_object['image_id'] = str(new_image_number) + '.png'
    properties_object['type_id'] = 3
    properties_object['type_name'] = 'aircraft carrier'

    properties['properties'] = properties_object
    new_geojson_list.append(properties)


########################################################################################################################
########################################################################################################################


image_root_path = "../images/"
image_file_list = os.listdir(image_root_path)
image_file_list.sort()

with open('labels_1050_reconstruction.json') as json_file:
    json_data = json.load(json_file)
    features = json_data["features"]

coords_list = []
image_id_list = []
new_geojson_list = []
last_image_number = 0

for i in range(len(features)):
    new_geojson_list.append(features[i])

last_image_id = new_geojson_list[-1]['properties']['image_id']
last_image_number = last_image_id.split(".")
new_image_number = int(last_image_number[0]) + 1

for i in range(len(image_file_list)):
    image_id = image_file_list[i]

    for j in range(len(features)):
        if features[j]['properties']['image_id'] == image_id and features[j]['properties']['type_id'] == 3:
            coords_list.append(features[j]['properties']['bounds_imcoords'])
            image_id_list.append(features[j]['properties']['image_id'])

########################################################################################################################
# # Todo : 단순 크롭0 -1
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭1 -2
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, 20, 0)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭2 -3
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, -20, 0)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭3 -4
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, 0, 20)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭4 -5
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, 0, -20)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭5 -6
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, 20, 20)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭6 -7
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, 20, -20)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭7 -8
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, -20, -20)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 단순 크롭8 -9
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     result = crop_leftup(coords_str, image_id, -20, 20)
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭0 -10
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 30)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭1 -11
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 60)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭2 -12
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 120)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭3 -13
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 150)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭4 -14
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 210)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭5 -15
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 240)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭6 -16
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 300)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 회전 크롭7 -17
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 330)
#     result = crop_leftup(r_result[1], image_id, 0, 0, r_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈 크롭0 -18
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     re_result = resize_image_coord(coords_str, image_id, 0.8)
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈, 회전, 크롭0 -18
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 30)
#     re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈, 회전, 크롭1 -19
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 60)
#     re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈, 회전, 크롭2 -20
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 120)
#     re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈, 회전, 크롭3 -21
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 150)
#     re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈, 회전, 크롭4 -22
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 210)
#     re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈, 회전, 크롭5 -23
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 240)
#     re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1
#
# # Todo : 리사이즈, 회전, 크롭5 -24
# for i in range(len(coords_list)):
#     coords_str = coords_list[i]
#     image_id = image_id_list[i]
#
#     r_result = rotate_image_coord(coords_str, image_id, 300)
#     re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
#     result = crop_leftup(re_result[1], image_id, 0, 0, re_result[0])
#     save_image_json(result)
#
#     new_image_number += 1

# Todo : 리사이즈, 회전, 크롭5 -24
for i in range(len(coords_list)):
    coords_str = coords_list[i]
    image_id = image_id_list[i]

    # r_result = rotate_image_coord(coords_str, image_id, 330)
    # re_result = resize_image_coord(r_result[1], image_id, 0.8, r_result[0])
    result = crop_leftup(coords_str, image_id, 0, 0)
    save_image_json(result)

    new_image_number += 1
########################################################################################################################

features = OrderedDict()
features['features'] = new_geojson_list

with open('labels_new.json', 'w', encoding='utf-8') as make_file:
    json.dump(features, make_file, indent=4)

# crop_leftup()

