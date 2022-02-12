from dataset import split
from generator import Generator
from model import FCN_model, FCN_Dense_model
from train import train
import base64
import tensorflow as tf
from tensorflow import keras
import os

def create_FCN_model():
    DATASET_PATH = 'eCybermission/dataset'
    split()
    print('Finished Creating Dataset...')
    model = FCN_model()
    train_generator = Generator('eCybermission/dataset/training')
    test_generator = Generator('eCybermission/dataset/testing')
    print('Training...')
    model_history = train(model, train_generator, test_generator, epochs=30, 'eCybermission/trained_models', modeltype='FCN')
    print('Completed Training, Model Saved.')

def create_FCN_Dense_model():
    DATASET_PATH = 'eCybermission/dataset'
    split()
    print('Finished Creating Dataset...')
    model = FCN_Dense_model()
    train_generator = Generator('eCybermission/dataset/training')
    test_generator = Generator('eCybermission/dataset/testing')
    print('Training...')
    model_history = train(model, train_generator, test_generator, epochs=30, 'eCybermission/trained_models', modeltype='FCN-Dense-Layers')
    print('Completed Training, Model Saved.')

def use_model(base64string, IMAGE_DIRECTORY_PATH='eCybermission/FCN/images'):
    if os.path.exists(IMAGE_DIRECTORY_PATH):
        shutil.rmtree(IMAGE_DIRECTORY_PATH)
    os.makedirs(IMAGE_DIRECTORY_PATH)
    image_path = os.path.join(IMAGE_DIRECTORY_PATH, 'info-image.jpg')
    image_data = base64.decodebytes(base64string)
    img = Image.open(io.BytesIO(image_data))
    img.save(image_path, 'jpeg')
    """
    Finished saving the base64 string as an image file.
    """
    print("Image saved...")
    #Putting the image into an image batch
    image_group = []
    image_group.append(cv2.imread(image_path)[:,:,::-1])
    BATCH_SIZE = len(image_group)
    largest_shape = tuple(max(image.shape[x] for image in image_group) for x in range(3))
    image_batch = np.zeros((BATCH_SIZE,) + largest_shape, dtype='float32')
    for index, image in enumerate(image_group):
        image_batch[index, :image.shape[0], :image.shape[1], :image.shape[2]] = image
    """
    At this point, the image batch is prepared, and ready to be put into the model.
    """
    print("Image batch created...")
    #TODO: finish making prediction with model