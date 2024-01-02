"""Defines training process for LSTM time-series model."""
import logging

import tensorflow as tf
from tensorflow import keras
from keras import layers
import numpy as np

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)
logger = logging.getLogger()


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
    model.fit(train, epochs=5, validation_data=validation)
    evaluation = model.evaluate(validation)
    logger.info(f"Model evaluation, loss: {evaluation[0]}, mae: {evaluation[1]}")
    model.save("saved_files/regularised_lstm", save_format="tf")

    return model


def persistence_forecast(dataset, batch_size):

    total_abs_err = 0
    predictions = 0

    for inputs, targets in dataset:

        # We take the last value from the input tensor
        preds = inputs[:, -1]
        total_abs_err += np.sum(np.abs(preds - targets))
        predictions += 1

    logger.info(
        f"Baseline: persistence forecast for 2 hours - MAE: {total_abs_err / (predictions*batch_size)}%"
    )


def compress_model(model: keras.Model) -> None:
    """Compresses the LSTM model into the TF-Lite format.

    Saves the model to disk.

    Args:
        model: the trained keras LSTM model

    Returns:
        None: the function saved the compressed file to disk.
    """

    converter = tf.lite.TFLiteConverter.from_saved_model(
        "./saved_files/regularised_lstm/"
    )
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,  # enable TensorFlow Lite ops.
        tf.lite.OpsSet.SELECT_TF_OPS,  # enable TensorFlow ops.
    ]
    tflite_model = converter.convert()
    open("saved_files/converted_model.tflite", "wb").write(tflite_model)
