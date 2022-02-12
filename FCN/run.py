from dataset import split
from generator import Generator
from model import FCN_model, FCN_Dense_model
from train import train
from PIL import Image
import base64
import tensorflow as tf
import os

def create_FCN_model():
    #creating a dataset
    split()
    print('Finished creating dataset...')
    #compiling model
    model = FCN_model()
    print('Model compiled...')
    #creating generator objects
    train_generator = Generator('eCybermission/dataset/training')
    test_generator = Generator('eCybermission/dataset/testing')
    print('Data generators created...')
    print('Training...')
    #training and saving model
    model_history = train(model=model, train_generator=train_generator, test_generator=test_generator, directory_path='eCybermission/trained_models', modeltype='FCN', epochs=30)
    print('Completed Training, Model Saved.')

def create_FCN_Dense_model():
    #creating a dataset
    split()
    print('Finished Creating Dataset...')
    #compiling model
    model = FCN_Dense_model()
    print('Model compiled...')
    #creating generator objects
    train_generator = Generator('eCybermission/dataset/training')
    test_generator = Generator('eCybermission/dataset/testing')
    print('Data generators created...')
    print('Training...')
    #training and saving model
    model_history = train(model=model, train_generator=train_generator, test_generator=test_generator, directory_path='eCybermission/trained_models', modeltype='FCN-Dense-Layers', epochs=30)
    print('Completed Training, Model Saved.')

def use_model(base64string, MODEL_PATH, model_type, IMAGE_DIRECTORY_PATH='eCybermission/FCN/images'):
    #deleting replacing any earlier images that were used
    if os.path.exists(IMAGE_DIRECTORY_PATH):
        shutil.rmtree(IMAGE_DIRECTORY_PATH)
    #creating image directory
    os.makedirs(IMAGE_DIRECTORY_PATH)
    #saving base64 string as image and putting it the correct location
    image_path = os.path.join(IMAGE_DIRECTORY_PATH, 'info-image.jpg')
    image_data = base64.decodebytes(base64string)
    img = Image.open(io.BytesIO(image_data))
    img.save(image_path, 'jpeg')
    print('Image saved...')
    #Putting the image into an image batch (same method as in generator.py!)
    image_group = []
    image_group.append(cv2.imread(image_path)[:,:,::-1])
    BATCH_SIZE = len(image_group)
    largest_shape = tuple(max(image.shape[x] for image in image_group) for x in range(3))
    image_batch = np.zeros((BATCH_SIZE,) + largest_shape, dtype='float32')
    for index, image in enumerate(image_group):
        image_batch[index, :image.shape[0], :image.shape[1], :image.shape[2]] = image
    ready_to_use = np.array(image_batch)
    print('Image batch created...')
    #create model
    if model_type == 'FCN':
        model = FCN_model()
    elif model_type == 'FCN-Dense-Layers':
        model = FCN_Dense_model()
    print('Model created...')
    #apply weights of saved model to new model (can be done because models share same structure)
    model = load_weights(MODEL_PATH)
    print('Model restored...')
    #making predictions
    predictions = model.predict(ready_to_use)
    print('Predictions made, returning predictions.')
    print(predictions)
    return predictions