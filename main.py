from yoloConvert import *
from trainValidateTest import *
from annotationTester import *
import argparse



def main():
    parser = argparse.ArgumentParser(description='convert to format, orgenize in train/test/vld folders')
    parser.add_argument('--clean', help='clean all artifacts. leave only original images and xml')
    parser.add_argument('--format', help='create txt file per image out of the original xml. the txt will bein yolo format')
    parser.add_argument('--show', help='shows 10 labled images iwth bounding boxes as a test')
    parser.add_argument('--prep', help='moves images and txt files into training testing and validation sets')
    parser.add_argument('-tr', help="percentage of training set", default='0.8')
    parser.add_argument('-ts', help="percentage of testing set", default='0.1')
    parser.add_argument('-vl', help="percentage of validation set", default='0.1')
    args = parser.parse_args()

    #set the annotation directory location
    path = '../Road_Sign_Dataset'

    if args.clean:
        # Move the splits into their folders
        shutil.rmtree(path + '/images/train', True)
        shutil.rmtree(path + '/images/val/', True)
        shutil.rmtree(path + '/images/test/', True)
        shutil.rmtree(path + '/labels/train/', True)
        shutil.rmtree(path + '/labels/val/', True)
        shutil.rmtree(path + '/labels/test/', True)
        shutil.rmtree(path + '/labels/test/', True)

    if args.format:
        convet_xml_to_lables(path+'/annotations')

    if args.show:
        show_random_labeling(path+'/annotations', int(args.show))

    if args.prep:
        split_and_move_dataset(path, float(args.tr), float(args.ts), float(args.vl))


if __name__ == "__main__":
    main()
