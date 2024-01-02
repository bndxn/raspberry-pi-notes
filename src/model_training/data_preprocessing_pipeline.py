"""Defines data preprocessing from DDB query result, prepares for input to model."""
import logging
from typing import Tuple
import numpy as np
import pandas as pd
from datetime import timedelta
from pickle import dump
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)
logger = logging.getLogger()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply basic data cleaning and reorganisation. Unused columns are dropped,
    then the timestamp recorded is rounded to the nearest minute. The values are
    then sorted by timestamp, only those after a certain date when the readings were
    more consistent are used, and then the index is set.

    Args:
        df: a dataframe of readings, including temperature and humidity.

    Returns:
        df: a dataframe of temperature readings, sorted by timestamp
    """
    df.drop(columns=["Unnamed: 0", "humidity.S"], inplace=True)

    df.rename(
        columns={"temperature.S": "temperature", "timestamp.S": "timestamp"},
        inplace=True,
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["timestamp"] = df["timestamp"].dt.round("1min")
    df.sort_values(by="timestamp")
    df = df[df["timestamp"] > "2023-05-28"]
    df.set_index("timestamp", inplace=True)
    df = df.dropna()

    logger.info("DynamoDB readings formatted")
    return pd.DataFrame(df)


def augment_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Augment missing data using readings from 24 hours previous.

    Args:
        df: a dataframe of temperature readings, sorted by timestamp

    Returns:
        df: a dataframe of temperature readings, sorted by timestamp, augmented
        to input missing data with the value from 24 hours previous.
    """
    logger.info(f"Dataframe size before augmentation: {df.shape}")

    df_original_shape = df.shape
    one_day = 10 * 24
    time_interval = timedelta(minutes=10)
    i = one_day

    while i < df.shape[0] - 1:

        current_time = pd.Timestamp(df.index[i])
        next_time = pd.Timestamp(df.index[i + 1])

        if (next_time - current_time) > time_interval + timedelta(minutes=60):

            previous_value_temp = df.iloc[i + 1 - one_day]["temperature"]
            new_row = pd.DataFrame(
                {"temperature": previous_value_temp},
                index=[pd.Timestamp(current_time + time_interval)],
            )
            df = pd.concat([df.iloc[: i + 1], new_row, df.iloc[i + 1 :]])

        i += 1

    logger.info("Missing data augmented")
    logger.info(f"Dataframe size after empty rows added: {df.shape}")
    logger.info(
        f"Rows added, {df.shape[0]-df_original_shape[0]},"
        f"or {np.round((df.shape[0]-df_original_shape[0])*100/df.shape[0],2)}% of the new total."
    )

    return df


def train_val_test_split(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Apply train, validation, and test split to time series data.

    Takes a preprocessed dataframe, assumed to be sorted chronologically,
    and returns three dataframes split into train, validation, and test;
    done chronologically in a 60%/20%/20% split.

    Args:
        df: a DataFrame

    Returns:
        df_train, df_test, df_val: a tuple of the train, test, and validation
        data.
    """
    train_index = int(np.round(df.shape[0] * 0.6))
    val_index = int(np.round(df.shape[0] * 0.8))

    df_train = df.iloc[
        :train_index,
    ]
    df_val = df.iloc[train_index:val_index]
    df_test = df.iloc[val_index:]

    logger.info("Train, test, validation split complete.")
    logger.info(
        f"Train index: {train_index}, val_index: {val_index}, end : {df.shape[0]}"
    )

    return df_train, df_test, df_val


def scale_data(
    df_train: pd.DataFrame,
    df_val: pd.DataFrame,
    df_test: pd.DataFrame,
    scaler_path: str,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Scales data and saves scaling object as a pickle file.

    Args:
        df_train, df_val, df_test: train, val, and test splits of time series
        data

    Returns:
        df_train_scaled, df_val_scaled, df_test_scaled: scaled train, val, and
        test splits of time series data, using StandardScaler.
    """
    logger.info("Fitting scaler")
    scaler = StandardScaler()
    scaler.fit(df_train)
    logger.info("Scaler fitted")
    logger.info(f"Scaler mean: {scaler.mean_}, scaler scale: {scaler.scale_}")

    dump(scaler, open(f"{scaler_path}/scaler.pkl", "wb"))

    return (
        scaler.transform(df_train),
        scaler.transform(df_val),
        scaler.transform(df_test),
    )


def generate_sequences(
    df_train, df_val, df_test
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Create the sequence and target generators for use in model training and evaluation.

    The task will be to take in one hour of readings,
    spaced 10 minutes apart, and predict the temperature in two hours.

    For example, there will be readings at 3:00pm, 3:10pm, ..., 4:00pm,
    and the task will be to predict the temperature at 6pm.
    """
    delay = 24
    sequence_length = 12
    batch_size = 128

    train = keras.preprocessing.timeseries_dataset_from_array(
        df_train[:-delay],
        df_train[sequence_length + delay :],
        sequence_length=sequence_length,
        batch_size=batch_size,
        shuffle=True,
    )

    validation = keras.preprocessing.timeseries_dataset_from_array(
        df_val[:-delay],
        df_val[sequence_length + delay :],
        sequence_length=sequence_length,
        batch_size=batch_size,
        shuffle=True,
    )

    test = keras.preprocessing.timeseries_dataset_from_array(
        df_test[:-delay],
        df_test[sequence_length + delay :],
        sequence_length=sequence_length,
        batch_size=batch_size,
        shuffle=True,
    )
    logger.info("Sequences generators created.")

    return train, validation, test


def run_preprocessing_pipeline(
    csv_input_path: str,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Run pipeline from CSV to generators ready for input to training.

    Args:
        csv_input_path: a string of the path to the location of the CSV

    Returns:
        A tuple (df_train, df_val, df_test), containing three generators
        which load 12 inputs and 1 target, from a scaled dataset of temperature
        readings.
    """
    df_raw = pd.read_csv(csv_input_path)

    df_cleaned = clean_data(df_raw)
    df_augmented = augment_missing_data(df_cleaned)
    df_train, df_val, df_test = train_val_test_split(df_augmented)
    df_train, df_val, df_test = scale_data(
        df_train, df_val, df_test, scaler_path="saved_files"
    )

    return generate_sequences(df_train, df_val, df_test)


if __name__ == "__main__":
    train, validation, test = run_preprocessing_pipeline("saved_files/ddb_output.csv")
