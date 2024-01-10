"""Tests for the dataio module"""
from unittest.mock import patch

import pandas as pd

from life_expectancy.data_io import load_data, save_data


def test_load_data(eu_life_expectancy_raw, capfd) -> None:
    """Tests the load data function from the data_io module.

    Args:
        eu_life_expectancy_raw: raw data fixture with the data.
        capfd: the capturer of the stdout and stderr.
    """
    with patch("life_expectancy.data_io.pd.read_csv") as mock_read_csv:
        mock_read_csv.return_value = eu_life_expectancy_raw
        mock_file_path = "mock_df.tsv"
        printmsg = "Data read"
        mock_read_csv.side_effect = print(printmsg, end="")

        actual_df = load_data(mock_file_path)

        pd.testing.assert_frame_equal(actual_df, eu_life_expectancy_raw)
        mock_read_csv.assert_called_once_with(mock_file_path, sep="\t")
        assert capfd.readouterr().out == printmsg


def test_save_data(capfd) -> None:
    """Tests the save data function from the data_io module.

    Args:
        capfd: the capturer of the stdout and stderr.
    """
    mock_df = pd.DataFrame([1, 2, 3], ["a", "b", "c"])
    mock_file_path = "mock_df.csv"
    with patch("life_expectancy.data_io.pd.DataFrame.to_csv") as mock_to_csv:
        printmsg = "Data saved"
        mock_to_csv.side_effect = print(printmsg, end="")
        save_data(mock_df, mock_file_path)

        mock_to_csv.assert_called_once_with(mock_file_path, index=False)
        assert capfd.readouterr().out == printmsg
