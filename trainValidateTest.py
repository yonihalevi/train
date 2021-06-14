import os
import shutil

from sklearn.model_selection import train_test_split


def move_files_to_folder(list_of_files, destination_folder):
    """Utility function to move images"""

    for f in list_of_files:
        try:
            shutil.copy(f, destination_folder)
        except:
            print(f)
            assert False


def split_and_move_dataset(path, train, test, validate):
    """ Read images and annotations """
    images = [os.path.join(path, 'images', x) for x in os.listdir(path + '/images') if x[-3:] == 'png']
    annotations = [os.path.join(path, 'annotations', x) for x in os.listdir(path + '/annotations') if x[-3:] == 'txt']

    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size=test+validate, random_state=1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size=(float(test)/(test+validate)), random_state=1)

    os.mkdir(path + '/images/train')
    os.mkdir( path + '/images/val/')
    os.mkdir( path + '/images/test/')
    os.mkdir( path + '/labels/train/')
    os.mkdir( path + '/labels/val/')
    os.mkdir( path + '/labels/test/')

    # Move the splits into their folders
    move_files_to_folder(train_images, path+'/images/train')
    move_files_to_folder(val_images, path+'/images/val/')
    move_files_to_folder(test_images, path+'/images/test/')
    move_files_to_folder(train_annotations, path+'/labels/train/')
    move_files_to_folder(val_annotations, path+'/labels/val/')
    move_files_to_folder(test_annotations, path+'/labels/test/')

