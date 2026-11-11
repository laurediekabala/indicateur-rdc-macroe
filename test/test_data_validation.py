
from src.data.data_loader import load_macro_data
from src.data.data_validation import validate_macro_data,missing_values_report, missingness_timeline
# Récupération des données
df = load_macro_data()
# Validation
report = validate_macro_data(df)

# Affichage du rapport
for key, value in report.items():
    print(f"{key} : {value}")


print("\nRAPPORT DE DISPONIBILITÉ DES DONNÉES")

missing_report = missing_values_report(df)

print(missing_report)    

print("\nDIAGNOSTIC TEMPOREL DES VALEURS MANQUANTES")

timeline = missingness_timeline(df)

print(timeline.to_string(index=False))