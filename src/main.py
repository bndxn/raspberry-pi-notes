"""Controller function for training model."""
from utils.ddb_query import DynamoResource
from model_training.data_preprocessing_pipeline import run_preprocessing_pipeline
from model_training.train_lstm_model import train_model, compress_model


def run_training_pipeline():
    """Defines the overall training process from data gathering, formatting, model training, and model conversion."""
    dynamoresource = DynamoResource()
    dynamoresource.query_all_time()
    train, validation, _ = run_preprocessing_pipeline("saved_files/ddb_output.csv")
    model = train_model(train, validation)
    compress_model(model)


if __name__ == "__main__":

    run_training_pipeline()
