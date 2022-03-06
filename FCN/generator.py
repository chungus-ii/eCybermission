import os, cv2
import numpy as np
import tensorflow as tf
from sklearn import preprocessing

class Generator(tf.keras.utils.Sequence):
    """
    This is the data generator class that defines the data generator objects that will be used in training and testing the model.
    The purpose of the generator is to give the images in batches, rather than loading them all into batches.
    All of the methods are made to initialize data or return data through the __getitem__ method, which is the Keras sequence 
    method for generating batches.
    """

    #DATASET_PATH is the training directory or the testing directory, not the directory that contains both
    def __init__(self, DATASET_PATH, BATCH_SIZE = 2, image_min_side = 50):
        #size of the batches that will be generated
        self.batch_size = BATCH_SIZE
        #if the image's smalles side is smaller than this, it will be enarged while keeping it's aspect ratio
        self.image_min_side = image_min_side
        #saving image paths and labels during initialization
        ABSOLUTE_DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', '..', DATASET_PATH)
        print(f'The Absolute Dataset Path is: {ABSOLUTE_DATASET_PATH}')
        self.load_image_paths_and_labels(ABSOLUTE_DATASET_PATH)
        self.create_image_groups()

    def load_image_paths_and_labels(self, ABSOLUTE_DATASET_PATH):
        """
        This is used to load a list of image paths and a list of their labels.
        This information will be saved to the object during initialization.
        """

        #list of paths of class directories within image directory
        classes = os.listdir(ABSOLUTE_DATASET_PATH)

        #creating lists for image paths and label
        self.image_paths = []
        self.image_labels = []

        #iterating through each class
        for class_name in classes:
            if class_name == 'popular':
                label = 1
            if class_name == 'not_popular':
                label = 0
            if class_name == 'medium':
                label = 0.5
            if class_name == 'low_medium':
                label = 0.25
            if class_name == 'high_medium':
                label = 0.75
            #path for the current class
            class_path = os.path.join(ABSOLUTE_DATASET_PATH, class_name)
            #iterating through each image in the class
            for image_file_name in os.listdir(class_path):
                #adding the image path
                self.image_paths.append(os.path.join(class_path, image_file_name))
                #adding the image label
                self.image_labels.append(label)
        #transforming all the labels into numbers
        self.image_labels = np.array(self.image_labels, dtype='float32')
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
        This is also where images that are smaller than the largest image will have zeros added to fit the model.
        """
        #get the shape of the largest image
        largest_shape = tuple(max(image.shape[x] for image in loaded_image_group) for x in range(3))
        #create an image batch object, with each image being an empty set of pixels the size of the largest image
        image_batch = np.zeros((self.batch_size,) + largest_shape, dtype='float32')
        #iterate through image_group, using enumerate to access both the image and the index of the image, i.e., (4, '4th_image')
        for index, image in enumerate(loaded_image_group):
            """
            Filling the image in the batch from the upper left part of image, replacing the empty pixels with pixels from the 
            actual image. The model will learn to ignore the extra empty space.
            """
            image_batch[index, :image.shape[0], :image.shape[1], :image.shape[2]] = image
        return image_batch

    def __len__(self):
        """
        The number of batches in the generator.
        This will be called for the len() function
        """
        return len(self.image_groups)

    def __getitem__(self, index):
        """
        This is the Keras sequence method for generating batches, all of the code builds up to this point
        """
        #getting 1 group of images and it's labels
        image_group = self.image_groups[index]
        label_group = self.label_groups[index]
        #converting the image group (image paths) into images
        loaded_images = self.load_images(image_group)
        #creating the image batch and aerating the images
        image_batch = self.construct_image_batch(loaded_images)
        #The culmination of all the work put into this file!
        return np.array(image_batch), np.array(label_group)