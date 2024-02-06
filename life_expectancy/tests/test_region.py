"""Tests for the Region enum class"""

from life_expectancy.region import Region


def test_get_country_list():
    """
    Runs the get_country_list() class method of enum Region and checks some basic assumptions.
    """
    country_list = Region.get_country_list()

    # Assert that there are no countries with more than two letters
    country_list_with_len_gt_2 = [c for c in country_list if len(c) > 2]
    assert len(country_list_with_len_gt_2) == 0

    # Assert that there are no countries that shouldn't be there
    not_countries = {"DE_TOT", "EEA30_2007", "EU27_2007"}
    assert len(set(country_list).intersection(not_countries)) == 0
