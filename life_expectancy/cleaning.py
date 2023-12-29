import argparse

import pandas as pd

from life_expectancy.data_io import load_data, save_data


def clean_data(df: pd.DataFrame, country: str | None = None) -> pd.DataFrame:
    """Cleans data and filters by the specified country.

    Args:
        df (pd.DataFrame): The data to be cleaned.
        country (str): The country to filter the data by. Optional.

    Returns:
        pd.DataFrame: The cleaned data.
    """

    # unpivot to long format
    df_eu_life_expectancy = df.copy()
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
    df_clean_data = df_eu_life_expectancy.dropna().copy()

    # filter data
    if country is not None:
        df_clean_data = df_clean_data[df_clean_data["region"] == country]

    return df_clean_data


if __name__ == "__main__":  # pragma: no cover
    INPUT_DATA_PATH = "life_expectancy/data/eu_life_expectancy_raw.tsv"
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="Specify country.", type=str, default=None)
    parser.add_argument("-i", "--input", help="Specify file to clean.", type=str, default=INPUT_DATA_PATH)

    # args
    args = parser.parse_args()
    arg_country = args.country
    arg_input = args.input

    # paths
    output_data_path = (
        f"life_expectancy/data/{arg_country.lower() if args.country is not None else 'eu'}_life_expectancy.csv"
    )

    data = load_data(arg_input)
    cleaned_data = clean_data(data, arg_country)
    save_data(cleaned_data, output_data_path)
