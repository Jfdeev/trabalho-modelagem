# ⚙️ Configurações do Projeto - Premier League Analytics

# 📊 Configurações de dados
MIN_MINUTES_FILTER = 50  # Minutos mínimos para considerar um jogador
DEFAULT_TEST_SIZE = 0.2  # Proporção padrão para teste
RANDOM_STATE = 42  # Seed para reprodutibilidade

# 🎨 Configurações visuais
PLOTLY_CONFIG = {
    'displayModeBar': False,
    'responsive': True,
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'premier_league_chart',
        'height': 500,
        'width': 700,
        'scale': 1
    }
}

# 📈 Configurações de modelagem
TARGET_VARIABLES = ['Goals', 'Assists', 'Total_Contributions', 'Performance_Index']
FEATURE_BLACKLIST = ['_Category', 'Player', 'Squad', 'Nation', 'Pos']

# 🏆 Configurações de performance
DEFAULT_TOP_N = 10
CONFIDENCE_LEVEL = 0.95
ALPHA = 0.05

# 📝 Mensagens de erro
ERROR_MESSAGES = {
    'no_data': "❌ Nenhum dado encontrado para análise",
    'insufficient_data': "⚠️ Dados insuficientes para análise estatística confiável",
    'no_numeric_columns': "❌ Nenhuma coluna numérica encontrada no dataset",
    'model_training_failed': "❌ Falha no treinamento do modelo",
    'correlation_failed': "⚠️ Não foi possível calcular correlações"
}

# 🎯 Configurações específicas por seção
SECTION_CONFIG = {
    'overview': {
        'min_variables': 3,
        'default_variables': ['Goals', 'Assists', 'Minutes', 'Age']
    },
    'exploratory': {
        'max_correlation_vars': 8,
        'default_correlation_vars': ['Goals', 'Assists', 'Expected_Goals', 'Minutes', 'Age']
    },
    'modeling': {
        'min_samples': 20,
        'max_features': 10
    }
}
