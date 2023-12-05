import argparse

import pandas as pd


def clean_data(country: str):
    """Functions that cleans data from eu_life_expectancy_raw.tsv"""

    # load data
    df_eu_life_expectancy_raw = pd.read_csv("life_expectancy/data/eu_life_expectancy_raw.tsv", sep="\t")

    # unpivot to long format
    df_eu_life_expectancy = df_eu_life_expectancy_raw.copy()
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
    df_pt_life_expectancy = df_eu_life_expectancy.query("region == @country")

    # export data
    df_pt_life_expectancy.to_csv(f"life_expectancy/data/{country.lower()}_life_expectancy.csv", index=False)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="Specify country.", type=str, default="PT")
    args = parser.parse_args()

    clean_data(args.country)
