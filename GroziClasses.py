import shutil
import os

class_img_path = "../grozi/classes/images"

def build_classes():
    classes = dict()
    files = [ os.path.join(class_img_path, f) for f in os.listdir(class_img_path) if x[-3:] == "jpg"]

