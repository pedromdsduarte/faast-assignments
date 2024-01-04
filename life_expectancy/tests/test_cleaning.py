"""Tests for the cleaning module"""
import os

import pandas as pd

from life_expectancy.cleaning import clean_data, load_data, save_data

from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    input_data_path = "life_expectancy/data/eu_life_expectancy_raw.tsv"
    output_data_path = os.path.join(OUTPUT_DIR, "pt_life_expectancy.csv")

    data = load_data(input_data_path)
    cleaned_data = clean_data(data, "PT")
    save_data(cleaned_data, output_data_path)
    pt_life_expectancy_actual = pd.read_csv(output_data_path)
    pd.testing.assert_frame_equal(pt_life_expectancy_actual, pt_life_expectancy_expected)
