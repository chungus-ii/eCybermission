import tensorflow as tf
import numpy as np
from dataset import split
from generator import Generator
from model import FCN_model, FCN_Dense_model
from train import train
from PIL import Image
import base64, os, sys, shutil, io, re, cv2

class Run():
    def create_FCN_model(self):
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
        model_history = train(model=model, train_generator=train_generator, test_generator=test_generator, direct_path='eCybermission/trained_models', modeltype='FCN', epochs=2)
        print('Completed Training, Model Saved.')

    def create_FCN_Dense_model(self):
        #creating a dataset
        split()
        print('Finished Creating Dataset...')
        #compiling model
        model = FCN_Dense_model()
        print('Model created...')
        #creating generator objects
        train_generator = Generator('eCybermission/dataset/training', BATCH_SIZE=2)
        test_generator = Generator('eCybermission/dataset/testing', BATCH_SIZE=2)
        print('Data generators created...')
        print('Training...')
        #training and saving model
        model_history = train(model=model, train_generator=train_generator, test_generator=test_generator, direct_path='eCybermission/trained_models', modeltype='FCN-Dense-Layers', epochs=10)
        print('Completed Training, Model Saved.')

    def use_model(self, base64string='', MODEL_PATH='', model_type='FCN-Dense-Layers', IMAGE_DIRECTORY_PATH='eCybermission/FCN/images'):
        #deleting replacing any earlier images that were used
        TRUE_IMAGE_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), '..', '..', IMAGE_DIRECTORY_PATH)
        if os.path.exists(IMAGE_DIRECTORY_PATH):
            shutil.rmtree(IMAGE_DIRECTORY_PATH)
        #creating image directory
        os.makedirs(IMAGE_DIRECTORY_PATH)
        #saving base64 string as image and putting it the correct location
        image_path = os.path.join(IMAGE_DIRECTORY_PATH, 'info-image.jpg')
        #image_data = base64.b64decode(str(base64string))
        #img = Image.open(io.BytesIO(image_data))
        #img.save(image_path, 'jpeg')
        if not isinstance(base64string, str):
            if ',' in base64string['content']:
                base64string = base64string['content'].split(',')[1]
            else:
                base64string = base64string['content']
        else:
            if ',' in base64string:
                base64string = base64string.split(',')[1]
        data = re.sub(rb'[^a-zA-Z0-9%s]+' % b'+/', b'', base64string.encode("utf-8"))  # normalize
        missing_padding = len(data) % 4
        if missing_padding:
            data += b'='* (4 - missing_padding)
        image_data = base64.b64decode(data, b'+/')
        img = Image.open(io.BytesIO(image_data))
        if img.mode == 'RGBA':
            img = img.convert('RGB')
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
        model.load_weights(MODEL_PATH)
        print('Model restored...')
        #making predictions
        predictions = (model.predict(ready_to_use)).tolist()
        print('Predictions made, returning predictions.')
        print(predictions)
        shutil.rmtree(IMAGE_DIRECTORY_PATH)
        return predictions[0]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Improper Usage: must be 2 arguments.')
    run = Run()
    if sys.argv[1] == 'FCN':
        run.create_FCN_model()
        sys.exit('FCN Model created, trained, tested, and saved.')
    elif sys.argv[1] == 'Dense':
        run.create_FCN_Dense_model()
        sys.exit('FCN Dense Model created, trained, tested, and saved.')
    sys.exit('Improper Usage: argument must be FCN or Dense')