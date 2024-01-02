"""Defines training process for LSTM time-series model."""
import logging

import tensorflow as tf
from tensorflow import keras
from keras import layers


def train_model(train, validation) -> keras.Model:
    """Given training and validation data, train a keras LSTM model.

    Args:
        train: a shuffled generator of a time series, with 12 inputs and
        one target, one hours later, for the train dataset
        validation: a shuffled generator of a time series, with 12 inputs and
        one target, one hours later, for the validation dataset

    Returns:
        model: a trained LSTM model
    """
    inputs = keras.Input(shape=(12, 1))

    x = layers.LSTM(16, recurrent_dropout=0.25)(inputs)
    outputs = layers.Dense(1)(x)

    model = keras.Model(inputs, outputs)

    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    model.fit(train, epochs=10, validation_data=validation)

    return model


def compress_model(model: keras.Model) -> None:
    """Compresses the LSTM model into the TF-Lite format.

    Saves the model to disk.

    Args:
        model: the trained keras LSTM model

    Returns:
        None: the function saved the compressed file to disk.
    """

    converter = tf.lite.TFLiteConverter.from_saved_model(
        "./saved_files/regularised_lstm_saved_model_format/"
    )
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,  # enable TensorFlow Lite ops.
        tf.lite.OpsSet.SELECT_TF_OPS,  # enable TensorFlow ops.
    ]
    tflite_model = converter.convert()
    open("saved_files/converted_model.tflite", "wb").write(tflite_model)
