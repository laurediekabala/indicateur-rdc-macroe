import pandas as pd
import pytest

from src.analysis.distribution import distribution_analysis


def test_detection_valeur_atypique():

    df = pd.DataFrame({
        "PIB": [1, 2, 3, 4, 100]
    }, index=[2020, 2021, 2022, 2023, 2024])

    result = distribution_analysis(df)

    assert result.loc["PIB", "nombre_valeurs_atypiques"] == 1


def test_calcul_iqr():

    df = pd.DataFrame({
        "PIB": [1, 2, 3, 4, 100]
    })

    result = distribution_analysis(df)

    assert result.loc["PIB", "iqr"] == pytest.approx(2.0)


def test_traitement_valeurs_manquantes():

    df = pd.DataFrame({
        "PIB": [1, 2, None, 4, 5]
    })

    result = distribution_analysis(df)

    assert result.loc["PIB", "n"] == 4


def test_indicateur_vide():

    df = pd.DataFrame({
        "PIB": [None, None, None]
    })

    result = distribution_analysis(df)

    assert result.loc["PIB", "n"] == 0
    assert pd.isna(result.loc["PIB", "iqr"])


def test_donnees_originales_non_modifiees():

    df = pd.DataFrame({
        "PIB": [1, 2, 3, 4, 100]
    })

    original = df.copy(deep=True)

    distribution_analysis(df)

    pd.testing.assert_frame_equal(df, original)


def test_rejet_dataframe_vide():

    with pytest.raises(ValueError):
        distribution_analysis(pd.DataFrame())