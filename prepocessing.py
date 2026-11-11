
from src.data.data_loader import load_macro_data
from src.preprocessing.preprocessing import prepare_macro_data


# Chargement des données brutes
df_raw = load_macro_data()

# Préparation des données
df_prepared = prepare_macro_data(df_raw)

# Vérification
print("Dimensions des données brutes :", df_raw.shape)
print("Dimensions après préparation :", df_prepared.shape)

print("\nAperçu des données préparées :")
print(df_prepared.head())

print("\nValeurs manquantes après préparation :")
print(df_prepared.isna().sum())

# Vérifier que les données brutes n'ont pas été modifiées
print(
    "\nDonnées brutes conservées :",
    df_raw.equals(df_prepared)
)
