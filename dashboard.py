#!/usr/bin/env python3
"""
⚽ PREMIER LEAGUE SCOUT CENTRAL - Versão Demonstração
Central de Análise para Contratação de Jogadores

Dashboard temático profissional para scouting de jogadores da Premier League
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Premier League Scout Central",
    page_icon="⚽",
    layout="wide"
)

# CSS temático da Premier League
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #37003c;
        text-align: center;
        font-weight: bold;
        background: linear-gradient(90deg, #37003c, #00ff85);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #37003c, #00ff85);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .player-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-title {
        color: #37003c;
        font-size: 1.8rem;
        font-weight: bold;
        border-bottom: 3px solid #00ff85;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
    
    .kpi-card {
        background-color: #f8f9fa;
        border-left: 4px solid #37003c;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega e processa dados do scouting"""
    df = pd.read_csv('dataset.csv')
    df_clean = df.dropna(subset=['Nation', 'Age', 'Born'])
    
    # Variáveis principais
    cols = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'MP', 'Starts', 'Min', 
            'Gls', 'Ast', 'G+A', 'xG', 'xAG', 'CrdY', 'CrdR']
    df_main = df_clean[cols].copy()
    
    # Métricas de scouting
    df_main['Gols_por_jogo'] = df_main['Gls'] / df_main['MP'].replace(0, 1)
    df_main['Assist_por_jogo'] = df_main['Ast'] / df_main['MP'].replace(0, 1)
    df_main['Participacao_gols'] = df_main['G+A'] / df_main['MP'].replace(0, 1)
    df_main['Min_por_jogo'] = df_main['Min'] / df_main['MP'].replace(0, 1)
    df_main['Taxa_titular'] = df_main['Starts'] / df_main['MP'].replace(0, 1)
    df_main['Valor_estimado'] = (df_main['xG'] * 2 + df_main['xAG'] - df_main['Age'] * 0.05) * 1000000
    df_main['Eficiencia_xG'] = df_main['Gls'] - df_main['xG']
    
    # Filtrar jogadores regulares
    return df_main[df_main['Min'] >= 300].reset_index(drop=True)

def main():
    # Header principal
    st.markdown('<h1 class="main-header">⚽ PREMIER LEAGUE SCOUT CENTRAL</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #666; margin-bottom: 2rem;">🎯 Sistema Inteligente de Análise para Contratação de Jogadores</p>', unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    # Sidebar - Filtros profissionais de scouting
    st.sidebar.markdown("## 🔍 PAINEL DE SCOUTING")
    st.sidebar.markdown("---")
    
    # Filtros
    age_range = st.sidebar.slider("📅 Faixa Etária", 16, 40, (18, 32))
    positions = st.sidebar.multiselect(
        "⚽ Posições", 
        options=sorted(df['Pos'].unique()),
        default=sorted(df['Pos'].unique())[:5]
    )
    min_games = st.sidebar.slider("🎮 Mínimo de Jogos", 5, 38, 10)
    
    # Aplicar filtros
    df_filtered = df[
        (df['Age'] >= age_range[0]) & 
        (df['Age'] <= age_range[1]) & 
        (df['Pos'].isin(positions)) &
        (df['MP'] >= min_games)
    ]
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h2>🎯</h2>
            <h3>{len(df_filtered)}</h3>
            <p>Jogadores Analisados</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_goals = df_filtered['Gols_por_jogo'].mean()
        st.markdown(f"""
        <div class="metric-box">
            <h2>⚽</h2>
            <h3>{avg_goals:.2f}</h3>
            <p>Média Gols/Jogo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_age = df_filtered['Age'].mean()
        st.markdown(f"""
        <div class="metric-box">
            <h2>📅</h2>
            <h3>{avg_age:.1f}</h3>
            <p>Idade Média</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_value = df_filtered['Valor_estimado'].mean()
        st.markdown(f"""
        <div class="metric-box">
            <h2>💰</h2>
            <h3>€{avg_value/1000000:.1f}M</h3>
            <p>Valor Médio</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs do dashboard
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Targets Premium", 
        "📊 Market Analysis", 
        "🔮 AI Predictor",
        "📋 Scout Report"
    ])
    
    with tab1:
        st.markdown('<div class="section-title">🎯 PRINCIPAIS ALVOS PARA CONTRATAÇÃO</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top Performers")
            top_performers = df_filtered.nlargest(8, 'Participacao_gols')
            
            for _, player in top_performers.iterrows():
                st.markdown(f"""
                <div class="player-card">
                    <h4>{player['Player']}</h4>
                    <p><strong>{player['Squad']}</strong> | {player['Pos']} | {int(player['Age'])} anos</p>
                    <p>⚽ {player['Gols_por_jogo']:.2f} G/J | 🎯 {player['Assist_por_jogo']:.2f} A/J | 💫 {player['Participacao_gols']:.2f} P/J</p>
                    <p>💰 Valor Est.: €{player['Valor_estimado']/1000000:.1f}M</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("💎 Young Talents (Sub-25)")
            young_talents = df_filtered[df_filtered['Age'] <= 25].nlargest(8, 'Participacao_gols')
            
            for _, player in young_talents.iterrows():
                potential = "🌟 Alto" if player['Participacao_gols'] > 0.3 else "⭐ Médio"
                st.markdown(f"""
                <div class="player-card">
                    <h4>{player['Player']}</h4>
                    <p><strong>{player['Squad']}</strong> | {player['Pos']} | {int(player['Age'])} anos</p>
                    <p>⚽ {player['Gols_por_jogo']:.2f} G/J | 🎯 {player['Assist_por_jogo']:.2f} A/J</p>
                    <p>🚀 Potencial: {potential} | 💰 €{player['Valor_estimado']/1000000:.1f}M</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-title">📊 ANÁLISE DE MERCADO</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot: Performance vs Valor
            fig1 = px.scatter(
                df_filtered,
                x='Valor_estimado',
                y='Participacao_gols',
                color='Pos',
                size='Age',
                hover_data=['Player', 'Squad'],
                title="💰 Valor Estimado vs Performance",
                labels={
                    'Valor_estimado': 'Valor Estimado (€)',
                    'Participacao_gols': 'Participação em Gols/Jogo'
                },
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            fig1.update_layout(height=500)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Performance por posição
            fig2 = px.box(
                df_filtered,
                x='Pos',
                y='Participacao_gols',
                color='Pos',
                title="📊 Performance por Posição",
                labels={'Participacao_gols': 'Participação Gols/Jogo'}
            )
            fig2.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Análise xG vs Performance Real
        st.subheader("🎯 Eficiência: Gols vs Expected Goals")
        fig3 = px.scatter(
            df_filtered,
            x='xG',
            y='Gls',
            color='Eficiencia_xG',
            size='Min_por_jogo',
            hover_data=['Player', 'Squad'],
            title="Jogadores acima da linha superam expectativas",
            color_continuous_scale='RdYlGn',
            labels={'Eficiencia_xG': 'Eficiência (Gols - xG)'}
        )
        
        # Linha de referência
        max_xg = df_filtered['xG'].max()
        fig3.add_shape(
            type='line',
            x0=0, y0=0, x1=max_xg, y1=max_xg,
            line=dict(dash='dash', color='red', width=2)
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.markdown('<div class="section-title">🔮 PREDITOR DE VALOR AI</div>', unsafe_allow_html=True)
        
        # Modelo de predição
        X = df_filtered[['xG', 'xAG', 'Age', 'Min_por_jogo']]
        y = df_filtered['Valor_estimado']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = LinearRegression().fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🤖 Simulador de Valor")
            st.markdown(f"**Precisão do Modelo:** R² = {r2:.3f}")
            
            # Interface de predição
            st.markdown("**Configure o perfil do jogador:**")
            pred_xg = st.slider("🎯 Expected Goals (temporada)", 0.0, 25.0, 10.0)
            pred_xag = st.slider("🅰️ Expected Assists", 0.0, 15.0, 5.0)
            pred_age = st.slider("📅 Idade", 16.0, 40.0, 25.0)
            pred_min = st.slider("⏱️ Minutos por jogo", 0.0, 90.0, 70.0)
            
            if st.button("💰 Calcular Valor de Mercado", type="primary"):
                prediction = model.predict([[pred_xg, pred_xag, pred_age, pred_min]])[0]
                
                if prediction > 20000000:
                    categoria = "💎 Premium"
                    cor = "success"
                elif prediction > 10000000:
                    categoria = "🌟 Promissor"
                    cor = "info"
                else:
                    categoria = "📈 Desenvolvimento"
                    cor = "warning"
                
                st.success(f"""
                ### 💰 Valor Estimado: €{prediction/1000000:.1f} Milhões
                **Categoria:** {categoria}
                
                **Baseado em:**
                - 🎯 Expected Goals: {pred_xg}
                - 🅰️ Expected Assists: {pred_xag}  
                - 📅 Idade: {pred_age} anos
                - ⏱️ Min/jogo: {pred_min}
                """)
        
        with col2:
            # Visualização do modelo
            fig_model = go.Figure()
            fig_model.add_trace(go.Scatter(
                x=y_test, 
                y=y_pred,
                mode='markers',
                name='Predições',
                marker=dict(color='#37003c', size=8, opacity=0.7)
            ))
            
            fig_model.add_trace(go.Scatter(
                x=[y_test.min(), y_test.max()], 
                y=[y_test.min(), y_test.max()],
                mode='lines',
                name='Predição Perfeita',
                line=dict(dash='dash', color='#00ff85', width=3)
            ))
            
            fig_model.update_layout(
                title=f"🤖 Performance do Modelo (R² = {r2:.3f})",
                xaxis_title="Valor Real (€)",
                yaxis_title="Valor Predito (€)",
                height=400
            )
            
            st.plotly_chart(fig_model, use_container_width=True)
            
            # Top 5 oportunidades
            df_filtered['Valor_real_pred'] = model.predict(X)
            df_filtered['Oportunidade'] = df_filtered['Valor_real_pred'] - df_filtered['Valor_estimado']
            
            st.markdown("### 💎 Top Oportunidades")
            opportunities = df_filtered.nlargest(5, 'Oportunidade')[['Player', 'Squad', 'Pos', 'Oportunidade']]
            
            for _, opp in opportunities.iterrows():
                if opp['Oportunidade'] > 0:
                    st.markdown(f"**{opp['Player']}** ({opp['Squad']}) - {opp['Pos']}")
                    st.markdown(f"Diferencial: +€{opp['Oportunidade']/1000000:.1f}M")
    
    with tab4:
        st.markdown('<div class="section-title">📋 RELATÓRIO EXECUTIVO DE SCOUTING</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 INSIGHTS ESTRATÉGICOS")
            
            # Estatísticas automáticas
            elite_count = len(df_filtered[df_filtered['Participacao_gols'] > 0.4])
            young_talent_count = len(df_filtered[(df_filtered['Age'] <= 23) & (df_filtered['Participacao_gols'] > 0.15)])
            efficient_count = len(df_filtered[df_filtered['Eficiencia_xG'] > 2])
            
            insights = [
                f"🏆 **{elite_count}** jogadores de elite identificados (>0.4 participação/jogo)",
                f"⭐ **{young_talent_count}** jovens talentos promissores (≤23 anos)",
                f"📈 **{efficient_count}** jogadores superam expectativas significativamente",
                f"💰 Valor médio de mercado: **€{df_filtered['Valor_estimado'].mean()/1000000:.1f}M**",
                f"🎯 Correlação xG-Gols: **{df_filtered['xG'].corr(df_filtered['Gls']):.3f}**"
            ]
            
            for insight in insights:
                st.markdown(f"- {insight}")
            
            st.markdown("### ✅ RECOMENDAÇÕES")
            st.markdown("""
            <div class="kpi-card">
            <h4>🎯 ESTRATÉGIA DE CONTRATAÇÃO</h4>
            <ul>
            <li><strong>Foque em Expected Goals:</strong> Jogadores com xG alto mantêm performance</li>
            <li><strong>Jovens Promissores:</strong> Investir em sub-25 com boa participação</li>
            <li><strong>Eficiência:</strong> Priorizar quem supera xG consistentemente</li>
            <li><strong>Valor:</strong> Usar modelo AI para validar preços</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Distribuição por categoria de valor
            df_filtered['Categoria_Valor'] = pd.cut(
                df_filtered['Valor_estimado']/1000000, 
                bins=[0, 5, 15, 30, 100], 
                labels=['💰 Econômico', '💎 Médio', '🌟 Premium', '👑 Elite']
            )
            
            fig_pie = px.pie(
                df_filtered['Categoria_Valor'].value_counts().reset_index(),
                values='count',
                names='Categoria_Valor',
                title="💰 Distribuição por Categoria de Valor",
                color_discrete_sequence=['#00ff85', '#37003c', '#667eea', '#764ba2']
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Top teams representation
            st.markdown("### 🏆 Top 5 Clubes Representados")
            top_teams = df_filtered['Squad'].value_counts().head()
            for team, count in top_teams.items():
                percentage = (count / len(df_filtered)) * 100
                st.markdown(f"**{team}:** {count} jogadores ({percentage:.1f}%)")
        
        # Download do relatório
        st.markdown("---")
        if st.button("📥 Gerar Relatório Completo", type="primary"):
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="💾 Download Relatório CSV",
                data=csv,
                file_name=f"scout_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
            st.success("✅ Relatório gerado com sucesso!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>⚽ <strong>Premier League Scout Central</strong> - Transformando dados em decisões inteligentes</p>
        <p>Desenvolvido com 💜 para análise profissional de futebol</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
