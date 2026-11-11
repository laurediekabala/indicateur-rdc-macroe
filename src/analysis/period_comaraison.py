
import numpy as np
import pandas as pd

from config.indicators import INDICATOR_METADATA


def compare_periods(
    df: pd.DataFrame,
    periods: dict
) -> pd.DataFrame:
    """
    Compare les indicateurs macroéconomiques sur plusieurs périodes.

    Les métadonnées définissent :
    - l'unité de mesure ;
    - la méthode de variation ;
    - l'unité de la variation.

    Le statut de période indique la disponibilité des observations :
    - Complète : toutes les années attendues sont disponibles.
    - Partielle : certaines années sont manquantes.
    - Indisponible : aucune observation disponible.
    """

    # 1. Validation de la structure
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Les données doivent être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    if df.columns.duplicated().any():
        raise ValueError("Colonnes dupliquées détectées.")

    if not isinstance(periods, dict) or not periods:
        raise ValueError("Les périodes doivent être un dictionnaire non vide.")

    # 2. Validation des années
    try:
        years = pd.to_numeric(df.index, errors="raise")
        years = np.asarray(years, dtype=float)

        if not np.isfinite(years).all():
            raise ValueError("Années invalides.")

        if not np.equal(years, np.floor(years)).all():
            raise ValueError("Les années doivent être entières.")

        years = years.astype(int)

    except (ValueError, TypeError) as error:
        raise ValueError(
            f"Index annuel invalide : {error}"
        ) from error

    if pd.Index(years).duplicated().any():
        raise ValueError("Des années sont dupliquées.")

    data = df.copy(deep=True)
    data.index = years
    data.index.name = "Annee"
    data = data.sort_index()

    # 3. Validation des périodes
    for name, bounds in periods.items():

        if not isinstance(bounds, (tuple, list)) or len(bounds) != 2:
            raise ValueError(
                f"La période {name} doit contenir deux années."
            )

        start_year, end_year = bounds

        if (
            not isinstance(start_year, (int, np.integer))
            or isinstance(start_year, (bool, np.bool_))
        ):
            raise TypeError(f"Année de début invalide pour {name}.")

        if (
            not isinstance(end_year, (int, np.integer))
            or isinstance(end_year, (bool, np.bool_))
        ):
            raise TypeError(f"Année de fin invalide pour {name}.")

        if start_year > end_year:
            raise ValueError(
                f"Période chronologique invalide : {name}."
            )

    # 4. Validation des métadonnées
    missing_metadata = set(data.columns) - set(INDICATOR_METADATA)

    if missing_metadata:
        raise ValueError(
            f"Métadonnées manquantes pour : {missing_metadata}"
        )

    required_fields = {
        "unit",
        "variation_method",
        "variation_unit"
    }

    for indicator in data.columns:

        metadata = INDICATOR_METADATA[indicator]

        if not isinstance(metadata, dict):
            raise TypeError(
                f"Les métadonnées de {indicator} doivent être un dictionnaire."
            )

        missing_fields = required_fields - set(metadata)

        if missing_fields:
            raise ValueError(
                f"Champs manquants dans les métadonnées de "
                f"{indicator} : {missing_fields}"
            )

        if metadata["variation_method"] not in {"difference", "pct"}:
            raise ValueError(
                f"Méthode de variation invalide pour {indicator}."
            )

        for field in required_fields:
            if (
                not isinstance(metadata[field], str)
                or not metadata[field].strip()
            ):
                raise ValueError(
                    f"Métadonnée invalide : {field} pour {indicator}."
                )

    # 5. Calcul des statistiques
    results = []

    for indicator in data.columns:

        series = data[indicator]

        if not pd.api.types.is_numeric_dtype(series):
            raise TypeError(
                f"L'indicateur {indicator} n'est pas numérique."
            )

        observed_values = series.dropna().to_numpy(dtype=float)

        if not np.isfinite(observed_values).all():
            raise ValueError(
                f"Valeurs infinies détectées dans {indicator}."
            )

        metadata = INDICATOR_METADATA[indicator]

        unit = metadata["unit"]
        variation_method = metadata["variation_method"]
        variation_unit = metadata["variation_unit"]

        for period_name, (start_year, end_year) in periods.items():

            expected_years = end_year - start_year + 1

            period_data = series.loc[
                (series.index >= start_year)
                & (series.index <= end_year)
            ].dropna()

            n = int(period_data.count())

            # 6. Calcul du taux de disponibilité
            availability_rate = (
                n / expected_years
            ) * 100

            # 7. Classification de la période
            if n == 0:
                statut_periode = "Indisponible"

            elif n == expected_years:
                statut_periode = "Complète"

            else:
                statut_periode = "Partielle"

            # 8. Gestion des périodes sans observations
            if n == 0:

                results.append({
                    "indicateur": indicator,
                    "periode": period_name,
                    "n": 0,
                    "taux_disponibilite": availability_rate,
                    "statut_periode": statut_periode,
                    "annee_initiale": None,
                    "annee_finale": None,
                    "moyenne": np.nan,
                    "mediane": np.nan,
                    "minimum": np.nan,
                    "maximum": np.nan,
                    "valeur_initiale": np.nan,
                    "valeur_finale": np.nan,
                    "variation_absolue": np.nan,
                    "variation_pct": np.nan,
                    "unite": unit,
                    "variation_method": variation_method,
                    "unite_variation": variation_unit
                })

                continue

            # 9. Valeurs initiale et finale
            initial_value = period_data.iloc[0]
            final_value = period_data.iloc[-1]

            # 10. Calcul des variations
            variation_absolute = final_value - initial_value

            variation_pct = np.nan

            if variation_method == "pct" and initial_value != 0:

                variation_pct = (
                    (final_value / initial_value) - 1
                ) * 100

            # 11. Construction du résultat
            results.append({
                "indicateur": indicator,
                "periode": period_name,
                "n": n,
                "taux_disponibilite": availability_rate,
                "statut_periode": statut_periode,
                "annee_initiale": int(period_data.index[0]),
                "annee_finale": int(period_data.index[-1]),
                "moyenne": period_data.mean(),
                "mediane": period_data.median(),
                "minimum": period_data.min(),
                "maximum": period_data.max(),
                "valeur_initiale": initial_value,
                "valeur_finale": final_value,
                "variation_absolue": variation_absolute,
                "variation_pct": variation_pct,
                "unite": unit,
                "variation_method": variation_method,
                "unite_variation": variation_unit
            })

    # 12. Construction du rapport final
    report = (
        pd.DataFrame(results)
        .set_index(["indicateur", "periode"])
    )

    return report
