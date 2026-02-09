# 📊 Dashboard Macroéconomique - République Démocratique du Congo

Un tableau de bord professionnel et interactif pour l'analyse des indicateurs macroéconomiques de la RDC, construit avec **Streamlit** et **Plotly**.

## 🎯 Objectif

Fournir une interface analytique complète pour visualiser et analyser les indicateurs macroéconomiques de la République Démocratique du Congo (1970-2024), incluant :

- **Croissance du PIB** 📈
- **Inflation** 💰
- **Population** 👥
- **Réserves de change** 💵
- **Taux de change CDF/USD** 💱
- **Taux de mortalité** 💔
- **Espérance de vie** 🏥
- **Taux de chômage** 📉
- **Exportations/Importations** 🌐

## ✨ Fonctionnalités Principales

### 📈 Analyse Univariée
- **Sélection d'indicateurs** : Choisissez n'importe quel indicateur pour une analyse approfondie
- **Indicateurs Clés (KPIs)** : Affichage des statistiques de croissance
- **Distribution** : Histogramme et boxplot côte à côte
- **Statistiques descriptives** : Tableau détaillé avec 13 métriques
- **Évolution temporelle** : Graphique interactif avec filtre par année
- **Taux de croissance** : Visualisation année sur année avec couleurs (vert/rouge)
- **Données annuelles** : Tableau complet avec gradients de couleur

### 🔗 Analyse de Corrélation
- **Matrice de corrélation** : Heatmap complète (Spearman)
- **Analyse bivariée** : Sélection de deux variables pour analyse détaillée
- **Test d'hypothèse** : Coefficient ρ, p-value et interprétation statistique
- **Scatter plot** : Graphique avec ligne de tendance OLS
- **Top 10 corrélations** : Les associations les plus fortes entre indicateurs

## 🛠️ Stack Technologique

| Composant | Version | Usage |
|-----------|---------|-------|
| **Python** | 3.11+ | Langage principal |
| **Streamlit** | 1.28+ | Framework web |
| **Plotly** | 5.17+ | Visualisations interactives |
| **Pandas** | 2.0+ | Manipulation de données |
| **NumPy** | 1.24+ | Calculs numériques |
| **SciPy** | 1.11+ | Analyse statistique |
| **wbgapi** | 1.0+ | API Banque Mondiale |
| **Statsmodels** | 0.14+ | Modèles statistiques |

## 📦 Installation

### Prérequis
- Python 3.11 ou supérieur
- pip ou conda

### Étapes d'installation

1. **Cloner le repository** (si applicable)
```bash
git clone https://github.com/votre-username/bcc-dashboard.git
cd BCC
```

2. **Créer un environnement virtuel**
```bash
python -m venv .venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### Démarrer le dashboard
```bash
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

### Configuration de base
- **Port** : Par défaut 8501
- **Layout** : Mode wide (full-width)
- **Sidebar** : Toujours visible

## 📊 Sources de Données

Les données proviennent de :
- **Banque Mondiale** (World Bank Open Data)
- **API wbgapi** pour récupération automatique
- **Période couverte** : 1970-2024
- **Mise à jour** : Annuelle

### Indicateurs Utilisés

| Code WB | Indicateur | Unité |
|---------|-----------|-------|
| NY.GDP.MKTP.KD.ZG | Croissance du PIB | % annuel |
| FP.CPI.TOTL.ZG | Inflation | % annuel |
| SP.POP.TOTL | Population totale | Nombre |
| FI.RES.TOTL.CD | Réserves de change | USD |
| PA.NUS.FCRF | Taux de change | CDF/USD |
| SP.DYN.CDRT.IN | Taux de mortalité brute | Par 1000 hab. |
| SP.DYN.LE00.IN | Espérance de vie | Années |
| SL.UEM.TOTL.ZS | Taux de chômage | % |
| NE.EXP.GNFS.CD | Exportations | USD |
| NE.IMP.GNFS.CD | Importations | USD |

## 📱 Responsivité

Le dashboard est **entièrement responsive** et optimisé pour :

- 🖥️ **Ordinateur de bureau** (1920px+)
- 💻 **Tablette** (768px-1200px)
- 📱 **Mobile** (480px-768px)
- 📲 **Petits appareils** (<480px)

**Media queries CSS** adaptent automatiquement :
- Taille des polices
- Espacement et padding
- Disposition des colonnes
- Hauteur des graphiques

## 🎨 Design

### Palette de Couleurs
- **Primaire** : Bleu #1f77b4
- **Accent** : Bleu foncé #0d5ca6
- **Success** : Vert #28a745
- **Warning** : Jaune #FFEB3B
- **Error** : Rouge #dc3545
- **Info/Contact** : Gris foncé #2c3e50

### Typographie
- **Font** : Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Titres** : Font-weight 700
- **Corps** : Font-weight 400-500

## 📋 Structure du Projet

```
BCC/
├── dashboard.py                 # Application Streamlit principale
├── bcc.py                       # Script d'extraction données (optionnel)
├── analyse.ipynb               # Notebook Jupyter pour exploration
├── analyse_complete_rdc.csv    # Données (générées)
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation (ce fichier)
├── .gitignore                  # Fichiers à ignorer git
└── .venv/                      # Environnement virtuel
```

## 🔧 Configuration Avancée

### Personnaliser le titre/icône
Dans `dashboard.py`, modifiez :
```python
st.set_page_config(
    page_title="Votre Titre",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Modifier les indicateurs
Dans `bcc.py` ou `dashboard.py`, changez le dictionnaire `indicateurs` :
```python
indicateurs = {
    'CODE_WB': 'Nom_Affichage',
    # Ajoutez d'autres codes...
}
```

### Changer la plage de dates
Modifiez la ligne :
```python
data = wb.data.DataFrame(indicateurs.keys(), 'COD', time=range(1970, 2025))
```

## 📈 Méthodes Statistiques

### Corrélation
- **Coefficient** : Spearman ρ (robuste aux outliers)
- **Hypothèse H0** : ρ = 0 (pas de corrélation)
- **Seuil** : α = 0.05
- **Interprétation** :
  - |ρ| < 0.3 : Corrélation faible
  - 0.3 ≤ |ρ| < 0.7 : Corrélation modérée
  - |ρ| ≥ 0.7 : Corrélation forte

### Croissance
- **Formule** : (Valeur_t / Valeur_t-1 - 1) × 100
- **Période** : Année sur année

## 🐛 Dépannage

### Erreur : "No module named 'streamlit'"
```bash
pip install streamlit
```

### Erreur : "wbgapi connection error"
- Vérifiez votre connexion Internet
- L'API World Bank peut être temporairement indisponible

### Graphiques non affichés
- Vérifiez que Plotly est installé : `pip install plotly`
- Actualisez la page du navigateur

## 📞 Contact

**Laurédie Kabala**
- 📧 Email : laurediekabala@gmail.com
- 📱 WhatsApp : +243 814 900 752
- 💼 Profil : Data Scientist & Analyste Quantitatif
- 🎓 Expertise : Macroéconomie • Finance • Télécommunications

## 📄 Licence

Ce projet est fourni à titre informatif. Les données proviennent de la Banque Mondiale (domaine public).

## 🤝 Contribution

Les suggestions et améliorations sont bienvenues ! Pour contribuer :
1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📚 Ressources Utiles

- [Documentation Streamlit](https://docs.streamlit.io)
- [Documentation Plotly](https://plotly.com/python/)
- [API Banque Mondiale](https://data.worldbank.org)
- [wbgapi Documentation](https://github.com/mmngreco/wbgapi)

## ✅ Checklist de Déploiement

- [ ] Tester sur desktop, tablette et mobile
- [ ] Vérifier la connexion API
- [ ] Valider les calculs statistiques
- [ ] Tester tous les filtres et sélecteurs
- [ ] Vérifier l'affichage sur navigateurs différents
- [ ] Documenter les modifications personnalisées

---

**Dernière mise à jour** : 9 février 2026  
**Version** : 1.0.0  
**Statut** : Production-Ready ✅
