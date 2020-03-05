""" 이미지 외곡 적용

사용 방법
1. 좌표 외곡 함수 선언하기
    perspective_coords()

2. 함수에 파라미터 입력하기 _ <외곡 방향 설정은 아래 참고 '외곡 방향 설정 모음'>
    perspective_coords("객체 좌표", "이미지 이름_00.png", "외곡 방향 입력")

    외곡 방향 설정 모음

    (0): 상 25 px / (1): 하 25 px
    (2): 좌 25 px / (3): 우 25 px

    (4): 상 50 px / (5): 하 50 px
    (6): 좌 50 px / (7): 우 50 px

    (8): 상 75 px  / (9): 하 75 px
    (10): 좌 75 px / (11): 우 75 px

3. 외곡 결과 리턴 받기
    result_perspective_result = perspective("좌표", input_image_name, option_perspective)

    perspective_result[0]: 외곡된 이미지
    perspective_result[1]: 이동한 좌표

4. 외곡 실패 할수도 있음. 실패할 시 문자열 delete 반환함.
   아래와 같이 예외처리 하기

    if perspective_result[1] is not "delete":
        print(" 'delete'가 반환되지 않을때만 json에 저장하기")


5. 좌표 외곡 후 외곡 이미지 저장하기

    if perspective_result[1] is not "delete":
        print(" 'delete'가 반환되지 않을때만 json에 저장하기")

        # 외곡된 이미지 저장하기
        result_perspective_image = perspective_coords(input_image_name, option_perspective)

"""


import cv2
import numpy as np

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


def perspective_coords(coords_str, image_name, perspective_direction):
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

    before_perspective_coords = coords_str.split(",")

    # 이동 결과를 적용할 바운딩 박스
    point_x_list2 = [float(before_perspective_coords[0]), float(before_perspective_coords[2]),
                     float(before_perspective_coords[4]), float(before_perspective_coords[6])]
    point_y_list2 = [float(before_perspective_coords[1]), float(before_perspective_coords[3]),
                     float(before_perspective_coords[5]), float(before_perspective_coords[7])]

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
    # print("이동 전 중심 좌표 x:", int(center_x))
    # print("이동 전 중심 좌표 y:", int(center_y))
    # cv2.imwrite('win.png', img)
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

    # cv2.imwrite('win2.png', perspective_ref)
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

                    # 원래 좌표에서 이동한 좌표를 빼기. (음수일 경우 '-' 계산, 양수일 경우 '+' 계산)
                    diff_x = center_x - x
                    diff_y = center_y - y

                    """ x축 계산 """
                    if positive_check(str(diff_x)):
                        # print("이동한 중심좌표 x: 좌측으로", diff_y)

                        for xx in range(len(point_x_list)):
                            point_x_list2[xx] = point_x_list2[xx] - diff_x

                    else:
                        # print("이동한 중심좌표 x: 우측으로", diff_y)
                        # 음수 -> 양수 변환
                        diff_x = diff_x * -1
                        for xx in range(len(point_x_list)):
                            point_x_list2[xx] = point_x_list2[xx] + diff_x

                    """ y축 계산 """
                    if positive_check(str(diff_y)):
                        # print("이동한 중심좌표 y: 아래로", diff_y)

                        for yy in range(len(point_y_list)):
                            point_y_list2[yy] = point_y_list2[yy] - diff_y

                    else:
                        # print("이동한 중심좌표 y: 위로", diff_y)

                        # 음수 -> 양수 변환 후 계산
                        diff_y = diff_y * -1

                        for yy in range(len(point_y_list)):
                            point_y_list2[yy] = point_y_list2[yy] + diff_y

                    # print("after x:", point_x_list2)
                    # print("after y:", point_y_list2)
                    print("done perspective coord")
                    before_center_count = 0
                    found = True
                    found_perspective = True
                    break
            else:
                before_center_count = 0

    """ ############# (끝) 바운딩 박스가 이동할 거리 구하고 이동하기 ################ """

    # 좌표 이동 결과 반환하기
    if found_perspective is True:
        perspective_result_coords = str(point_x_list2[0]) + "," + str(point_y_list2[0]) + "," + \
                                    str(point_x_list2[1]) + "," + str(point_y_list2[1]) + "," + \
                                    str(point_x_list2[2]) + "," + str(point_y_list2[2]) + "," + \
                                    str(point_x_list2[3]) + "," + str(point_y_list2[3])

    # 좌표 이동 실패할 시 delete 반환
    else:
        perspective_result_coords = "delete"

    return perspective_result_coords



def perspective_images(image_name, perspective_direction):

    """
    :param image_name: 이미지 이름
    :param perspective_direction: 외곡 방향
    :return: 외곡된 이미지 반환
    """

    """ ############# 이미지 원근감 적용 ################ """
    img = cv2.imread(image_path + image_name)

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
    perspective_result = cv2.warpPerspective(img, M, (3000, 3000))

    print("done perspective image")

    """ ############# (끝) 이미지 원근감 적용 ################ """
    return perspective_result


# 새 이미지 저장하기, 좌표 이동 결과 반환 받기
result_perspective_coords = perspective_coords("좌표", input_image_name, option_perspective)
print("coord_result:", result_perspective_coords)

# 외곡 성공 할때만 이동한 좌표를 json에 추가하기
if perspective_coords is not "delete":
    print(" 'delete'가 반환되지 않을때만 이동한 좌표를 json에 적용하기")
    
    # 외곡된 이미지 저장하기
    result_perspective_image = perspective_coords(input_image_name, option_perspective)
