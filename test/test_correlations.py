
import pandas as pd

from src.analysis.correlations import (
    calculate_correlations,
    calculate_correlation_counts
)
from src.analysis.correlations import (
    calculate_indicator_variations,
    calculate_correlations_on_variations
)


# Jeu de données fictif pour vérifier les calculs
data = pd.DataFrame({
    "Croissance_PIB_%": [2, 3, 4, 5, 6, 7],
    "Exportations_USD": [10, 20, 30, 40, 50, 60],
    "Inflation_%": [8, 7, 6, 5, 4, 3],
    "Population_Totale": [100, 110, 120, 130, 140, 150]
})

# Pearson
pearson = calculate_correlations(
    data,
    method="pearson"
)

print("\nMATRICE DE CORRELATION DE PEARSON")
print(pearson.round(3).to_string())

# Spearman
spearman = calculate_correlations(
    data,
    method="spearman"
)

print("\nMATRICE DE CORRELATION DE SPEARMAN")
print(spearman.round(3).to_string())

# Jeu de données avec valeurs manquantes et relation non linéaire
data_missing = pd.DataFrame({
    "PIB": [1, 2, 3, 4, 5, 6],
    "Exportations": [2, 4, None, 8, 10, 12],
    "Inflation": [10, 9, 8, 7, 6, 5],
    "Population": [1, 4, 9, 16, 25, 36]
})

# Calcul Pearson
pearson_missing = calculate_correlations(
    data_missing,
    method="pearson",
    min_periods=5
)

print("\nPEARSON AVEC VALEURS MANQUANTES")
print(pearson_missing.round(3).to_string())

# Calcul Spearman
spearman_missing = calculate_correlations(
    data_missing,
    method="spearman",
    min_periods=5
)

print("\nSPEARMAN AVEC VALEURS MANQUANTES")
print(spearman_missing.round(3).to_string())
# Nombre d'observations communes
counts = calculate_correlation_counts(data_missing)

print("\nNOMBRE D'OBSERVATIONS COMMUNES")
print(counts.to_string())

from src.data.data_loader import load_macro_data
from src.preprocessing.preprocessing import prepare_macro_data


# Chargement des données réelles
df_macro = prepare_macro_data(load_macro_data())

# Corrélations de Pearson
corr_macro = calculate_correlations(
    df_macro,
    method="pearson",
    min_periods=10
)

# Nombre d'observations communes
counts_macro = calculate_correlation_counts(df_macro)

print("\nCORRELATIONS MACROECONOMIQUES - PEARSON")
print(corr_macro.round(3).to_string())

print("\nNOMBRE D'OBSERVATIONS COMMUNES")
print(counts_macro.to_string())


from src.data.data_loader import load_macro_data
from src.preprocessing.preprocessing import prepare_macro_data


# Chargement des données réelles
df_macro = prepare_macro_data(load_macro_data())

# Calcul des variations annuelles
variations = calculate_indicator_variations(df_macro)

print("\nVARIATIONS ANNUELLES DES INDICATEURS")
print(variations.tail(10).round(3).to_string())

# Corrélations sur les variations annuelles
corr_variations = calculate_correlations_on_variations(
    df_macro,
    method="pearson",
    min_periods=10
)

print("\nCORRELATIONS DE PEARSON SUR LES VARIATIONS")
print(corr_variations.round(3).to_string())

# Nombre d'observations communes
counts_variations = calculate_correlation_counts(variations)

print("\nOBSERVATIONS COMMUNES SUR LES VARIATIONS")
print(counts_variations.to_string())
