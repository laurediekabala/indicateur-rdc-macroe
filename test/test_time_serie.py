
import pandas as pd
import pytest

from src.analysis.times_series import (
    calculate_annual_variation,
    calculate_cagr
)


def test_variation_annuelle_pct():

    series = pd.Series(
        [100, 120, 150],
        index=[2020, 2021, 2022]
    )

    result = calculate_annual_variation(series, method="pct")

    assert result.loc[2021] == pytest.approx(20.0)
    assert result.loc[2022] == pytest.approx(25.0)


def test_variation_en_points():

    series = pd.Series(
        [10, 12, 15],
        index=[2020, 2021, 2022]
    )

    result = calculate_annual_variation(
        series,
        method="difference"
    )

    assert result.loc[2021] == pytest.approx(2.0)
    assert result.loc[2022] == pytest.approx(3.0)


def test_annees_manquantes():

    series = pd.Series(
        [1000, 1200, 1500],
        index=[2020, 2021, 2023]
    )

    result = calculate_annual_variation(series, method="pct")

    assert result.loc[2021] == pytest.approx(20.0)
    assert pd.isna(result.loc[2022])
    assert pd.isna(result.loc[2023])


def test_calcul_cagr():

    series = pd.Series(
        [100, 121],
        index=[2020, 2022]
    )

    result = calculate_cagr(series, 2020, 2022)

    assert result == pytest.approx(10.0)


def test_cagr_valeur_initiale_manquante():

    series = pd.Series(
        [None, 121],
        index=[2020, 2022]
    )

    with pytest.raises(ValueError):
        calculate_cagr(series, 2020, 2022)


def test_cagr_valeur_non_positive():

    series = pd.Series(
        [0, 100],
        index=[2020, 2022]
    )

    with pytest.raises(ValueError):
        calculate_cagr(series, 2020, 2022)


def test_methode_invalide():

    series = pd.Series(
        [100, 120],
        index=[2020, 2021]
    )

    with pytest.raises(ValueError):
        calculate_annual_variation(series, method="incorrect")


def test_donnees_originales_non_modifiees():

    series = pd.Series(
        [100, 120, 150],
        index=[2020, 2021, 2022]
    )

    original = series.copy(deep=True)

    calculate_annual_variation(series)

    pd.testing.assert_series_equal(series, original)
