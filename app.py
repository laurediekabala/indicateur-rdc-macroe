import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.indicators import INDICATOR_METADATA

from src.data.data_loader import load_macro_data
from src.preprocessing.preprocessing import prepare_macro_data

from src.analysis.statistiques import build_descriptive_statistics
from src.analysis.distribution import distribution_analysis
from src.analysis.times_series import (
    calculate_annual_variation,
    calculate_cagr,
)
from src.analysis.period_comaraison import compare_periods
from src.analysis.correlations import (
    calculate_correlations,
    calculate_correlation_counts,
    calculate_indicator_variations,
    calculate_correlations_on_variations,
)
from src.data.data_validation import (
    validate_macro_data,
    missing_values_report,
    missingness_timeline,
)
from src.preprocessing.missing_data import build_missing_data_report


# ============================================================
# 1. CONFIGURATION ET IDENTITE VISUELLE
# ============================================================

st.set_page_config(
    page_title="Observatoire macroéconomique | RDC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Charte graphique : bleu marine, bleu et turquoise.
st.markdown(
    """
    <style>
        :root {
            --navy: #10243A;
            --blue: #176B87;
            --teal: #20A39E;
            --light-bg: #F4F7FA;
            --text: #263445;
            --muted: #68788A;
        }

        .stApp {
            background: var(--light-bg);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: rgba(244, 247, 250, 0.92);
        }

        [data-testid="stSidebar"] {
            background: #10243A;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #F3F7FA;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            padding-top: 0.22rem;
            padding-bottom: 0.22rem;
        }

        .brand-block {
            padding: 1.15rem 1.2rem;
            border-radius: 14px;
            background: linear-gradient(125deg, #10243A 0%, #176B87 100%);
            color: white;
            margin-bottom: 1.2rem;
        }

        .brand-kicker {
            color: #B8E6E3;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.72rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .brand-title {
            color: white;
            font-size: 1.55rem;
            font-weight: 750;
            line-height: 1.2;
            margin: 0;
        }

        .brand-subtitle {
            color: #E1EDF3;
            font-size: 0.91rem;
            margin-top: 0.45rem;
            margin-bottom: 0;
        }

        .section-intro {
            color: #68788A;
            font-size: 0.96rem;
            margin-top: -0.45rem;
            margin-bottom: 1rem;
        }

        .sidebar-brand {
            padding: 0.5rem 0 1rem 0;
        }

        .sidebar-brand .name {
            font-size: 1.15rem;
            font-weight: 750;
            color: #FFFFFF;
        }

        .sidebar-brand .desc {
            font-size: 0.78rem;
            color: #B8C9D8;
            line-height: 1.45;
        }

        .contact-panel {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 12px;
            padding: 0.85rem 0.8rem;
            margin-top: 0.4rem;
        }

        .contact-title {
            color: #FFFFFF;
            font-weight: 700;
            font-size: 0.9rem;
            margin-bottom: 0.55rem;
        }

        .contact-panel a {
            display: block;
            color: #DCEFF5 !important;
            text-decoration: none;
            font-size: 0.79rem;
            padding: 0.27rem 0;
            overflow-wrap: anywhere;
        }

        .contact-panel a:hover {
            color: #66D6CE !important;
            text-decoration: underline;
        }

        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E3EAF0;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(16,36,58,0.035);
        }

        div[data-testid="stMetricLabel"] {
            color: #68788A;
        }

        div[data-testid="stMetricValue"] {
            color: #10243A;
            font-weight: 750;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #E3EAF0;
            border-radius: 10px;
            overflow: hidden;
        }

        .source-note {
            color: #68788A;
            font-size: 0.78rem;
            border-top: 1px solid #DDE5EC;
            padding-top: 0.75rem;
            margin-top: 1.5rem;
        }

        h1, h2, h3 {
            color: #10243A;
        }

        @media (max-width: 768px) {
            .brand-title { font-size: 1.25rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def style_chart(fig, height=440):
    """Applique une présentation homogène aux graphiques Plotly."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(family="Arial, sans-serif", color="#263445", size=12),
        title=dict(font=dict(size=17, color="#10243A"), x=0.02, xanchor="left"),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=25, r=25, t=65, b=35),
        hoverlabel=dict(bgcolor="#10243A", font_color="white"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#E9EEF3", zeroline=False)
    return fig


def show_chart(fig, height=440):
    """Affiche un graphique avec le style commun de l'application."""
    style_chart(fig, height=height)
    st.plotly_chart(fig, width="stretch")



def show_table(data, height=None):
    """
    Affiche un tableau en utilisant toute la largeur disponible.
    La hauteur est définie uniquement lorsqu'elle est précisée.
    """
    if height is None:
        st.dataframe(
            data,
            width="stretch"
        )
    else:
        st.dataframe(
            data,
            width="stretch",
            height=height
        )



# ============================================================
# 2. EN-TETE DE L'APPLICATION
# ============================================================

st.markdown(
    """
    <div class="brand-block">
        <div class="brand-kicker">Observatoire économique</div>
        <p class="brand-title">Indicateurs macroéconomiques de la RDC</p>
        <p class="brand-subtitle">
            Exploration statistique, analyse temporelle et suivi
            de la qualité des données économiques.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. CHARGEMENT ET PREPARATION DES DONNEES
# ============================================================

@st.cache_data(show_spinner="Chargement des données économiques...")
def get_macro_data():
    raw_data = load_macro_data()
    data = prepare_macro_data(raw_data)
    return data


try:
    df = get_macro_data()
except Exception as error:
    st.error(f"Impossible de charger les données macroéconomiques : {error}")
    st.info(
        "Vérifiez votre connexion Internet et la disponibilité "
        "de l'API de la Banque mondiale."
    )
    st.stop()

if df.empty:
    st.error("Le jeu de données est vide. Aucune analyse ne peut être affichée.")
    st.stop()


# ============================================================
# 4. INFORMATIONS GENERALES ET NAVIGATION
# ============================================================

first_year = int(df.index.min())
last_year = int(df.index.max())
number_indicators = len(df.columns)
number_observations = len(df)

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="name">📊 Observatoire RDC</div>
        <div class="desc">Tableau de bord d'analyse macroéconomique</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Sélectionner une rubrique",
    [
        "Vue d'ensemble",
        "Statistiques descriptives",
        "Distribution statistique",
        "Analyse temporelle",
        "Comparaison des périodes",
        "Corrélations économiques",
        "Qualité des données",
        "À propos",
    ],
)

st.sidebar.divider()
st.sidebar.caption(f"Base temporelle : {first_year} – {last_year}")
st.sidebar.caption("Source principale : Banque mondiale")

st.sidebar.divider()
st.sidebar.markdown(
    """
    <div class="contact-panel">
        <div class="contact-title">Contact du développeur</div>
        <a href="https://wa.me/243814900752" target="_blank">
            ◉ WhatsApp : +243 814 900 752
        </a>
        <a href="mailto:laurediekabala@gmail.com">
            ✉ Gmail : laurediekabala@gmail.com
        </a>
        <a href="https://www.linkedin.com/in/laurent-kabala-20a6473a2"
           target="_blank">
            in LinkedIn : Laurent Kabala
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 5. VUE D'ENSEMBLE
# ============================================================

if page == "Vue d'ensemble":
    st.header("Vue d'ensemble économique")
    st.markdown(
        '<p class="section-intro">Un aperçu de la couverture statistique '
        "et des indicateurs disponibles dans la base.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Indicateurs", f"{number_indicators}")
    col2.metric("Années couvertes", f"{number_observations}")
    col3.metric("Première année", f"{first_year}")
    col4.metric("Dernière année", f"{last_year}")

    st.divider()
    st.subheader("Évolution historique d'un indicateur")

    indicator = st.selectbox("Choisir un indicateur", df.columns.tolist())
    metadata = INDICATOR_METADATA[indicator]
    observed = df[indicator].dropna()

    if not observed.empty:
        fig = px.line(
            x=observed.index,
            y=observed.values,
            markers=True,
            labels={"x": "Année", "y": metadata["unit"]},
            title=indicator,
        )
        fig.update_traces(line=dict(width=3, color="#176B87"),
                          marker=dict(size=6, color="#20A39E"))
        show_chart(fig)
    else:
        st.warning("Aucune observation disponible pour cet indicateur.")

    st.subheader("Aperçu des données")
    show_table(df)


# ============================================================
# 6. STATISTIQUES DESCRIPTIVES
# ============================================================

elif page == "Statistiques descriptives":
    st.header("Statistiques descriptives")
    st.markdown(
        '<p class="section-intro">Résumé statistique calculé à partir '
        "des observations effectivement disponibles. Aucune valeur "
        "manquante n'est imputée.</p>",
        unsafe_allow_html=True,
    )

    statistics = build_descriptive_statistics(df)
    show_table(statistics)

    st.subheader("Analyse détaillée d'un indicateur")
    indicator = st.selectbox(
        "Choisir un indicateur",
        statistics.index.tolist(),
    )
    result = statistics.loc[indicator]

    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre d'observations", int(result["n"]))
    col2.metric(
        "Moyenne",
        f"{result['moyenne']:,.2f}" if pd.notna(result["moyenne"]) else "N/A",
    )
    col3.metric(
        "Médiane",
        f"{result['mediane']:,.2f}" if pd.notna(result["mediane"]) else "N/A",
    )

    st.subheader("Autres statistiques")
    show_table(result.to_frame("Valeur"))


# ============================================================
# 7. ANALYSE DES DISTRIBUTIONS
# ============================================================

elif page == "Distribution statistique":
    st.header("Analyse des distributions")
    st.markdown(
        '<p class="section-intro">Étude de la forme des distributions et '
        "repérage des observations potentiellement atypiques à l'aide "
        "des bornes de Tukey. Une valeur atypique n'est pas "
        "nécessairement une erreur.</p>",
        unsafe_allow_html=True,
    )

    distribution = distribution_analysis(df)
    show_table(distribution)

    indicator = st.selectbox("Choisir un indicateur", df.columns.tolist())
    observed = df[indicator].dropna()

    if not observed.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(
                observed,
                nbins=20,
                title=f"Distribution de {indicator}",
                labels={"value": indicator},
            )
            fig.update_traces(marker_color="#176B87")
            show_chart(fig, height=390)

        with col2:
            fig = px.box(
                observed,
                title=f"Diagramme en boîte – {indicator}",
                labels={"value": indicator},
                points="outliers",
            )
            fig.update_traces(marker_color="#20A39E")
            show_chart(fig, height=390)
    else:
        st.warning("Aucune observation disponible pour cet indicateur.")


# ============================================================
# 8. ANALYSE TEMPORELLE
# ============================================================

elif page == "Analyse temporelle":
    st.header("Analyse temporelle")
    st.markdown(
        '<p class="section-intro">Analyse de l’évolution historique, '
        "des variations annuelles et du taux de croissance annuel moyen "
        "composé lorsque son utilisation est statistiquement pertinente.</p>",
        unsafe_allow_html=True,
    )

    indicator = st.selectbox("Choisir un indicateur", df.columns.tolist())
    metadata = INDICATOR_METADATA[indicator]
    series = df[indicator]
    observed = series.dropna()

    if observed.empty:
        st.warning("Aucune observation disponible.")
    else:
        st.subheader("Évolution historique")
        fig = px.line(
            x=observed.index,
            y=observed.values,
            markers=True,
            labels={"x": "Année", "y": metadata["unit"]},
            title=indicator,
        )
        fig.update_traces(line=dict(width=3, color="#176B87"),
                          marker=dict(color="#20A39E", size=6))
        show_chart(fig)

        st.subheader("Variation annuelle")
        method = metadata["variation_method"]
        variation = calculate_annual_variation(series, method=method)
        variation_unit = metadata["variation_unit"]
        variation_data = variation.dropna()

        if not variation_data.empty:
            fig = px.bar(
                x=variation_data.index,
                y=variation_data.values,
                labels={"x": "Année", "y": variation_unit},
                title=f"Variation annuelle – {indicator}",
            )
            fig.update_traces(marker_color="#176B87")
            show_chart(fig, height=390)
            show_table(variation.to_frame("Variation annuelle"))
        else:
            st.info(
                "Pas suffisamment de données consécutives pour calculer "
                "les variations annuelles."
            )

        st.subheader("Taux de croissance annuel moyen composé (TCAM)")
        st.caption(
            "Le TCAM utilise les valeurs initiale et finale. Il est "
            "interprétable pour une série de niveau strictement positive. "
            "Il n'est généralement pas adapté aux taux pouvant être nuls "
            "ou négatifs, comme la croissance du PIB ou l'inflation."
        )

        available_years = observed.index.astype(int).tolist()
        col1, col2 = st.columns(2)

        with col1:
            start_year = st.selectbox(
                "Année de début",
                available_years,
                index=0,
                key="cagr_start_year",
            )

        with col2:
            end_year = st.selectbox(
                "Année de fin",
                available_years,
                index=len(available_years) - 1,
                key="cagr_end_year",
            )

        if st.button("Calculer le TCAM"):
            try:
                cagr = calculate_cagr(series, int(start_year), int(end_year))
                st.metric("TCAM", f"{cagr:.2f} %")
                st.caption(
                    "Résultat annualisé calculé sur les deux valeurs "
                    "observées aux bornes de la période."
                )
            except (ValueError, TypeError) as error:
                st.warning(str(error))


# ============================================================
# 9. COMPARAISON DES PERIODES
# ============================================================

elif page == "Comparaison des périodes":
    st.header("Comparaison des périodes économiques")
    st.markdown(
        '<p class="section-intro">Comparez les statistiques et les '
        "évolutions des indicateurs entre deux périodes définies.</p>",
        unsafe_allow_html=True,
    )

    default_end_1 = min(first_year + 30, last_year)
    default_start_2 = min(default_end_1 + 1, last_year)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Première période")
        start_1 = st.number_input(
            "Année de début – période 1",
            min_value=first_year,
            max_value=last_year,
            value=first_year,
            key="start_1",
        )
        end_1 = st.number_input(
            "Année de fin – période 1",
            min_value=first_year,
            max_value=last_year,
            value=default_end_1,
            key="end_1",
        )

    with col2:
        st.subheader("Deuxième période")
        start_2 = st.number_input(
            "Année de début – période 2",
            min_value=first_year,
            max_value=last_year,
            value=default_start_2,
            key="start_2",
        )
        end_2 = st.number_input(
            "Année de fin – période 2",
            min_value=first_year,
            max_value=last_year,
            value=last_year,
            key="end_2",
        )

    if st.button("Comparer les périodes"):
        if start_1 > end_1 or start_2 > end_2:
            st.error(
                "Chaque année de début doit être inférieure ou égale "
                "à son année de fin."
            )
        else:
            periods = {
                "Période 1": (int(start_1), int(end_1)),
                "Période 2": (int(start_2), int(end_2)),
            }

            try:
                comparison = compare_periods(df, periods)
                st.subheader("Résultats de la comparaison")
                show_table(comparison)
                st.info(
                    "Le taux de disponibilité permet d'identifier les "
                    "périodes dont les données sont incomplètes. Les "
                    "valeurs initiales et finales correspondent aux "
                    "premières et dernières observations disponibles "
                    "dans chaque période."
                )
            except (ValueError, TypeError) as error:
                st.error(str(error))


# ============================================================
# 10. CORRELATIONS ECONOMIQUES
# ============================================================

elif page == "Corrélations économiques":
    st.header("Corrélations économiques")
    st.markdown(
        '<p class="section-intro">Étude des associations statistiques '
        "entre indicateurs. Une corrélation ne démontre pas une relation "
        "de causalité.</p>",
        unsafe_allow_html=True,
    )

    method = st.selectbox(
        "Méthode de corrélation",
        ["pearson", "spearman"],
    )
    analysis_type = st.radio(
        "Type d'analyse",
        ["Niveaux des indicateurs", "Variations annuelles"],
        horizontal=True,
    )
    min_periods = st.slider(
        "Nombre minimal d'observations communes",
        min_value=2,
        max_value=len(df),
        value=min(10, len(df)),
    )

    try:
        if analysis_type == "Niveaux des indicateurs":
            correlations = calculate_correlations(
                df,
                method=method,
                min_periods=min_periods,
            )
            counts = calculate_correlation_counts(df)
        else:
            correlations = calculate_correlations_on_variations(
                df,
                method=method,
                min_periods=min_periods,
            )
            variations = calculate_indicator_variations(df)
            counts = calculate_correlation_counts(variations)

        st.subheader("Matrice de corrélation")
        fig = go.Figure(
            data=go.Heatmap(
                z=correlations.values,
                x=correlations.columns,
                y=correlations.index,
                zmin=-1,
                zmax=1,
                colorscale="RdBu",
                reversescale=True,
                colorbar_title="Corrélation",
                hovertemplate=(
                    "Indicateur X : %{x}<br>"
                    "Indicateur Y : %{y}<br>"
                    "Corrélation : %{z:.3f}<extra></extra>"
                ),
            )
        )
        fig.update_layout(
            title=f"Corrélations – {method.capitalize()}",
            height=700,
            xaxis_tickangle=-35,
        )
        show_chart(fig, height=700)

        st.subheader("Valeurs des corrélations")
        show_table(correlations)

        st.subheader("Nombre d'observations communes")
        show_table(counts)

        st.caption(
            "Le nombre d'observations communes varie selon les paires "
            "d'indicateurs. Interprétez chaque coefficient en tenant "
            "compte de cet effectif et de la période réellement couverte."
        )
    except (ValueError, TypeError) as error:
        st.error(str(error))


# ============================================================
# 11. QUALITE DES DONNEES
# ============================================================

elif page == "Qualité des données":
    st.header("Qualité et disponibilité des données")
    st.markdown(
        '<p class="section-intro">Contrôle de la structure temporelle, '
        "de la validité des valeurs et de la couverture statistique "
        "des indicateurs.</p>",
        unsafe_allow_html=True,
    )

    st.subheader("Validation générale")
    validation = validate_macro_data(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Observations", validation["nombre_observations"])
    col2.metric("Indicateurs", validation["nombre_indicateurs"])
    col3.metric("Années absentes", len(validation["annees_manquantes"]))

    if validation["colonnes_non_numeriques"]:
        st.warning(
            f"Colonnes non numériques : "
            f"{validation['colonnes_non_numeriques']}"
        )

    if validation["valeurs_infinies"]:
        st.error(f"Valeurs infinies : {validation['valeurs_infinies']}")

    if validation["annees_manquantes"]:
        st.warning(f"Années absentes : {validation['annees_manquantes']}")
    else:
        st.success("Aucune année manquante dans la structure temporelle.")

    st.divider()
    st.subheader("Disponibilité des indicateurs")

    missing_report = missing_values_report(df)
    show_table(missing_report)

    # Renommer explicitement l'index pour ne pas dépendre du nom
    # que lui attribue la fonction de rapport.
    plot_data = (
        missing_report
        .rename_axis("indicateur")
        .reset_index()
    )

    fig = px.bar(
        plot_data,
        x="indicateur",
        y="pourcentage_disponible",
        color="statut",
        labels={
            "indicateur": "Indicateur",
            "pourcentage_disponible": "Disponibilité (%)",
            "statut": "Statut",
        },
        title="Taux de disponibilité par indicateur",
    )
    fig.update_layout(xaxis_tickangle=-35)
    show_chart(fig, height=500)

    st.divider()
    st.subheader("Diagnostic détaillé des données manquantes")
    detailed_report = build_missing_data_report(df)
    show_table(detailed_report)

    st.divider()
    st.subheader("Répartition temporelle des valeurs manquantes")
    timeline = missingness_timeline(df)
    show_table(timeline)


# ============================================================
# 12. A PROPOS DE L'APPLICATION
# ============================================================

elif page == "À propos":

    st.header("À propos de l'application")

    st.markdown(
        '<p class="section-intro">'
        "Présentation du projet, de ses objectifs, "
        "de ses sources de données et de sa méthodologie."
        "</p>",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # PRESENTATION
    # --------------------------------------------------------

    st.subheader("Présentation du projet")

    st.markdown("""
    L'**Observatoire macroéconomique de la République
    démocratique du Congo** est une application interactive
    consacrée à l'exploration et à l'analyse statistique
    des principaux indicateurs macroéconomiques du pays.

    Elle permet de suivre les évolutions économiques,
    d'étudier les tendances historiques et de comparer
    différentes périodes afin de faciliter la compréhension
    des dynamiques macroéconomiques de la RDC.

    Le projet s'appuie sur Python et des outils de
    visualisation de données pour rendre les analyses
    accessibles et exploitables.
    """)

    st.divider()

    # --------------------------------------------------------
    # OBJECTIFS
    # --------------------------------------------------------

    st.subheader("Objectifs du projet")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Analyse économique**
        - Suivre l'évolution des indicateurs.
        - Identifier les tendances historiques.
        - Comparer différentes périodes économiques.
        - Explorer les relations entre indicateurs.
        """)

    with col2:
        st.markdown("""
        **Analyse statistique**
        - Produire des statistiques descriptives.
        - Étudier les distributions.
        - Calculer les variations annuelles.
        - Évaluer la disponibilité des données.
        """)

    st.divider()

    # --------------------------------------------------------
    # PERIMETRE
    # --------------------------------------------------------

    st.subheader("Périmètre de l'analyse")

    col1, col2, col3 = st.columns(3)

    col1.metric("Pays étudié", "RDC")
    col2.metric("Indicateurs", number_indicators)
    col3.metric(
        "Période couverte",
        f"{first_year} – {last_year}"
    )

    st.markdown("""
    Les indicateurs étudiés couvrent notamment :

    - Les réserves internationales.
    - L'inflation.
    - Les exportations et les importations.
    - La croissance du PIB.
    - Le taux de change.
    - Le chômage.
    - La mortalité brute.
    - L'espérance de vie.
    - La population totale.
    """)

    st.divider()

    # --------------------------------------------------------
    # SOURCES DES DONNEES
    # --------------------------------------------------------

    st.subheader("Sources des données")

    st.markdown("""
    La source principale utilisée dans ce projet est la
    **Banque mondiale**, à travers sa base
    *World Development Indicators (WDI)*.

    Les données sont relatives à la République démocratique
    du Congo, identifiée par le code pays **COD**.

    """)

    st.markdown(
        "[Consulter la base World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)"
    )

    st.info("""
    **Important :** la disponibilité des séries varie selon
    les indicateurs et les années. Les observations absentes
    sont conservées comme valeurs manquantes. Aucune
    interpolation ou imputation automatique n'est appliquée
    pour masquer les lacunes des données sources.
    """)

    st.divider()

    # --------------------------------------------------------
    # METHODOLOGIE
    # --------------------------------------------------------

    st.subheader("Méthodologie statistique")

    with st.expander("1. Statistiques descriptives"):
        st.markdown("""
        Calcul de mesures statistiques permettant de résumer
        les distributions : moyenne, médiane, minimum,
        maximum, écart-type et autres indicateurs pertinents.
        """)

    with st.expander("2. Analyse des distributions"):
        st.markdown("""
        Étude de la forme des distributions, de leur dispersion
        et de leurs caractéristiques statistiques.
        """)

    with st.expander("3. Analyse temporelle"):
        st.markdown("""
        Étude de l'évolution des indicateurs dans le temps,
        calcul des variations annuelles et, lorsque cela est
        statistiquement pertinent, du taux de croissance
        annuel moyen (TCAM).
        """)

    with st.expander("4. Comparaison des périodes"):
        st.markdown("""
        Comparaison des niveaux moyens, médianes, valeurs
        extrêmes et évolutions entre différentes périodes
        économiques.
        """)

    with st.expander("5. Analyse des corrélations"):
        st.markdown("""
        Utilisation des coefficients de Pearson et de Spearman
        pour étudier les relations statistiques entre les
        indicateurs.

        Une corrélation ne démontre pas une relation de
        causalité. Les résultats doivent être interprétés
        en tenant compte des tendances temporelles et du
        nombre d'observations disponibles.
        """)

    with st.expander("6. Qualité des données"):
        st.markdown("""
        Vérification de la structure des données, des valeurs
        manquantes, de la couverture temporelle et de la
        disponibilité des observations.
        """)

    st.divider()

    # --------------------------------------------------------
    # LIMITES
    # --------------------------------------------------------

    st.subheader("Limites de l'analyse")

    st.markdown("""
    Les résultats présentés dépendent de la qualité,
    de la disponibilité et de la méthodologie de production
    des données sources.

    Certaines séries ne couvrent pas l'ensemble de la période
    étudiée. Les comparaisons statistiques doivent donc tenir
    compte du nombre d'observations disponibles.

    Les analyses présentées sont essentiellement descriptives
    et exploratoires. Elles ne constituent pas, à elles seules,
    des preuves de causalité ni des prévisions économiques.
    """)

    st.divider()

    # --------------------------------------------------------
    # AUTEUR
    # --------------------------------------------------------

    st.subheader("Développement du projet")

    st.markdown("""
    **Laurent Kabala**

    Data Scientist |Data Engineer|Data Analyst

    Formation en mathématiques, statistiques et informatique.

    Ce projet s'inscrit dans une démarche de valorisation
    des données économiques à travers les méthodes
    statistiques, l'analyse de données et la visualisation.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "[LinkedIn](https://www.linkedin.com/in/laurent-kabala-20a6473a2)"
        )

        st.markdown(
            "[GitHub](https://github.com/laurediekabala)"
        )

    with col2:
        st.markdown(
            "[Envoyer un e-mail](mailto:laurediekabala@gmail.com)"
        )

        st.markdown(
            "[WhatsApp : +243 814 900 752](https://wa.me/243814900752)"
        )

# ============================================================
# 12. PIED DE PAGE
# ============================================================

st.markdown(
    f"""
    <div class="source-note">
        <strong>Observatoire macroéconomique de la RDC</strong><br>
        Période couverte : {first_year}–{last_year} |
        Source principale : Banque mondiale<br>
        Les résultats dépendent de la disponibilité et de la qualité
        des séries sources. Les données manquantes ne sont pas
        automatiquement imputées.
    </div>
    """,
    unsafe_allow_html=True,
)
