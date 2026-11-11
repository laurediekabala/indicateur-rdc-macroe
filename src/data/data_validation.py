
import numpy as np
import pandas as pd


def _validate_dataframe(df: pd.DataFrame) -> None:
    """
    Vérifie la structure générale d'un DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Les données doivent être un DataFrame pandas."
        )

    if df.empty:
        raise ValueError(
            "Le DataFrame est vide."
        )

    if df.columns.empty:
        raise ValueError(
            "Le DataFrame ne contient aucune colonne."
        )

    if df.columns.duplicated().any():
        raise ValueError(
            "Le DataFrame contient des colonnes dupliquées."
        )


def _validate_year_index(index: pd.Index) -> pd.Index:
    """
    Valide un index annuel et retourne des années entières.

    Contrôles :
    - Années numériques.
    - Absence de valeurs infinies.
    - Années entières.
    - Absence de doublons.
    - Ordre chronologique croissant.
    """

    try:
        years = pd.to_numeric(index, errors="raise")
        years = np.asarray(years, dtype=float)

    except (ValueError, TypeError):
        raise ValueError(
            "L'index doit contenir des années numériques."
        ) from None

    if not np.isfinite(years).all():
        raise ValueError(
            "L'index contient des années invalides."
        )

    if not np.equal(years, np.floor(years)).all():
        raise ValueError(
            "Les années doivent être des nombres entiers."
        )

    years = pd.Index(
        years.astype(int),
        name="Annee"
    )

    if years.duplicated().any():
        raise ValueError(
            "Le DataFrame contient des années dupliquées."
        )

    if not years.is_monotonic_increasing:
        raise ValueError(
            "Les années ne sont pas classées chronologiquement."
        )

    return years


def validate_macro_data(df: pd.DataFrame) -> dict:
    """
    Contrôle la qualité d'un DataFrame macroéconomique.

    Retourne un rapport de validation sans modifier
    les données originales.
    """

    # 1. Validation de la structure
    _validate_dataframe(df)

    # 2. Validation des années
    years = _validate_year_index(df.index)

    # 3. Détection des années absentes
    expected_years = set(
        range(years.min(), years.max() + 1)
    )

    missing_years = sorted(
        expected_years - set(years)
    )

    # 4. Analyse des colonnes
    non_numeric = []
    missing_values = {}
    infinite_values = {}

    for column in df.columns:

        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):
            non_numeric.append(column)
            continue

        missing_count = int(
            series.isna().sum()
        )

        if missing_count > 0:
            missing_values[column] = missing_count

        numeric_values = series.dropna().to_numpy(
            dtype=float
        )

        infinite_count = int(
            np.isinf(numeric_values).sum()
        )

        if infinite_count > 0:
            infinite_values[column] = infinite_count

    # 5. Construction du rapport
    report = {
        "nombre_observations": len(df),
        "nombre_indicateurs": len(df.columns),
        "premiere_annee": int(years.min()),
        "derniere_annee": int(years.max()),
        "annees_manquantes": missing_years,
        "colonnes_non_numeriques": non_numeric,
        "valeurs_manquantes": missing_values,
        "valeurs_infinies": infinite_values,
    }

    return report


def missing_values_report(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Produit un rapport détaillé des valeurs manquantes.

    Les pourcentages sont calculés sur le nombre total
    d'observations de chaque indicateur.
    """

    _validate_dataframe(df)

    report = pd.DataFrame({
        "nombre_manquant": df.isna().sum(),
        "pourcentage_manquant": (
            df.isna().mean() * 100
        )
    })

    report["pourcentage_disponible"] = (
        100 - report["pourcentage_manquant"]
    )

    report["statut"] = np.select(
        [
            report["pourcentage_manquant"] == 0,
            report["pourcentage_manquant"] <= 5,
            report["pourcentage_manquant"] <= 20,
            report["pourcentage_manquant"] <= 50
        ],
        [
            "Complet",
            "Très bonne disponibilité",
            "Disponibilité acceptable",
            "Disponibilité limitée"
        ],
        default="Disponibilité très faible"
    )

    return report.sort_values(
        by="pourcentage_manquant",
        ascending=False
    )


def missingness_timeline(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyse la répartition temporelle des valeurs manquantes.

    Calcule pour chaque indicateur :
    - Le nombre d'années manquantes.
    - Les années concernées.
    - La longueur maximale d'une séquence
      d'années consécutives manquantes.
    """

    _validate_dataframe(df)

    years = _validate_year_index(df.index)

    results = []

    for column in df.columns:

        missing_years = sorted(
            years[df[column].isna()].tolist()
        )

        # Calcul de la plus longue séquence manquante
        longest_gap = 0
        current_gap = 0
        previous_year = None

        for year in missing_years:

            if (
                previous_year is not None
                and year == previous_year + 1
            ):
                current_gap += 1
            else:
                current_gap = 1

            longest_gap = max(
                longest_gap,
                current_gap
            )

            previous_year = year

        results.append({
            "indicateur": column,
            "nombre_manquant": len(missing_years),
            "annees_manquantes": missing_years,
            "plus_longue_lacune": longest_gap
        })

    return pd.DataFrame(results)
