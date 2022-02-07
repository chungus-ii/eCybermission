import os
import tensorflow as tf
from model import FCN_model, FCN_Dense_model
from generator import Generator

def train(model, train_generator, test_generator, epochs = 30, directory_path, modeltype):
    #compiling the model
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    #creating directory for the models, but only if it does not already exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    model_path = os.path.join(directory_path, f'(Model:{modeltype})_(Epoch:{epoch:02d})_(Loss:{loss:.2f})_(Accuracy:{acc:.2f}).h5')
