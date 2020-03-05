"""
todo: 이미지 상하, 좌우, 상하좌우 반전

flip_result = flip_image_n_object("이미지 좌표", "원본 이미지 이름", "반전 옵션")

flip_result[0]:
flip_result[1]:
"""

import cv2

"""
(flip_option)
0: 상하 반전
1: 좌우 반전
-1: 상하좌우 반전
"""
flip_option = -1


def flip_image_n_object(coords_str, image_id, flip_direction):
    """
    :param coords_str: 반전 할 객체의 좌표
    :param image_id: 반전 할 이미지 이름
    :param flip_direction: 반전할 방향 (0: 상하 반전 / 1: 좌우 반전 / -1: 상하좌우 반전)
    :return: 반전된 이미지, 반전된 객체의 좌표 반환함
    """

    before_flip_coords = coords_str.split(",")

    originalImage = cv2.imread(image_id)

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

    ############# 이미지, 좌표 반전 ################
    # flip_result_img = None
    if flip_direction is 0:
        # print("상하 반전")
        flip_result_img = cv2.flip(originalImage, flip_direction) # 0

        for i in range(len(point_y_list)):
            point_y_list[i] = 3000 - float(point_y_list[i])

    elif flip_direction is 1:
        # print("좌우 반전")
        flip_result_img = cv2.flip(originalImage, flip_direction) # 1

        for i in range(len(point_y_list)):
            point_x_list[i] = 3000 - float(point_x_list[i])

    elif flip_direction is -1:
        # print("상하좌우 반전")
        flip_result_img = cv2.flip(originalImage, -1) # -1

        for i in range(len(point_x_list)):
            point_x_list[i] = 3000 - float(point_x_list[i])

        for i in range(len(point_y_list)):
            point_y_list[i] = 3000 - float(point_y_list[i])

    # cv2.imwrite("flip.png", flip_result_img)

    ############# (끝) 이미지, 좌표 반전 ################

    # 좌표 이동 결과 반환하기
    flip_result_coords = str(point_x_list[0]) + "," + str(point_y_list[0]) + "," + \
                           str(point_x_list[1]) + "," + str(point_y_list[1]) + "," + \
                           str(point_x_list[2]) + "," + str(point_y_list[2]) + "," + \
                           str(point_x_list[3]) + "," + str(point_y_list[3])

    return flip_result_img, flip_result_coords
    # return flip_result_coords

# todo: 아래 반전 메소드 실행 후 결과값 반환하기
# flip_result[0]: 반전 된 이미지
# flip_result[1]: 반전 된 좌표
flip_result = flip_image_n_object("이미지 좌표", "원본 이미지 이름", "반전 옵션")
