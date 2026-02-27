import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import wbgapi as wb
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

# Configuration Streamlit
st.set_page_config(
    page_title="Dashboard RDC - Indicateurs Macroéconomiques",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé - Design professionnel et responsive
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-sizing: border-box;
    }
    
    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
    }
    
    .main {
        width: 100%;
        max-width: 100%;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1f77b4 0%, #0d5ca6 100%);
        color: white;
        text-align: center;
        margin: -2rem -2rem 2rem -2rem;
        padding: 2rem 1rem;
        border-radius: 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        word-wrap: break-word;
    }
    
    .main-header-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-top: 0.5rem;
        word-wrap: break-word;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 8px rgba(31, 119, 180, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.15);
    }
    
    .section-title {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.75rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        word-wrap: break-word;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f77b4;
        word-wrap: break-word;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
        margin-top: 0.5rem;
        word-wrap: break-word;
    }
    
    .correlation-significant {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .correlation-not-significant {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .data-table {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        overflow-x: auto;
    }
    
    .sidebar-section {
        margin: 1.5rem 0;
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 0.5rem;
    }
    
    hr {
        margin: 2rem 0;
        border: 1px solid #e0e0e0;
    }
    
    /* Styles pour les tables */
    [data-testid="dataframe"] {
        width: 100%;
        overflow-x: auto;
        font-size: 0.9rem;
    }
    
    [data-testid="dataframe"] thead {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    
    [data-testid="dataframe"] thead th {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #0d5ca6 !important;
        padding: 0.75rem !important;
        white-space: nowrap;
    }
    
    [data-testid="dataframe"] tbody tr:nth-child(odd) {
        background-color: #f8f9fa;
    }
    
    [data-testid="dataframe"] tbody tr:nth-child(even) {
        background-color: #ffffff;
    }
    
    [data-testid="dataframe"] tbody tr:hover {
        background-color: #e8f0f7 !important;
    }
    
    [data-testid="dataframe"] td {
        padding: 0.75rem !important;
        border-bottom: 1px solid #e0e0e0 !important;
    }
    
    /* Media Queries pour Mobile et Tablette */
    @media (max-width: 1200px) {
        .main-header {
            font-size: 2rem;
            margin: -1.5rem -1.5rem 1.5rem -1.5rem;
            padding: 1.5rem 1rem;
        }
        
        .main-header-subtitle {
            font-size: 0.9rem;
        }
        
        .section-title {
            font-size: 1.4rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .kpi-value {
            font-size: 1.8rem;
        }
        
        .kpi-label {
            font-size: 0.85rem;
        }
        
        .metric-card {
            padding: 1.2rem;
            margin: 0.3rem 0;
        }
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.6rem;
            margin: -1rem -1rem 1rem -1rem;
            padding: 1rem;
        }
        
        .main-header-subtitle {
            font-size: 0.8rem;
            margin-top: 0.3rem;
        }
        
        .section-title {
            font-size: 1.2rem;
            margin-top: 1rem;
            margin-bottom: 0.8rem;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 0.5rem;
        }
        
        .kpi-value {
            font-size: 1.5rem;
        }
        
        .kpi-label {
            font-size: 0.75rem;
        }
        
        .metric-card {
            padding: 1rem;
            margin: 0.25rem 0;
            border-left: 3px solid #1f77b4;
        }
        
        .data-table {
            padding: 0.75rem;
        }
        
        [data-testid="dataframe"] {
            font-size: 0.8rem;
        }
        
        [data-testid="dataframe"] thead th {
            padding: 0.5rem !important;
            font-size: 0.75rem;
        }
        
        [data-testid="dataframe"] td {
            padding: 0.5rem !important;
        }
        
        .correlation-significant,
        .correlation-not-significant {
            padding: 0.75rem;
            margin: 0.75rem 0;
            font-size: 0.9rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.3rem;
            margin: -0.5rem -0.5rem 0.8rem -0.5rem;
            padding: 0.75rem;
        }
        
        .main-header-subtitle {
            font-size: 0.7rem;
            margin-top: 0.2rem;
        }
        
        .section-title {
            font-size: 1rem;
            margin-top: 0.8rem;
            margin-bottom: 0.6rem;
            padding-bottom: 0.3rem;
        }
        
        .kpi-value {
            font-size: 1.3rem;
        }
        
        .kpi-label {
            font-size: 0.65rem;
        }
        
        .metric-card {
            padding: 0.8rem;
            margin: 0.2rem 0;
        }
        
        .data-table {
            padding: 0.5rem;
        }
        
        [data-testid="dataframe"] {
            font-size: 0.7rem;
        }
        
        [data-testid="dataframe"] thead th {
            padding: 0.3rem !important;
            font-size: 0.65rem;
        }
        
        [data-testid="dataframe"] td {
            padding: 0.3rem !important;
        }
        
        hr {
            margin: 1rem 0;
        }
    }
    
    /* Optimisation pour Plotly Charts */
    .plotly-container {
        width: 100% !important;
        height: auto !important;
    }
    
    /* Optimisation pour les inputs */
    .stSelectbox, .stSlider, .stRadio {
        width: 100%;
    }
    
    input[type="text"],
    input[type="number"],
    select,
    textarea {
        max-width: 100%;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal avec gradient
st.markdown("<h1 class='main-header'>📊 Tableau de Bord Macroéconomique<br><span class='main-header-subtitle'>République Démocratique du Congo - Indicateurs FMI/Banque Mondiale</span></h1>", unsafe_allow_html=True)

# Fonction pour charger les données depuis l'API du FMI
@st.cache_data
def load_data():
    """Récupère les indicateurs macroéconomiques pour la RDC"""
    pays = 'COD'
    
    indicateurs = {
        'NY.GDP.MKTP.KD.ZG': 'Croissance_PIB_%',
        'FP.CPI.TOTL.ZG': 'Inflation_%',
        'SP.POP.TOTL': 'Population_Totale',
        'FI.RES.TOTL.CD': 'Reserves_Change_USD',
        'PA.NUS.FCRF': 'Taux_de_Change_CDF_USD',
        'SP.DYN.CDRT.IN': 'Taux_Mortalite_Brute_1000',
        'SP.DYN.LE00.IN': 'Esperance_Vie_Ans',
        'SL.UEM.TOTL.ZS': 'Taux_Chomage_%',
        'NE.EXP.GNFS.CD': 'Exportations_USD',
        'NE.IMP.GNFS.CD': 'Importations_USD'
    }
    
    try:
        # Récupération des données
        data = wb.data.DataFrame(indicateurs.keys(), pays, time=range(1970, 2025))
        
        # Renommage
        data.index = [indicateurs[i] for i in data.index.get_level_values(0)]
        df = data.T
        df.index = [int(annee.replace('YR', '')) for annee in df.index]
        df.index.name = 'Annee'
        
        return df.sort_index()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

# Fonction pour calculer le taux de croissance
def calculate_growth_rate(serie):
    """Calcule le taux de croissance année sur année en pourcentage"""
    return serie.pct_change() * 100

# Charger les données
df = load_data()

if df is not None:
    # Sidebar - Navigation
    st.sidebar.markdown("<h2>🔧 Navigation</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio(
        "Sélectionnez une analyse:",
        ["📈 Analyse Univariée", "🔗 Analyse de Corrélation"]
    )
    
    # Section Contact Professionnel
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); padding: 1.5rem; border-radius: 0.75rem; color: white; margin-top: 2rem; border-left: 5px solid #3498db;'>
        <h3 style='margin-top: 0; color: #3498db; font-size: 1.2rem;'>📧 Contact & Profil</h3>
        <p style='font-size: 0.85rem; line-height: 1.8; margin: 0.8rem 0; color: #ecf0f1;'>
            <b>Data Scientist & Analyste Quantitatif</b><br>
            <span style='font-size: 0.75rem; color: #bdc3c7;'>Expertise: Macroéconomie • Finance • Télécommunications</span>
        </p>
        <hr style='border: 1px solid rgba(52, 152, 219, 0.3); margin: 1rem 0;'>
        <p style='font-size: 0.8rem; margin: 0.8rem 0; color: #ecf0f1; line-height: 1.5;'>
            <span style='color: #3498db;'>✉️</span> <b>Email:</b><br>
            <span style='font-size: 0.75rem; word-break: break-word;'>laurediekabala@gmail.com</span>
        </p>
        <p style='font-size: 0.8rem; margin: 0.8rem 0; color: #ecf0f1; line-height: 1.5;'>
            <span style='color: #3498db;'>📱</span> <b>WhatsApp:</b><br>
            <span style='font-size: 0.75rem;'>+243 814 900 752</span>
        </p>
        <hr style='border: 1px solid rgba(52, 152, 219, 0.3); margin: 1rem 0;'>
        <p style='font-size: 0.7rem; color: #95a5a6; font-style: italic; margin: 0.5rem 0;'>
            💡 Analyse professionnelle des indicateurs macroéconomiques de la RDC
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== PAGE 1: ANALYSE UNIVARIÉE =====
    if page == "📈 Analyse Univariée":
        st.markdown("<h2 class='section-title'>📊 Analyse Détaillée de l'Indicateur Sélectionné</h2>", unsafe_allow_html=True)
        
        # Sélection de la variable
        variable = st.selectbox(
            "📌 Choisissez un indicateur à analyser:",
            df.columns.tolist(),
            help="Sélectionnez l'indicateur macroéconomique que vous souhaitez analyser en détail"
        )
        
        # Filtrer les données de la variable sélectionnée
        serie = df[variable].dropna()
        taux_croissance = calculate_growth_rate(serie)
        
        # KPIs - Taux de croissance
        st.markdown("<h3 class='section-title'>📈 Indicateurs Clés (KPIs) - Taux de Croissance (%)</h3>", unsafe_allow_html=True)
        
        # Responsive columns: 4 sur desktop, 2 sur tablette, 1 sur mobile
        kpi_growth_col1, kpi_growth_col2, kpi_growth_col3, kpi_growth_col4 = st.columns([1, 1, 1, 1])
        
        with kpi_growth_col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-value'>{taux_croissance.mean():.2f}%</div>
                <div class='kpi-label'>Croissance Moyenne</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_growth_col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-value'>{taux_croissance.max():.2f}%</div>
                <div class='kpi-label'>Croissance Max</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_growth_col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-value'>{taux_croissance.min():.2f}%</div>
                <div class='kpi-label'>Croissance Min</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_growth_col4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-value'>{taux_croissance.std():.2f}%</div>
                <div class='kpi-label'>Volatilité</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== SECTION 2: GRAPHIQUES - HISTOGRAMME ET BOXPLOT =====
        st.markdown("<h3 class='section-title'>📊 Distribution de l'Indicateur</h3>", unsafe_allow_html=True)
        
        fig_dist = make_subplots(
            rows=1, cols=2,
            subplot_titles=(f"Histogramme - {variable}", f"Boxplot - {variable}"),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Histogramme
        fig_dist.add_trace(
            go.Histogram(
                x=serie,
                nbinsx=30,
                marker=dict(
                    color='#1f77b4',
                    line=dict(color='#0d5ca6', width=1)
                ),
                name=variable,
                showlegend=False,
                opacity=0.8,
                hovertemplate="<b>Intervalle</b><br>Fréquence: %{y}<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Boxplot
        fig_dist.add_trace(
            go.Box(
                y=serie,
                marker=dict(color='#FF6B6B'),
                name=variable,
                showlegend=False,
                boxmean='sd',
                hovertemplate="<b>Valeur</b><br>%{y:.2f}<extra></extra>"
            ),
            row=1, col=2
        )
        
        fig_dist.update_xaxes(title_text="Valeurs", row=1, col=1, showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
        fig_dist.update_yaxes(title_text="Fréquence", row=1, col=1, showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
        fig_dist.update_yaxes(title_text="Valeurs", row=1, col=2, showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
        
        fig_dist.update_layout(
            height=600,
            autosize=True,
            showlegend=False,
            template='plotly_white',
            font=dict(family="Segoe UI, sans-serif", size=10),
            title_font_size=14,
            hovermode='closest',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_dist, use_container_width=True, config={'responsive': True, 'displayModeBar': True, 'displaylogo': False})
        
        st.markdown("---")
        
        # ===== SECTION 3: TABLEAU STATISTIQUE =====
        st.markdown("<h3 class='section-title'>📋 Tableau Statistique Descriptif</h3>", unsafe_allow_html=True)
        
        stats_df = pd.DataFrame({
            'Statistique': [
                'Nombre d\'observations',
                'Moyenne',
                'Médiane',
                'Écart-type',
                'Variance',
                'Minimum',
                'Q1 (25%)',
                'Q3 (75%)',
                'Maximum',
                'Étendue',
                'Asymétrie (Skewness)',
                'Aplatissement (Kurtosis)',
                'Coefficient de Variation (%)'
            ],
            'Valeur': [
                f"{len(serie)}",
                f"{serie.mean():.4f}",
                f"{serie.median():.4f}",
                f"{serie.std():.4f}",
                f"{serie.var():.4f}",
                f"{serie.min():.4f}",
                f"{serie.quantile(0.25):.4f}",
                f"{serie.quantile(0.75):.4f}",
                f"{serie.max():.4f}",
                f"{serie.max() - serie.min():.4f}",
                f"{serie.skew():.4f}",
                f"{serie.kurtosis():.4f}",
                f"{(serie.std() / serie.mean() * 100):.2f}" if serie.mean() != 0 else "N/A"
            ]
        })
        
        st.markdown("<div class='data-table'>", unsafe_allow_html=True)
        
        try:
            # Appliquer le style avec une fonction robuste pour une meilleure lisibilité
            def apply_stats_style(col):
                if col.name == 'Statistique':
                    return ['background-color: #1f77b4; color: white; font-weight: bold; padding: 8px;'] * len(col)
                else:
                    # Couleur contrastée pour une meilleure lisibilité
                    colors = []
                    for i, val in enumerate(col):
                        if i % 2 == 0:
                            colors.append('background-color: #FFF59D; color: #333333; padding: 8px; font-weight: 500;')  # Jaune clair avec texte sombre
                        else:
                            colors.append('background-color: #FFEB3B; color: #333333; padding: 8px; font-weight: 500;')  # Jaune plus vif
                    return colors
            
            styled_stats = stats_df.style.apply(apply_stats_style, axis=0)
            st.dataframe(styled_stats, use_container_width=True, hide_index=True)
        except:
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== SECTION 4: ÉVOLUTION TEMPORELLE DE LA VALEUR =====
        st.markdown("<h3 class='section-title'>📈 Evolution Temporelle de la Valeur</h3>", unsafe_allow_html=True)
        
        col_time1, col_time2 = st.columns([3, 1])
        
        with col_time2:
            # Sélection de la période
            min_year = int(df.index.min())
            max_year = int(df.index.max())
            
            date_range = st.slider(
                "📅 Sélectionnez la période:",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                step=1,
                help="Choisissez la période à afficher"
            )
        
        # Filtrer les données selon la période
        df_filtered = df.loc[date_range[0]:date_range[1], variable].dropna()
        
        # Graphique temporel - Valeurs brutes
        fig_time = go.Figure()
        
        fig_time.add_trace(go.Scatter(
            x=df_filtered.index,
            y=df_filtered.values,
            mode='lines+markers',
            name=variable,
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color='#1f77b4', line=dict(color='white', width=2)),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)',
            hovertemplate=f"<b>{variable}</b><br>Année: %{{x}}<br>Valeur: %{{y:.2f}}<extra></extra>"
        ))
        
        fig_time.update_layout(
            title=dict(text=f"<b>Evolution de {variable} ({date_range[0]} - {date_range[1]})</b>", x=0.5),
            xaxis_title="<b>Année</b>",
            yaxis_title=f"<b>{variable}</b>",
            height=500,
            autosize=True,
            template='plotly_white',
            hovermode='x unified',
            font=dict(family="Segoe UI, sans-serif", size=10),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_time, use_container_width=True, config={'responsive': True, 'displayModeBar': True, 'displaylogo': False})
        
        st.markdown("---")
        
        # ===== SECTION 5: TAUX DE CROISSANCE =====
        st.markdown("<h3 class='section-title'>📊 Taux de Croissance Année sur Année (%)</h3>", unsafe_allow_html=True)
        
        # Filtrer le taux de croissance pour la période sélectionnée
        taux_croissance_filtered = taux_croissance.loc[date_range[0]:date_range[1]].dropna()
        
        # Graphique du taux de croissance
        fig_growth = go.Figure()
        
        # Colorer les barres selon le signe (positif/négatif)
        colors = ['#28a745' if x >= 0 else '#dc3545' for x in taux_croissance_filtered.values]
        
        fig_growth.add_trace(go.Bar(
            x=taux_croissance_filtered.index,
            y=taux_croissance_filtered.values,
            name='Taux de croissance',
            marker=dict(
                color=colors,
                line=dict(color='white', width=1)
            ),
            hovertemplate="<b>Année: %{x}</b><br>Taux de croissance: %{y:.2f}%<extra></extra>",
            text=[f"{v:.2f}%" for v in taux_croissance_filtered.values],
            textposition='auto',
            textfont=dict(size=10)
        ))
        
        # Ajouter une ligne horizontale à zéro
        fig_growth.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig_growth.update_layout(
            title=dict(text=f"<b>Taux de Croissance Annuel - {variable} ({date_range[0]} - {date_range[1]})</b>", x=0.5),
            xaxis_title="<b>Année</b>",
            yaxis_title="<b>Taux de Croissance (%)</b>",
            height=500,
            autosize=True,
            template='plotly_white',
            hovermode='x unified',
            font=dict(family="Segoe UI, sans-serif", size=10),
            showlegend=False,
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_growth, use_container_width=True, config={'responsive': True, 'displayModeBar': True, 'displaylogo': False})
        
        st.markdown("---")
        
        # ===== SECTION 6: TABLEAU DES DONNÉES =====
        st.markdown("<h3 class='section-title'>📊 Données Annuelles Détaillées</h3>", unsafe_allow_html=True)
        
        # Créer le tableau avec les années et les valeurs
        data_display_dict = {
            'Année': df_filtered.index,
            variable: df_filtered.values.round(4)
        }
        
        # Ajouter le taux de croissance seulement pour les années où il existe
        if len(taux_croissance_filtered) > 0:
            # Créer une série du taux de croissance alignée avec les années
            taux_croissance_aligned = pd.Series(
                [np.nan] + taux_croissance_filtered.values.round(2).tolist(),
                index=df_filtered.index
            )
            data_display_dict['Taux de Croissance (%)'] = taux_croissance_aligned.values
        
        data_display = pd.DataFrame(data_display_dict).reset_index(drop=True)
        
        st.markdown("<div class='data-table'>", unsafe_allow_html=True)
        
        # Fonction pour appliquer les styles
        def highlight_columns(col):
            """Colore les colonnes numériques avec gradient"""
            if col.name == 'Année':
                return ['background-color: #1f77b4; color: white; font-weight: bold;'] * len(col)
            
            # Pour les colonnes numériques
            valid_vals = col.dropna()
            if len(valid_vals) < 2:
                return [''] * len(col)
            
            min_val = valid_vals.min()
            max_val = valid_vals.max()
            
            if min_val == max_val:
                return ['background-color: #ffeb3b;'] * len(col)
            
            colors = []
            for val in col:
                if pd.isna(val):
                    colors.append('background-color: #ffffff;')
                else:
                    normalized = (val - min_val) / (max_val - min_val)
                    
                    if normalized < 0.25:
                        color = f'rgba(220, 53, 69, 0.5)'
                    elif normalized < 0.5:
                        color = f'rgba(255, 193, 7, 0.5)'
                    elif normalized < 0.75:
                        color = f'rgba(255, 235, 59, 0.5)'
                    else:
                        color = f'rgba(40, 167, 69, 0.5)'
                    
                    colors.append(f'background-color: {color};')
            
            return colors
        
        # Appliquer le style avec une meilleure approche
        try:
            styled_data = data_display.style.apply(highlight_columns, axis=0)
            st.dataframe(styled_data, use_container_width=True, hide_index=True)
        except:
            # En cas d'erreur, afficher le dataframe sans style
            st.dataframe(data_display, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ===== PAGE 2: ANALYSE DE CORRÉLATION =====
    elif page == "🔗 Analyse de Corrélation":
        st.markdown("<h2 class='section-title'>🔗 Analyse de Corrélation entre Indicateurs</h2>", unsafe_allow_html=True)
        
        # Matrice de corrélation
        st.markdown("<h3 class='section-title'>� Matrice de Corrélation Complète (Spearman)</h3>", unsafe_allow_html=True)
        
        # Calculer la corrélation
        corr_matrix = df.corr(method='spearman')
        
        # Heatmap professionnelle
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            zmin=-1,
            zmax=1,
            colorbar=dict(
                title="Coefficient<br>Spearman",
                thickness=15,
                len=0.7,
                tickfont=dict(size=10)
            ),
            text=corr_matrix.values.round(2),
            texttemplate='%{text:.2f}',
            textfont={"size": 9, "color": "black"},
            hovertemplate="<b>%{y} vs %{x}</b><br>Corrélation: %{z:.4f}<extra></extra>"
        ))
        
        fig_heatmap.update_layout(
            height=700,
            autosize=True,
            title=dict(text="<b>Matrice de Corrélation - Coefficient Spearman</b>", x=0.5, font=dict(size=14)),
            xaxis_title="<b>Indicateurs</b>",
            yaxis_title="<b>Indicateurs</b>",
            template='plotly_white',
            font=dict(family="Segoe UI, sans-serif", size=9),
            margin=dict(l=80, r=80, t=100, b=80)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True, config={'responsive': True, 'displayModeBar': True, 'displaylogo': False})
        
        st.markdown("---")
        
        # Sélection de deux variables pour l'analyse détaillée
        st.markdown("<h3 class='section-title'>📊 Analyse de Corrélation Bivariée - Détails</h3>", unsafe_allow_html=True)
        
        col_sel1, col_sel2 = st.columns(2)
        
        with col_sel1:
            var1 = st.selectbox(
                "🔵 Sélectionnez la première variable:",
                df.columns.tolist(),
                key="var1"
            )
        
        with col_sel2:
            var2 = st.selectbox(
                "🔵 Sélectionnez la deuxième variable:",
                df.columns.tolist(),
                key="var2",
                index=1 if len(df.columns) > 1 else 0
            )
        
        if var1 != var2:
            # Préparer les données pour les deux variables
            data_corr = df[[var1, var2]].dropna()
            
            if len(data_corr) > 2:
                # Calculer la corrélation de Spearman
                corr_coeff, p_value = spearmanr(data_corr[var1], data_corr[var2])
                
                # Afficher les résultats du test d'hypothèse
                st.markdown("<h4>✅ Résultats du Test de Corrélation Spearman</h4>", unsafe_allow_html=True)
                
                col_test1, col_test2, col_test3, col_test4 = st.columns(4)
                
                with col_test1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='kpi-value'>{corr_coeff:.4f}</div>
                        <div class='kpi-label'>Coefficient ρ</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_test2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='kpi-value'>{p_value:.4f}</div>
                        <div class='kpi-label'>P-value</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_test3:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='kpi-value'>{len(data_corr)}</div>
                        <div class='kpi-label'>N observations</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_test4:
                    # Interprétation
                    alpha = 0.05
                    if p_value < alpha:
                        color_bg = "#d4edda"
                        color_border = "#28a745"
                        text = "SIGNIFICATIVE ✓"
                    else:
                        color_bg = "#f8d7da"
                        color_border = "#dc3545"
                        text = "NON SIGNIFICATIVE ✗"
                    
                    st.markdown(f"""
                    <div style='background-color: {color_bg}; border-left: 4px solid {color_border}; padding: 1.2rem; border-radius: 0.5rem; text-align: center;'>
                        <b style='font-size: 1.1rem;'>{text}</b><br>
                        <span style='font-size: 0.9rem;'>α = {alpha}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Interprétation détaillée
                st.markdown("<h4>📌 Interprétation Détaillée</h4>", unsafe_allow_html=True)
                
                # Déterminer la force
                abs_corr = abs(corr_coeff)
                if abs_corr < 0.3:
                    force = "**faible**"
                    emoji_force = "📍"
                elif abs_corr < 0.7:
                    force = "**modérée**"
                    emoji_force = "📊"
                else:
                    force = "**forte**"
                    emoji_force = "🔴"
                
                direction = "positive ⬆️" if corr_coeff > 0 else "négative ⬇️"
                
                if p_value < alpha:
                    css_class = "correlation-significant"
                    conclusion = f"""
                    ✅ **Il existe une corrélation statistiquement significative {force} {direction}** 
                    entre **{var1}** et **{var2}** (ρ = {corr_coeff:.4f}, p-value = {p_value:.4f} < {alpha}).
                    
                    **Interprétation:** Les deux indicateurs varient ensemble de manière statistiquement significative.
                    """
                else:
                    css_class = "correlation-not-significant"
                    conclusion = f"""
                    ❌ **Pas de corrélation statistiquement significative** 
                    entre **{var1}** et **{var2}** (ρ = {corr_coeff:.4f}, p-value = {p_value:.4f} ≥ {alpha}).
                    
                    **Interprétation:** Les variations de ces deux indicateurs sont indépendantes statistiquement.
                    """
                
                st.markdown(f"<div class='{css_class}'>{conclusion}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Graphique de corrélation - Scatter plot avec ligne de tendance
                st.markdown("<h4>📈 Graphique de Corrélation Bivariée</h4>", unsafe_allow_html=True)
                
                fig_scatter = px.scatter(
                    x=data_corr[var1],
                    y=data_corr[var2],
                    trendline="ols",
                    labels={
                        'x': var1,
                        'y': var2,
                    },
                    title=f"<b>Corrélation entre {var1} et {var2} (ρ = {corr_coeff:.4f}, p = {p_value:.4f})</b>"
                )
                
                fig_scatter.update_traces(
                    marker=dict(
                        size=10,
                        color='#1f77b4',
                        line=dict(color='white', width=1),
                        opacity=0.7
                    ),
                    selector=dict(mode='markers')
                )
                
                fig_scatter.update_traces(
                    line=dict(color='#FF6B6B', width=3, dash='dash'),
                    selector=dict(mode='lines')
                )
                
                fig_scatter.update_layout(
                    height=550,
                    autosize=True,
                    hovermode='closest',
                    template='plotly_white',
                    font=dict(family="Segoe UI, sans-serif", size=10),
                    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True, 'displayModeBar': True, 'displaylogo': False})
                
                st.markdown("---")
                
                # Tableau des données bivariées
                st.markdown("<h4>📋 Données Utilisées pour l'Analyse</h4>", unsafe_allow_html=True)
                
                display_data = pd.DataFrame({
                    'Année': data_corr.index,
                    var1: data_corr[var1].values.round(4),
                    var2: data_corr[var2].values.round(4)
                })
                
                st.markdown("<div class='data-table'>", unsafe_allow_html=True)
                
                # Fonction pour le style bivariable
                def highlight_bivar(col):
                    if col.name == 'Année':
                        return ['background-color: #1f77b4; color: white; font-weight: bold;'] * len(col)
                    
                    valid_vals = col.dropna()
                    if len(valid_vals) < 2:
                        return [''] * len(col)
                    
                    min_val = valid_vals.min()
                    max_val = valid_vals.max()
                    
                    if min_val == max_val:
                        return ['background-color: #ffeb3b;'] * len(col)
                    
                    colors = []
                    for val in col:
                        if pd.isna(val):
                            colors.append('')
                        else:
                            normalized = (val - min_val) / (max_val - min_val)
                            
                            if normalized < 0.25:
                                color = f'rgba(220, 53, 69, 0.4)'
                            elif normalized < 0.5:
                                color = f'rgba(255, 193, 7, 0.4)'
                            elif normalized < 0.75:
                                color = f'rgba(255, 235, 59, 0.4)'
                            else:
                                color = f'rgba(40, 167, 69, 0.4)'
                            
                            colors.append(f'background-color: {color};')
                    
                    return colors
                
                try:
                    styled_bivar = display_data.style.apply(highlight_bivar, axis=0)
                    st.dataframe(styled_bivar, use_container_width=True, hide_index=True)
                except:
                    st.dataframe(display_data, use_container_width=True, hide_index=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("❌ Données insuffisantes pour cette analyse (au moins 3 observations requises).")
        else:
            st.warning("⚠️ Veuillez sélectionner deux variables différentes.")
        
        st.markdown("---")
        
        # Afficher les corrélations les plus fortes
        st.markdown("<h3 class='section-title'>🏆 Top 10 - Corrélations les Plus Fortes</h3>", unsafe_allow_html=True)
        
        # Créer une liste de toutes les corrélations
        correlations_list = []
        for i, var_i in enumerate(corr_matrix.columns):
            for j, var_j in enumerate(corr_matrix.columns):
                if i < j:  # Éviter les doublons
                    correlations_list.append({
                        'Variable 1': var_i,
                        'Variable 2': var_j,
                        'Corrélation': corr_matrix.loc[var_i, var_j]
                    })
        
        corr_df = pd.DataFrame(correlations_list).sort_values('Corrélation', key=abs, ascending=False).head(10)
        
        st.markdown("<div class='data-table'>", unsafe_allow_html=True)
        
        # Fonction pour style corrélation
        def highlight_corr(col):
            if col.name in ['Variable 1', 'Variable 2']:
                return ['background-color: #1f77b4; color: white; font-weight: bold;'] * len(col)
            
            # Pour la colonne Corrélation
            colors = []
            for val in col:
                abs_val = abs(val)
                if abs_val < 0.3:
                    color = f'rgba(220, 53, 69, 0.5)'
                elif abs_val < 0.7:
                    color = f'rgba(255, 193, 7, 0.5)'
                else:
                    color = f'rgba(40, 167, 69, 0.5)'
                
                colors.append(f'background-color: {color};')
            
            return colors
        
        try:
            styled_corr = corr_df.style.apply(highlight_corr, axis=0).format({'Corrélation': '{:.4f}'})
            st.dataframe(styled_corr, use_container_width=True, hide_index=True)
        except:
            st.dataframe(corr_df, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("❌ Impossible de charger les données. Vérifiez votre connexion Internet.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.95rem; margin-top: 2rem; padding: 2rem 0;'>
    <b>📊 Tableau de Bord Professionnel - Indicateurs Macroéconomiques RDC</b><br><br>
    <span style='color: #888; font-size: 0.85rem;'>
    🔹 Données sources: Banque Mondiale API (World Bank Open Data)<br>
    🔹 Période couverte: 1970 - 2024<br>
    🔹 Méthode statistique: Corrélation de Spearman<br>
    🔹 Dernière mise à jour: 2024<br><br>
    <i>© 2026 - Dashboard Statistique & Analytique. Tous droits réservés.</i>
    </span>
    </div>
    """,
    unsafe_allow_html=True
)
