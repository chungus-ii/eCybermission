import os, cv2, shutil
import numpy as np
import tensorflow as tf

def split(BASE_PATH = 'selfies/', DATASET_PATH = 'dataset/', TRAIN_SIZE = 240, TEST_SIZE = 60):
    """
        This is used to create a directory called dataset
        The final structure of the directory should look like this:
        - dataset
            - training
                - popular
                - not-popular
            - testing
                - popular
                - not-popular
        The dataset/training and dataset/testing directories are the two directories that will be utilized by data generators.
    """
    ABSOLUTE_DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', DATASET_PATH)
    ABSOLUTE_BASE_PATH = os.path.join(os.path.dirname(__file__), '..', BASE_PATH)

    #if dataset exists, remove it to create a new one
    if os.path.exists(ABSOLUTE_DATASET_PATH):
        shutil.rmtree(ABSOLUTE_DATASET_PATH)

    #list of paths of class directories within image directory
    classes = os.listdir(ABSOLUTE_BASE_PATH)

    #new directory for dataset
    os.makedirs(ABSOLUTE_DATASET_PATH)

    #create training set directory inside of dataset directory
    training_directory = os.path.join(ABSOLUTE_DATASET_PATH, 'training')
    os.makedirs(training_directory)

    #create testing directory inside of dataset directory
    testing_directory = os.path.join(ABSOLUTE_DATASET_PATH, 'testing')
    os.makedirs(testing_directory)

    #copying images from image directory into dataset directory
    for class_name in classes:
        print(f"Copying images for {class_name} images...")

        #create directory for current class in testing directory
        class_train = os.path.join(training_directory, class_name)
        os.makedirs(class_train)

        #create directory for current class in training directory
        class_test = os.path.join(testing_directory, class_name)
        os.makedirs(class_test)

        #shuffle the image list before seperation
        class_path = os.path.join(ABSOLUTE_BASE_PATH, class_name)
        class_images_list = os.listdir(class_path)
        np.random.shuffle(class_images_list)

        #It should be noted that each of the classes in the selfies directory has 300 images
        #putting 275 of the images into training set
        for image in class_images_list[:TRAIN_SIZE]:
            shutil.copy2(os.path.join(class_path, image), class_train)

        #putting the next 75 images into the testing set
        for image in class_images_list[TRAIN_SIZE:TRAIN_SIZE+TEST_SIZE]:
            shutil.copy2(os.path.join(class_path, image), class_test)