
import pandas as pd
import numpy as np
import pytest

from src.analysis.period_comaraison import compare_periods


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Exportations_USD": [100, 150, 200, 250, 300],
            "Inflation_%": [10, 12, 15, 11, 9]
        },
        index=[2020, 2021, 2022, 2023, 2024]
    )


@pytest.fixture
def periods():
    return {
        "2020-2022": (2020, 2022),
        "2023-2024": (2023, 2024)
    }


def test_absolute_variation(sample_data, periods):
    result = compare_periods(sample_data, periods)

    value = result.loc[
        ("Exportations_USD", "2020-2022"),
        "variation_absolue"
    ]

    assert value == 100


def test_relative_variation_for_level(sample_data, periods):
    result = compare_periods(sample_data, periods)

    value = result.loc[
        ("Exportations_USD", "2020-2022"),
        "variation_pct"
    ]

    assert value == 100


def test_no_relative_variation_for_rate(sample_data, periods):
    result = compare_periods(sample_data, periods)

    value = result.loc[
        ("Inflation_%", "2020-2022"),
        "variation_pct"
    ]

    assert pd.isna(value)


def test_availability_rate(sample_data, periods):
    result = compare_periods(sample_data, periods)

    value = result.loc[
        ("Exportations_USD", "2020-2022"),
        "taux_disponibilite"
    ]

    assert value == 100


def test_empty_period(sample_data):
    result = compare_periods(
        sample_data,
        {"1990-1992": (1990, 1992)}
    )

    assert result.loc[
        ("Exportations_USD", "1990-1992"),
        "n"
    ] == 0


def test_input_not_modified(sample_data, periods):
    original = sample_data.copy(deep=True)

    compare_periods(sample_data, periods)

    pd.testing.assert_frame_equal(sample_data, original)
