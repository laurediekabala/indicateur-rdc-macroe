
from src.data.data_loader import load_macro_data

from src.preprocessing.missing_data import (
    build_missing_data_report,
    get_observed_series
)


# 1. Chargement des données
df = load_macro_data()


# 2. Rapport détaillé
report = build_missing_data_report(df)

print("\nRAPPORT DE DISPONIBILITE")
print(report.to_string())


# 3. Extraction des exportations disponibles
exports = get_observed_series(
    df,
    indicator="Exportations_USD"
)

print("\nEXPORTATIONS DISPONIBLES")
print(exports)


# 4. Extraction du chômage à partir de 1991
unemployment = get_observed_series(
    df,
    indicator="Taux_Chomage_%",
    start_year=1991
)

print("\nTAUX DE CHOMAGE DISPONIBLE DEPUIS 1991")
print(unemployment)


# 5. Vérification des données originales
print("\nDIMENSIONS INITIALES :", df.shape)
print("NOMBRE D'EXPORTATIONS DISPONIBLES :", len(exports))
print("NOMBRE D'ANNEES DE CHOMAGE DISPONIBLES :",
      len(unemployment))
