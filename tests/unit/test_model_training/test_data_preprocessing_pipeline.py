import pytest
import numpy as np
import pandas as pd
from model_training import data_preprocessing_pipeline


@pytest.fixture
def example_ddb_data():

    df = pd.DataFrame(
        np.array(
            [
                [1, 61.76, 20.10, "2023-05-06 23:20:04.475087"],
                [2, 61.67, 20.19, "2023-05-06 23:30:03.932921"],
                [3, 61.46, 20.16, "2023-05-06 23:40:04.417794"],
            ]
        ),
        columns=["Unnamed: 0", "humidity.S", "temperature.S", "timestamp.S"],
    )

    return df


def test_clean_data(example_ddb_data):
    """Checks that cleaning stages prepare data in required format."""

    df_cleaned = data_preprocessing_pipeline.clean_data(example_ddb_data)

    assert df_cleaned.index.values[0] == pd.Timestamp("2023-05-06 23:20:00")
    assert df_cleaned["temperature"].iloc[0] == "20.1"

    assert df_cleaned.index.values[1] == pd.Timestamp("2023-05-06 23:30:00")
    assert df_cleaned["temperature"].iloc[1] == "20.19"

    assert df_cleaned.index.values[2] == pd.Timestamp("2023-05-06 23:40:00")
    assert df_cleaned["temperature"].iloc[2] == "20.16"
