import pytest
import numpy as np
import pandas as pd
from model_training import data_preprocessing_pipeline

# @pytest.fixture
# def example_ddb_data():

#     df = pd.DataFrame(np.array([
#     [1,61.76,20.10,'2023-05-06 23:20:04.475087'],
#     [2,61.67,20.19,'2023-05-06 23:30:03.932921'],
#     [3,61.46,20.16,'2023-05-06 23:40:04.417794'],
#     ]),
#     columns = ['Unnamed: 0','humidity.S','temperature.S','timestamp.S'])

#     return df

def test_basic_maths():

    value = 6+1
    assert value ==7 

def test_clean_data(example_ddb_data):

    df = example_ddb_data

    df_cleaned = data_preprocessing_pipeline.clean_data(df)

    assert df_cleaned == pd.DataFrame(np.array(
        [
        [pd.Timestamp('2023-05-06 23:20:00'), 20.10],
        [pd.Timestamp('2023-05-06 23:30:00'), 20.19],
        [pd.Timestamp('2023-05-06 23:50:00'), 20.16]
        ]))