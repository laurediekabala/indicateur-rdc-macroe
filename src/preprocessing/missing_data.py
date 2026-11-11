
import numpy as np
import pandas as pd


def _validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie la structure du DataFrame et retourne
    une copie triée chronologiquement.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Les données doivent être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    if df.columns.duplicated().any():
        raise ValueError("Des colonnes sont dupliquées.")

    try:
        years = pd.to_numeric(df.index, errors="raise")
        years = np.asarray(years, dtype=float)

        if not np.isfinite(years).all():
            raise ValueError("Les années contiennent des valeurs invalides.")

        if not np.equal(years, np.floor(years)).all():
            raise ValueError("Les années doivent être entières.")

        years = years.astype(int)

    except (ValueError, TypeError) as error:
        raise ValueError(f"Index des années invalide : {error}") from error

    if pd.Index(years).duplicated().any():
        raise ValueError("Des années sont dupliquées.")

    data = df.copy(deep=True)
    data.index = years
    data.index.name = "Annee"

    return data.sort_index()


def _find_missing_periods(missing_years: list) -> list:
    """
    Regroupe les années manquantes consécutives en périodes.
    Exemple : [1960, 1961, 1962, 1965] devient
    [(1960, 1962), (1965, 1965)].
    """

    if not missing_years:
        return []

    periods = []
    start = previous = missing_years[0]

    for year in missing_years[1:]:

        if year == previous + 1:
            previous = year

        else:
            periods.append((start, previous))
            start = previous = year

    periods.append((start, previous))

    return periods


def build_missing_data_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Produit un diagnostic détaillé de disponibilité
    pour chaque indicateur.
    """

    data = _validate_dataframe(df)
    results = []

    for column in data.columns:

        series = data[column]

        missing_years = sorted(
            data.index[series.isna()].tolist()
        )

        available_years = data.index[series.notna()].tolist()

        periods = _find_missing_periods(missing_years)

        results.append({
            "indicateur": column,
            "observations_disponibles": len(available_years),
            "nombre_manquant": len(missing_years),
            "taux_disponibilite": round(
                series.notna().mean() * 100, 2
            ),
            "premiere_annee_disponible": (
                min(available_years) if available_years else None
            ),
            "derniere_annee_disponible": (
                max(available_years) if available_years else None
            ),
            "periodes_manquantes": periods,
            "annees_manquantes": missing_years
        })

    return (
        pd.DataFrame(results)
        .set_index("indicateur")
        .sort_values("taux_disponibilite")
    )


def get_observed_series(
    df: pd.DataFrame,
    indicator: str,
    start_year: int = None,
    end_year: int = None
) -> pd.Series:
    """
    Extrait les observations réellement disponibles
    pour un indicateur, sur une période donnée.

    Aucune interpolation ni imputation n'est effectuée.
    """

    data = _validate_dataframe(df)

    if indicator not in data.columns:
        raise KeyError(f"Indicateur introuvable : {indicator}")

    if start_year is not None and end_year is not None:
        if start_year > end_year:
            raise ValueError(
                "L'année de début doit précéder l'année de fin."
            )

    series = data[indicator].copy()

    if start_year is not None:
        series = series.loc[series.index >= start_year]

    if end_year is not None:
        series = series.loc[series.index <= end_year]

    # Conserver uniquement les observations disponibles
    series = series.dropna()

    return series
