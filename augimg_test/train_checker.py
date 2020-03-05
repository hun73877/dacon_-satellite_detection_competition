""" 학습 파일 확인용 """

import sys
import json
from PIL import Image, ImageDraw, ImageFont

image_name = sys.argv[1]

with open('labels.json') as json_file:
    json_data = json.load(json_file)
    features = json_data["features"]

features_list = []
features_name = []

img = Image.open(image_name)

for i in range(len(features)):

    if features[i]['properties']['image_id'] == image_name:

        features_list.append(features[i]['properties']['bounds_imcoords'])
        features_name.append(features[i]['properties']['type_name'])

        print(str(i) +": "+features[i]['properties']['type_name'])



for i in range(len(features_list)):
    featureA = features_list[i]
    listA = featureA.split(",")

    featureB = features_name[i]
    listB = featureB.split(",")

    p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y = float(listA[0]), float(listA[1]), float(listA[2]), float(listA[3]), \
                                             float(listA[4]), float(listA[5]), float(listA[6]), float(listA[7])

    draw = ImageDraw.Draw(img)
    draw.line([(p1x, p1y), (p2x, p2y),
               (p3x, p3y), (p4x, p4y),
               (p1x, p1y)],
              width=3, fill="red")

    font = ImageFont.truetype('arial.ttf', 30)
    draw.text((p1x, p1y), listB[0], fill="yellow", font=font)

img.show()
