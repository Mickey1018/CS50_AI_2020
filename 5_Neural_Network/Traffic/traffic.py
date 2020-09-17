import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow.keras import datasets, layers, models

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy.ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    path = data_dir

    # os.listdir() method returns the list of all files
    # and directories in the specified path.
    # loop for each file or directory in data_dir
    for file_dir in os.listdir(path):

        # os.path.join() concatenates various path components
        # with exactly one directory separator (‘/’)
        joined_path = os.path.join(path, file_dir)

        # os.path.isdir() checks whether the specified path
        # is an existing directory or not
        # and return True or False
        if os.path.isdir(joined_path):
            print(f"Loading images from {joined_path}...")

            # list out all files in the joined path
            # and loop for each image
            for image in os.listdir(joined_path):

                # join image to the joined_path
                image_path = os.path.join(joined_path, image)

                try:
                    # cv2.imread() method loads an image from the specified file.
                    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

                    # dimension we want to resize to
                    dim = (IMG_WIDTH, IMG_HEIGHT)

                    # resize image
                    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

                    # add img to the images list
                    images.append(img)

                    # label represent the category of image belongs to
                    # which is equal to the directory name, i.e. 0,1,2,...
                    # convert the directory name to integer type
                    # add label to the labels list
                    label = int(file_dir)
                    labels.append(label)

                except Exception as e:
                    print(f"Problem with loading file: {image}")
                    print(str(e))

    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.

    different numbers of convolutional and pooling layers
different numbers and sizes of filters for convolutional layers
different pool sizes for pooling layers
different numbers and sizes of hidden layers
dropout
    """
    model = models.Sequential()
    # add a convolution layer
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), padding='same'))
    # add a maximum pooling layer
    model.add(layers.MaxPooling2D((2, 2)))
    # add a convolution layer
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    # add a maximum pooling layer
    model.add(layers.MaxPooling2D((2, 2)))
    # add a convolution layer
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    # Flatten
    model.add(layers.Flatten())
    # Dropout half of the nodes
    model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
    # add a hidden layer (fully connected layer)
    model.add(layers.Dense(64, activation='relu'))
    # Dropout half of the nodes
    model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
    # add an output layer
    model.add(layers.Dense(NUM_CATEGORIES, activation='softmax'))
    # train the model
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


if __name__ == "__main__":
    main()
