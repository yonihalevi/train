import random
from time import time

from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from yoloConvert import *
import numpy as np

class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))


def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size

    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
    transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h

    transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
    transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
    transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
    transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]

    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0, y0), (x1, y1)))

        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])

    plt.imshow(np.array(image))
    plt.waitforbuttonpress(1000)
    plt.close(1)


def show_random_labeling(path, count):
    # Get the annotations
    annotations = [os.path.join(path, x) for x in os.listdir(path) if x[-3:] == "txt"]

    #annotation_file = random.choice(annotations)

    for ann_file in random.choices(annotations,  k = count):

        with open(ann_file, "r") as file:
            annotation_list = file.read().split("\n")[:-1]
            annotation_list = [x.split(" ") for x in annotation_list]
            annotation_list = [[float(y) for y in x] for x in annotation_list]

        # Get the corresponding image file
        image_file = ann_file.replace("annotations", "images").replace("txt", "png")
        assert os.path.exists(image_file)

        # Load the image
        image = Image.open(image_file)
        # Plot the Bounding Box1
        plot_bounding_box(image, annotation_list)

if __name__ == "__main__":
    main()