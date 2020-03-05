""""
todo: 객체 위치 이동하기 (수직, 수평 이동하기)

(사용 방법)
1. 해당 파일을 터미널에서 다음 인자값으로 실행하기
    a. 파일명
    b. 이동할 x 방향 (음수: 좌 / 양수: 우)
    c. 이동할 y 방향 (음수: 상 / 양수: 하)

(객체 편집 함수로 전달할 파라미터)
1. 이미지 파일명
2. 객체의 좌표
3. 이동할 x축
4. 이동할 y축

(결과)
1. 상, 하, 좌, 우로 이동한 이미지가 새로 생성됨 (새 이미지 생성)
2. 이동한 이미지에 맞게 수정된 객체의 라벨 데이터 생성 (새 이미지의 이름, 좌표, 클래스 이름 등의 데이터가 생성됨)
"""

import sys
import json
from _collections import OrderedDict
import numpy as np
import cv2
import os

# input_image_name = sys.argv[1]
# input_move_x = sys.argv[2]
# input_move_y = sys.argv[3]

# 편집할 이미지가 저장된 경로
image_path = '../images/'

# 편집할(이동할) 이미지 번호
input_image_name = "407"

# 편집할 json 파일 경로
original_json_path = 'labelsssss.json'

# 새로 저장할 json 경로 (위 경로와 겹칠 경우 기존 라벨링에 데이터가 추가됨)
# edit_object_location_result_path = '/labels_move_location_result.json'
edit_object_location_result_path = original_json_path

# todo: x축 음수: 좌 / 양수: 우
input_move_x = "-1200"

# todo: y축 음수: 상 / 양수: 하
input_move_y = "0"

""" ######### 객체 좌표 이동하기 ######### """

def positive_check(input_value):
    """
    :param input_value: 양수여부 판단할 값 입력
    :return: 값이 양수일 경우 True, 음수일 경우 False 반환
    """
    if input_value == '':
        return False
    elif(input_value[0] == '+' and input_value[1:].isdecimal()) or input_value.isdecimal():
        return True
    else:
        return False

# 음수를 양수로 변환하기
def remove_negative(negative_value):
    """
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

def move_object_location(bounds_imcoords, save_image_name, move_x, move_y):
    """
        :param bounds_imcoords: 이동할 객체의 원본 좌표
        :param input_image_name: 이동한 객체를 새로 저장할 이미지명
        :param move_x: 이동할 x축 (가로) _ 이동방향 _ 음수: 좌 / 양수: 우
        :param move_y: 이동할 y축 (세로) _ 이동방향 _ 음수: 상 / 양수: 하
    """

    before_edit_coords_listA = bounds_imcoords.split(",")

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
        point_x_list = move_location_result(point_x_list, move_x, "positive") # 이동 전 x축 리스트 / 이동할 x 축 값 입력

    else:
        # print("x축을 음수 방향으로 이동합니다")

        # 음수를 양수로 변환하기
        move_x = remove_negative(move_x)
        
        # 음수 이동 결과 반환 받기
        point_x_list = move_location_result(point_x_list, move_x, "negative") # 이동 전 x축 리스트 / 이동할 x 축 값 입력

    # todo: y 축 이동 방향 확인하기 (양수 여부 체크)
    if positive_check(move_y):
        # print("y축을 양수 방향으로 이동합니다")

        # 양수 이동 결과 반환 받기
        point_y_list = move_location_result(point_y_list, move_y, "positive") # 이동 전 x축 리스트 / 이동할 x 축 값 입력

    else:
        # print("y축을 음수 방향으로 이동합니다")

        # 음수를 양수로 변환하기
        move_y = remove_negative(move_y)
        # print("y축 음수를 양수로 변환 완료:", move_y)

        # 음수 이동 결과 반환 받기
        point_y_list = move_location_result(point_y_list, move_y, "negative") # 이동 전 y축 리스트 / 이동할 y축 값 입력

    # 좌표 이동 결과 반환하기
    result_location_move = str(point_x_list[0]) + "," + str(point_y_list[0]) + "," + \
                           str(point_x_list[1]) + "," + str(point_y_list[1]) + "," + \
                           str(point_x_list[2]) + "," + str(point_y_list[2]) + "," + \
                           str(point_x_list[3]) + "," + str(point_y_list[3])

    """이미지 저장하기"""
    # 원본 이미지 불러오기
    img_source = cv2.imread(image_path + str(input_image_name) + ".png")
    # print(image_path + str(input_image_name) + ".png")

    """
    이미지 x축 이동 방향: 음수: 좌 / 양수: 우
    이미지 y축 이동 방향: 음수: 상 / 양수: 하
    np.float32([[1, 0, '이동할 x축 입력'], [0, 1, '이동할 y축 입력']])
    """
    height, width = img_source.shape[:2]
    M = np.float32([[1, 0, input_move_x], [0, 1, input_move_y]])
    img_translation = cv2.warpAffine(img_source, M, (width, height))

    # 이미지 저장하기
    # cv2.imwrite("저장할 경로/파일명", "입력받은 방향으로 이동한 이미지")
    cv2.imwrite(str(save_image_name)+".png", img_translation)

    # 수정된 좌표값 반환하기
    return result_location_move

""" ######### (끝) 객체 좌표 이동하기 ######### """

with open(original_json_path) as json_file:

    json_data = json.load(json_file)
    """라벨JSON파일 받아옴"""

    original_features = json_data["features"]
    """JSON파일은 features란 이름의 리스트안에 모든 내용이 들어가있으므로 features를 꺼내옴"""

before_edit_coord_list = []
"""
(before_edit_coord_list: 좌표값들을 넣을 리스트)
1. 좌표 값을 담는다.
2. point 1~4의 xy 값을 각각 담는다
3. xy 값을 가공해서 원해 문자열 형태로 합친다
"""



result_edit_coord_list = []
"""
(result_edit_coord_list: 가공된 좌표를 담을 리스트)
1. 가공이 완료된 좌표를 담는다.
"""

edit_features_name_list = []
"""수정할 파일명 리스트"""

# if original_features[int(i)]['properties']['image_id'] == input_image_name + '.png':

new_geojson_list = []
"""수정된 json 정보를 담을 리스트"""

# todo: json에 저장된 데이터를 리스트에 정리하기
for i in range(len(original_features)):

    new_geojson_list.append(original_features[i])
    # """수정된 json 정보를 담기전에 기존 json 데이터를 담아둔다"""

last_name = new_geojson_list[-1]['properties']['image_id']
"""기존 JSON파일의 마지막 항목의 이미지 이름을 꺼내온다"""

last_number = last_name.split(".")
"""number.png형식이므로 나눠준다"""

add_number = int(last_number[0]) + 1
"""마지막 파일이 100.png였으면 새로운 features는 101.png부터 시작"""

# features 배열 계층
features = OrderedDict()

save_count = 1

before_image_id = None

# todo: 편집할 이미지의 좌표 검색
for i in range(len(original_features)):

    if original_features[int(i)]['properties']['image_id'] == input_image_name + '.png':

        # todo: 편집할 좌표  x / y 를 x list, y list 로 나누어 저장하기
        coords = original_features[int(i)]['properties']['bounds_imcoords']

        # 새 이미지 저장하기, 좌표 이동 결과 반환 받기
        move_result = move_object_location(coords, add_number, input_move_x, input_move_y)

        # 수정된 라벨 좌표 반영하기
        # 첫 번 째 이미지 번호의 json 데이터 조회하기
        # for j in range(len(original_features)):

            # # 해당 이미지 번호에 포함된 모든 선박 라벨 데이터를 json list 에 추가하기
            # if original_features[j]["properties"]["image_id"] == input_image_name + ".png":

        # top/feature/properties/(data)
        properties_data = OrderedDict()
        '''properties 내부에 데이터 저장할 json'''

        # top/feature/properties
        properties = OrderedDict()
        '''properties 계층이 될 JSON'''

        # top/feature/properties/image_id(새로 저장할 이미지 번호)
        properties_data['image_id'] = str(add_number) + '.png'

        # top/feature/properties/bounds_imcoords(수정된 선박 좌표)
        properties_data['bounds_imcoords'] = move_result

        # top/feature/properties/type_id(클래스 번호)
        properties_data['type_id'] = original_features[int(i)]["properties"]["type_id"]

        # top/feature/properties/type_name(선박 이름)
        properties_data['type_name'] = original_features[int(i)]["properties"]["type_name"]

        # top/feature/properties/original_label_index(원본 라벨링 인덱스 번호)
        properties_data["original_label_bounds_imcoords"] = original_features[int(i)]["properties"]["bounds_imcoords"]

        # top/feature/properties/original_image_id(원본 이미지 번호)
        properties_data["original_image_id"] = original_features[int(i)]["properties"]["image_id"]

        # top/feature/properties/original_label_index(원본 라벨링 인덱스 번호)
        # properties_data["original_label_index"] = j

        properties['properties'] = properties_data
        '''위에서 생성된 요소를 properties에 넣는다'''

        # features 배열 계층에 추가할 인덱스
        new_geojson_list.append(properties)

        print("("+ str(save_count) + ")저장 완료")

        save_count += 1

        #################################################################

        print("new json 라벨링 완료:", str(add_number) + ".png")

        # 입력받은 이미지를 모두 담았다면 다음 입력받은 이미지 조회하기
        if before_image_id is None:
            # add_number += 1
            before_image_id = original_features[int(i)]['properties']['image_id']

        if before_image_id != original_features[int(i)]['properties']['image_id']:
            add_number += 1
            before_image_id = original_features[int(i)]['properties']['image_id']



features['features'] = new_geojson_list
'''마지막으로 해당 properties를 리스트에 넣는다'''

# json 파일 새로 저장
with open(edit_object_location_result_path, 'w', encoding='utf-8') as make_file:
    json.dump(features, make_file, indent="\t")

print("(객체 위치 이동 후 새 json 생성 완료)")
