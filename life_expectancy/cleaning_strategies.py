import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from life_expectancy.region import Region


class AbstractCleaningStrategy(ABC):
    """Abstract class that defines a strategy for cleaning some variants life_expectancy data."""

    def __init__(self, col_dtypes=None):
        super().__init__()
        self.col_dtypes = {"year": np.int64, "value": float} if col_dtypes is None else col_dtypes

    @abstractmethod
    def load_data(self, data_path: Path, *args, **kwargs) -> pd.DataFrame:
        """Loads data from a file in a specified path to a dataframe."""

    @abstractmethod
    def save_data(self, data: pd.DataFrame, output_path: Path | str, *args, **kwargs):
        """Saves data to a file specified by the given path."""

    @abstractmethod
    def clean_data(self, df: pd.DataFrame, country: Region | None = None) -> pd.DataFrame:
        """Cleans data and filters by the specified country."""

    def _ensure_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to correct type based on the col_dtypes dictionary defined on instantiation.

        Args:
            df (pd.DataFrame): The dataframe containing the columns to be converted.

        Returns:
            pd.DataFrame: the dataframe with the correct dtypes.
        """
        # ensure data types
        for col, dtype in self.col_dtypes.items():
            df[col] = df[col].astype(dtype)
        return df

    def _filter_col(self, df: pd.DataFrame, filter_col: str, filter_value: Any) -> pd.DataFrame:
        """Filters the dataframe by a given column and value.

        Args:
            df (pd.DataFrame): The dataframe to be filtered.
            filter_col (str): The column to filter by.
            filter_value (Any): The value to filter by.

        Returns:
            pd.DataFrame: The filtered dataframe.
        """
        if filter_col is not None and filter_value is not None:
            df = df[df[filter_col] == filter_value]
        return df


class CSVCleaningStrategy(AbstractCleaningStrategy):
    """Class that implements the strategy for cleaning life_expectancy data in CSV formats."""

    def load_data(self, data_path: Path | str, *args, sep: str = "\t", **kwargs):
        """Reads the csv from a specified path to a dataframe.

        Args:
            data_path (str): The path from which to load the data.
            sep (str, optional): The separator to use for the file. Defaults to "\t".

        Returns:
            pd.DataFrame: The dataframe containing the data.
        """
        df_data = pd.read_csv(data_path, sep=sep)
        return df_data

    def save_data(self, df: pd.DataFrame, path: str, *args, **kwargs) -> None:
        """Saves data to csv specified by the given path.

        Args:
            df (pd.DataFrame): The dataframe to export to csv.
            path (str): The location to save the data to.
        """
        df.to_csv(path, index=False)

    def clean_data(self, df: pd.DataFrame, country: Region | None = None) -> pd.DataFrame:
        """
        Args:
            df (pd.DataFrame): The data to be cleaned.
            country (Region): The country to filter the data by. Optional.

        Returns:
            pd.DataFrame: The cleaned data.
        """

        # unpivot to long format
        df_eu_life_expectancy = df.copy()
        df_eu_life_expectancy[["unit", "sex", "age", "region"]] = df_eu_life_expectancy[
            "unit,sex,age,geo\\time"
        ].str.split(",", expand=True)
        df_eu_life_expectancy = df_eu_life_expectancy.drop("unit,sex,age,geo\\time", axis=1)
        df_eu_life_expectancy = df_eu_life_expectancy.melt(id_vars=["unit", "sex", "age", "region"], var_name="year")

        # ensure data types
        df_eu_life_expectancy["value"] = df_eu_life_expectancy["value"].str.extract(r"(\d+\.\d)")
        df_eu_life_expectancy = self._ensure_data_types(df_eu_life_expectancy)

        # drop nulls
        df_clean_data = df_eu_life_expectancy.dropna()

        # filter data
        region_name = country.name if country is not None else None
        df_clean_data = self._filter_col(df_clean_data, "region", region_name)

        return df_clean_data.reset_index(drop=True)


class JSONCleaningStrategy(AbstractCleaningStrategy):
    """Class that implements the strategy for cleaning life_expectancy data in CSV formats."""

    def load_data(self, data_path: Path | str, *args, **kwargs):
        """Reads the csv from a specified path to a dataframe.

        Args:
            data_path (str): The path from which to load the data.

        Returns:
            pd.DataFrame: The dataframe containing the data.
        """
        df_data = pd.read_json(data_path, *args, **kwargs)
        return df_data

    def save_data(self, df: pd.DataFrame, path: str, *args, **kwargs) -> None:
        """Saves data to json specified by the given path.

        Args:
            df (pd.DataFrame): The dataframe to export to json.
            path (str): The location to save the data to.
        """
        df.to_json(path, index=False)

    def clean_data(self, df: pd.DataFrame, country: Region | None = None) -> pd.DataFrame:
        """
        Args:
            df (pd.DataFrame): The data to be cleaned.
            country (Region): The country to filter the data by. Optional.

        Returns:
            pd.DataFrame: The cleaned data.
        """

        # filter and rename columns
        df_eu_life_expectancy = df.copy()
        df_eu_life_expectancy = df_eu_life_expectancy.rename({"country": "region", "life_expectancy": "value"}, axis=1)
        df_eu_life_expectancy = df_eu_life_expectancy.drop(["flag", "flag_detail"], axis=1)

        # ensure data types
        df_eu_life_expectancy = self._ensure_data_types(df_eu_life_expectancy)

        # drop nulls
        df_clean_data = df_eu_life_expectancy.dropna()

        # filter data
        region_name = country.name if country is not None else None
        df_clean_data = self._filter_col(df_clean_data, "region", region_name)

        return df_clean_data.reset_index(drop=True)


if __name__ == "__main__":  # pragma: no cover
    INPUT_DATA_PATH = "life_expectancy/data/eu_life_expectancy_raw.tsv"
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="Specify country.", type=str, default="PT")
    parser.add_argument("-i", "--input", help="Specify file to clean.", type=str, default=INPUT_DATA_PATH)

    # args
    args = parser.parse_args()
    arg_country = Region[args.country.upper()]
    arg_input = args.input

    # paths
    file_ext = Path(arg_input).suffix
    # keep same file extension
    output_data_path = f"life_expectancy/data/{str(arg_country.value).lower() if args.country is not None else 'eu'}_life_expectancy{file_ext}"

    strategies = {".csv": CSVCleaningStrategy, ".tsv": CSVCleaningStrategy, ".json": JSONCleaningStrategy}
    cleaning_strategy = strategies[file_ext]()
    data = cleaning_strategy.load_data(arg_input)
    cleaned_data = cleaning_strategy.clean_data(data, arg_country.PT)
    cleaning_strategy.save_data(cleaned_data, output_data_path)
