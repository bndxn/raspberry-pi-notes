"""Controller function for training model."""

from model_training.data_preprocessing_pipeline import run_preprocessing_pipeline
from model_training.train_lstm_model import train_model, compress_model


if __name__ == "__main__":
    train, validation, test = run_preprocessing_pipeline("analysis/ddb_output.csv")

    model = train_model(train, validation)

    compress_model(model)
