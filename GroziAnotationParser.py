import sys

import pyexcel_ods3 as ods
import cv2


data = ods.read_data("../grozi/classes/grozi.ods")
sheet = data['grozi']


def get_class_name_from_id(classid):
    return str(classid)


def get_bboxes_for_image(imageid):

    with open("classes.txt") as f:
        classes = {int(line[:line.find(" ")].strip()): line[line.find(" "):].strip() for line in f}

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
            boxes[item[0]]['label'] = f"{get_class_name_from_id(item[1])}:{classes[item[1]]}"

    return boxes


def display_bboxes_on_image(imageid):

    img = cv2.imread(f'../grozi/src/3264/{imageid}.jpg')
    bboxes = get_bboxes_for_image(imageid)
    img_height = img.shape[0]
    img_width = img.shape[1]

    for box in bboxes.values():

        label_size, base_line = cv2.getTextSize(box['label'], cv2.FONT_HERSHEY_SIMPLEX, 2, 1)
        left = round(box['lx'] * img_width)
        right = round(box['rx'] * img_width)
        top = round(box['ty'] * img_height)
        bottom = round(box['by'] * img_height)

        cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), cv2.LINE_4)
        cv2.rectangle(img, (left, top - round(1.5 * label_size[1])),
                      (left + round(1.5 * label_size[0]), top + base_line),
                      (255, 0, 0), cv2.FILLED)
        cv2.putText(img, box['label'], (left, top), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=5)

    scale_percent = 30  # percent of original size
    width = int(img_width * scale_percent / 100.0)
    height = int(img_height * scale_percent / 100.0)
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
