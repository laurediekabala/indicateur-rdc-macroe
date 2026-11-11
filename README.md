# 📊 Analyse des indicateurs macroéconomiques de la République Démocratique du Congo

Une application interactive d'analyse macroéconomique développée avec **Python, Streamlit et Plotly**, destinée à explorer, visualiser et analyser l'évolution des principaux indicateurs économiques et démographiques de la République Démocratique du Congo (RDC) sur la période **1960–2024**.

## 🎯 1. Objectif du projet

Ce projet vise à mettre à disposition un outil d'analyse statistique permettant de suivre l'évolution de l'économie congolaise à travers différents indicateurs macroéconomiques.

L'application permet notamment de :

- Explorer l'évolution historique des indicateurs économiques.
- Produire des statistiques descriptives.
- Étudier la distribution des variables.
- Analyser les variations annuelles.
- Comparer différentes périodes économiques.
- Identifier les relations statistiques entre les indicateurs.
- Évaluer la disponibilité et la qualité des données utilisées.

L'objectif est de faciliter l'analyse économique et de fournir une base quantitative pour l'interprétation des tendances macroéconomiques de la RDC.

## 📌 2. Indicateurs macroéconomiques étudiés

L'application exploite dix indicateurs répartis entre plusieurs dimensions économiques et démographiques.

| Indicateur | Description | Unité |
|---|---|---|
| Croissance du PIB | Croissance annuelle du produit intérieur brut | % |
| Inflation | Variation annuelle des prix à la consommation | % |
| Population totale | Population totale du pays | Habitants |
| Réserves de change | Réserves totales en devises | USD |
| Taux de change | Taux de change entre le franc congolais et le dollar américain | CDF/USD |
| Taux de chômage | Part de la population active au chômage | % |
| Taux de mortalité brute | Nombre de décès pour 1 000 habitants | Pour 1 000 habitants |
| Espérance de vie | Espérance de vie à la naissance | Années |
| Exportations | Valeur des exportations de biens et services | USD |
| Importations | Valeur des importations de biens et services | USD |

**Période de référence :** 1960–2024.

La disponibilité effective varie selon les indicateurs. Toutes les séries ne couvrent pas nécessairement l'ensemble de la période.

## ✨ 3. Fonctionnalités de l'application

L'application est organisée autour de sept espaces d'analyse.

### 3.1. Vue d'ensemble

Cette section présente une vision synthétique des données macroéconomiques.

Elle permet de consulter les principaux indicateurs, leur évolution générale et les informations essentielles sur le jeu de données.

### 3.2. Statistiques descriptives

Cette section permet de caractériser les propriétés statistiques des indicateurs.

Les analyses portent notamment sur :

- Le nombre d'observations disponibles.
- La moyenne arithmétique.
- La médiane.
- L'écart-type.
- La variance.
- Les valeurs minimales et maximales.
- Les quartiles et autres mesures de position et de dispersion.

Ces statistiques permettent de comprendre le comportement général des variables et leur variabilité dans le temps.

### 3.3. Distribution statistique

Cette section permet d'étudier la distribution des indicateurs à travers des représentations graphiques et des mesures statistiques.

Les visualisations permettent notamment d'examiner :

- La concentration des observations.
- La dispersion des valeurs.
- L'asymétrie des distributions.
- La présence de valeurs extrêmes.
- Les différences de distribution entre les indicateurs.

Les graphiques facilitent l'identification des caractéristiques statistiques pouvant influencer l'interprétation des séries.

### 3.4. Analyse temporelle

Cette section étudie l'évolution des indicateurs dans le temps.

Elle permet notamment de :

- Visualiser les séries chronologiques.
- Examiner les variations annuelles.
- Calculer les différences absolues entre deux années successives.
- Calculer les variations relatives en pourcentage lorsque cela est statistiquement pertinent.
- Étudier les tendances et les changements observés sur la période.

Les méthodes de calcul sont adaptées à la nature de chaque indicateur.

### 3.5. Comparaison des périodes économiques

Cette section permet de comparer les performances des indicateurs entre plusieurs périodes.

Les statistiques calculées comprennent notamment :

- Le nombre d'observations disponibles.
- Le taux de disponibilité.
- La première et la dernière année observées.
- La moyenne et la médiane.
- Les valeurs minimales et maximales.
- Les valeurs initiales et finales.
- La variation absolue.
- La variation relative, lorsque son calcul est pertinent.

Cette fonctionnalité permet de mettre en évidence les différences entre plusieurs périodes économiques.

### 3.6. Corrélations économiques

Cette section examine les relations statistiques entre les différents indicateurs macroéconomiques.

Elle propose notamment :

- Une matrice de corrélation.
- Le coefficient de corrélation de Pearson.
- Le coefficient de corrélation de Spearman.
- Les tests statistiques associés.
- Les p-values.
- Les effectifs d'observations utilisés pour chaque paire de variables.

L'analyse permet d'identifier les associations statistiques entre les indicateurs.

**Précaution méthodologique :** une corrélation statistique ne démontre pas une relation de causalité. Les tendances temporelles communes peuvent également influencer les coefficients obtenus.

### 3.7. Qualité des données

Cette section est consacrée au diagnostic de la qualité et de la disponibilité des données.

Elle permet notamment de :

- Vérifier la structure du jeu de données.
- Identifier les valeurs manquantes.
- Calculer les taux de disponibilité.
- Identifier les périodes incomplètes.
- Examiner les années disponibles pour chaque indicateur.
- Produire des rapports de validation.

L'objectif est de rendre les limites des données visibles avant toute interprétation statistique.

**Important :** les valeurs manquantes ne sont pas automatiquement remplacées par interpolation ou imputation. Les analyses doivent tenir compte de la couverture réelle de chaque série.

## 🛠️ 4. Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3.11+ | Langage principal |
| Streamlit | Interface web interactive |
| Plotly | Visualisations interactives |
| Pandas | Manipulation et analyse des données |
| NumPy | Calculs numériques |
| SciPy | Méthodes et tests statistiques |
| Statsmodels | Outils d'analyse statistique |
| wbgapi | Accès aux données de la Banque mondiale |

Les versions exactes des dépendances sont définies dans le fichier `requirements.txt`.

## 🏗️ 5. Architecture du projet

Le projet adopte une architecture modulaire afin de séparer les responsabilités et de faciliter la maintenance et l'évolution de l'application.

```text
indicateur-rdc-macroe/
│
├── dashboard.py
│
├── config/
│   └── indicators.py
│
├── src/
│   ├── data/
│   │   ├── data_loader.py
│   │   └── data_validation.py
│   │
│   ├── preprocessing/
│   │   ├── preprocessing.py
│   │   └── missing_data.py
│   │
│   └── analysis/
│       ├── statistiques.py
│       ├── distribution.py
│       ├── times_series.py
│       ├── period_comaraison.py
│       └── correlations.py
│
├── test/
│   ├── test_data_validation.py
│   ├── missing_data_test.py
│   ├── test_distribution.py
│   └── ...
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

*Remarque : cette arborescence présente les principaux modules du projet. Les fichiers de tests et de configuration supplémentaires peuvent être ajoutés au fur et à mesure de son évolution.*

### Responsabilités des principaux modules

| Module | Responsabilité |
|---|---|
| `config/indicators.py` | Configuration et métadonnées des indicateurs |
| `src/data/data_loader.py` | Chargement des données macroéconomiques |
| `src/data/data_validation.py` | Validation de la structure et de la cohérence des données |
| `src/preprocessing/preprocessing.py` | Préparation et organisation des données |
| `src/preprocessing/missing_data.py` | Analyse des valeurs manquantes |
| `src/analysis/statistiques.py` | Calcul des statistiques descriptives |
| `src/analysis/distribution.py` | Analyse des distributions statistiques |
| `src/analysis/times_series.py` | Analyse des séries temporelles et variations annuelles |
| `src/analysis/period_comaraison.py` | Comparaison des périodes économiques |
| `src/analysis/correlations.py` | Analyse des corrélations statistiques |
| `app_macro_rdc_professionnel.py` | Interface principale Streamlit |

## 📦 6. Installation

### Prérequis

- Python 3.11 ou supérieur.
- pip.
- Une connexion Internet pour récupérer les données depuis la Banque mondiale, lorsque le chargement nécessite un accès à l'API.

### Étape 1 : Cloner le dépôt

```bash
git clone https://github.com/laurediekabala/indicateur-rdc-macroe.git

cd indicateur-rdc-macroe
```

*Adapter l'adresse du dépôt si le nom ou l'URL du repository GitHub est différent.*

### Étape 2 : Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv .env
```

Sous Linux/macOS :

```bash
python3 -m venv .env
```

### Étape 3 : Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.env\Scripts\Activate.ps1
```

Sous Windows CMD :

```cmd
.env\Scripts\activate.bat
```

Sous Linux/macOS :

```bash
source .env/bin/activate
```

### Étape 4 : Installer les dépendances

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

## 🚀 7. Exécution de l'application

Depuis le répertoire racine du projet, exécuter :

```bash
streamlit run app_macro_rdc_professionnel.py
```

L'application sera accessible depuis le navigateur à l'adresse :

```text
http://localhost:8501
```

Pour arrêter l'application, utiliser `Ctrl + C` dans le terminal.

## 📊 8. Sources et collecte des données

Les données utilisées proviennent principalement de la **Banque mondiale**, à travers son portail World Development Indicators (WDI).

La récupération des données est effectuée à l'aide de la bibliothèque Python `wbgapi`.

- Pays : République démocratique du Congo.
- Code pays : `COD`.
- Période de référence : 1960–2024.
- Fréquence : annuelle.
- Source : World Bank Open Data.

### Principaux codes des indicateurs

| Code Banque mondiale | Indicateur |
|---|---|
| `NY.GDP.MKTP.KD.ZG` | Croissance du PIB |
| `FP.CPI.TOTL.ZG` | Inflation |
| `SP.POP.TOTL` | Population totale |
| `FI.RES.TOTL.CD` | Réserves totales |
| `PA.NUS.FCRF` | Taux de change officiel |
| `SP.DYN.CDRT.IN` | Taux de mortalité brute |
| `SP.DYN.LE00.IN` | Espérance de vie à la naissance |
| `SL.UEM.TOTL.ZS` | Taux de chômage |
| `NE.EXP.GNFS.CD` | Exportations de biens et services |
| `NE.IMP.GNFS.CD` | Importations de biens et services |

**Source officielle :** https://data.worldbank.org/country/congo-dem-rep

## ⚠️ 9. Limites et disponibilité des données

La couverture historique des indicateurs n'est pas uniforme.

Certaines séries disposent de données sur presque toute la période, tandis que d'autres ne sont disponibles que pour une partie des années étudiées.

En particulier, les exportations, les importations et le chômage présentent une couverture historique plus limitée.

Cette situation implique plusieurs précautions :

- Les statistiques sont calculées sur les observations disponibles.
- Les effectifs peuvent varier d'un indicateur à l'autre.
- Les corrélations peuvent être calculées sur des échantillons différents.
- Les comparaisons de périodes doivent tenir compte du taux de disponibilité.
- Les périodes sans observations ne doivent pas être interprétées comme des valeurs nulles.

La qualité de l'analyse dépend donc de la disponibilité et de la fiabilité des séries statistiques.

## 📐 10. Méthodes statistiques

### 10.1. Moyenne arithmétique

La moyenne arithmétique mesure le niveau moyen d'un indicateur sur une période donnée.

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

Elle est notamment utilisée pour résumer les niveaux observés d'un indicateur.

### 10.2. Moyenne géométrique et taux de croissance annuel moyen

Pour une série strictement positive, le taux de croissance annuel moyen géométrique (TCAM) peut être calculé à partir des valeurs initiale et finale :

\[
TCAM=\left(\frac{V_f}{V_i}\right)^{\frac{1}{n}}-1
\]

Avec :

- \(V_i\) : valeur initiale.
- \(V_f\) : valeur finale.
- \(n\) : nombre d'intervalles annuels.

Cette méthode est adaptée à l'étude de la croissance composée.

Elle n'est pas applicable directement aux séries dont les valeurs initiales ou finales sont nulles ou négatives, notamment certains taux de croissance du PIB ou d'inflation.

### 10.3. Variations annuelles

Selon la nature de l'indicateur, deux approches peuvent être utilisées.

**Variation absolue :**

\[
\Delta X_t=X_t-X_{t-1}
\]

**Variation relative :**

\[
Variation(\%)=\frac{X_t-X_{t-1}}{X_{t-1}}\times100
\]

Le choix de la méthode dépend de la signification économique de la variable.

### 10.4. Corrélation de Pearson

Mesure l'intensité de la relation linéaire entre deux variables quantitatives.

### 10.5. Corrélation de Spearman

Mesure l'intensité de la relation monotone entre deux variables à partir de leurs rangs.

### 10.6. Tests statistiques

Les tests de corrélation permettent notamment d'examiner l'hypothèse nulle d'absence d'association statistique.

Le seuil de significativité doit être interprété avec prudence et ne constitue pas une preuve de causalité.

## 🧪 11. Tests et validation

Le projet comprend des modules de tests destinés à contrôler le bon fonctionnement des fonctions analytiques.

Pour exécuter l'ensemble des tests :

```bash
pytest -v
```

Pour exécuter un test particulier :

```bash
pytest test/test_distribution.py -v
```

Les tests peuvent notamment porter sur :

- La validation des données.
- La détection des valeurs manquantes.
- Les calculs statistiques.
- Les distributions.
- Les variations temporelles.
- Les comparaisons de périodes.
- Les corrélations.

## 🐛 12. Dépannage

### Erreur : `No module named 'streamlit'`

Installer Streamlit :

```bash
pip install streamlit
```

### Erreur de connexion à la Banque mondiale

- Vérifier la connexion Internet.
- Vérifier la disponibilité du service World Bank API.
- Relancer le chargement des données.

### Erreur de module introuvable

Vérifier que :

- L'environnement virtuel est activé.
- Les dépendances sont installées.
- La commande Streamlit est exécutée depuis le répertoire racine du projet.

### Graphiques non affichés

Vérifier l'installation de Plotly :

```bash
pip install plotly
```

Puis relancer l'application.

## 👨‍💻 13. Auteur et contact

**Laurent Kabara**

Data Scientist | Data Analyst | Data Engineer

- 📧 Email : laurediekabala@gmail.com
- 📱 WhatsApp : +243 814 900 752
- 💼 LinkedIn : https://www.linkedin.com/in/laurent-kabala-20a6473a2/
- 🐙 GitHub : https://github.com/laurediekabala

Domaines d'intérêt :

- Data Science et analyse statistique.
- Analyse macroéconomique.
- Modélisation et interprétation des données.
- Ingénierie des données.
- Business Intelligence.

## 📄 14. Licence et utilisation

Ce projet est développé à des fins d'analyse, d'apprentissage et de valorisation des données macroéconomiques de la République démocratique du Congo.

Les données sont issues de la Banque mondiale. Leur utilisation doit respecter les conditions de diffusion et de réutilisation de la source officielle.

Les résultats statistiques doivent être interprétés en tenant compte des limites de couverture et de qualité des données.

## 🤝 15. Contribution

Les suggestions, corrections et améliorations sont les bienvenues.

Pour contribuer :

1. Forker le repository.
2. Créer une branche dédiée.
3. Effectuer les modifications.
4. Tester les nouvelles fonctionnalités.
5. Soumettre une Pull Request.

## 📚 16. Ressources utiles

- Documentation Python : https://docs.python.org/3/
- Documentation Streamlit : https://docs.streamlit.io/
- Documentation Plotly : https://plotly.com/python/
- Documentation Pandas : https://pandas.pydata.org/docs/
- Documentation NumPy : https://numpy.org/doc/
- Documentation SciPy : https://docs.scipy.org/doc/scipy/
- Documentation wbgapi : https://github.com/mmngreco/wbgapi
- Banque mondiale : https://data.worldbank.org/

---

**Version :** 2.0.0  
**Dernière mise à jour :** Novembre 2026  
**Statut :** Application en développement et amélioration continue.