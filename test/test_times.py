import numpy as np
import pandas as pd
import pytest

from src.analysis.times_series import (
    calculate_annual_variation,
    calculate_cagr
)
print("\nTEST DES VALEURS MANQUANTES DU TCAM")

series_missing = pd.Series(
    [None, 60, 70, 80],
    index=[2010, 2015, 2018, 2020]
)

try:
    calculate_cagr(
        series_missing,
        start_year=2010,
        end_year=2020
    )

    raise AssertionError("Une erreur était attendue.")

except ValueError as error:
    print("Erreur correctement détectée :", error)
print("\nTEST DES VALEURS INITIALES OU FINALES NULLES")

series_zero = pd.Series(
    [0, 50, 100],
    index=[2020, 2021, 2022]
)

try:
    calculate_cagr(series_zero, 2020, 2022)
    raise AssertionError("Une erreur était attendue.")

except ValueError as error:
    print("Valeur nulle détectée :", error)


print("\nTEST DES VALEURS NEGATIVES")

series_negative = pd.Series(
    [100, 80, -20],
    index=[2020, 2021, 2022]
)

try:
    calculate_cagr(series_negative, 2020, 2022)
    raise AssertionError("Une erreur était attendue.")

except ValueError as error:
    print("Valeur négative détectée :", error)    