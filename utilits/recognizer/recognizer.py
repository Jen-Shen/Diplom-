import os

from io import BytesIO

from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

import numpy as np



def predict(uploaded_image):
    # dimensions of our images.
    img_width, img_height = 150, 150

    # load image you want to make prediction for
    img = image.load_img(uploaded_image, target_size=(img_width, img_height))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255

    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(5))
    model.add(Activation('softmax'))

    model.load_weights('cnn_multiclass.h5')

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    pred = model.predict(img_tensor)

    index_predict = np.argmax(pred[0])

    # if probabilities are spread out and there's no clear winner, return "unsure"
    if pred[0][index_predict] <= 0.5:
        return "unsure"

    dict_labels = {0: 'benchpress', 1: 'hyperext-bench', 2: 'leg-press', 3: 'plyo-box', 4: 'power-rack'}

    return dict_labels[index_predict]


def upload(file_path):
    target = 'media/images'

    if not os.path.isdir(target):
        os.mkdir(target)

    filename = os.path.basename(file_path)

    destination = os.path.join(target, filename)

    with open(file_path, 'rb') as f:
        file_bytes = BytesIO(f.read())

    predicted_class = predict(file_bytes)

    return predicted_class
