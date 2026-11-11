
import pandas as pd

from config.indicators import INDICATOR_METADATA
from src.analysis.times_series import calculate_annual_variation



def calculate_correlations(
    df: pd.DataFrame,
    method: str = "pearson",
    min_periods: int = 5
) -> pd.DataFrame:
    """
    Calcule la matrice de corrélation entre les indicateurs
    macroéconomiques.

    Parameters
    ----------
    df : pd.DataFrame
        Données macroéconomiques indexées par année.

    method : str
        Méthode de corrélation : pearson ou spearman.

    min_periods : int
        Nombre minimal d'observations communes.

    Returns
    -------
    pd.DataFrame
        Matrice de corrélation.
    """

    # 1. Validation du DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df doit être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    if not df.columns.is_unique:
        raise ValueError("Les colonnes doivent être uniques.")

    # 2. Validation de la méthode
    if method not in {"pearson", "spearman"}:
        raise ValueError(
            "La méthode doit être 'pearson' ou 'spearman'."
        )

    # 3. Validation du nombre minimal d'observations
    if (
        isinstance(min_periods, bool)
        or not isinstance(min_periods, int)
        or min_periods < 2
    ):
        raise ValueError(
            "min_periods doit être un entier supérieur ou égal à 2."
        )

    # 4. Vérification des colonnes numériques
    non_numeric = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if non_numeric:
        raise TypeError(
            f"Colonnes non numériques détectées : {non_numeric}"
        )

    # 5. Vérification des valeurs infinies
    if df.isin([float("inf"), float("-inf")]).any().any():
        raise ValueError(
            "Le DataFrame contient des valeurs infinies."
        )

    # 6. Calcul de la matrice de corrélation
    correlations = df.corr(
        method=method,
        min_periods=min_periods
    )

    return correlations

def calculate_correlation_counts(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcule le nombre d'observations communes
    disponibles pour chaque paire d'indicateurs.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df doit être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    if not df.columns.is_unique:
        raise ValueError("Les colonnes doivent être uniques.")

    non_numeric = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if non_numeric:
        raise TypeError(
            f"Colonnes non numériques détectées : {non_numeric}"
        )

    if df.isin([float("inf"), float("-inf")]).any().any():
        raise ValueError(
            "Le DataFrame contient des valeurs infinies."
        )

    # 1 si une observation est disponible, 0 sinon
    valid = df.notna().astype(int)

    # Produit matriciel : nombre de valeurs communes
    counts = valid.T.dot(valid)

    return counts

def calculate_indicator_variations(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcule les variations annuelles de chaque indicateur
    selon sa méthode définie dans INDICATOR_METADATA.

    Les années manquantes sont conservées afin d'éviter
    de calculer une variation entre deux années non consécutives.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df doit être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    if not df.columns.is_unique:
        raise ValueError("Les colonnes doivent être uniques.")

    non_numeric = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if non_numeric:
        raise TypeError(
            f"Colonnes non numériques détectées : {non_numeric}"
        )

    if df.isin([float("inf"), float("-inf")]).any().any():
        raise ValueError(
            "Le DataFrame contient des valeurs infinies."
        )

    variations = {}

    for column in df.columns:

        if column not in INDICATOR_METADATA:
            raise ValueError(
                f"Métadonnées absentes pour l'indicateur : {column}"
            )

        metadata = INDICATOR_METADATA[column]

        method = metadata.get("variation_method")

        if method not in {"difference", "pct"}:
            raise ValueError(
                f"Méthode de variation invalide pour {column}."
            )

        variations[column] = calculate_annual_variation(
            df[column],
            method=method
        )

    return pd.DataFrame(variations)


def calculate_correlations_on_variations(
    df: pd.DataFrame,
    method: str = "pearson",
    min_periods: int = 10
) -> pd.DataFrame:
    """
    Calcule les corrélations entre les variations annuelles
    des indicateurs macroéconomiques.
    """

    variations = calculate_indicator_variations(df)

    return calculate_correlations(
        variations,
        method=method,
        min_periods=min_periods
    )
