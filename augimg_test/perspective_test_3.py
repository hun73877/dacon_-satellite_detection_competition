import cv2
import json
from _collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# originalImage = cv2.imread('../images/0.png')

# 원근감 줄 이미지 번호
input_image_name = "32.png"

# 원근감 옵션 입력
option_perspective = 3
"""
    원근감 설정 모음
    
        (0): 상 25 px / (1): 하 25 px 
        (2): 좌 25 px / (3): 우 25 px 
        
        (4): 상 50 px / (5): 하 50 px 
        (6): 좌 50 px / (7): 우 50 px 
        
        (8): 상 75 px  / (9): 하 75 px 
        (10): 좌 75 px / (11): 우 75 px 
"""

# 편집할 이미지가 저장된 경로
image_path = '../images/'

# 편집할 json 파일 경로
original_json_path = 'labels.json'

# 새로 저장할 json 경로 (위 경로와 겹칠 경우 기존 라벨링에 데이터가 추가됨)
# edit_object_location_result_path = '/labels_move_location_result.json'
edit_object_location_result_path = original_json_path

def perspective(coords_str, image_name, perspective_direction):
    """
        :param coords_str: 외곡 적용할 객체의 좌표
        :param image_name: 외곡 적용할 이미지의 이름
        :param perspective_direction: 원근 옵션 (아래 원근 옵션 참고)
        :return: 좌표, 반전된 객체의 좌표 (좌표 못 찾으면 'delete' 반환 )

        
        ############# 원근감 옵션 ################
        
        원근감 설정 모음
        (0): 상 25 px / (1): 하 25 px 
        (2): 좌 25 px / (3): 우 25 px 
        
        (4): 상 50 px / (5): 하 50 px 
        (6): 좌 50 px / (7): 우 50 px 
        
        (8): 상 75 px  / (9): 하 75 px 
        (10): 좌 75 px / (11): 우 75 px  
        
        좌표점 순서는 좌상->좌하->우상->우하
    """

    def positive_check(input_value):

        """
        :param input_value: 양수여부 판단할 값 입력
        :return: 값이 양수일 경우 True, 음수일 경우 False 반환
        """

        if input_value == '':
            return False
        elif (input_value[0] == '+' and input_value[1:].isdecimal()) or input_value.isdecimal():
            return True
        else:
            return False

    """ ############# 좌표 이동 준비 ################ """

    print(image_path + image_name)
    img = cv2.imread(image_path + image_name)
    perspective_result = cv2.imread(image_path + image_name)

    before_perspective_coords = coords_str.split(",")

    # 이동 결과를 적용할 바운딩 박스
    point_x_list2 = [float(before_perspective_coords[0]), float(before_perspective_coords[2]),
                     float(before_perspective_coords[4]), float(before_perspective_coords[6])]
    point_y_list2 = [float(before_perspective_coords[1]), float(before_perspective_coords[3]),
                     float(before_perspective_coords[5]), float(before_perspective_coords[7])]
    print("before:", point_x_list2)
    print("before:", point_y_list2)

    # 바운딩박스의 중심점 구하기.
    point_x_list = []
    point_y_list = []
    for i in range(len(before_perspective_coords)):
        if i is 0 or i is 2 or i is 4 or i is 6:
            point_xx = str(before_perspective_coords[i]).split(".")
            point_x_list.append(int(point_xx[0]))
        else:
            point_yy = str(before_perspective_coords[i]).split(".")
            point_y_list.append(int(point_yy[0]))

    point_x_list.sort()
    point_y_list.sort()

    center_x = (point_x_list[3] + point_x_list[0]) / 2
    center_y = (point_y_list[3] + point_y_list[0]) / 2

    center_x = int(center_x)
    center_y = int(center_y)

    cv2.circle(img, (center_x, center_y), 6, (0, 0, 255), -1)  # red
    # img[int(center_y), int(center_x)] = [255, 0, 0]  # green
    print("이동 전 중심 좌표 x:", int(center_x))
    print("이동 전 중심 좌표 y:", int(center_y))
    cv2.imwrite('win.png', img)
    """ ############# (끝) 좌표 이동 준비 ################ """

    perspective_direction_list = [
        [[225, 200], [175, 2800], [2775, 200], [2825, 2800]],
        [[175, 200], [225, 2800], [2825, 200], [2785, 2800]],
        [[200, 225], [200, 2775], [2800, 175], [2800, 2825]],
        [[200, 175], [200, 2825], [2800, 225], [2800, 2775]],

        [[250, 200], [150, 2800], [2750, 200], [2850, 2800]],
        [[150, 200], [250, 2800], [2850, 200], [2750, 2800]],
        [[200, 250], [200, 2750], [2800, 150], [2800, 2850]],
        [[200, 150], [200, 2850], [2800, 250], [2800, 2750]],

        [[275, 200], [125, 2800], [2725, 200], [2875, 2800]],
        [[125, 200], [275, 2800], [2875, 200], [2725, 2800]],
        [[200, 275], [200, 2725], [2800, 125], [2800, 2875]],
        [[200, 125], [200, 2875], [2800, 275], [2800, 2725]],

        [[200, 200], [200, 2800], [2800, 200], [2800, 2800]]
    ]

    # 시작 좌표
    pts1 = np.float32(perspective_direction_list[12])

    # 이동할 좌표. (원근감 적용하기)
    pts2 = np.float32(perspective_direction_list[perspective_direction])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    perspective_ref = cv2.warpPerspective(img, M, (3000, 3000))
    perspective_result = cv2.warpPerspective(perspective_result, M, (3000, 3000))

    cv2.imwrite('win2.png', perspective_ref)
    """ ############# (끝) 원근감 적용 ################ """

    """ ############# 바운딩 박스가 이동할 거리 구하고 이동하기  ################ """
    found = False
    found_perspective = False
    before_center_count = 0
    for y in range(0, 3000, 3):
        if found:
            # 좌표 찾았다면 반복문 중단
            break
        for x in range(0, 3000, 3):

            if perspective_ref[int(y), int(x)][0] == 0 and \
                    perspective_ref[int(y), int(x)][1] == 0 and \
                    perspective_ref[int(y), int(x)][2] == 255:
                before_center_count += 1

            if before_center_count == 1:
                before_center_count += 1

            # 점 검출 3번 하기
            elif before_center_count == 3:

                if found == False:
                    # x += 2
                    y += 3

                    perspective_ref[int(y), int(x)] = [255, 255, 255]  # white
                    cv2.imwrite('win3.png', perspective_ref)

                    # 원래 좌표에서 이동한 좌표를 빼기. (음수일 경우 '-' 계산, 양수일 경우 '+' 계산)
                    diff_x = center_x - x
                    diff_y = center_y - y

                    """ x축 계산 """
                    if positive_check(str(diff_x)):
                        print("이동한 중심좌표 x: 좌측으로", diff_y)

                        for xx in range(len(point_x_list)):
                            point_x_list2[xx] = point_x_list2[xx] - diff_x

                    else:
                        print("이동한 중심좌표 x: 우측으로", diff_y)

                        # 음수 -> 양수 변환
                        diff_x = diff_x * -1
                        for xx in range(len(point_x_list)):
                            point_x_list2[xx] = point_x_list2[xx] + diff_x

                    """ y축 계산 """
                    if positive_check(str(diff_y)):
                        print("이동한 중심좌표 y: 아래로", diff_y)

                        for yy in range(len(point_y_list)):
                            point_y_list2[yy] = point_y_list2[yy] - diff_y

                    else:
                        print("이동한 중심좌표 y: 위로", diff_y)

                        # 음수 -> 양수 변환 후 계산
                        diff_y = diff_y * -1

                        for yy in range(len(point_y_list)):
                            point_y_list2[yy] = point_y_list2[yy] + diff_y

                    print("after x:", point_x_list2)
                    print("after y:", point_y_list2)
                    print("save perspective")
                    before_center_count = 0
                    found = True
                    found_perspective = True
                    break
            else:
                before_center_count = 0

    """ ############# (끝) 바운딩 박스가 이동할 거리 구하고 이동하기 ################ """

    if found_perspective is True:
        # 좌표 이동 결과 반환하기
        perspective_result_coords = str(point_x_list2[0]) + "," + str(point_y_list2[0]) + "," + \
                                    str(point_x_list2[1]) + "," + str(point_y_list2[1]) + "," + \
                                    str(point_x_list2[2]) + "," + str(point_y_list2[2]) + "," + \
                                    str(point_x_list2[3]) + "," + str(point_y_list2[3])
    else:
        perspective_result_coords = "delete"

    return perspective_result, perspective_result_coords
    # return flip_result_coords


with open(original_json_path) as json_file:
    json_data = json.load(json_file)
    """라벨JSON파일 받아옴"""

    original_features = json_data["features"]
    """JSON파일은 features란 이름의 리스트안에 모든 내용이 들어가있으므로 features를 꺼내옴"""

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
        perspective_result = perspective(coords, input_image_name, option_perspective)
        print("coord_result:", perspective_result[1])

        # 외곡 성공 할때만 json에 추가하기
        if perspective_result[1] is not "delete":
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
            properties_data['bounds_imcoords'] = perspective_result[1]

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

            print("(" + str(save_count) + ")저장 완료")

            save_count += 1

            #################################################################

            print("new json 라벨링 완료:", str(add_number) + ".png")

            # 입력받은 이미지를 모두 담았다면 다음 입력받은 이미지 조회하기
            if before_image_id is None:
                # add_number += 1
                cv2.imwrite(str(add_number) + '.png', perspective_result[0])
                before_image_id = original_features[int(i)]['properties']['image_id']

            if before_image_id != original_features[int(i)]['properties']['image_id']:
                cv2.imwrite(str(add_number) + '.png', perspective_result[0])
                add_number += 1
                before_image_id = original_features[int(i)]['properties']['image_id']

features['features'] = new_geojson_list
'''마지막으로 해당 properties를 리스트에 넣는다'''

# json 파일 새로 저장
with open(edit_object_location_result_path, 'w', encoding='utf-8') as make_file:
    json.dump(features, make_file, indent="\t")

print("(객체 위치 이동 후 새 json 생성 완료)")
