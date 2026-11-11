
import numpy as np
import pandas as pd


def prepare_macro_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prépare les données macroéconomiques pour les analyses.

    Les données originales ne sont jamais modifiées.
    Les valeurs manquantes sont conservées.
    """

    # 1. Vérifier le type de données
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Les données doivent être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Impossible de préparer un DataFrame vide.")

    # 2. Créer une copie indépendante
    data = df.copy(deep=True)

    # 3. Vérifier les colonnes dupliquées
    if data.columns.duplicated().any():
        raise ValueError("Présence de colonnes dupliquées.")

    # 4. Vérifier et convertir les années
    try:
        years = pd.to_numeric(data.index, errors="raise")

        if not np.isfinite(years).all():
            raise ValueError("L'index contient des années invalides.")

        if not np.equal(years, np.floor(years)).all():
            raise ValueError("Les années doivent être des nombres entiers.")

        data.index = years.astype(int)

    except (ValueError, TypeError) as error:
        raise ValueError(
            f"Index des années invalide : {error}"
        ) from error

    # 5. Vérifier les années dupliquées
    if data.index.duplicated().any():
        raise ValueError("Présence d'années dupliquées.")

    # 6. Convertir les colonnes en valeurs numériques
    for column in data.columns:
        try:
            data[column] = pd.to_numeric(
                data[column],
                errors="raise"
            )
        except (ValueError, TypeError) as error:
            raise ValueError(
                f"Valeurs non numériques dans {column} : {error}"
            ) from error

    # 7. Vérifier les valeurs infinies
    if np.isinf(data.to_numpy(dtype=float)).any():
        raise ValueError("Les données contiennent des valeurs infinies.")

    # 8. Trier chronologiquement
    data = data.sort_index()

    # 9. Nommer l'index
    data.index.name = "Annee"
    data.columns.name = None

    return data
