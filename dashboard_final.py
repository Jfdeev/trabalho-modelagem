import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from scipy import stats
import statsmodels.api as sm

warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Análise Premier League",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado avançado
st.markdown("""
<style>
    /* Tema principal */
    .main {
        padding-top: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Cards modernos */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%);
        color: #2c3e50; /* Texto escuro para contraste */
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }

    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }

    .metric-card h3 {
        color: #34495e; /* Títulos em cinza escuro */
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }

    .metric-card p {
        color: #2c3e50; /* Parágrafos em cinza escuro */
        margin: 0.25rem 0;
    }

    .metric-card strong {
        color: #2c3e50; /* Texto em negrito escuro */
    }

    /* Cards escuros para seções específicas */
    .metric-card-dark {
        background: linear-gradient(145deg, #34495e 0%, #2c3e50 100%);
        color: white; /* Texto branco para contraste */
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }

    .metric-card-dark:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .metric-card-dark h3 {
        color: #ecf0f1; /* Títulos em branco */
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }

    .metric-card-dark p {
        color: #bdc3c7; /* Parágrafos em cinza claro */
        margin: 0.25rem 0;
    }

    .metric-card-dark strong {
        color: white; /* Texto em negrito branco */
    }

    /* Boxes de insight aprimorados */
    .insight-box {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border-left: 5px solid #FFD700;
    }

    .insight-box h3,
    .insight-box h4 {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        margin-top: 0;
    }

    .insight-box p {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .success-box {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(86, 171, 47, 0.3);
    }

    .success-box h3,
    .success-box h4 {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        margin-top: 0;
    }

    .success-box p {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .warning-box {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);
    }

    .warning-box h3,
    .warning-box h4 {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        margin-top: 0;
    }

    .warning-box p {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    /* Tabs estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        color: #333 !important;
    }

    /* Sidebar melhorada */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Métricas principais */
    .big-metric {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }

    .big-metric h1 {
        font-size: 3em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .big-metric p {
        font-size: 1.2em;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }

    /* Animações */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Botões personalizados */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    /* Títulos aprimorados */
    h1 {
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
    }

    h2 {
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        border-bottom: 3px solid #FFD700;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }

    h3 {
        color: #333;
        margin: 1.5rem 0 1rem 0;
    }

    /* Selectbox personalizado */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 10px;
    }

    /* Slider personalizado */
    .stSlider > div > div {
        background: rgba(255,255,255,0.1);
    }

    /* Footer */
    .footer {
        background: rgba(0,0,0,0.1);
        padding: 2rem;
        border-radius: 15px;
        margin: 3rem 0 1rem 0;
        text-align: center;
        color: white;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega e prepara os dados com tratamento avançado"""
    try:
        df = pd.read_csv('dataset.csv')

        # Verificar se há colunas duplicadas e remover
        if df.columns.duplicated().any():
            st.warning("Colunas duplicadas detectadas no dataset. Removendo automaticamente...")
            df = df.loc[:, ~df.columns.duplicated()]

        # Mapeamento de colunas para nomes mais intuitivos
        column_mapping = {
            'Gls': 'Goals',
            'Ast': 'Assists',
            'Min': 'Minutes',
            'MP': 'Matches_Played',
            '90s': 'Ninety_Minutes',
            'G+A': 'Goals_Assists',
            'xG': 'Expected_Goals',
            'xAG': 'Expected_Assists',
            'CrdY': 'Yellow_Cards',
            'CrdR': 'Red_Cards'
        }

        # Aplicar mapeamento apenas para colunas que existem
        existing_mappings = {old: new for old, new in column_mapping.items() if old in df.columns}
        df = df.rename(columns=existing_mappings)

        # Tratamento de valores ausentes
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())

        # Limpeza de dados categóricos
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna('Unknown')

        # Engenharia de variáveis aprimorada
        if 'Goals' in df.columns and 'Minutes' in df.columns:
            df['Goals_per_90'] = np.where(df['Minutes'] > 0, (df['Goals'] / df['Minutes']) * 90, 0)

        if 'Assists' in df.columns and 'Minutes' in df.columns:
            df['Assists_per_90'] = np.where(df['Minutes'] > 0, (df['Assists'] / df['Minutes']) * 90, 0)

        if 'Goals' in df.columns and 'Assists' in df.columns:
            df['Total_Contributions'] = df['Goals'] + df['Assists']

        if 'Expected_Goals' in df.columns and 'Goals' in df.columns:
            df['Goal_Efficiency'] = np.where(df['Expected_Goals'] > 0, df['Goals'] / df['Expected_Goals'], 1)
            df['Goal_Difference'] = df['Goals'] - df['Expected_Goals']

        # Variável de performance composta
        if all(col in df.columns for col in ['Goals', 'Assists', 'Minutes']):
            # Normalizar minutos para evitar valores extremos
            minutes_normalized = np.clip(df['Minutes'] / 90, 0.1, 50)  # Min 0.1, Max 50 jogos
            df['Performance_Index'] = (df['Goals'] * 3 + df['Assists'] * 2) * np.log1p(minutes_normalized)

        # Classificação de jogadores por gols
        if 'Goals' in df.columns:
            df['Goal_Category'] = pd.cut(
                df['Goals'],
                bins=[-0.1, 0, 2, 5, 10, float('inf')],
                labels=['Zero', 'Low', 'Medium', 'High', 'Elite'],
                include_lowest=True
            )

        # Filtrar apenas jogadores com dados mínimos de qualidade
        min_minutes = 50  # Jogadores com pelo menos ~0.5 jogos de 90min
        if 'Minutes' in df.columns:
            df = df[df['Minutes'] >= min_minutes].copy()

        # Resetar índice após filtragem
        df = df.reset_index(drop=True)

        st.success(f"Dataset carregado: {len(df)} jogadores com dados válidos")
        return df

    except FileNotFoundError:
        st.error("Arquivo 'dataset.csv' não encontrado. Verifique se o arquivo está no diretório correto.")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

@st.cache_data
def calculate_correlation_matrix(df, columns):
    """Calcula matriz de correlação com cache para performance"""
    try:
        return df[columns].corr()
    except Exception as e:
        st.warning(f"Erro ao calcular correlações: {e}")
        return pd.DataFrame()

@st.cache_data
def get_descriptive_stats(df, columns):
    """Calcula estatísticas descritivas com cache"""
    try:
        return df[columns].describe()
    except Exception as e:
        st.warning(f"Erro ao calcular estatísticas: {e}")
        return pd.DataFrame()

@st.cache_data
def train_linear_model(X_train, y_train, X_test, y_test):
    """Treina modelo linear com cache para evitar retreinamento desnecessário"""
    try:
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predições
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Métricas
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
        mae_test = mean_absolute_error(y_test, y_pred_test)

        return {
            'model': model,
            'y_pred_train': y_pred_train,
            'y_pred_test': y_pred_test,
            'r2_train': r2_train,
            'r2_test': r2_test,
            'rmse_test': rmse_test,
            'mae_test': mae_test
        }
    except Exception as e:
        st.error(f"Erro no treinamento do modelo: {e}")
        return None

def show_overview(df):
    """Seção de visão geral aprimorada com métricas avançadas"""

    # Header principal com animação
    st.markdown("""
    <div class="fade-in">
        <h1>ANÁLISE PREMIER LEAGUE 2023/24</h1>
        <center><em>Decodificando o futebol através dos dados</em></center>
    </div>
    """, unsafe_allow_html=True)

    # Métricas principais em cards grandes
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="big-metric fade-in">
            <h1>{len(df)}</h1>
            <p>Jogadores Analisados</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_goals = df['Goals'].sum() if 'Goals' in df.columns else 0
        st.markdown(f"""
        <div class="big-metric fade-in">
            <h1>{total_goals}</h1>
            <p>🥅 Gols Totais</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        total_assists = df['Assists'].sum() if 'Assists' in df.columns else 0
        st.markdown(f"""
        <div class="big-metric fade-in">
            <h1>{total_assists}</h1>
            <p>Assistências Totais</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        unique_positions = df['Pos'].nunique() if 'Pos' in df.columns else 0
        st.markdown(f"""
        <div class="big-metric fade-in">
            <h1>{unique_positions}</h1>
            <p>Posições Únicas</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Análise de distribuição avançada
    col1, col2 = st.columns(2)

    with col1:
        if 'Goals' in df.columns:
            st.subheader("Distribuição de Gols")

            # Histograma interativo
            fig = px.histogram(
                df, x='Goals', nbins=20,
                title="Distribuição de Gols por Jogador",
                color_discrete_sequence=['#667eea'],
                template='plotly_white'
            )

            # Adicionar linha da média
            mean_goals = df['Goals'].mean()
            fig.add_vline(
                x=mean_goals,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Média: {mean_goals:.1f}"
            )

            fig.update_layout(
                xaxis_title="Número de Gols",
                yaxis_title="Frequência",
                showlegend=False,
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if 'Pos' in df.columns:
            st.subheader("🎭 Jogadores por Posição")

            pos_counts = df['Pos'].value_counts()

            # Gráfico de pizza interativo
            fig = px.pie(
                values=pos_counts.values,
                names=pos_counts.index,
                title="Distribuição por Posição",
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Jogadores: %{value}<br>Percentual: %{percent}<extra></extra>'
            )

            fig.update_layout(height=400)

            st.plotly_chart(fig, use_container_width=True)

    # Estatísticas descritivas interativas
    st.subheader("� Estatísticas Descritivas")

    # Seleção de variáveis para análise
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    important_cols = []

    for col in ['Goals', 'Assists', 'Expected_Goals', 'Minutes', 'Age']:
        if col in numeric_cols:
            important_cols.append(col)

    if not important_cols:
        important_cols = numeric_cols[:6]  # Fallback

    selected_vars = st.multiselect(
        "Selecione as variáveis para análise:",
        options=important_cols,
        default=important_cols[:4] if len(important_cols) >= 4 else important_cols
    )

    if selected_vars:
        stats_df = df[selected_vars].describe().round(3)

        # Exibir com formatação melhorada
        st.dataframe(
            stats_df,
            use_container_width=True,
            height=300
        )

        # Insights automáticos
        st.markdown("""
        <div class="insight-box">
            <h3>Insights Automáticos</h3>
        """, unsafe_allow_html=True)

        for var in selected_vars:
            if var in df.columns:
                mean_val = df[var].mean()
                std_val = df[var].std()
                cv = (std_val / mean_val) * 100 if mean_val > 0 else 0

                if cv > 100:
                    variability = "alta variabilidade"
                elif cv > 50:
                    variability = "variabilidade moderada"
                else:
                    variability = "baixa variabilidade"

                st.markdown(f"• {var}: Média de {mean_val:.2f} com {variability} (CV: {cv:.1f}%)")

        st.markdown("</div>", unsafe_allow_html=True)

def show_exploratory_analysis(df):
    """Análise exploratória com recursos avançados e interativos"""
    st.header("Análise Exploratória Avançada")

    # Filtros interativos no topo
    st.subheader("Controles de Análise")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Seletor de métrica principal
        metric_options = []
        for col in ['Goals', 'Assists', 'Total_Contributions', 'Performance_Index']:
            if col in df.columns:
                metric_options.append(col)

        if metric_options:
            main_metric = st.selectbox(
                "Métrica Principal para Análise:",
                metric_options,
                help="Selecione a métrica que será o foco da análise"
            )
        else:
            main_metric = 'Goals'  # fallback

    with col2:
        # Valor fixo para top performers
        top_n = 10

    with col3:
        # Filtro por categoria de performance
        if 'Goal_Category' in df.columns:
            categories = df['Goal_Category'].cat.categories.tolist()
            selected_categories = st.multiselect(
                "Categorias de Performance:",
                categories,
                default=categories,
                help="Filtrar jogadores por categoria de gols"
            )

            if selected_categories:
                df_filtered = df[df['Goal_Category'].isin(selected_categories)]
            else:
                df_filtered = df
        else:
            df_filtered = df

    # Top Performers Avançado
    st.subheader("Hall da Fama")

    col1, col2, col3 = st.columns(3)

    with col1:
        if 'Goals' in df_filtered.columns:
            st.markdown("### Artilheiros")
            top_scorers = df_filtered.nlargest(top_n, 'Goals')[['Player', 'Goals', 'Pos']]

            # Gráfico de barras interativo
            fig = px.bar(
                top_scorers,
                x='Goals',
                y='Player',
                color='Goals',
                orientation='h',
                title=f"Top {top_n} Artilheiros",
                color_continuous_scale='Viridis',
                template='plotly_white'
            )

            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if 'Assists' in df_filtered.columns:
            st.markdown("### Assistentes")
            top_assists = df_filtered.nlargest(top_n, 'Assists')[['Player', 'Assists', 'Pos']]

            fig = px.bar(
                top_assists,
                x='Assists',
                y='Player',
                color='Assists',
                orientation='h',
                title=f"Top {top_n} Assistentes",
                color_continuous_scale='Plasma',
                template='plotly_white'
            )

            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    with col3:
        if main_metric in df_filtered.columns:
            st.markdown(f"### 💫 {main_metric}")
            top_metric = df_filtered.nlargest(top_n, main_metric)[['Player', main_metric, 'Pos']]

            fig = px.bar(
                top_metric,
                x=main_metric,
                y='Player',
                color=main_metric,
                orientation='h',
                title=f"Top {top_n} - {main_metric}",
                color_continuous_scale='Cividis',
                template='plotly_white'
            )

            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    # Análise de Correlações Avançada
    st.subheader("🔗 Matriz de Correlações Interativa")

    # Seleção de variáveis para correlação
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    correlation_vars = st.multiselect(
        "Selecione variáveis para análise de correlação:",
        numeric_cols,
        default=[col for col in ['Goals', 'Assists', 'Expected_Goals', 'Minutes', 'Age'] if col in numeric_cols][:5]
    )

    if len(correlation_vars) >= 2:
        correlation_matrix = df_filtered[correlation_vars].corr()

        # Heatmap interativo
        fig = px.imshow(
            correlation_matrix,
            x=correlation_vars,
            y=correlation_vars,
            color_continuous_scale='RdBu',
            title="Matriz de Correlações",
            aspect='auto',
            text_auto='.3f'
        )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Top correlações
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)
        correlations = correlation_matrix.where(mask).stack().reset_index()
        correlations.columns = ['Var1', 'Var2', 'Correlação']
        correlations = correlations.reindex(correlations['Correlação'].abs().sort_values(ascending=False).index)

        st.markdown("### Correlações Mais Significativas:")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("🔥 Correlações Positivas Fortes:")
            positive_corr = correlations[correlations['Correlação'] > 0.5].head(5)
            for _, row in positive_corr.iterrows():
                st.markdown(f"• {row['Var1']} × {row['Var2']}: {row['Correlação']:.3f}")

        with col2:
            st.markdown("Correlações Negativas Fortes:")
            negative_corr = correlations[correlations['Correlação'] < -0.3].head(5)
            for _, row in negative_corr.iterrows():
                st.markdown(f"• {row['Var1']} × {row['Var2']}: {row['Correlação']:.3f}")

    # Análise por Posição
    if 'Pos' in df_filtered.columns:
        st.subheader("🎭 Performance por Posição")

        # Box plot interativo
        if main_metric in df_filtered.columns:
            fig = px.box(
                df_filtered,
                x='Pos',
                y=main_metric,
                title=f"Distribuição de {main_metric} por Posição",
                color='Pos',
                template='plotly_white'
            )

            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Estatísticas por posição
        pos_stats = df_filtered.groupby('Pos')[correlation_vars].mean().round(3)

        st.markdown("### 📊 Médias por Posição:")
        st.dataframe(pos_stats, use_container_width=True)

    # Insights Automáticos
    st.markdown("""
    <div class="success-box">
        <h3>Insights Automáticos da Análise</h3>
    """, unsafe_allow_html=True)

    # Gerar insights baseados nos dados
    if 'Goals' in df_filtered.columns:
        max_goals = df_filtered['Goals'].max()
        avg_goals = df_filtered['Goals'].mean()
        top_scorer = df_filtered.loc[df_filtered['Goals'].idxmax(), 'Player']

        st.markdown(f"• Artilheiro: {top_scorer} com {max_goals} gols ({max_goals/avg_goals:.1f}x a média)")

    if len(correlation_vars) >= 2:
        strongest_corr = correlations.iloc[0]
        st.markdown(f"• Correlação mais forte: {strongest_corr['Var1']} × {strongest_corr['Var2']} ({strongest_corr['Correlação']:.3f})")

    if 'Pos' in df_filtered.columns and main_metric in df_filtered.columns:
        best_position = pos_stats[main_metric].idxmax()
        best_avg = pos_stats.loc[best_position, main_metric]
        st.markdown(f"• Posição com melhor {main_metric}: {best_position} (média: {best_avg:.2f})")

    st.markdown("</div>", unsafe_allow_html=True)

def show_statistical_modeling(df):
    """Modelagem estatística com regressão linear"""
    st.header("Modelagem Estatística - Regressão Linear")

    # Configurações da modelagem
    st.subheader("Configurações do Modelo")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Seleção de variável dependente
        target_options = []
        for col in ['Goals', 'Assists', 'Total_Contributions', 'Performance_Index']:
            if col in df.columns:
                target_options.append(col)

        if target_options:
            target_var = st.selectbox(
                "Variável Dependente (Y):",
                target_options,
                help="O que queremos prever"
            )
        else:
            st.error("Nenhuma variável dependente encontrada")
            return

    with col2:
        # Seleção de features
        feature_options = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if col != target_var and not col.endswith('_Category'):
                feature_options.append(col)

        selected_features = st.multiselect(
            "📊 Variáveis Independentes (X):",
            feature_options,
            default=feature_options[:4] if len(feature_options) >= 4 else feature_options,
            help="Variáveis que usaremos para fazer a predição"
        )

    with col3:
        # Configurações do modelo
        test_size = st.slider(
            "📊 Tamanho do Teste (%):",
            min_value=10,
            max_value=40,
            value=20,
            help="Porcentagem dos dados para teste"
        ) / 100

        random_state = st.number_input(
            "🎲 Seed Aleatória:",
            min_value=1,
            max_value=1000,
            value=42,
            help="Para reprodutibilidade dos resultados"
        )

    if not selected_features:
        st.warning("⚠️ Selecione pelo menos uma variável independente")
        return

    # Preparação dos dados
    try:
        X = df[selected_features].fillna(df[selected_features].median())
        y = df[target_var].fillna(df[target_var].median())

        # Verificar se há dados suficientes
        if len(X) < 10:
            st.error("❌ Dados insuficientes para modelagem")
            return

        # Divisão treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        st.success(f"✅ Dados preparados: {len(X_train)} treino + {len(X_test)} teste")

    except Exception as e:
        st.error(f"❌ Erro na preparação dos dados: {e}")
        return

    # Modelagem com Regressão Linear
    st.subheader("Regressão Linear")

    try:
        # Treinar modelo
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predições
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Métricas
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
        mae_test = mean_absolute_error(y_test, y_pred_test)

        # Exibir métricas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 R² Score</h3>
                <p><strong>Treino:</strong> {r2_train:.3f}</p>
                <p><strong>Teste:</strong> {r2_test:.3f}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📏 RMSE</h3>
                <p><strong>Teste:</strong> {rmse_test:.3f}</p>
                <p> (Raiz do Erro Quadrático Médio)</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>MAE</h3>
                <p><strong>Teste:</strong> {mae_test:.3f}</p>
                <p> (Erro Absoluto Médio)</p>
            </div>
            """, unsafe_allow_html=True)

        # Interpretação do modelo
        quality = "excelente" if r2_test > 0.8 else "boa" if r2_test > 0.6 else "moderada" if r2_test > 0.4 else "fraca"
        st.markdown(f"""
        <div class="insight-box">
            <h4>Interpretação do Modelo</h4>
            <p>O modelo explica <strong>{r2_test*100:.1f}%</strong> da variabilidade em {target_var}</p>
            <p>Performance: <strong>{quality}</strong></p>
            <p>Erro médio: <strong>{mae_test:.2f}</strong> unidades</p>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Erro no treinamento do modelo: {e}")
        return

    # Gráfico de predições vs reais
    st.subheader("Predições vs Valores Reais")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=y_test,
        y=y_pred_test,
        mode='markers',
        name='Predições',
        marker=dict(size=8, opacity=0.7, color='blue'),
        hovertemplate='<b>Regressão Linear</b><br>Real: %{x:.2f}<br>Predito: %{y:.2f}<extra></extra>'
    ))

    # Linha de predição perfeita
    min_val = min(y_test.min(), y_pred_test.min())
    max_val = max(y_test.max(), y_pred_test.max())

    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        name='Predição Perfeita',
        line=dict(color='red', dash='dash', width=2)
    ))

    fig.update_layout(
        title=f"Predições vs Valores Reais - {target_var}",
        xaxis_title=f"{target_var} Real",
        yaxis_title=f"{target_var} Predito",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Intervalos de confiança
    st.subheader("📏 Intervalos de Confiança (95%)")

    try:
        # Usar statsmodels para intervalos de confiança
        X_sm = sm.add_constant(X_train)
        model_sm = sm.OLS(y_train, X_sm).fit()

        conf_int = model_sm.conf_int()
        conf_int.columns = ['Limite Inferior', 'Limite Superior']
        conf_int.index = ['Intercepto'] + selected_features

        # Adicionar coeficientes
        conf_int['Coeficiente'] = model_sm.params
        conf_int['P-valor'] = model_sm.pvalues

        # Reordenar colunas
        conf_int = conf_int[['Coeficiente', 'Limite Inferior', 'Limite Superior', 'P-valor']]

        st.dataframe(conf_int.round(4), use_container_width=True)

        # Gráfico dos intervalos de confiança
        coef_plot_df = conf_int[conf_int.index != 'Intercepto'].copy()

        if not coef_plot_df.empty:
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=coef_plot_df['Coeficiente'],
                y=coef_plot_df.index,
                mode='markers',
                marker=dict(size=10, color='blue'),
                error_x=dict(
                    type='data',
                    symmetric=False,
                    array=coef_plot_df['Limite Superior'] - coef_plot_df['Coeficiente'],
                    arrayminus=coef_plot_df['Coeficiente'] - coef_plot_df['Limite Inferior']
                ),
                name='Coeficientes com IC 95%'
            ))

            # Linha vertical em zero
            fig.add_vline(x=0, line_dash="dash", line_color="red",
                         annotation_text="Sem efeito")

            fig.update_layout(
                title="Intervalos de Confiança dos Coeficientes (95%)",
                xaxis_title="Valor do Coeficiente",
                yaxis_title="Variáveis",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

        # Interpretação automática
        significant_vars = conf_int[conf_int['P-valor'] < 0.05].index.tolist()
        if 'Intercepto' in significant_vars:
            significant_vars.remove('Intercepto')

        if significant_vars:
            st.markdown(f"""
            <div class="insight-box">
                <h4>📊 Variáveis Estatisticamente Significativas (p < 0.05):</h4>
                <p>{', '.join(significant_vars)}</p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"⚠️ Não foi possível calcular intervalos de confiança: {e}")

    # Simulador de predições
    st.subheader("Simulador de Predições")

    with st.expander("Fazer Predição Personalizada"):
        prediction_inputs = {}

        for feature in selected_features:
            min_val = float(df[feature].min())
            max_val = float(df[feature].max())
            mean_val = float(df[feature].mean())

            prediction_inputs[feature] = st.slider(
                f"{feature}:",
                min_value=min_val,
                max_value=max_val,
                value=mean_val
            )

        if st.button("Fazer Predição"):
            new_data = pd.DataFrame([prediction_inputs])
            new_data_sm = sm.add_constant(new_data)

            prediction = model_sm.get_prediction(new_data_sm)
            pred_value = prediction.predicted_mean[0]
            pred_summary = prediction.summary_frame(alpha=0.05)

            ci_lower = pred_summary['obs_ci_lower'].iloc[0]
            ci_upper = pred_summary['obs_ci_upper'].iloc[0]

            st.markdown(f"""
            <div class="success-box">
                <h4>Resultado da Predição</h4>
                <p><strong>Valor Predito:</strong> {pred_value:.2f}</p>
                <p><strong>Intervalo de Confiança (95%):</strong> [{ci_lower:.2f}, {ci_upper:.2f}]</p>
            </div>
            """, unsafe_allow_html=True)

    # Preparação dos dados
    X = df[selected_features].fillna(df[selected_features].mean())

    # Normalização
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

def show_statistical_tests_advanced(df):
    """Seção avançada com múltiplos testes estatísticos"""
    st.header("Testes Estatísticos Avançados")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        st.error("❌ Dados insuficientes para testes estatísticos")
        return

    st.subheader("Configuração dos Testes")

    test_type = st.selectbox(
        "📊 Escolha o tipo de teste:",
        [
            "🔗 Correlação (Pearson vs Spearman)",
            "Normalidade (Shapiro-Wilk)",
            "⚖️ Comparação de Grupos (t-test, Mann-Whitney)",
            "🎲 ANOVA (One-way)",
            "Regressão Linear (Significância)",
            "📊 Teste de Homocedasticidade"
        ]
    )

    if "Correlação" in test_type:
        st.subheader("🔗 Análise de Correlação")

        col1, col2 = st.columns(2)

        with col1:
            var1 = st.selectbox("Variável 1:", numeric_cols)

        with col2:
            var2 = st.selectbox("Variável 2:", [col for col in numeric_cols if col != var1])

        if var1 and var2:
            # Pearson
            from scipy.stats import pearsonr, spearmanr

            # Remover valores nulos
            data_clean = df[[var1, var2]].dropna()

            if len(data_clean) > 3:
                pearson_corr, pearson_p = pearsonr(data_clean[var1], data_clean[var2])
                spearman_corr, spearman_p = spearmanr(data_clean[var1], data_clean[var2])

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📊 Pearson</h3>
                        <p><strong>r = {pearson_corr:.4f}</strong></p>
                        <p>p-valor: {pearson_p:.4f}</p>
                        <p>{'✅ Significativo' if pearson_p < 0.05 else '❌ Não significativo'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Spearman</h3>
                        <p><strong>ρ = {spearman_corr:.4f}</strong></p>
                        <p>p-valor: {spearman_p:.4f}</p>
                        <p>{'✅ Significativo' if spearman_p < 0.05 else '❌ Não significativo'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Gráfico de dispersão
                fig = px.scatter(
                    data_clean,
                    x=var1,
                    y=var2,
                    title=f"Correlação: {var1} vs {var2}",
                    trendline="ols"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Interpretação
                strength = "forte" if abs(pearson_corr) > 0.7 else "moderada" if abs(pearson_corr) > 0.3 else "fraca"
                direction = "positiva" if pearson_corr > 0 else "negativa"

                st.markdown(f"""
                <div class="insight-box">
                    <h4>📝 Interpretação</h4>
                    <p>Correlação <strong>{strength}</strong> e <strong>{direction}</strong> entre {var1} e {var2}</p>
                    <p>{'As variáveis têm relação linear significativa' if pearson_p < 0.05 else 'Não há evidência de relação linear significativa'}</p>
                </div>
                """, unsafe_allow_html=True)

    elif "Normalidade" in test_type:
        st.subheader("Teste de Normalidade")

        selected_var = st.selectbox("Escolha a variável:", numeric_cols)

        if selected_var:
            from scipy.stats import shapiro, normaltest

            data = df[selected_var].dropna()

            if len(data) > 3:
                # Shapiro-Wilk
                shapiro_stat, shapiro_p = shapiro(data)

                # D'Agostino
                dagostino_stat, dagostino_p = normaltest(data)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🔬 Shapiro-Wilk</h3>
                        <p><strong>W = {shapiro_stat:.4f}</strong></p>
                        <p>p-valor: {shapiro_p:.4f}</p>
                        <p>{'❌ Não normal' if shapiro_p < 0.05 else '✅ Normal'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📊 D'Agostino</h3>
                        <p><strong>K² = {dagostino_stat:.4f}</strong></p>
                        <p>p-valor: {dagostino_p:.4f}</p>
                        <p>{'❌ Não normal' if dagostino_p < 0.05 else '✅ Normal'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    # Estatísticas descritivas
                    mean_val = data.mean()
                    std_val = data.std()
                    skew_val = data.skew()
                    kurt_val = data.kurtosis()

                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Descritivas</h3>
                        <p>Média: {mean_val:.2f}</p>
                        <p>Desvio: {std_val:.2f}</p>
                        <p>Assimetria: {skew_val:.2f}</p>
                        <p>Curtose: {kurt_val:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Histograma com curva normal
                fig = go.Figure()

                # Histograma
                fig.add_trace(go.Histogram(
                    x=data,
                    name="Dados",
                    nbinsx=30,
                    opacity=0.7,
                    histnorm='probability density'
                ))

                # Curva normal teórica
                x_norm = np.linspace(data.min(), data.max(), 100)
                y_norm = stats.norm.pdf(x_norm, mean_val, std_val)

                fig.add_trace(go.Scatter(
                    x=x_norm,
                    y=y_norm,
                    mode='lines',
                    name='Normal Teórica',
                    line=dict(color='red', width=2)
                ))

                fig.update_layout(
                    title=f"Distribuição de {selected_var}",
                    xaxis_title=selected_var,
                    yaxis_title="Densidade",
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

    elif "Comparação de Grupos" in test_type:
        st.subheader("⚖️ Comparação de Grupos")

        # Selecionar variável categórica para grupos
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        if not categorical_cols:
            st.warning("❌ Nenhuma variável categórica disponível para formar grupos")
            return

        col1, col2 = st.columns(2)

        with col1:
            group_var = st.selectbox("Variável de Agrupamento:", categorical_cols)

        with col2:
            numeric_var = st.selectbox("Variável Numérica:", numeric_cols)

        if group_var and numeric_var:
            # Filtrar apenas grupos com dados suficientes
            group_counts = df[group_var].value_counts()
            valid_groups = group_counts[group_counts >= 5].index.tolist()[:2]  # Máximo 2 grupos

            if len(valid_groups) >= 2:
                group1_data = df[df[group_var] == valid_groups[0]][numeric_var].dropna()
                group2_data = df[df[group_var] == valid_groups[1]][numeric_var].dropna()

                from scipy.stats import ttest_ind, mannwhitneyu

                # t-test
                t_stat, t_p = ttest_ind(group1_data, group2_data)

                # Mann-Whitney U
                u_stat, u_p = mannwhitneyu(group1_data, group2_data, alternative='two-sided')

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📊 t-test</h3>
                        <p><strong>t = {t_stat:.4f}</strong></p>
                        <p>p-valor: {t_p:.4f}</p>
                        <p>{'✅ Diferença significativa' if t_p < 0.05 else '❌ Sem diferença'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🎲 Mann-Whitney</h3>
                        <p><strong>U = {u_stat:.0f}</strong></p>
                        <p>p-valor: {u_p:.4f}</p>
                        <p>{'✅ Diferença significativa' if u_p < 0.05 else '❌ Sem diferença'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    effect_size = abs(group1_data.mean() - group2_data.mean()) / np.sqrt((group1_data.var() + group2_data.var()) / 2)

                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📏 Tamanho do Efeito</h3>
                        <p><strong>d = {effect_size:.4f}</strong></p>
                        <p>Grupo 1 (n={len(group1_data)})</p>
                        <p>Grupo 2 (n={len(group2_data)})</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Box plot comparativo
                fig = go.Figure()

                fig.add_trace(go.Box(
                    y=group1_data,
                    name=f"{valid_groups[0]}",
                    boxpoints='outliers'
                ))

                fig.add_trace(go.Box(
                    y=group2_data,
                    name=f"{valid_groups[1]}",
                    boxpoints='outliers'
                ))

                fig.update_layout(
                    title=f"Comparação: {numeric_var} por {group_var}",
                    yaxis_title=numeric_var,
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

    elif "Regressão Linear" in test_type:
        st.subheader("Teste de Hipótese H1 - Regressão Linear")

        st.markdown("""
        <div class="insight-box">
            <h4>📋 Formulação das Hipóteses</h4>
            <p><strong>H0:</strong> Não existe relação linear significativa entre as variáveis (β = 0)</p>
            <p><strong>H1:</strong> Existe relação linear significativa entre as variáveis (β ≠ 0)</p>
            <p><strong>Nível de significância:</strong> α = 0.05</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            dependent_var = st.selectbox(
                "Variável Dependente (Y):",
                numeric_cols,
                help="Variável que queremos prever"
            )

        with col2:
            independent_vars = st.multiselect(
                "Variáveis Independentes (X):",
                [col for col in numeric_cols if col != dependent_var],
                help="Variáveis preditoras"
            )

        if dependent_var and independent_vars:
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import r2_score
            import statsmodels.api as sm
            from scipy import stats

            # Preparar dados
            X = df[independent_vars].dropna()
            y = df[dependent_var].dropna()

            # Sincronizar índices
            common_idx = X.index.intersection(y.index)
            X = X.loc[common_idx]
            y = y.loc[common_idx]

            if len(X) > len(independent_vars) + 1:  # Verificar se há dados suficientes

                # Modelo sklearn para métricas básicas
                model_sklearn = LinearRegression()
                model_sklearn.fit(X, y)
                y_pred = model_sklearn.predict(X)
                r2 = r2_score(y, y_pred)

                # Modelo statsmodels para testes de significância
                X_sm = sm.add_constant(X)  # Adicionar intercepto
                model_sm = sm.OLS(y, X_sm).fit()

                # Teste F global
                f_statistic = model_sm.fvalue
                f_pvalue = model_sm.f_pvalue

                # Resultados do teste de hipótese
                st.subheader("📊 Resultados do Teste de Hipótese H1")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📈 Teste F Global</h3>
                        <p><strong>F = {f_statistic:.4f}</strong></p>
                        <p>p-valor: {f_pvalue:.6f}</p>
                        <p>{'✅ Rejeitar H0' if f_pvalue < 0.05 else '❌ Não rejeitar H0'}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📊 R² Ajustado</h3>
                        <p><strong>R²adj = {model_sm.rsquared_adj:.4f}</strong></p>
                        <p>R² = {r2:.4f}</p>
                        <p>{(r2*100):.1f}% da variância explicada</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    # Critério de decisão
                    decision = "SIGNIFICATIVA" if f_pvalue < 0.05 else "NÃO SIGNIFICATIVA"
                    decision_color = "green" if f_pvalue < 0.05 else "red"

                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>⚖️ Decisão</h3>
                        <p><strong style="color: {decision_color};">{decision}</strong></p>
                        <p>Graus de liberdade: {model_sm.df_model:.0f}</p>
                        <p>Resíduos: {model_sm.df_resid:.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Tabela de coeficientes
                st.subheader("📋 Análise dos Coeficientes")

                coef_data = []
                for i, var in enumerate(['const'] + independent_vars):
                    coef_val = model_sm.params[var]
                    p_val = model_sm.pvalues[var]
                    t_val = model_sm.tvalues[var]
                    conf_int = model_sm.conf_int().loc[var]

                    coef_data.append({
                        'Variável': var,
                        'Coeficiente': f"{coef_val:.4f}",
                        'Erro Padrão': f"{model_sm.bse[var]:.4f}",
                        'Estatística t': f"{t_val:.4f}",
                        'p-valor': f"{p_val:.6f}",
                        'IC 95% Inferior': f"{conf_int[0]:.4f}",
                        'IC 95% Superior': f"{conf_int[1]:.4f}",
                        'Significativo': "✅" if p_val < 0.05 else "❌"
                    })

                import pandas as pd
                coef_df = pd.DataFrame(coef_data)
                st.dataframe(coef_df, use_container_width=True)

                # Gráfico de resíduos vs preditos
                residuals = y - y_pred

                col1, col2 = st.columns(2)

                with col1:
                    fig_resid = go.Figure()
                    fig_resid.add_trace(go.Scatter(
                        x=y_pred,
                        y=residuals,
                        mode='markers',
                        name='Resíduos',
                        marker=dict(color='blue', opacity=0.6)
                    ))
                    fig_resid.add_hline(y=0, line_dash="dash", line_color="red")
                    fig_resid.update_layout(
                        title="Resíduos vs Valores Preditos",
                        xaxis_title="Valores Preditos",
                        yaxis_title="Resíduos",
                        height=400
                    )
                    st.plotly_chart(fig_resid, use_container_width=True)

                with col2:
                    # Q-Q plot dos resíduos
                    from scipy.stats import probplot

                    qq_data = probplot(residuals, dist="norm")

                    fig_qq = go.Figure()
                    fig_qq.add_trace(go.Scatter(
                        x=qq_data[0][0],
                        y=qq_data[0][1],
                        mode='markers',
                        name='Resíduos',
                        marker=dict(color='green', opacity=0.6)
                    ))
                    fig_qq.add_trace(go.Scatter(
                        x=qq_data[0][0],
                        y=qq_data[1][1] + qq_data[1][0] * qq_data[0][0],
                        mode='lines',
                        name='Linha Teórica',
                        line=dict(color='red', dash='dash')
                    ))
                    fig_qq.update_layout(
                        title="Q-Q Plot dos Resíduos",
                        xaxis_title="Quantis Teóricos",
                        yaxis_title="Quantis da Amostra",
                        height=400
                    )
                    st.plotly_chart(fig_qq, use_container_width=True)

                # Interpretação dos resultados
                st.subheader("📝 Interpretação dos Resultados")

                interpretation = []

                if f_pvalue < 0.05:
                    interpretation.append("✅ **Conclusão H1:** Rejeitamos a hipótese nula (H0). Há evidência estatística suficiente para afirmar que existe uma relação linear significativa entre as variáveis.")
                    interpretation.append(f"📊 O modelo explica {(r2*100):.1f}% da variabilidade na variável dependente '{dependent_var}'.")
                else:
                    interpretation.append("❌ **Conclusão H0:** Não rejeitamos a hipótese nula (H0). Não há evidência estatística suficiente para afirmar que existe uma relação linear significativa.")

                # Análise individual dos coeficientes
                significant_vars = [var for var in independent_vars if model_sm.pvalues[var] < 0.05]
                non_significant_vars = [var for var in independent_vars if model_sm.pvalues[var] >= 0.05]

                if significant_vars:
                    interpretation.append(f"🎯 **Variáveis significativas:** {', '.join(significant_vars)}")
                if non_significant_vars:
                    interpretation.append(f"⚠️ **Variáveis não significativas:** {', '.join(non_significant_vars)}")

                interpretation.append(f"📈 **Qualidade do ajuste:** R² ajustado = {model_sm.rsquared_adj:.4f}")

                for text in interpretation:
                    st.markdown(text)

                # Pressupostos do modelo
                with st.expander("🔍 Verificação dos Pressupostos"):
                    st.markdown("""
                    **Pressupostos da Regressão Linear:**
                    1. **Linearidade:** Relação linear entre X e Y
                    2. **Independência:** Observações independentes
                    3. **Homocedasticidade:** Variância constante dos erros
                    4. **Normalidade:** Resíduos seguem distribuição normal

                    **Verificação visual:**
                    - **Gráfico de Resíduos:** Pontos devem estar distribuídos aleatoriamente em torno de zero
                    - **Q-Q Plot:** Pontos devem seguir aproximadamente a linha diagonal
                    """)
            else:
                st.warning("❌ Dados insuficientes para realizar a regressão linear")

def show_player_comparison(df):
    """Nova seção para comparação detalhada entre jogadores"""
    st.header("🥊 Comparação de Jogadores")

    # Seleção de jogadores
    st.subheader("👥 Selecione os Jogadores")

    col1, col2 = st.columns(2)

    with col1:
        player1 = st.selectbox(
            "🔵 Jogador 1:",
            df['Player'].tolist(),
            help="Selecione o primeiro jogador para comparação"
        )

    with col2:
        player2 = st.selectbox(
            "🔴 Jogador 2:",
            df['Player'].tolist(),
            index=1 if len(df) > 1 else 0,
            help="Selecione o segundo jogador para comparação"
        )

    if player1 == player2:
        st.warning("⚠️ Selecione jogadores diferentes para comparação")
        return

    # Dados dos jogadores
    p1_data = df[df['Player'] == player1].iloc[0]
    p2_data = df[df['Player'] == player2].iloc[0]

    # Comparação visual em cards
    st.subheader("📊 Comparação Geral")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #1f77b4;">
            <h3>🔵 {player1}</h3>
            <p><strong>Posição:</strong> {p1_data.get('Pos', 'N/A')}</p>
            <p><strong>Idade:</strong> {p1_data.get('Age', 'N/A')}</p>
            <p><strong>Time:</strong> {p1_data.get('Squad', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; font-size: 3em;">
            ⚔️
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #ff7f0e;">
            <h3>🔴 {player2}</h3>
            <p><strong>Posição:</strong> {p2_data.get('Pos', 'N/A')}</p>
            <p><strong>Idade:</strong> {p2_data.get('Age', 'N/A')}</p>
            <p><strong>Time:</strong> {p2_data.get('Squad', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    # Métricas de performance
    st.subheader("⚽ Métricas de Performance")

    metrics_to_compare = []
    for col in ['Goals', 'Assists', 'Expected_Goals', 'Minutes', 'Goals_per_90', 'Assists_per_90']:
        if col in df.columns:
            metrics_to_compare.append(col)

    if metrics_to_compare:
        comparison_data = []

        for metric in metrics_to_compare:
            p1_val = p1_data.get(metric, 0)
            p2_val = p2_data.get(metric, 0)

            comparison_data.append({
                'Métrica': metric,
                player1: p1_val,
                player2: p2_val,
                'Diferença': p1_val - p2_val,
                'Vantagem': player1 if p1_val > p2_val else player2 if p2_val > p1_val else 'Empate'
            })

        comparison_df = pd.DataFrame(comparison_data)

        # Gráfico radar/polar
        fig = go.Figure()

        # Normalizar valores para o gráfico radar
        for i, metric in enumerate(metrics_to_compare):
            max_val = df[metric].max() if df[metric].max() > 0 else 1

            p1_norm = (p1_data.get(metric, 0) / max_val) * 100
            p2_norm = (p2_data.get(metric, 0) / max_val) * 100

            if i == 0:  # Primeiro loop
                fig.add_trace(go.Scatterpolar(
                    r=[p1_norm] + [0] * (len(metrics_to_compare) - 1),
                    theta=metrics_to_compare,
                    fill='toself',
                    name=player1,
                    line_color='blue'
                ))

                fig.add_trace(go.Scatterpolar(
                    r=[p2_norm] + [0] * (len(metrics_to_compare) - 1),
                    theta=metrics_to_compare,
                    fill='toself',
                    name=player2,
                    line_color='red'
                ))
            else:
                # Atualizar dados existentes
                fig.data[0].r = [p1_data.get(m, 0) / df[m].max() * 100 for m in metrics_to_compare]
                fig.data[1].r = [p2_data.get(m, 0) / df[m].max() * 100 for m in metrics_to_compare]

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Comparação de Performance (% do máximo no dataset)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Tabela de comparação
        st.subheader("📋 Tabela Comparativa")
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    # Insights da comparação
    st.subheader("Insights da Comparação")

    insights = []

    if 'Goals' in df.columns:
        goals_diff = p1_data.get('Goals', 0) - p2_data.get('Goals', 0)
        if abs(goals_diff) > 0:
            better_scorer = player1 if goals_diff > 0 else player2
            insights.append(f"⚽ {better_scorer} é mais artilheiro ({abs(goals_diff)} gols de diferença)")

    if 'Assists' in df.columns:
        assists_diff = p1_data.get('Assists', 0) - p2_data.get('Assists', 0)
        if abs(assists_diff) > 0:
            better_assistant = player1 if assists_diff > 0 else player2
            insights.append(f"{better_assistant} é melhor assistente ({abs(assists_diff)} assistências de diferença)")

    if 'Minutes' in df.columns:
        minutes_diff = p1_data.get('Minutes', 0) - p2_data.get('Minutes', 0)
        if abs(minutes_diff) > 90:  # Mais de um jogo de diferença
            more_minutes = player1 if minutes_diff > 0 else player2
            insights.append(f"⏱️ {more_minutes} jogou mais ({abs(minutes_diff):.0f} minutos de diferença)")

    if insights:
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box">
                {insight}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📊 Jogadores com performance muito similar!")

def show_team_analysis(df):
    """Nova seção para análise por time"""
    st.header("🏟️ Análise por Times")

    if 'Squad' not in df.columns:
        st.error("❌ Dados de times não disponíveis")
        return

    # Seleção de time
    teams = sorted(df['Squad'].unique())
    selected_team = st.selectbox(
        "⚽ Selecione um Time:",
        teams,
        help="Escolha um time para análise detalhada"
    )

    team_data = df[df['Squad'] == selected_team]

    # Estatísticas do time
    st.subheader(f"📊 Estatísticas - {selected_team}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_players = len(team_data)
        st.markdown(f"""
        <div class="big-metric">
            <h1>{total_players}</h1>
            <p>👥 Jogadores</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_goals = team_data['Goals'].sum() if 'Goals' in team_data.columns else 0
        st.markdown(f"""
        <div class="big-metric">
            <h1>{total_goals}</h1>
            <p>⚽ Gols Totais</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        avg_age = team_data['Age'].mean() if 'Age' in team_data.columns else 0
        st.markdown(f"""
        <div class="big-metric">
            <h1>{avg_age:.1f}</h1>
            <p>👶 Idade Média</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        total_minutes = team_data['Minutes'].sum() if 'Minutes' in team_data.columns else 0
        st.markdown(f"""
        <div class="big-metric">
            <h1>{total_minutes:,}</h1>
            <p>⏱️ Minutos Totais</p>
        </div>
        """, unsafe_allow_html=True)

    # Top jogadores do time
    st.subheader(f"🌟 Destaques do {selected_team}")

    col1, col2 = st.columns(2)

    with col1:
        if 'Goals' in team_data.columns:
            top_scorer = team_data.loc[team_data['Goals'].idxmax()]
            st.markdown(f"""
            <div class="success-box">
                <h3>👑 Artilheiro</h3>
                <p><strong>{top_scorer['Player']}</strong></p>
                <p>{top_scorer['Goals']} gols</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if 'Assists' in team_data.columns:
            top_assistant = team_data.loc[team_data['Assists'].idxmax()]
            st.markdown(f"""
            <div class="success-box">
                <h3>Melhor Assistente</h3>
                <p><strong>{top_assistant['Player']}</strong></p>
                <p>{top_assistant['Assists']} assistências</p>
            </div>
            """, unsafe_allow_html=True)

    # Distribuição por posição no time
    if 'Pos' in team_data.columns:
        st.subheader("📊 Distribuição por Posição")

        pos_dist = team_data['Pos'].value_counts()

        fig = px.bar(
            x=pos_dist.index,
            y=pos_dist.values,
            title=f"Jogadores por Posição - {selected_team}",
            color=pos_dist.values,
            color_continuous_scale='Viridis'
        )

        fig.update_layout(
            xaxis_title="Posição",
            yaxis_title="Número de Jogadores",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Comparação com outros times
    st.subheader("🏆 Comparação com Outros Times")

    # Ranking de times
    team_stats = df.groupby('Squad').agg({
        'Goals': 'sum',
        'Assists': 'sum' if 'Assists' in df.columns else lambda x: 0,
        'Player': 'count'
    }).round(2)

    team_stats.columns = ['Gols Totais', 'Assistências Totais', 'Jogadores']
    team_stats = team_stats.sort_values('Gols Totais', ascending=False)

    # Posição do time selecionado
    team_position = team_stats.index.get_loc(selected_team) + 1

    st.markdown(f"""
    <div class="insight-box">
        <h3>Posição no Ranking</h3>
        <p><strong>{selected_team}</strong> está em <strong>{team_position}º lugar</strong> em gols totais</p>
    </div>
    """, unsafe_allow_html=True)

    # Top 10 times
    st.markdown("### 🏅 Top 10 Times por Gols")
    st.dataframe(team_stats.head(10), use_container_width=True)
    """Modelagem estatística e regressão linear"""
    st.header("📈 Modelagem Estatística")

    st.subheader("🎯 Modelo de Regressão Linear")

    # Seleção de variáveis para o modelo
    target_options = []
    feature_options = []

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in ['Goals', 'Assists', 'G+A', 'Performance_Score']:
        if col in df.columns:
            target_options.append(col)

    for col in ['xG', 'Shots', 'Min', 'Age', 'Goals_per_90', 'Assists_per_90']:
        if col in df.columns:
            feature_options.append(col)

    if target_options and feature_options:
        col1, col2 = st.columns(2)

        with col1:
            target_var = st.selectbox("Variável Dependente (Y):", target_options)

        with col2:
            selected_features = st.multiselect(
                "Variáveis Independentes (X):",
                feature_options,
                default=feature_options[:3] if len(feature_options) >= 3 else feature_options
            )

        if target_var and selected_features:
            # Preparar dados
            X = df[selected_features].fillna(df[selected_features].median())
            y = df[target_var].fillna(df[target_var].median())

            # Dividir dados
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Modelo de regressão linear
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Predições
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)

            # Métricas
            r2_train = r2_score(y_train, y_pred_train)
            r2_test = r2_score(y_test, y_pred_test)
            rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
            mae_test = mean_absolute_error(y_test, y_pred_test)

            # Exibir métricas
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("R² Treino", f"{r2_train:.3f}")
            with col2:
                st.metric("R² Teste", f"{r2_test:.3f}")
            with col3:
                st.metric("RMSE", f"{rmse_test:.3f}")
            with col4:
                st.metric("MAE", f"{mae_test:.3f}")

            # Gráfico de predições vs valores reais
            fig = px.scatter(
                x=y_test,
                y=y_pred_test,
                title=f"Predições vs Valores Reais - {target_var}",
                labels={'x': f'{target_var} Real', 'y': f'{target_var} Predito'}
            )

            # Linha de predição perfeita
            min_val = min(y_test.min(), y_pred_test.min())
            max_val = max(y_test.max(), y_pred_test.max())
            fig.add_scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode='lines',
                name='Predição Perfeita',
                line=dict(color='red', dash='dash')
            )

            st.plotly_chart(fig, use_container_width=True)

            # Coeficientes do modelo
            st.subheader("📊 Coeficientes do Modelo")

            coefficients_df = pd.DataFrame({
                'Variável': selected_features,
                'Coeficiente': model.coef_,
                'Abs_Coeficiente': np.abs(model.coef_)
            }).sort_values('Abs_Coeficiente', ascending=False)

            st.dataframe(coefficients_df, hide_index=True)

            # Intervalos de confiança usando statsmodels
            X_sm = sm.add_constant(X_train)
            model_sm = sm.OLS(y_train, X_sm).fit()

            st.subheader("📏 Intervalos de Confiança (95%)")
            conf_int = model_sm.conf_int()
            conf_int.columns = ['Limite Inferior', 'Limite Superior']
            conf_int.index = ['Intercepto'] + selected_features
            st.dataframe(conf_int.round(4))

def show_hypothesis_testing(df):
    """Testes de hipóteses"""
    st.header("🧪 Testes de Hipóteses")

    st.markdown("""
    ### 📋 Hipóteses Testadas
    Análise estatística rigorosa com base nos dados da Premier League:
    """)

    # Teste 1: Expected Goals prediz gols reais
    if 'Expected_Goals' in df.columns and 'Goals' in df.columns:
        st.subheader("H1: Expected Goals (xG) prediz gols reais")

        st.markdown("""
        <div class="insight-box">
            <h4>📋 Formulação da Hipótese</h4>
            <p><strong>H0:</strong> Não existe correlação significativa entre Expected Goals e gols reais (ρ = 0)</p>
            <p><strong>H1:</strong> Existe correlação significativa entre Expected Goals e gols reais (ρ ≠ 0)</p>
            <p><strong>Nível de significância:</strong> α = 0.05</p>
        </div>
        """, unsafe_allow_html=True)

        # Preparar dados - remover valores nulos
        clean_data = df[['Expected_Goals', 'Goals']].dropna()

        if len(clean_data) > 10:  # Verificar se há dados suficientes
            # Correlação de Pearson
            corr_coef, p_value = stats.pearsonr(clean_data['Expected_Goals'], clean_data['Goals'])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 Correlação</h3>
                    <p><strong>r = {corr_coef:.4f}</strong></p>
                    <p>Força: {'Forte' if abs(corr_coef) > 0.7 else 'Moderada' if abs(corr_coef) > 0.3 else 'Fraca'}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 p-valor</h3>
                    <p><strong>{p_value:.2e}</strong></p>
                    <p>Critério: p < 0.05</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                resultado = "✅ Rejeitamos H0" if p_value < 0.05 else "❌ Não rejeitamos H0"
                resultado_cor = "green" if p_value < 0.05 else "red"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚖️ Decisão</h3>
                    <p><strong style="color: {resultado_cor};">{resultado}</strong></p>
                    <p>n = {len(clean_data)} observações</p>
                </div>
                """, unsafe_allow_html=True)

            # Gráfico de dispersão
            fig = px.scatter(
                clean_data,
                x='Expected_Goals',
                y='Goals',
                title="Relação entre Expected Goals e Gols Reais",
                trendline="ols",
                labels={'Expected_Goals': 'Expected Goals (xG)', 'Goals': 'Gols Reais'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Interpretação detalhada
            st.markdown(f"""
            <div class="insight-box">
                <h4>📝 Interpretação dos Resultados</h4>
                <p><strong>Conclusão:</strong> {'Existe correlação significativa entre Expected Goals e gols reais.' if p_value < 0.05 else 'Não há evidência de correlação significativa.'}</p>
                <p><strong>Força da relação:</strong> Correlação {'forte' if abs(corr_coef) > 0.7 else 'moderada' if abs(corr_coef) > 0.3 else 'fraca'} (r = {corr_coef:.4f})</p>
                <p><strong>Significância:</strong> {'Estatisticamente significativo' if p_value < 0.05 else 'Não estatisticamente significativo'} (p = {p_value:.4f})</p>
                <p><strong>Interpretação prática:</strong> {'Expected Goals é um bom preditor de performance ofensiva real.' if p_value < 0.05 and abs(corr_coef) > 0.5 else 'Expected Goals tem relação limitada com gols reais neste dataset.'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❌ Dados insuficientes para realizar o teste de correlação")
    else:
        st.warning("❌ Colunas 'Expected_Goals' ou 'Goals' não encontradas no dataset")

    # Teste 2: Diferença de performance entre posições
    if 'Pos' in df.columns and 'Goals' in df.columns:
        st.subheader("H2: Existe diferença de performance entre posições")

        st.markdown("""
        <div class="insight-box">
            <h4>📋 Formulação da Hipótese</h4>
            <p><strong>H0:</strong> Não existe diferença significativa de gols entre posições</p>
            <p><strong>H1:</strong> Existe diferença significativa de gols entre posições</p>
            <p><strong>Teste:</strong> ANOVA (Analysis of Variance)</p>
        </div>
        """, unsafe_allow_html=True)

        # ANOVA
        positions = df['Pos'].unique()
        groups = [df[df['Pos'] == pos]['Goals'].dropna() for pos in positions]

        # Remover grupos vazios e com poucos dados
        groups = [group for group in groups if len(group) >= 3]

        if len(groups) >= 2:
            f_stat, p_value = stats.f_oneway(*groups)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 F-statistic</h3>
                    <p><strong>F = {f_stat:.4f}</strong></p>
                    <p>{len(groups)} grupos comparados</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 p-valor</h3>
                    <p><strong>{p_value:.4f}</strong></p>
                    <p>Critério: p < 0.05</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                resultado = "✅ Rejeitamos H0" if p_value < 0.05 else "❌ Não rejeitamos H0"
                resultado_cor = "green" if p_value < 0.05 else "red"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚖️ Decisão</h3>
                    <p><strong style="color: {resultado_cor};">{resultado}</strong></p>
                    <p>Total: {sum(len(g) for g in groups)} jogadores</p>
                </div>
                """, unsafe_allow_html=True)

            # Box plot por posição
            pos_data = []
            for pos in positions:
                pos_goals = df[df['Pos'] == pos]['Goals'].tolist()
                if len(pos_goals) >= 3:  # Apenas posições com dados suficientes
                    pos_data.extend([(pos, goal) for goal in pos_goals])

            if pos_data:
                pos_df = pd.DataFrame(pos_data, columns=['Posição', 'Gols'])

                fig = px.box(
                    pos_df,
                    x='Posição',
                    y='Gols',
                    title="Distribuição de Gols por Posição"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div class="insight-box">
                <h4>📝 Interpretação dos Resultados</h4>
                <p><strong>Conclusão:</strong> {'Existe diferença significativa de performance entre posições.' if p_value < 0.05 else 'Não há evidência de diferença significativa entre posições.'}</p>
                <p><strong>Estatística F:</strong> {f_stat:.4f} - {'Indica variação entre grupos maior que dentro dos grupos' if f_stat > 1 else 'Pouca variação entre grupos'}</p>
                <p><strong>Interpretação prática:</strong> {'Posição é um fator relevante para performance ofensiva.' if p_value < 0.05 else 'Posição não parece influenciar significativamente o número de gols.'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❌ Dados insuficientes para ANOVA (precisa de pelo menos 2 grupos com 3+ observações cada)")

    # Teste 3: Correlação entre idade e performance
    if 'Age' in df.columns and 'Goals' in df.columns:
        st.subheader("H3: Idade influencia performance")

        st.markdown("""
        <div class="insight-box">
            <h4>📋 Formulação da Hipótese</h4>
            <p><strong>H0:</strong> Não existe correlação significativa entre idade e gols (ρ = 0)</p>
            <p><strong>H1:</strong> Existe correlação significativa entre idade e gols (ρ ≠ 0)</p>
            <p><strong>Teste:</strong> Correlação de Pearson</p>
        </div>
        """, unsafe_allow_html=True)

        # Preparar dados
        age_goals_data = df[['Age', 'Goals']].dropna()

        if len(age_goals_data) > 10:
            corr_coef, p_value = stats.pearsonr(age_goals_data['Age'], age_goals_data['Goals'])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 Correlação</h3>
                    <p><strong>r = {corr_coef:.4f}</strong></p>
                    <p>Direção: {'Positiva' if corr_coef > 0 else 'Negativa'}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 p-valor</h3>
                    <p><strong>{p_value:.4f}</strong></p>
                    <p>Critério: p < 0.05</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                resultado = "✅ Rejeitamos H0" if p_value < 0.05 else "❌ Não rejeitamos H0"
                resultado_cor = "green" if p_value < 0.05 else "red"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚖️ Decisão</h3>
                    <p><strong style="color: {resultado_cor};">{resultado}</strong></p>
                    <p>n = {len(age_goals_data)} jogadores</p>
                </div>
                """, unsafe_allow_html=True)

            # Gráfico de dispersão idade vs gols
            fig = px.scatter(
                age_goals_data,
                x='Age',
                y='Goals',
                title="Relação entre Idade e Número de Gols",
                trendline="ols"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div class="insight-box">
                <h4>📝 Interpretação dos Resultados</h4>
                <p><strong>Conclusão:</strong> {'Existe correlação significativa entre idade e performance.' if p_value < 0.05 else 'Não há evidência de correlação significativa entre idade e performance.'}</p>
                <p><strong>Direção:</strong> {'Jogadores mais velhos tendem a marcar mais gols' if corr_coef > 0 and p_value < 0.05 else 'Jogadores mais novos tendem a marcar mais gols' if corr_coef < 0 and p_value < 0.05 else 'Idade não parece influenciar significativamente o número de gols'}</p>
                <p><strong>Força:</strong> Correlação {'forte' if abs(corr_coef) > 0.7 else 'moderada' if abs(corr_coef) > 0.3 else 'fraca'} (|r| = {abs(corr_coef):.4f})</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❌ Dados insuficientes para teste de correlação idade-performance")

    # Resumo dos testes
    st.subheader("📊 Resumo dos Testes de Hipóteses")

    st.markdown("""
    <div class="insight-box">
        <h4>🎯 Metodologia Aplicada</h4>
        <p><strong>Testes realizados:</strong> Correlação de Pearson e ANOVA</p>
        <p><strong>Nível de significância:</strong> α = 0.05 (95% de confiança)</p>
        <p><strong>Interpretação:</strong> p < 0.05 indica evidência estatística suficiente para rejeitar H0</p>
        <p><strong>Limitações:</strong> Resultados válidos para este dataset específico da temporada 2023/24</p>
    </div>
    """, unsafe_allow_html=True)

def show_visualizations(df):
    """Visualizações avançadas"""
    st.header("📊 Visualizações dos Dados")

    # Distribuição de gols
    if 'Goals' in df.columns:
        st.subheader("⚽ Distribuição de Gols")

        fig = px.histogram(
            df,
            x='Goals',
            nbins=20,
            title="Distribuição do Número de Gols",
            labels={'Goals': 'Número de Gols', 'count': 'Frequência'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Box plot por posição
    if 'Pos' in df.columns and 'Goals' in df.columns:
        st.subheader("📦 Performance por Posição")

        fig = px.box(
            df,
            x='Pos',
            y='Goals',
            title="Distribuição de Gols por Posição"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Scatter plot interativo
    if all(col in df.columns for col in ['xG', 'Goals']):
        st.subheader("🎯 Relação xG vs Gols Reais")

        fig = px.scatter(
            df,
            x='xG',
            y='Goals',
            color='Pos' if 'Pos' in df.columns else None,
            hover_data=['Player'] if 'Player' in df.columns else None,
            title="Expected Goals vs Gols Reais"
        )

        # Linha de tendência
        if len(df['xG'].dropna()) > 1:
            z = np.polyfit(df['xG'].dropna(), df['Goals'].dropna(), 1)
            p = np.poly1d(z)
            fig.add_scatter(
                x=df['xG'],
                y=p(df['xG']),
                mode='lines',
                name='Linha de Tendência',
                line=dict(color='red', width=2)
            )

        st.plotly_chart(fig, use_container_width=True)

def show_insights_solutions(df):
    """Insights e soluções práticas"""
    st.header("💡 Insights e Soluções Práticas")

    st.subheader("🔍 Principais Descobertas")

    insights = []

    # Insight sobre xG
    if 'xG' in df.columns and 'Goals' in df.columns:
        corr_xg = df['xG'].corr(df['Goals'])
        if abs(corr_xg) > 0.7:
            insights.append(f"⚽ Expected Goals é um excelente preditor: Correlação de {corr_xg:.3f} com gols reais")

    # Insight sobre top performers
    if 'Goals' in df.columns:
        top_scorer_goals = df['Goals'].max()
        avg_goals = df['Goals'].mean()
        insights.append(f"🏆 Concentração de performance: O artilheiro máximo ({top_scorer_goals} gols) marca {top_scorer_goals/avg_goals:.1f}x mais que a média ({avg_goals:.1f} gols)")

    # Insight sobre posições
    if 'Pos' in df.columns and 'Goals' in df.columns:
        pos_performance = df.groupby('Pos')['Goals'].mean().sort_values(ascending=False)
        if len(pos_performance) > 1:
            best_pos = pos_performance.index[0]
            best_avg = pos_performance.iloc[0]
            insights.append(f"🎯 Posição mais efetiva: {best_pos} tem média de {best_avg:.1f} gols")

    for insight in insights:
        st.markdown(f"""
        <div class="insight-box">
        {insight}
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🎯 Recomendações Práticas")

    recommendations = [
        "📊 Para Scouts: Utilize xG como métrica principal de avaliação - é mais confiável que gols totais",
        "💰 Para Contratações: Foque em jogadores com alto xG mas baixos gols realizados - podem estar subperformando temporariamente",
        "📈 Para Desenvolvimento: Analise eficiência de conversão para identificar jogadores que precisam melhorar finalização",
        "🎮 Para Estratégia: Considere posição ao definir expectativas de performance ofensiva",
        "⏱️ Para Gestão: Normalize métricas por 90 minutos para comparações justas entre jogadores"
    ]

    for rec in recommendations:
        st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 5px solid #4CAF50; color: #155724;">
        {rec}
        </div>
        """, unsafe_allow_html=True)

    st.subheader("⚠️ Limitações do Estudo")

    limitations = [
        "📅 Temporal: Análise limitada a uma temporada - padrões podem variar ao longo do tempo",
        "🏥 Contextual: Não considera lesões, mudanças táticas ou fatores externos",
        "⚽ Escopo: Foco em métricas ofensivas - defesa e meio-campo podem ter outros indicadores importantes",
        "📊 Causal: Correlações não implicam causalidade - são indicadores, não garantias"
    ]

    for limitation in limitations:
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 5px solid #ffc107; color: #856404;">
        {limitation}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Função principal do dashboard com interface moderna"""

    # Header principal com design atraente
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: white; font-size: 3.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            ⚽ PREMIER LEAGUE ANALYTICS
        </h1>
        <p style="color: white; font-size: 1.3em; margin: 1rem 0; opacity: 0.9;">
            🔬 <em>Decodificando o futebol através da ciência de dados</em> 📊
        </p>
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 15px; margin: 1rem auto; max-width: 600px;">
            <p style="color: white; margin: 0; font-size: 1.1em;">
                574 jogadores • 36 variáveis • Análises avançadas • Insights acionáveis
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Carregar dados com feedback visual
    with st.spinner('🔄 Carregando e preparando dados...'):
        df = load_data()

    if df is None:
        st.markdown("""
        <div class="warning-box">
            <h3>❌ Erro no Carregamento</h3>
            <p>Não foi possível carregar o dataset. Verifique se o arquivo 'dataset.csv' está disponível.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Sidebar aprimorada
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;">🎛️ PAINEL DE CONTROLE</h2>
        <p style="color: white; opacity: 0.8; margin: 0.5rem 0 0 0;">Personalize sua análise</p>
    </div>
    """, unsafe_allow_html=True)

    # Filtros avançados na sidebar
    with st.sidebar.expander("🎯 Filtros de Jogadores", expanded=True):
        # Filtro por posição
        if 'Pos' in df.columns:
            positions = ['Todas'] + sorted(list(df['Pos'].unique()))
            selected_pos = st.selectbox(
                "📍 Posição:",
                positions,
                help="Filtrar jogadores por posição"
            )

            if selected_pos != 'Todas':
                df = df[df['Pos'] == selected_pos]

        # Filtro por minutos (usando coluna correta)
        minutes_col = 'Minutes' if 'Minutes' in df.columns else 'Min'
        if minutes_col in df.columns:
            min_minutes = st.slider(
                "⏱️ Minutos mínimos jogados:",
                0,
                int(df[minutes_col].max()),
                0,
                help="Filtrar jogadores por tempo de jogo"
            )
            df = df[df[minutes_col] >= min_minutes]

        # Filtro por gols
        if 'Goals' in df.columns:
            min_goals = st.slider(
                "⚽ Gols mínimos:",
                0,
                int(df['Goals'].max()),
                0,
                help="Filtrar por número de gols"
            )
            df = df[df['Goals'] >= min_goals]

    # Status dos filtros
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: white; margin: 0 0 0.5rem 0;">📊 Dados Filtrados</h4>
        <p style="color: white; margin: 0;"><strong>{len(df)} jogadores</strong> selecionados</p>
        <p style="color: white; margin: 0; opacity: 0.8; font-size: 0.9em;">
            {f'Posição: {selected_pos}' if selected_pos != 'Todas' else 'Todas as posições'}<br>
            {f'Min. {min_minutes} minutos' if min_minutes > 0 else 'Sem filtro de minutos'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Configurações de visualização
    with st.sidebar.expander("🎨 Configurações de Visualização"):
        theme = st.selectbox(
            "🎨 Tema dos Gráficos:",
            ['plotly_white', 'plotly_dark', 'simple_white'],
            help="Escolha o tema visual dos gráficos"
        )

        show_animations = st.checkbox(
            "✨ Animações",
            value=True,
            help="Ativar animações nos gráficos"
        )

    # Armazenar configurações no session_state
    st.session_state.update({
        'theme': theme,
        'show_animations': show_animations
    })

    # Navegação principal simplificada - foco nas funcionalidades essenciais
    tab_config = {
        "🏠 Visão Geral": "overview",
        "🔍 Análise Exploratória": "exploratory",
        "📈 Modelagem Linear": "modeling",
        "� Testes de Hipóteses": "hypothesis",
        " Insights e Soluções": "insights"
    }

    selected_tab = st.selectbox(
        "🗺️ Navegação:",
        list(tab_config.keys()),
        help="Escolha a seção para explorar"
    )

    # Executar seção selecionada com tratamento de erros
    section = tab_config[selected_tab]

    try:
        if section == "overview":
            show_overview(df)
        elif section == "exploratory":
            show_exploratory_analysis(df)
        elif section == "modeling":
            show_statistical_modeling(df)
        elif section == "hypothesis":
            show_hypothesis_testing(df)
        elif section == "insights":
            show_insights_solutions(df)

    except Exception as e:
        st.markdown(f"""
        <div class="warning-box">
            <h3>⚠️ Erro na Seção</h3>
            <p>Ocorreu um erro ao carregar a seção <strong>{selected_tab}</strong>:</p>
            <p style="color: #ff6b6b; font-family: monospace;">{str(e)}</p>
            <p>🔄 Sugestões:</p>
            <ul>
                <li>Recarregue a página (F5)</li>
                <li>Verifique se o dataset está carregado corretamente</li>
                <li>Tente selecionar outra seção</li>
                <li>Se o problema persistir, verifique os dados de entrada</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Log detalhado do erro para desenvolvimento
        if st.checkbox("🔧 Mostrar detalhes técnicos do erro", key="show_error_details"):
            st.exception(e)

if __name__ == "__main__":
    main()
