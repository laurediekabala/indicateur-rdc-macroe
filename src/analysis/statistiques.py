import numpy as np
import pandas as pd


def build_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques descriptives de chaque indicateur
    macroéconomique à partir des observations disponibles.

    Les valeurs manquantes sont exclues individuellement
    pour chaque indicateur. Aucune imputation n'est effectuée.

    L'écart-type et la variance sont calculés avec ddof=1
    (estimateurs d'échantillon).

    Parameters
    ----------
    df : pd.DataFrame
        Données macroéconomiques avec les années en index.

    Returns
    -------
    pd.DataFrame
        Tableau des statistiques descriptives par indicateur.
    """

    # 1. Vérifier la structure
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Les données doivent être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    if df.columns.duplicated().any():
        raise ValueError("Le DataFrame contient des colonnes dupliquées.")

    # 2. Vérifier les années
    try:
        years = pd.to_numeric(df.index, errors="raise")
        years = np.asarray(years, dtype=float)

        if not np.isfinite(years).all():
            raise ValueError("Les années contiennent des valeurs invalides.")

        if not np.equal(years, np.floor(years)).all():
            raise ValueError("Les années doivent être entières.")

        years = years.astype(int)

    except (ValueError, TypeError) as error:
        raise ValueError(
            f"Index des années invalide : {error}"
        ) from error

    if pd.Index(years).duplicated().any():
        raise ValueError("Le DataFrame contient des années dupliquées.")

    # 3. Travailler sur une copie triée
    data = df.copy(deep=True)
    data.index = years
    data.index.name = "Annee"
    data = data.sort_index()

    results = []

    # 4. Calculer les statistiques indicateur par indicateur
    for column in data.columns:

        series = data[column]

        if not pd.api.types.is_numeric_dtype(series):
            raise TypeError(
                f"L'indicateur {column} contient des valeurs non numériques."
            )

        observed = series.dropna()

        if np.isinf(observed.to_numpy(dtype=float)).any():
            raise ValueError(
                f"L'indicateur {column} contient des valeurs infinies."
            )

        # Cas où aucune observation n'est disponible
        if observed.empty:
            results.append({
                "indicateur": column,
                "n": 0,
                "annee_debut": None,
                "annee_fin": None,
                "moyenne": np.nan,
                "mediane": np.nan,
                "ecart_type": np.nan,
                "variance": np.nan,
                "minimum": np.nan,
                "q1": np.nan,
                "q3": np.nan,
                "maximum": np.nan,
                "ecart_interquartile": np.nan
            })
            continue

        # 5. Calcul des quartiles
        q1 = observed.quantile(0.25)
        q3 = observed.quantile(0.75)

        results.append({
            "indicateur": column,
            "n": int(observed.count()),
            "annee_debut": int(observed.index.min()),
            "annee_fin": int(observed.index.max()),
            "moyenne": observed.mean(),
            "mediane": observed.median(),
            "ecart_type": observed.std(ddof=1),
            "variance": observed.var(ddof=1),
            "minimum": observed.min(),
            "q1": q1,
            "q3": q3,
            "maximum": observed.max(),
            "ecart_interquartile": q3 - q1
        })

    # 6. Construire le tableau final
    report = (
        pd.DataFrame(results)
        .set_index("indicateur")
    )

    return report