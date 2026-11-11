from src.data.data_loader import load_macro_data
from src.preprocessing.preprocessing import prepare_macro_data
from src.analysis.period_comaraison import compare_periods

# 1. Chargement et préparation
df = prepare_macro_data(load_macro_data())

# 2. Définition des périodes
periods = {
    "2000-2009": (2000, 2009),
    "2010-2019": (2010, 2019),
    "2020-2024": (2020, 2024)
}

# 3. Comparaison
result = compare_periods(df, periods)

# 4. Affichage
print("\nCOMPARAISON DES PERIODES ECONOMIQUES\n")
print(result.to_string())