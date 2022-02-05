import os
import cv2
import numpy as np
from tensorflow as tf
from sklearn as preprocessing

class Generator(tf.keras.utils.Sequence):
    """
    This is the data generator class that defines the data generator objects that will be used in training and testing the model.
    All of the methods are made to initialize data or return data through the __getitem__ method, which is the Keras sequence 
    method for generating batches.
    """

    #DATASET_PATH is the training directory or the testing directory, not the directory that contains both
    def init(self, DATASET_PATH, BATCH_SIZE = 64, image_min_side = 50):
        #size of the batches that will be generated
        self.batch_size = BATCH_SIZE
        #if the image's smalles side is smaller than this, it will be enarged while keeping it's aspect ratio
        self.image_min_side = image_min_side
        #saving image paths and labels during initialization
        self.load_image_paths_labels(DATASET_PATH)
    
    def load_image_paths_and_labels(self, DATASET_PATH):
        """
        This is used to load a list of image paths and a list of their labels.
        This information will be saved to the object during initialization.
        """
        
        #list of paths of class directories within image directory
        classes = os.listdir(DATASET_PATH)
        #creation of LabelBinarizer object, 
        lb = preprocessing.LabelBinarizer()
        #fitting LabelBinarizer to current classes
        lb.fit(classes)

        #creating lists for image paths and label
        self.image_paths = []
        self.image_labels = []
        
        #iterating through each class
        for class_name in classes:
            #path for the current class
            class_path = os.path.join(DATASET_PATH, class_name)
            #iterating through each image in the class
            for image_file_name in os.listdir(class_path):
                #adding the image path
                self.image_paths.append(os.path.join(class_path, image_file_name))
                #adding the image label
                self.image_labels.append(class_name)
        #transforming all the labels into numbers
        self.image_labels = np.array(lb.transform(self.image_labels), dtype='float32')
        #check that the image_paths and image_labels are the same, which is necessary becuase each label corresponds with an image
        assert len(self.image_paths) == len(self.image_labels)

    def create_image_groups(self):
        """
        This is used to load the image paths and labels into groups.
        This information will be saved to the model during initialization.
        """
        #shuffle the images
        seed = 4321
        np.random.seed(seed)
        np.random.shuffle(self.image_paths)
        np.random.seed(seed)
        np.random.shuffle(self.image_labels)

        #Divide image_labels and image_paths, based on BATCH_SIZE
        self.image_groups = [[self.image_paths[x % len(self.image_paths)] for x in range(i, i + self.batch_size)] for i in range(0, len(self.image_paths), self.batch_size)]
        self.label_groups = [[self.image_labels[x % len(self.image_labels)] for x in range(i, i + self.batch_size)] for i in range(0, len(self.image_labels), self.batch_size)]

    def resize_image(self, image):
        """
        This method ensures that each image's smallest side is greater than image_min_side.
        It should be noted that this method works with actual images, not image paths
        """
        #getting information about the image
        height, width, color = image.shape
        smallest = self.image_min_side
        #creating a number to multiply both sides by, ensuring that the images smallest side is as large as image_min_side while maintaining image aspect ratio
        if min(height, width) < self.image_min_side:
            multiplier = float(smallest)/height if height < width else float(smallest)/width
        else:
            multiplier = 1
        #multiplying dimensions by multiplier to get new dimensions
        new_height = int(height*multiplier)
        new_width = int(width*multiplier)
        #resizing image
        #for some reason, cv2.resize() expects the tuple to be (width, height)
        new_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return new_image
    
    def load_images(self, image_group):
        """
        This method uses image paths to load images, and ensures that they meet the requirement of image_min_side.
        It also makes the color channel RGB, instead of GRAY, BGRA, or BGR
        """
        #initializing list of images in image_group
        images = []
        #iterating through each image
        for image_path in image_group:
            #loading image through image path
            image = cv2.imread(image_path)
            #using the length of the image shape to find out what type of color channel it uses
            image_shape = len(image.shape)
            #convering to RGB
            if image_shape == 2:
                image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
            elif image_shape == 4:
                image = cv2.cvtColor(image,cv2.COLOR_BGRA2RGB)
            elif image_shape == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #ensuring image meets image_min_side requirement
            transformed_image = self.resize_image(image)
            images.append(transformed_image)
        return images

    def construct_image_batch(self, loaded_image_group):
        """
        This method uses the loaded image_group from load images to create an image batch.
        This is also where images that are smaller than the largest image will have zeros added to it.
        """
        #TODO: Complete this method, then finish generator.py
