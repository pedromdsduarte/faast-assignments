import pandas as pd


def load_data(data_path: str, sep: str = "\t") -> pd.DataFrame:
    """Reads the csv from a specified path to a dataframe.

    Args:
        data_path (str): The path from which to load the data.
        sep (str, optional): The separator to use for the file. Defaults to "\t".

    Returns:
        pd.DataFrame: The dataframe containing the data.
    """
    df_eu_life_expectancy_raw = pd.read_csv(data_path, sep=sep)
    return df_eu_life_expectancy_raw


def save_data(df: pd.DataFrame, path: str):
    """Saves data to csv specified by the given path.

    Args:
        df (pd.DataFrame): The dataframe to export to csv.
        path (str): The location to save the data to.
    """
    df.to_csv(path, index=False)
