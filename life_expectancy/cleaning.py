import argparse

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


def clean_data(data: pd.DataFrame, country: str) -> pd.DataFrame:
    """Cleans data and filters by the specified country.

    Args:
        data (pd.DataFrame): The data to be cleaned.
        country (str): The country to filter the data by.

    Returns:
        pd.DataFrame: The cleaned data.
    """

    # unpivot to long format
    df_eu_life_expectancy = data.copy()
    df_eu_life_expectancy[["unit", "sex", "age", "region"]] = df_eu_life_expectancy["unit,sex,age,geo\\time"].str.split(
        ",", expand=True
    )
    df_eu_life_expectancy = df_eu_life_expectancy.drop("unit,sex,age,geo\\time", axis=1)
    df_eu_life_expectancy = df_eu_life_expectancy.melt(id_vars=["unit", "sex", "age", "region"], var_name="year")

    # ensure data types
    df_eu_life_expectancy["year"] = df_eu_life_expectancy["year"].astype(int)
    df_eu_life_expectancy["value"] = df_eu_life_expectancy["value"].str.extract(r"(\d+\.\d)")
    df_eu_life_expectancy["value"] = df_eu_life_expectancy["value"].astype(float)

    # drop nulls
    df_eu_life_expectancy = df_eu_life_expectancy.dropna()

    # filter data
    df_pt_life_expectancy = df_eu_life_expectancy[df_eu_life_expectancy["region"] == country]

    return df_pt_life_expectancy


def save_data(data: pd.DataFrame, path: str):
    """Saves data to csv specified by the given path.

    Args:
        data (pd.DataFrame): The dataframe to export to csv.
        path (str): The location to save the data to.
    """
    data.to_csv(path, index=False)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="Specify country.", type=str, default="PT")

    # args
    args = parser.parse_args()
    country = args.country

    # paths
    input_data_path = "life_expectancy/data/eu_life_expectancy_raw.tsv"
    output_data_path = f"life_expectancy/data/{country.lower()}_life_expectancy.csv"

    data = load_data(input_data_path)
    cleaned_data = clean_data(data, country)
    save_data(cleaned_data, output_data_path)
