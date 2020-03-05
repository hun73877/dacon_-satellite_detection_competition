""""
todo: 객체 위치 이동하기 (상, 하, 좌, 우 이동하기)

(사용 방법)
"move_result = move_object_location(coords_str, image_id, input_move_x, input_move_y)"

input_move_x: 이동할 x 방향 (음수: 좌 / 양수: 우)
input_move_y: 이동할 y 방향 (음수: 상 / 양수: 하)

move_result[0]: 좌표 이동 결과 반환
move_result[1]: 이미지 이동 결과 반환
"""

import sys
import json
from _collections import OrderedDict
import numpy as np
import cv2
import os

# 편집할(이동할) 이미지 번호
input_image_name = "419.png"

# todo: x축 음수: 좌 / 양수: 우
input_move_x = "-1700"

# todo: y축 음수: 상 / 양수: 하
input_move_y = "-1650"

""" ######### 객체 좌표 이동하기 ######### """


def positive_check(input_value):
    """
    (숫자의 양수 여부 판단하기)
    :param input_value: 양수여부 판단할 값 입력
    :return: 값이 양수일 경우 True, 음수일 경우 False 반환
    """
    if input_value == '':
        return False
    elif (input_value[0] == '+' and input_value[1:].isdecimal()) or input_value.isdecimal():
        return True
    else:
        return False



def remove_negative(negative_value):
    """
    (음수를 양수로 변환하기)
    :param negative_value: 음수 값 입력
    :return: 음수 부호를 제외한 값을 반환함
    """

    result = None

    for i in range(len(negative_value)):

        if i == 0:
            pass

        # 1. negative_value를 한 글자씩 배열에 담기
        # 2. 배열화된 negative_value의 0번 인덱스인 음수 부호 (-) 제거
        else:
            if result is None:
                result = negative_value[i]
            else:
                result = result + negative_value[i]

    return result


def move_location_result(list, value, direction):
    """
        :param list: 이동 전 좌표 목록
        :param value: 이동 전 좌표 거리
        :param direction: 이동 방향 (음수, 양수 방향)
        :return: 좌표 이동 결과를 리스트로 반환
    """

    # 음수 방향만큼 좌표 이동
    if direction is "negative":
        for i in range(len(list)):
            list[i] = float(list[i]) - float(value)

    # 양수 방향만큼 좌표 이동
    else:
        for i in range(len(list)):
            list[i] = float(list[i]) + float(value)

    # 음수 이동이 완료된 좌표 리스트 반환하기
    return list


def move_object_location(coords_str, image_id, move_x, move_y):
    """
        (바운딩 박스, 이미지의 좌표 이동하기)
        :param coords_str: 이동할 객체의 원본 좌표
        :param image_id: 이동할 객체의 원본 이미지 이름
        :param move_x: 이동할 x축 (가로) _ 이동방향 _ 음수: 좌 / 양수: 우
        :param move_y: 이동할 y축 (세로) _ 이동방향 _ 음수: 상 / 양수: 하
        :return: 입력한 방향으로 이동한 이미지, 좌표
    """

    before_edit_coords_listA = coords_str.split(",")

    """이미지의 x 좌표를 리스트에 담기 (point 1, 2, 3, 4 x)"""
    point_x_list = [float(before_edit_coords_listA[0]),
                    float(before_edit_coords_listA[2]),
                    float(before_edit_coords_listA[4]),
                    float(before_edit_coords_listA[6])]

    """이미지의 y 좌표를 리스트에 담기 (point 1, 2, 3, 4 y)"""
    point_y_list = [float(before_edit_coords_listA[1]),
                    float(before_edit_coords_listA[3]),
                    float(before_edit_coords_listA[5]),
                    float(before_edit_coords_listA[7])]

    # todo: x 축 이동 방향 확인하기 (양수 여부 체크)
    if positive_check(move_x):
        # print("x축을 양수 방향으로 이동합니다")

        # 양수 이동 결과 반환 받기
        point_x_list = move_location_result(point_x_list, move_x, "positive")  # 이동 전 x축 리스트 / 이동할 x 축 값 입력

    else:
        # print("x축을 음수 방향으로 이동합니다")

        # 음수를 양수로 변환하기
        move_x = remove_negative(move_x)

        # 음수 이동 결과 반환 받기
        point_x_list = move_location_result(point_x_list, move_x, "negative")  # 이동 전 x축 리스트 / 이동할 x 축 값 입력

    # todo: y 축 이동 방향 확인하기 (양수 여부 체크)
    if positive_check(move_y):
        # print("y축을 양수 방향으로 이동합니다")

        # 양수 이동 결과 반환 받기
        point_y_list = move_location_result(point_y_list, move_y, "positive")  # 이동 전 x축 리스트 / 이동할 x 축 값 입력

    else:
        # print("y축을 음수 방향으로 이동합니다")

        # 음수를 양수로 변환하기
        move_y = remove_negative(move_y)
        # print("y축 음수를 양수로 변환 완료:", move_y)

        # 음수 이동 결과 반환 받기
        point_y_list = move_location_result(point_y_list, move_y, "negative")  # 이동 전 y축 리스트 / 이동할 y축 값 입력

    # 좌표 이동 결과 반환하기
    result_move_coords = str(point_x_list[0]) + "," + str(point_y_list[0]) + "," + \
                           str(point_x_list[1]) + "," + str(point_y_list[1]) + "," + \
                           str(point_x_list[2]) + "," + str(point_y_list[2]) + "," + \
                           str(point_x_list[3]) + "," + str(point_y_list[3])

    """이미지 저장하기"""
    # 원본 이미지 불러오기
    img_source = cv2.imread(str(image_id) + ".png")
    # print(image_path + str(input_image_name) + ".png")

    """
    이미지 x축 이동 방향: 음수: 좌 / 양수: 우
    이미지 y축 이동 방향: 음수: 상 / 양수: 하
    np.float32([[1, 0, '이동할 x축 입력'], [0, 1, '이동할 y축 입력']])
    """
    height, width = img_source.shape[:2]
    M = np.float32([[1, 0, input_move_x], [0, 1, input_move_y]])
    result_img_move = cv2.warpAffine(img_source, M, (width, height))

    # 이미지 저장하기
    # cv2.imwrite("저장할 경로/파일명", "입력받은 방향으로 이동한 이미지")
    # cv2.imwrite(str(image_name) + ".png", img_translation)

    return result_move_coords, result_img_move

""" ######### (끝) 객체 좌표 이동하기 ######### """




move_result = move_object_location("coords_str", input_image_name, input_move_x, input_move_y)