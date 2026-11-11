
# Pays étudié : République démocratique du Congo
COUNTRY_CODE = "COD"

# Période d'analyse
START_YEAR = 1960
END_YEAR = 2024

# Dictionnaire des indicateurs macroéconomiques
INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "Croissance_PIB_%",
    "FP.CPI.TOTL.ZG": "Inflation_%",
    "SP.POP.TOTL": "Population_Totale",
    "FI.RES.TOTL.CD": "Reserves_USD",
    "PA.NUS.FCRF": "Taux_de_Change_CDF_USD",
    "SP.DYN.CDRT.IN": "Taux_Mortalite_Brute_1000",
    "SP.DYN.LE00.IN": "Esperance_Vie_Ans",
    "SL.UEM.TOTL.ZS": "Taux_Chomage_%",
    "NE.EXP.GNFS.CD": "Exportations_USD",
    "NE.IMP.GNFS.CD": "Importations_USD"
}
INDICATOR_TYPES = {
    "Croissance_PIB_%": "rate",
    "Inflation_%": "rate",
    "Taux_Chomage_%": "rate",
    "Exportations_USD": "level",
    "Importations_USD": "level",
    "Population_Totale": "level",
    "Reserves_USD": "level",
    "Taux_de_Change_CDF_USD": "level",
    "Esperance_Vie_Ans": "level",
    "Taux_Mortalite_Brute_1000": "rate"
}
INDICATOR_METADATA = {
    "Croissance_PIB_%": {
        "unit": "%",
        "variation_method": "difference",
        "variation_unit": "points de pourcentage"
    },

    "Inflation_%": {
        "unit": "%",
        "variation_method": "difference",
        "variation_unit": "points de pourcentage"
    },

    "Taux_Chomage_%": {
        "unit": "%",
        "variation_method": "difference",
        "variation_unit": "points de pourcentage"
    },

    "Taux_Mortalite_Brute_1000": {
        "unit": "décès pour 1 000 habitants",
        "variation_method": "difference",
        "variation_unit": "décès pour 1 000 habitants"
    },

    "Esperance_Vie_Ans": {
        "unit": "années",
        "variation_method": "difference",
        "variation_unit": "années"
    },

    "Taux_de_Change_CDF_USD": {
        "unit": "CDF pour 1 USD",
        "variation_method": "pct",
        "variation_unit": "%"
    },

    "Reserves_USD": {
        "unit": "USD courants",
        "variation_method": "pct",
        "variation_unit": "%"
    },

    "Exportations_USD": {
        "unit": "USD courants",
        "variation_method": "pct",
        "variation_unit": "%"
    },

    "Importations_USD": {
        "unit": "USD courants",
        "variation_method": "pct",
        "variation_unit": "%"
    },

    "Population_Totale": {
        "unit": "habitants",
        "variation_method": "pct",
        "variation_unit": "%"
    }
}