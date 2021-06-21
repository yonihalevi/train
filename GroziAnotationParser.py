import sys
import numpy as np

import pyexcel_ods3 as ods
import cv2


data = ods.read_data("../grozi/classes/grozi.ods")
sheet = data['grozi']

def get_class_name_from_id(classid):
    return str(classid)


def get_bboxes_for_image(imageid):
    boxes = dict()
    for item in sheet[1:]:
        if len(item) > 2 and item[2] == imageid:
            boxes[item[0]] = dict()
            boxes[item[0]]['classid'] = item[1]
            boxes[item[0]]['imageid'] = item[2]
            boxes[item[0]]['lx'] = item[3]
            boxes[item[0]]['rx'] = item[4]
            boxes[item[0]]['ty'] = item[5]
            boxes[item[0]]['by'] = item[6]
            boxes[item[0]]['label'] = f"class type:{get_class_name_from_id(item[1])}"

    return boxes


def display_bboxes_on_image(imageid):

    img = cv2.imread(f'../grozi/src/3264/{imageid}.jpg')
    bboxes = get_bboxes_for_image(imageid)


    for box in bboxes.values():

        labelSize, baseLine = cv2.getTextSize(box['label'], cv2.FONT_HERSHEY_SIMPLEX, 2, 1)
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        left = round(box['lx'] * imgWidth)
        right = round(box['rx'] * imgWidth)
        top = round(box['ty'] * imgHeight)
        bottom = round(box['by'] * imgHeight)

        cv2.rectangle(img, (left, top), (right, bottom), (255,0,0), cv2.LINE_4)
        cv2.rectangle(img, (left, top - round(1.5 * labelSize[1])),
                      (left + round(1.5 * labelSize[0]), top + baseLine),
                      (255,0,0), cv2.FILLED)
        cv2.putText(img, box['label'], (left, top), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=5)


    scale_percent = 30  # percent of original size
    width = int(imgWidth * scale_percent / 100.0)
    height = int(imgHeight * scale_percent / 100.0)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("image", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(imageid):
    display_bboxes_on_image(imageid)


if __name__ == "__main__":
    main(int(sys.argv[1]))



