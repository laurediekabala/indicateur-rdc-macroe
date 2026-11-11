import pandas as pd
import numpy as np
from src.analysis.statistiques import build_descriptive_statistics 
def test_descriptive_statistics():

    # Jeu de données fictif pour tester le module
    df = pd.DataFrame(
        {
            "PIB": [10, 20, 30, 40, 50],
            "Inflation": [2.0, 3.0, np.nan, 5.0, 6.0],
            "Population": [100, 110, 120, 130, 140]
        },
        index=[2019, 2020, 2021, 2022, 2023]
    )

    original = df.copy(deep=True)

    report = build_descriptive_statistics(df)

    # Vérifier les indicateurs
    assert len(report) == 3

    # Vérifier le nombre d'observations
    assert report.loc["PIB", "n"] == 5
    assert report.loc["Inflation", "n"] == 4

    # Vérifier la moyenne du PIB
    assert report.loc["PIB", "moyenne"] == 30

    # Vérifier la médiane du PIB
    assert report.loc["PIB", "mediane"] == 30

    # Vérifier les années disponibles pour l'inflation
    assert report.loc["Inflation", "annee_debut"] == 2019
    assert report.loc["Inflation", "annee_fin"] == 2023

    # Vérifier que les données originales ne sont pas modifiées
    pd.testing.assert_frame_equal(df, original)

    print("Tous les tests sont réussis.")
    print(report)


if __name__ == "__main__":
    test_descriptive_statistics()