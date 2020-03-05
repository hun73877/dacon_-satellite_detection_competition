import json
import random
import shutil
from _collections import OrderedDict
import time
import json

"""
재정렬된 데이터를 저장할 경로 생성하기

mkdir reconstruction \
      reconstruction/images

"""

"""" 아래 형식으로 입력하기: 재정렬된 데이터 저장할 json 경로"""
dir_reconstruction_features = 'reconstruction'

""" 아래 형식으로 입력하기: 원본 json / 이미지가 저장된 경로"""
dir_original_features = 'data_images_train_2'

# =========================================================================

# 원본 json 파일 경로
file_original_features = dir_original_features+'/labels.json'

# 원본 이미지 경로
dir_original_images = dir_original_features + '/images/'

# 새로 생성할 json 파일 경로
file_reconstruction_features = dir_reconstruction_features + '/labels_1050_reconstruction.json'

# 이미지 새로 저장할 경로
file_reconstruction_images = dir_reconstruction_features + '/images/'

with open(file_original_features) as json_file:

    """라벨JSON파일 받아옴"""
    json_data = json.load(json_file)  # print(json.dumps(json_data, indent="\t"))

    """JSON파일은 features란 이름의 리스트안에 모든 내용이 들어가있으므로 features를 꺼내옴"""
    original_features = json_data["features"]

# 라벨 데이터 조회하기
def object_count(json_file_path):

    with open(json_file_path) as json_file:
        json_data = json.load(json_file)
        features = json_data["features"]

    # 선박 갯수를 종류별로 세기
    maritime_vessels_count = 0
    aircraft_carrier_count = 0
    oil_tanker_count = 0
    container_count = 0

    for i in range(len(features)):

        if features[i]["properties"]["type_name"] == "maritime vessels":
            maritime_vessels_count = maritime_vessels_count + 1

        elif features[i]["properties"]["type_name"] == "aircraft carrier":
            aircraft_carrier_count = aircraft_carrier_count + 1

        elif features[i]["properties"]["type_name"] == "oil tanker":
            oil_tanker_count = oil_tanker_count + 1

        elif features[i]["properties"]["type_name"] == "container":
            container_count = container_count + 1

    print("-----------------------------------")
    print("(object Count):",json_file_path)
    print("maritime vessels:", maritime_vessels_count)
    print("aircraft carrier:", aircraft_carrier_count)
    print("oil tanker:", oil_tanker_count)
    print("container:", container_count)
    print("total:", maritime_vessels_count + aircraft_carrier_count + oil_tanker_count + container_count)
    print("-----------------------------------")

# json 재정렬 (무작위)
def start_shuffle_json(original_json):

    # json 파일 실행하기
    with open(original_json) as json_file:
        json_data = json.load(json_file)  # print(json.dumps(json_data, indent="\t"))
        original_json = json_data["features"]

    image_id_list = []
    shuffle_parameter = int

    before_image_id = None

    # 원본 이미지 이름을 리스트화
    """
    객체가 없는 이미지는 출력되지 않기 때문에 리스트에도 저장되지 않음
    """
    for i in range(len(original_json)):

        if before_image_id is None:
            split = str(original_json[int(i)]["properties"]["image_id"]).split(".")
            image_id_list.append(str(split[0]))
            before_image_id = original_json[int(i)]["properties"]["image_id"]

        if before_image_id != original_json[i]["properties"]["image_id"]:
            split = str(original_json[int(i)]["properties"]["image_id"]).split(".")
            image_id_list.append(str(split[0]))
            before_image_id = original_json[int(i)]["properties"]["image_id"]


    # 리스트 순서 섞기
    random.shuffle(image_id_list)

    shuffle_parameter = str()

    count = 1

    # reconstruction_json() 메소드로 전달하기 위해 값 가공하기
    for i in range(len(image_id_list)):

        if i == 0:
            shuffle_parameter = str(image_id_list[i])

        else:
            shuffle_parameter = str(shuffle_parameter) + " " + str(image_id_list[i])

        count += 1

    # json 재정렬 시작
    reconstruction_json(str(shuffle_parameter))

# json 재정렬 하기
def reconstruction_json(image_number):

    if not image_number is None:

        # 재정렬 할 이미지 번호 입력받기
        split_result = image_number.split(" ")

        # top/feature/(json array)
        new_geojson_list = []

        # features 배열 계층
        features = OrderedDict()

        # 새로 정렬할 이미지 번호
        new_reconstruction_image_number = 0

        # 입력 이미지의 json 데이터 조회하기
        for i in range(len(split_result)):

            # 첫 번 째 이미지 번호의 json 데이터 조회하기
            for j in range(len(original_features)):

                # 해당 이미지 번호에 포함된 모든 선박 라벨 데이터를 json list 에 추가하기
                if original_features[j]["properties"]["image_id"] == split_result[i] + ".png":

                    # top/feature/properties/(data)
                    properties_data = OrderedDict()
                    '''properties 내부에 데이터 저장할 json'''

                    # top/feature/properties
                    properties = OrderedDict()
                    '''properties 계층이 될 JSON'''

                    # top/feature/properties/bounds_imcoords(선박 좌표)
                    properties_data['bounds_imcoords'] = original_features[int(j)]["properties"]["bounds_imcoords"]

                    # top/feature/properties/image_id(재정렬된 이미지 번호)
                    properties_data['image_id'] = str(new_reconstruction_image_number) + '.png'

                    # top/feature/properties/type_id(클래스 번호)
                    properties_data['type_id'] = original_features[int(j)]["properties"]["type_id"]

                    # top/feature/properties/type_name(선박 이름)
                    properties_data['type_name'] = original_features[int(j)]["properties"]["type_name"]

                    # top/feature/properties/original_image_id(원본 이미지 번호)
                    properties_data["original_image_id"] = original_features[int(j)]["properties"]["image_id"]

                    # top/feature/properties/original_label_index(원본 라벨링 인덱스 번호)
                    properties_data["original_label_index"] = j

                    properties['properties'] = properties_data
                    '''위에서 생성된 요소를 properties에 넣는다'''

                    # 재정렬 된 이미지 번호, 선박 이름 값 조회
                    print("image_id[" + str(j) + "]:",original_features[j]["properties"]["image_id"],"/ type_name:",original_features[int(j)]["properties"]["type_name"])

                    # features 배열 계층에 추가할 인덱스
                    new_geojson_list.append(properties)

            # 입력받은 이미지의 object 데이터를 모두 담았다면 다음 입력받은 이미지 조회하기
            new_reconstruction_image_number += 1

        features['features'] = new_geojson_list
        '''마지막으로 해당 properties를 리스트에 넣는다'''

        # json 파일 새로 저장
        with open(file_reconstruction_features, 'w', encoding='utf-8') as make_file:
            json.dump(features, make_file, indent="\t")

        print("(재정렬 후 새로운 json 생성 완료)")
        object_count(file_reconstruction_features)

        # # 저장한 파일 출력하기
        # with open(file_reconstruction_features, 'r') as f:
        #     features = json.load(f)
        #
        # print(json.dumps(features, indent="\t"))

def copy_n_reconstruction_image(reconstruction_features):

    """
        :param reconstruction_features
            재정렬된 json 파일 경로 입력하기
    """

    # 1. 재정렬된 json 파일의 original_image_id(원본 이미지 번호) 조회하기
    with open(reconstruction_features) as json_file:

        """라벨JSON파일 받아옴"""
        json_data = json.load(json_file)  # print(json.dumps(json_data, indent="\t"))

        """JSON파일은 features란 이름의 리스트안에 모든 내용이 들어가있으므로 features를 꺼내옴"""
        reconstruction_features = json_data["features"]

    image_count = 0
    before_image_count = None
    # 이미지 총 개수 세어서 저장된 이미지 수와 차이 확인하기
    for i in range(len(original_features)):

        if before_image_count is None:
            before_image_count = original_features[i]["properties"]["image_id"]
            image_count+=1

        elif before_image_count != original_features[i]["properties"]["image_id"]:
            before_image_count = original_features[i]["properties"]["image_id"]
            image_count+=1

    # 같은 이미지가 중복 저장되지 않게 하기
    before_image_id = None

    save_count = 0

    # 원본 이미지 가져와서 저장하기
    # todo: json에 라벨 데이터가 없는 이미지는 복사되지 않음.
    #  if 순수 2차 데이터 2767장을 재정렬 & 저장할 시에 -121장 누락되며, 총 2646장 복사됨 (정상임)
    for i in range(len(reconstruction_features)):

        if before_image_id is None:

            # 재렬령된 번호로 새로 저장하기
            shutil.copy(dir_original_images + reconstruction_features[int(i)]["properties"]["original_image_id"], # 원본 이미지 경로
                        file_reconstruction_images + reconstruction_features[int(i)]["properties"]["image_id"])  # 새로 이미지 저장할 경로

            # 재정렬된 이미지 번호 확인하기
            print("(이미지 저장 완료)", dir_original_images + reconstruction_features[int(i)]["properties"]["original_image_id"] + '가',
                  file_reconstruction_images + reconstruction_features[int(i)]["properties"]["image_id"] + "로 재정렬 됨 ")

            before_image_id = reconstruction_features[int(i)]["properties"]["image_id"]
            save_count += 1

        if before_image_id != reconstruction_features[i]["properties"]["image_id"]:

            # 재렬령된 번호로 새로 저장하기
            shutil.copy(dir_original_images + reconstruction_features[int(i)]["properties"]["original_image_id"], # 원본 이미지 경로
                        file_reconstruction_images + reconstruction_features[int(i)]["properties"]["image_id"])  # 새로 이미지 저장할 경로

            # 재정렬된 이미지 번호 확인하기
            print("(이미지 저장 완료)", dir_original_images + reconstruction_features[int(i)]["properties"]["original_image_id"] + '가',
                  file_reconstruction_images + reconstruction_features[int(i)]["properties"]["image_id"] + "로 재정렬 됨 ")

            before_image_id = reconstruction_features[int(i)]["properties"]["image_id"]
            save_count += 1


    print("저장 완료")
    print("save_count:",save_count)
    print("total_image_count:",image_count)
    print("none json data로 인해 누락된 이미지 수(정상임):",int(image_count) - int(save_count))

    print("save_path:",file_reconstruction_images)



def main():

    print("저장 경로: ",dir_reconstruction_features)
    object_count(file_original_features)

    while True:

        print("1: json 재정렬_직접 입력(이미지 자동 저장) / 2: json 재정렬_무작위 / 3: 이미지 저장하기 / 4: 이미지 번호 검색 / 5: 클래스 번호 검색 / q: 종료")

        input_menu_number = input('> ')

        if input_menu_number == 'q' or input_menu_number == 'Q' or input_menu_number == 'ㅂ':
            break

        elif input_menu_number == '1':

            print("재정렬 할 이미지 번호 입력")

            search_image_number = input('>>>> ')

            print("저장 중")
            
            # json 재정렬 하기
            reconstruction_json(str(search_image_number))

            # 재정렬된 json 참고해서 이미지 새로 생성하기
            copy_n_reconstruction_image(file_reconstruction_features)

        elif input_menu_number == '2':
            print("재정렬 될 데이터 수: ")
            object_count(file_original_features)

            search_image_number = input('진행: y / 취소: n >>>> ')

            if search_image_number == 'y':

                # 무작위 재정렬 하기
                start_shuffle_json(file_original_features)

            else:
                print("취소됨")

        elif input_menu_number == '3':
            print("저장할 데이터: ")
            object_count(file_reconstruction_features)

            search_image_number = input('진행: y / 취소: n  >>>> ')

            if search_image_number == 'y':
                print("저장 중")
                copy_n_reconstruction_image(file_reconstruction_features)

            else:
                print("취소됨")

        elif input_menu_number == '4':

            print("조회할 이미지 번호 입력")

            search_image_number = input('>>>> ')

            if search_image_number.isdecimal():

                # 입력한 이미지의 라벨링 갯수 세기
                label_count = 1

                # 입력한 이미지에 저장된 모든 선박 이름 불러오기
                for i in range(len(original_features)):

                    if original_features[i]["properties"]["image_id"] == str(search_image_number) + ".png":

                        if not original_features[i]["properties"]["image_id"] is None:

                            # 입력한 이미지 번호가 일치할 때 선박 종류 출력하기
                            print(original_features[i]["properties"]["image_id"] + "[" + str(i) + "]: " + original_features[int(i)]["properties"]["type_name"], "(count: " + str(label_count) + ")")

        elif input_menu_number == '5':

            print("조회할 클래스 번호 입력")
            print("1: container / 2: oil tanker / 3: aircraft carrier / 4: maritime vessels")

            search_image_number = input('>>>> ')

            # 이미지당 객체수 세기
            label_count = 0
            
            # 검색된 총 객체수 세기
            total_object_count = 0
            
            # 같은 이미지가 중복 출력되지 않게 하기
            before_image_id = None

            # 입력한 이미지에 저장된 모든 선박 이름 불러오기
            for i in range(len(original_features)):

                if int(original_features[i]["properties"]["type_id"]) == int(search_image_number):

                    total_object_count += 1

                    if before_image_id is None:

                        label_count += 1

                        print(original_features[i]["properties"]["type_name"] + "[" + str(i) + "]: " +
                              original_features[int(i)]["properties"]["image_id"],
                              "(count: " + str(label_count) + ")")

                        before_image_id = original_features[i]["properties"]["image_id"]

                    if before_image_id != original_features[i]["properties"]["image_id"]:

                        label_count += 1

                        # 입력한 클래스 번호가 일치하면 이미지 번호 출력하기
                        print(original_features[i]["properties"]["type_name"] + "[" + str(i) + "]: " +
                              original_features[int(i)]["properties"]["image_id"],
                              "(count: " + str(label_count) + ")")

                        before_image_id = original_features[i]["properties"]["image_id"]

                        if before_image_id == original_features[i]["properties"]["image_id"]:

                            label_count = 0



            print("조회한 클래스 번호: " + search_image_number + " / Total: ",total_object_count)


if __name__ == "__main__":
	main()
