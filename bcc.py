import wbgapi as wb
import pandas as pd

# Configuration
pays = 'COD' # RD Congo

# Dictionnaire enrichi avec les indicateurs sociaux
indicateurs = {
    'NY.GDP.MKTP.KD.ZG': 'Croissance_PIB_%',
    'FP.CPI.TOTL.ZG': 'Inflation_%',
    'SP.POP.TOTL': 'Population_Totale',
    'FI.RES.TOTL.CD': 'Reserves_Change_USD',
    'PA.NUS.FCRF': 'Taux_de_Change_CDF_USD',
    'SP.DYN.CDRT.IN': 'Taux_Mortalite_Brute_1000', # Mortalité
    'SP.DYN.LE00.IN': 'Esperance_Vie_Ans'          # Bonus pour le contexte
}

print(f"Extraction des données socio-économiques pour la RDC...")

# Récupération (1960-2024 pour avoir une vue historique solide)
data = wb.data.DataFrame(indicateurs.keys(), pays, time=range(1970, 2025))

# Renommage et pivotement
data.index = [indicateurs[i] for i in data.index.get_level_values(0)]
df_final = data.T
df_final.index = [annee.replace('YR', '') for annee in df_final.index]

# Affichage des 5 dernières années
print("\n--- Tableau de Bord Intégré (RDC) ---")
print(df_final.tail(5))

# Sauvegarde
df_final.to_csv('analyse_complete_rdc.csv')