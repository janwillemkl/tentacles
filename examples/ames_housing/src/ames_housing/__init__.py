"""Ames housing price prediction model training pipeline."""

from dagster import Definitions
from tentacles.io_managers.fs_io_manager import FilesystemIOManager
from tentacles.io_managers.serializers.csv_serializer import CSVSerializer
from tentacles.resources.mlflow_session import MlflowSession

from ames_housing.assets.ames_housing_data import ames_housing_data
from ames_housing.assets.ames_housing_features import ames_housing_features
from ames_housing.assets.price_prediction_models import (
    gradient_boosting_model,
    linear_regression_model,
    random_forest_model,
)
from ames_housing.assets.train_test import train_test_data
from ames_housing.constants import (
    AMES_HOUSING_DATA_SET_SEPARATOR,
    AMES_HOUSING_DATA_SET_URL,
    MLFLOW_EXPERIMENT,
    MLFLOW_TRACKING_URL,
)
from ames_housing.resources.csv_data_set_loader import CSVDataSetLoader

definitions = Definitions(
    assets=[
        ames_housing_data,
        ames_housing_features,
        train_test_data,
        linear_regression_model,
        random_forest_model,
        gradient_boosting_model,
    ],
    resources={
        "data_set_downloader": CSVDataSetLoader(
            path_or_url=AMES_HOUSING_DATA_SET_URL,
            separator=AMES_HOUSING_DATA_SET_SEPARATOR,
        ),
        "mlflow_session": MlflowSession(
            tracking_url=MLFLOW_TRACKING_URL, experiment=MLFLOW_EXPERIMENT
        ),
        "csv_io_manager": FilesystemIOManager(
            base_dir="data",
            extension=".csv",
            serializer=CSVSerializer(),
        ),
    },
)
