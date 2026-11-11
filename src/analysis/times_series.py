
import numpy as np
import pandas as pd


def _validate_series(series: pd.Series) -> pd.Series:
    """
    Vérifie une série temporelle annuelle et retourne
    une copie triée chronologiquement.
    """

    if not isinstance(series, pd.Series):
        raise TypeError("Les données doivent être une Series pandas.")

    if series.empty:
        raise ValueError("La série temporelle est vide.")

    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError("La série doit contenir des valeurs numériques.")

    try:
        years = pd.to_numeric(series.index, errors="raise")
        years = np.asarray(years, dtype=float)

        if not np.isfinite(years).all():
            raise ValueError("Les années contiennent des valeurs invalides.")

        if not np.equal(years, np.floor(years)).all():
            raise ValueError("Les années doivent être entières.")

        years = years.astype(int)

    except (ValueError, TypeError) as error:
        raise ValueError(f"Index annuel invalide : {error}") from error

    if pd.Index(years).duplicated().any():
        raise ValueError("La série contient des années dupliquées.")

    data = series.copy(deep=True)
    data.index = years
    data.index.name = "Annee"

    data = data.sort_index()

    if not np.isfinite(data.dropna().to_numpy(dtype=float)).all():
        raise ValueError("La série contient des valeurs infinies.")

    return data


def calculate_annual_variation(
    series: pd.Series,
    method: str = "pct"
) -> pd.Series:
    """
    Calcule la variation annuelle d'une série temporelle.

    Parameters
    ----------
    series : pd.Series
        Série indexée par année.

    method : str
        'pct' : variation relative en pourcentage.
        'difference' : différence absolue entre deux années.

    Returns
    -------
    pd.Series
        Série annuelle des variations.

    Les années absentes sont réintroduites avant le calcul.
    Aucune variation n'est calculée entre deux années
    non consécutives.
    """

    data = _validate_series(series)

    if method not in {"pct", "difference"}:
        raise ValueError(
            "La méthode doit être 'pct' ou 'difference'."
        )

    # Reconstituer le calendrier annuel complet.
    # Les années sans observation restent NaN.
    full_years = range(data.index.min(), data.index.max() + 1)

    data = data.reindex(full_years)
    data.index.name = "Annee"

    if method == "difference":
        result = data.diff()

    else:
        # fill_method=None empêche le remplissage automatique
        # des valeurs manquantes.
        result = data.pct_change(fill_method=None) * 100

    return result.rename(
        "Variation_annuelle"
        if method == "difference"
        else "Variation_annuelle_%"
    )


def calculate_cagr(
    series: pd.Series,
    start_year: int,
    end_year: int
) -> float:
    """
    Calcule le taux de croissance annuel moyen composé (TCAM).

    Formule :
        CAGR = ((valeur_finale / valeur_initiale)
                ** (1 / nombre_annees) - 1) * 100

    Les valeurs initiale et finale doivent être positives.

    Attention :
    Le calcul repose sur les deux valeurs extrêmes de la période.
    Il ne nécessite pas que toutes les années intermédiaires
    soient disponibles.
    """

    data = _validate_series(series)

    if not isinstance(start_year, (int, np.integer)):
        raise TypeError("L'année de début doit être un entier.")

    if not isinstance(end_year, (int, np.integer)):
        raise TypeError("L'année de fin doit être un entier.")

    if start_year >= end_year:
        raise ValueError(
            "L'année de début doit être inférieure à l'année de fin."
        )

    if start_year not in data.index:
        raise ValueError(
            f"L'année initiale {start_year} est absente de la série."
        )

    if end_year not in data.index:
        raise ValueError(
            f"L'année finale {end_year} est absente de la série."
        )

    initial_value = data.loc[start_year]
    final_value = data.loc[end_year]

    if pd.isna(initial_value) or pd.isna(final_value):
        raise ValueError(
            "Les valeurs initiale et finale doivent être disponibles."
        )

    if initial_value <= 0 or final_value <= 0:
        raise ValueError(
            "Le TCAM nécessite des valeurs initiale et finale positives."
        )

    number_of_years = end_year - start_year

    cagr = (
        (final_value / initial_value) ** (1 / number_of_years) - 1
    ) * 100

    return float(cagr)
