"""
Generic setup of the data sources and the model training.

Based on:
    https://github.com/fchollet/keras/blob/master/examples/mnist_mlp.py
and also on
    https://github.com/fchollet/keras/blob/master/examples/mnist_cnn.py

"""

#import keras
# import tensorflow.keras as keras
from tensorflow.keras import backend as K
from tensorflow.keras.datasets import mnist, cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, Callback
from tensorflow.keras.layers import Conv2D, MaxPooling2D

# from keras import backend as K

import logging

# Helper: Early stopping.
early_stopper = EarlyStopping(
    monitor='val_loss', min_delta=0.1, patience=2, verbose=0, mode='auto')

# patience=5)
# monitor='val_loss',patience=2,verbose=0
# In your case, you can see that your training loss is not dropping - which means you are learning nothing after each epoch.
# It look like there's nothing to learn in this model, aside from some trivial linear-like fit or cutoff value.


def get_cifar10_mlp():
    """Retrieve the CIFAR dataset and process the data."""
    # Set defaults.
    nb_classes = 10  # dataset dependent
    batch_size = 64
    epochs = 4
    input_shape = (3072,)  # because it's RGB

    # Get the data.
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    x_train = x_train.reshape(50000, 3072)
    x_test = x_test.reshape(10000, 3072)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    # convert class vectors to binary class matrices
    y_train = to_categorical(y_train, nb_classes)
    y_test = to_categorical(y_test, nb_classes)

    return (nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs)


def get_cifar10_cnn():
    """Retrieve the MNIST dataset and process the data."""
    # Set defaults.
    nb_classes = 10  # dataset dependent
    batch_size = 128
    epochs = 4

    # the data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # convert class vectors to binary class matrices
    y_train = to_categorical(y_train, nb_classes)
    y_test = to_categorical(y_test,  nb_classes)

    # x._train shape: (50000, 32, 32, 3)
    # input shape (32, 32, 3)
    input_shape = x_train.shape[1:]

    #print('x_train shape:', x_train.shape)
    #print(x_train.shape[0], 'train samples')
    #print(x_test.shape[0], 'test samples')
    #print('input shape', input_shape)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    return (nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs)


def get_mnist_mlp():
    """Retrieve the MNIST dataset and process the data."""
    # Set defaults.
    nb_classes = 10  # dataset dependent
    batch_size = 64
    epochs = 4
    input_shape = (784,)

    # Get the data.
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    # convert class vectors to binary class matrices
    y_train = to_categorical(y_train, nb_classes)
    y_test = to_categorical(y_test, nb_classes)

    return (nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs)


def get_mnist_cnn():
    """Retrieve the MNIST dataset and process the data."""
    # Set defaults.
    nb_classes = 10  # dataset dependent
    batch_size = 128
    epochs = 4

    # Input image dimensions
    img_rows, img_cols = 28, 28

    # Get the data.
    # the data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    #x_train = x_train.reshape(60000, 784)
    #x_test  = x_test.reshape(10000, 784)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    #print('x_train shape:', x_train.shape)
    #print(x_train.shape[0], 'train samples')
    #print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = to_categorical(y_train, nb_classes)
    y_test = to_categorical(y_test,  nb_classes)

    # convert class vectors to binary class matrices
    #y_train = keras.utils.to_categorical(y_train, nb_classes)
    #y_test = keras.utils.to_categorical(y_test, nb_classes)

    return (nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs)


def compile_model_mlp(genome, nb_classes, input_shape):
    """Compile a sequential model.

    Args:
        network (dict): the parameters of the network

    Returns:
        a compiled network.

    """
    # Get our network parameters.
    nb_layers = genome.geneparam['nb_layers']
    nb_neurons = genome.nb_neurons()
    activation = genome.geneparam['activation']
    optimizer = genome.geneparam['optimizer']

    logging.info("Architecture:%s,%s,%s,%d" %
                 (str(nb_neurons), activation, optimizer, nb_layers))

    model = Sequential()

    # Add each layer.
    for i in range(nb_layers):

        # Need input shape for first layer.
        if i == 0:
            model.add(
                Dense(nb_neurons[i], activation=activation, input_shape=input_shape))
        else:
            model.add(Dense(nb_neurons[i], activation=activation))

        model.add(Dropout(0.2))  # hard-coded dropout for each layer

    # Output layer.
    model.add(Dense(nb_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])

    return model


def compile_model_cnn(genome, nb_classes, input_shape):
    """Compile a sequential model.

    Args:
        genome (dict): the parameters of the genome

    Returns:
        a compiled network.

    """
    # Get our network parameters.
    nb_layers = genome.geneparam['nb_layers']
    nb_neurons = genome.nb_neurons()
    activation = genome.geneparam['activation']
    optimizer = genome.geneparam['optimizer']

    logging.info("Architecture:%s,%s,%s,%d" %
                 (str(nb_neurons), activation, optimizer, nb_layers))

    model = Sequential()

    # Add each layer.
    for i in range(0, nb_layers):
        # Need input shape for first layer.
        if i == 0:
            model.add(Conv2D(nb_neurons[i], kernel_size=(
                3, 3), activation=activation, padding='same', input_shape=input_shape))
        else:
            model.add(Conv2D(nb_neurons[i], kernel_size=(
                3, 3), activation=activation))

        if i < 2:  # otherwise we hit zero
            model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Dropout(0.2))

    model.add(Flatten())
    # always use last nb_neurons value for dense layer
    model.add(Dense(nb_neurons[len(nb_neurons) - 1], activation=activation))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation='softmax'))

    # BAYESIAN CONVOLUTIONAL NEURAL NETWORKS WITH BERNOULLI APPROXIMATE VARIATIONAL INFERENCE
    # need to read this paper

    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])

    return model


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


def train_and_score(genome, dataset):
    """Train the model, return test loss.

    Args:
        network (dict): the parameters of the network
        dataset (str): Dataset to use for training/evaluating

    """
    logging.info("Getting Keras datasets")

    if dataset == 'cifar10_mlp':
        nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs = get_cifar10_mlp()
    elif dataset == 'cifar10_cnn':
        nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs = get_cifar10_cnn()
    elif dataset == 'mnist_mlp':
        nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs = get_mnist_mlp()
    elif dataset == 'mnist_cnn':
        nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test, epochs = get_mnist_cnn()

    logging.info("Compling Keras model")

    if dataset == 'cifar10_mlp':
        model = compile_model_mlp(genome, nb_classes, input_shape)
    elif dataset == 'cifar10_cnn':
        model = compile_model_cnn(genome, nb_classes, input_shape)
    elif dataset == 'mnist_mlp':
        model = compile_model_mlp(genome, nb_classes, input_shape)
    elif dataset == 'mnist_cnn':
        model = compile_model_cnn(genome, nb_classes, input_shape)

    history = LossHistory()

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              # using early stopping so no real limit - don't want to waste time on horrible architectures
              verbose=1,
              validation_data=(x_test, y_test),
              # callbacks=[history])
              callbacks=[early_stopper])

    score = model.evaluate(x_test, y_test, verbose=0)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    K.clear_session()
    # we do not care about keeping any of this in memory -
    # we just need to know the final scores and the architecture

    return score[1]  # 1 is accuracy. 0 is loss.
