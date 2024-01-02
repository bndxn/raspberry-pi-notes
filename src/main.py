"""Controller function for training model."""

from model_training.data_preprocessing_pipeline import run_preprocessing_pipeline


train, validation, test = run_preprocessing_pipeline("analysis/ddb_output.csv")
