"""
Build a machine learning model to recognize handwritten digits.
"""

__author__ = 'Dylan Warnecke'

__version__ = '1.1'

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from activations import tanh
from layers import Dense, Dropout, InputLayer
from losses.categorical_cross_entropy import CategoricalCrossEntropy
from model import Model
from optimizers.adam import Adam
from utilities import make_one_hot


if __name__ == '__main__':
    # Import and convert the training data
    training_set = pd.read_csv('training-digits.csv')
    training_pixels = training_set.drop(columns='label').to_numpy()
    training_digits = training_set.loc[:, 'label'].to_numpy()
    training_digits = make_one_hot(training_digits, 10)

    # Make the neural network model
    digit_model = Model(
        CategoricalCrossEntropy(from_logits=True),
        InputLayer(784),
        Dense(128, tanh),
        Dropout(0.3),
        Dense(128, tanh),
        Dropout(0.3),
        Dense(10))

    # Fit the model using gradient descent
    training_history = digit_model.fit(
        training_pixels, training_digits,
        batch_size=256,
        epochs=30,
        learning_rate=1e-4,
        optimizer=Adam(0.9, 0.99))

    # Plot the model training history
    plt.plot(training_history)
    plt.title("Training Model Loss Over Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.yscale('log')
    plt.show()

    # Import and convert the testing data
    testing_set = pd.read_csv('testing-digits.csv')
    testing_set_size = testing_set.shape[0]
    testing_pixels = testing_set.to_numpy()
    testing_images = testing_pixels.reshape((testing_set_size, 28, 28))

    # Shuffle the testing data examples
    generator = np.random.default_rng()
    shuffling_indices = generator.permutation(testing_set_size)
    testing_pixels = testing_pixels[shuffling_indices]
    testing_images = testing_images[shuffling_indices]

    # Message that the model performance is being evaluated
    print("Model performance being evaluated...")

    # Check the model performance in practice
    for digit_idx in range(testing_set_size):
        evaluation_digit = testing_images[digit_idx]
        flattened_digit = np.ravel(evaluation_digit)
        digit_prediction = digit_model.predict(flattened_digit[np.newaxis])
        digit_prediction = digit_prediction.argmax(axis=1)[0]

        # Message the predicted digit and show it
        print(f"Predicted number: {digit_prediction}", end='')
        plt.imshow(evaluation_digit)
        plt.show()
        print("\r", end='')

        # Check if the model should still be evaluated
        if (digit_idx + 1) % 7 == 0:
            keyboard_input = input("Continue evaluation (y/n): ")
            if keyboard_input != 'y':
                break
