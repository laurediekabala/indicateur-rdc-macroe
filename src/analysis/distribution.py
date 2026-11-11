
import numpy as np
import pandas as pd


def distribution_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse la distribution statistique de chaque indicateur.

    Les valeurs manquantes sont ignorées individuellement.
    Les valeurs atypiques sont détectées avec la méthode de Tukey.

    Aucune observation n'est supprimée ou modifiée.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contenant les indicateurs en colonnes.

    Returns
    -------
    pd.DataFrame
        Rapport statistique sur la distribution des indicateurs.
    """

    # 1. Vérifier la structure du DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Les données doivent être un DataFrame pandas."
        )

    if df.empty:
        raise ValueError(
            "Le DataFrame est vide."
        )

    if df.columns.duplicated().any():
        raise ValueError(
            "Colonnes dupliquées détectées."
        )

    results = []

    # 2. Analyser chaque indicateur séparément
    for column in df.columns:

        series = df[column]

        # 3. Gérer les indicateurs entièrement vides
        if series.isna().all():

            results.append({
                "indicateur": column,
                "n": 0,
                "asymetrie": None,
                "kurtosis": None,
                "iqr": None,
                "borne_inferieure": None,
                "borne_superieure": None,
                "nombre_valeurs_atypiques": None,
                "taux_valeurs_atypiques": None
            })

            continue

        # 4. Vérifier le type numérique
        if not pd.api.types.is_numeric_dtype(series):
            raise TypeError(
                f"L'indicateur {column} n'est pas numérique."
            )

        # 5. Conserver uniquement les observations disponibles
        observed = series.dropna()

        # 6. Vérifier les valeurs infinies
        if not np.isfinite(
            observed.to_numpy(dtype=float)
        ).all():

            raise ValueError(
                f"Valeurs infinies détectées dans {column}."
            )

        # 7. Calculer les quartiles
        q1 = observed.quantile(0.25)
        q3 = observed.quantile(0.75)

        # 8. Calculer l'écart interquartile
        iqr = q3 - q1

        # 9. Déterminer les bornes de Tukey
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # 10. Détecter les valeurs potentiellement atypiques
        outliers = (
            (observed < lower_bound)
            | (observed > upper_bound)
        )

        # 11. Calculer les statistiques de distribution
        results.append({

            "indicateur": column,

            "n": int(observed.count()),

            "asymetrie": observed.skew(),

            "kurtosis": observed.kurt(),

            "iqr": iqr,

            "borne_inferieure": lower_bound,

            "borne_superieure": upper_bound,

            "nombre_valeurs_atypiques": int(
                outliers.sum()
            ),

            "taux_valeurs_atypiques": round(
                outliers.mean() * 100, 2
            )
        })

    # 12. Construire le rapport final
    report = (
        pd.DataFrame(results)
        .set_index("indicateur")
    )

    return report
