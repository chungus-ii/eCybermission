import sys
from dataset import split
from generator import Generator
from model import FCN_model, FCN_Dense_model
from train import train

if len(sys.argv) != 2 or len(sys.argv) != 3:
    print('Improper Usage: must enter train or use.')
    sys.exit(1)
if sys.argv[1] == 'train':
    if len(sys.argv) != 2:
        print('Improper Usage: train can not have any additional arguments.')
        sys.exit(1)
    DATASET_PATH = 'eCybermission/dataset'
    split()
    print('Finished Creating Dataset...')
    model = FCN_Dense_model()
    train_generator = Generator('eCybermission/dataset/training')
    test_generator = Generator('eCybermission/dataset/testing')
    print('Training...')
    model_history = train(model, train_generator, test_generator, epochs=30, 'eCybermission/trained_models', modeltype='FCN-Dense-Layers')
    print('Completed Training, Model Saved.')
elif sys.argv[1] == 'use':
    if len(sys.argv) != 3:
        print('Improper Usage: use needs to have 1 additional argument, the path to the model that you want to use.')
        sys.exit(1)
    #TODO: Figure out how to use a saved model, and use it with an image
else:
    print('Improper Usage: must enter train or use.')