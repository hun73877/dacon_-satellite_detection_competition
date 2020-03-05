import cv2
import json
from _collections import OrderedDict
import matplotlib.pyplot as plt

# originalImage = cv2.imread('../images/0.png')

"""
(flip_option)
0: 상하 반전
1: 좌우 반전
-1: 상하좌우 반전
"""
flip_option = 1

# 편집할(이동할) 이미지 번호
input_image_name = "400.png"

# 편집할 이미지가 저장된 경로
image_path = '../images/'

# 편집할 json 파일 경로
original_json_path = 'labelsssss.json'

# 새로 저장할 json 경로 (위 경로와 겹칠 경우 기존 라벨링에 데이터가 추가됨)
# edit_object_location_result_path = '/labels_move_location_result.json'
edit_object_location_result_path = original_json_path

# def flip_object_location(location, flip_direction):
#
#     if flip_direction is 0:
#         for i in range(len(location)):
#             location[i] = 3000 + float(location[i])
#     elif flip_direction is 1:
#         for i in range(len(location)):
#             location[i] = 3000 - float(location[i])
#     # else:
#     #     for i in range(len(location)):
#     #         location[i] = 3000 - float(location[i])
#
#     return location

def flip_image_n_object(coords_str, image_id, flip_direction):
    """
    :param coords_str: 반전 할 객체의 좌표
    :param image_id: 반전 할 이미지 이름
    :param flip_direction: 반전할 방향 (0: 상하 반전 / 1: 좌우 반전 / -1: 상하좌우 반전)
    :return: 반전된 이미지, 반전된 객체의 좌표
    """

    before_flip_coords = coords_str.split(",")

    originalImage = cv2.imread(image_path+image_id)

    """이미지의 x 좌표를 리스트에 담기 (point 1, 2, 3, 4 x)"""
    point_x_list = [float(before_flip_coords[0]),
                    float(before_flip_coords[2]),
                    float(before_flip_coords[4]),
                    float(before_flip_coords[6])]

    """이미지의 y 좌표를 리스트에 담기 (point 1, 2, 3, 4 y)"""
    point_y_list = [float(before_flip_coords[1]),
                    float(before_flip_coords[3]),
                    float(before_flip_coords[5]),
                    float(before_flip_coords[7])]

    ############# 이미지 저장 ################
    # flip_result_img = None
    if flip_direction is 0:
        print("상하 반전")
        flip_result_img = cv2.flip(originalImage, flip_direction) # 0

        for i in range(len(point_y_list)):
            point_y_list[i] = 3000 - float(point_y_list[i])

    elif flip_direction is 1:
        print("좌우 반전")
        flip_result_img = cv2.flip(originalImage, flip_direction) # 1

        for i in range(len(point_y_list)):
            point_x_list[i] = 3000 - float(point_x_list[i])

    elif flip_direction is -1:
        print("상하좌우 반전")
        flip_result_img = cv2.flip(originalImage, -1) # -1

        for i in range(len(point_x_list)):
            point_x_list[i] = 3000 - float(point_x_list[i])

        for i in range(len(point_y_list)):
            point_y_list[i] = 3000 - float(point_y_list[i])

    # cv2.imwrite("flip.png", flip_result_img)

    ############# (끝) 이미지 저장 ################

    # 좌표 이동 결과 반환하기
    flip_result_coords = str(point_x_list[0]) + "," + str(point_y_list[0]) + "," + \
                           str(point_x_list[1]) + "," + str(point_y_list[1]) + "," + \
                           str(point_x_list[2]) + "," + str(point_y_list[2]) + "," + \
                           str(point_x_list[3]) + "," + str(point_y_list[3])

    return flip_result_img, flip_result_coords
    # return flip_result_coords

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

    if original_features[int(i)]['properties']['image_id'] == input_image_name:

        # todo: 편집할 좌표  x / y 를 x list, y list 로 나누어 저장하기
        coords = original_features[int(i)]['properties']['bounds_imcoords']

        # 새 이미지 저장하기, 좌표 이동 결과 반환 받기
        flip_result = flip_image_n_object(coords, input_image_name, flip_option)

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
        properties_data['bounds_imcoords'] = flip_result[1]

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
            cv2.imwrite(str(add_number) + '.png', flip_result[0])
            before_image_id = original_features[int(i)]['properties']['image_id']

        if before_image_id != original_features[int(i)]['properties']['image_id']:
            cv2.imwrite(str(add_number) + '.png', flip_result[0])
            add_number += 1
            before_image_id = original_features[int(i)]['properties']['image_id']



features['features'] = new_geojson_list
'''마지막으로 해당 properties를 리스트에 넣는다'''

# json 파일 새로 저장
with open(edit_object_location_result_path, 'w', encoding='utf-8') as make_file:
    json.dump(features, make_file, indent="\t")

print("(객체 위치 이동 후 새 json 생성 완료)")

