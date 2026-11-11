
import pandas as pd
import wbgapi as wb

from config.indicators import (
    COUNTRY_CODE,
    START_YEAR,
    END_YEAR,
    INDICATORS
)


def load_macro_data():
    """
    Récupère les indicateurs macroéconomiques
    de la RDC depuis l'API de la Banque mondiale.

    Returns
    -------
    pd.DataFrame
        DataFrame avec les années en index
        et les indicateurs en colonnes.
    """

    try:
        data = wb.data.DataFrame(
            list(INDICATORS.keys()),
            COUNTRY_CODE,
            time=range(START_YEAR, END_YEAR + 1)
        )

        # Renommer les indicateurs
        data = data.rename(index=INDICATORS)

        # Transposer pour avoir les années en lignes
        df = data.T.copy()

        # Convertir les années au format entier
        df.index = (
            df.index.astype(str)
            .str.replace("YR", "", regex=False)
            .astype(int)
        )

        df.index.name = "Annee"

        # Ordonner chronologiquement
        df = df.sort_index()

        return df

    except Exception as error:
        raise RuntimeError(
            f"Échec du chargement des données : {error}"
        ) from error
