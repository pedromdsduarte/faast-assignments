"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region


def test_clean_data(eu_life_expectancy_raw, pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""

    pt_life_expectancy_actual = clean_data(eu_life_expectancy_raw, Region.PT)
    pd.testing.assert_frame_equal(pt_life_expectancy_actual, pt_life_expectancy_expected)
