import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from sklearn.linear_model import LinearRegression
import numpy as np

# Função de normalização segura para evitar divisão por zero.
def safe_normalize(series):
    """Normalizes a pandas Series, handling the case where max equals min."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        # Se todos os valores são iguais, retorna 0.5 (neutro) para todos.
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - min_val) / (max_val - min_val)


def calcular_slope(series):
    """Calcula o coeficiente angular (slope) de uma série de dados usando regressão linear."""
    y = series.dropna().values.reshape(-1, 1)
    if len(y) < 2:
        return 0
    x = np.array(series.dropna().index).reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(x, y)
    return model.coef_[0][0]

st.set_page_config(
    page_title="Dashboard de Análise Comparativa - IA Snake",
    layout="wide"
)

@st.cache_data
def load_all_data(padrao_arquivo="stats_*.json"):
    """
    Encontra todos os arquivos JSON que correspondem ao padrão, os carrega
    e os combina em um único DataFrame com uma coluna 'agent'.
    """
    lista_arquivos = glob.glob(padrao_arquivo)
    if not lista_arquivos:
        return None
    
    lista_dfs = []
    for arquivo in lista_arquivos:
        try:
            df_temp = pd.read_json(arquivo)
            if not df_temp.empty:
                nome_agente = arquivo.replace("stats_", "").replace(".json", "").replace("\\", "/").split("/")[-1]
                df_temp['agent'] = nome_agente
                lista_dfs.append(df_temp)
        except (ValueError, FileNotFoundError):
            # Ignora arquivos JSON corrompidos ou vazios
            st.warning(f"Não foi possível carregar o arquivo: {arquivo}. Ele pode estar vazio ou mal formatado.")
            continue
            
    if not lista_dfs:
        return None
        
    df_completo = pd.concat(lista_dfs, ignore_index=True)
    return df_completo

st.title("🐍 Dashboard de Análise Comparativa de Agentes - Snake")

df_total = load_all_data()

if df_total is None:
    st.error("Nenhum arquivo de estatísticas ('stats_*.json') foi encontrado. Por favor, gere os dados primeiro.")
else:
    st.sidebar.header("Filtros e Controles")
    
    lista_agentes = df_total['agent'].unique()
    agentes_selecionados = st.sidebar.multiselect(
        "Selecione os agentes para comparar:",
        options=lista_agentes,
        default=list(lista_agentes)
    )
    
    if agentes_selecionados:
        df_filtrado = df_total[df_total['agent'].isin(agentes_selecionados)]
        # Criar uma cópia explícita para evitar o SettingWithCopyWarning.
        df_filtrado = df_filtrado.copy()
    else:
        df_filtrado = df_total.iloc[0:0]

    janela_media_movel = st.sidebar.number_input(
        "Janela da Média Móvel (partidas):",
        min_value=1, max_value=1000, value=100
    )

    max_score_geral = int(df_filtrado['score'].max()) if not df_filtrado.empty else 20
    # Garante que o valor padrão do slider esteja sempre dentro do intervalo [min_value, max_value].
    default_slider_value = max(1, min(10, max_score_geral))
    score_threshold = st.sidebar.slider(
        "Limiar de Proficiência (Pontos):",
        min_value=1,
        max_value=max_score_geral,
        value=default_slider_value
    )

    st.header("Análise Comparativa de Desempenho")

    if not df_filtrado.empty and agentes_selecionados:
        cols = st.columns(len(agentes_selecionados))
        for i, agente in enumerate(agentes_selecionados):
            df_agente = df_filtrado[df_filtrado['agent'] == agente]
            pontuacao_media = df_agente['score'].mean()
            with cols[i]:
                st.metric(label=f"Pontuação Média ({agente})", value=f"{pontuacao_media:.2f}")

    tab1, tab2, tab3 = st.tabs(["📈 Curva de Aprendizado", "📊 Distribuição de Pontuações", "🏆 Leaderboard de Desempenho"])

    with tab1:
        st.subheader("Evolução da Pontuação Média ao Longo do Tempo")
        if not df_filtrado.empty:
            fig1, ax1 = plt.subplots(figsize=(12, 6))
            
            df_filtrado['media_movel_score'] = df_filtrado.groupby('agent')['score'].rolling(window=janela_media_movel, min_periods=1).mean().reset_index(level=0, drop=True)

            sns.lineplot(data=df_filtrado, x=df_filtrado.index, y='media_movel_score', hue='agent', ax=ax1)
            ax1.set_title(f'Comparativo de Curvas de Aprendizado (Média Móvel de {janela_media_movel} Partidas)')
            ax1.set_xlabel('Número da Partida (Índice Global)')
            ax1.set_ylabel('Pontuação Média Móvel')
            st.pyplot(fig1)
        else:
            st.warning("Selecione pelo menos um agente para visualizar a curva de aprendizado.")

    with tab2:
        st.subheader("Comparativo da Distribuição das Pontuações Finais")
        if not df_filtrado.empty:
            fig2, (ax_box, ax_hist) = plt.subplots(1, 2, figsize=(16, 6))
            sns.boxplot(data=df_filtrado, x='agent', y='score', ax=ax_box)
            ax_box.set_title('Resumo Estatístico (Box Plot)')
            ax_box.set_xlabel('Agente')
            ax_box.set_ylabel('Pontuação Final')
            sns.histplot(data=df_filtrado, x='score', hue='agent', kde=True, element="step", ax=ax_hist)
            ax_hist.set_title('Frequência das Pontuações (Histograma)')
            ax_hist.set_xlabel('Pontuação Final')
            ax_hist.set_ylabel('Frequência')
            plt.tight_layout()
            st.pyplot(fig2)
            st.markdown("""
            **Como ler estes gráficos:**
            - O **Box Plot** resume a distribuição: a linha no meio da caixa é a **mediana**, a caixa representa 50% das partidas, e os pontos fora das "antenas" são partidas excepcionais (*outliers*).
            - O **Histograma** mostra quais pontuações são mais comuns para cada agente. Picos mais à direita indicam um melhor desempenho geral. A sobreposição permite comparar diretamente a consistência dos agentes.
            """)
        else:
            st.warning("Selecione pelo menos um agente para visualizar as distribuições.")

    with tab3:
        if not df_filtrado.empty and 'agent' in df_filtrado.columns and len(agentes_selecionados) > 1:
            leaderboard_data = []
            
            for agente in agentes_selecionados:
                df_agente = df_filtrado[df_filtrado['agent'] == agente].copy().reset_index(drop=True)
                if not df_agente.empty:
                    metricas_agente = {"Agente": agente}
                    pontuacao_media = df_agente['score'].mean()
                    metricas_agente["Pontuação Média"] = pontuacao_media
                    metricas_agente["Consistência (Desvio Padrão)"] = df_agente['score'].std()
                    media_movel_series = df_agente['score'].rolling(window=janela_media_movel, min_periods=1).mean()
                    metricas_agente["Taxa de Aprendizado (Slope)"] = calcular_slope(media_movel_series)
                    
                    indices_acima = media_movel_series.index[media_movel_series >= score_threshold]
                    atingiu_limiar = len(indices_acima) > 0
                    metricas_agente[f"Atingiu Limiar de {score_threshold} Pontos?"] = "✅ Sim" if atingiu_limiar else "❌ Não"
                    
                    if atingiu_limiar:
                        partidas_para_atingir = indices_acima[0]
                        metricas_agente["Custo por Ponto (Partidas/Score)"] = partidas_para_atingir / pontuacao_media if pontuacao_media > 0 else float('inf')
                    else:
                        metricas_agente["Custo por Ponto (Partidas/Score)"] = float('inf')
                    
                    leaderboard_data.append(metricas_agente)
            
            if leaderboard_data:
                st.subheader("Tabela de Métricas Detalhadas")
                df_leaderboard = pd.DataFrame(leaderboard_data).set_index("Agente")
                
                formatters = { "Pontuação Média": "{:.2f}", "Consistência (Desvio Padrão)": "{:.2f}", "Taxa de Aprendizado (Slope)": "{:.4f}", "Custo por Ponto (Partidas/Score)": "{:.2f}" }
                st.dataframe(df_leaderboard.style.format(formatters, na_rep="N/A"))
                
                # Dicionário com as descrições dos presets
                preset_descriptions = {
                    "Balanceado": "Todos os fatores têm o mesmo peso. Ideal para uma visão geral e equilibrada do desempenho.",
                    "Performance Máxima": "Prioriza agentes que atingem pontuações altas e são consistentes, mesmo que demorem mais para aprender.",
                    "Aprendiz Rápido": "Prioriza agentes que aprendem rápido (slope alto) e atingem os limiares de proficiência com poucas partidas."
                }
                
                presets = {
                    "Balanceado": {m: 1.0 for m in df_leaderboard.columns if isinstance(df_leaderboard[m].iloc[0], (int, float))},
                    "Performance Máxima": {"Pontuação Média": 3.0, "Consistência (Desvio Padrão)": 1.5, "Taxa de Aprendizado (Slope)": 0.5},
                    "Aprendiz Rápido": {"Taxa de Aprendizado (Slope)": 3.0, "Custo por Ponto (Partidas/Score)": 2.0}
                }
                preset_selecionado = st.selectbox("Selecione uma Estratégia de Ranking (Preset):", options=list(presets.keys()))
                st.info(f"**Estratégia '{preset_selecionado}':** {preset_descriptions[preset_selecionado]}")

                df_rank = df_leaderboard.copy()
                for col in df_rank.columns: 
                    if df_rank[col].dtype == 'object':
                        df_rank[col] = pd.to_numeric(df_rank[col], errors='coerce')

                df_normalized = df_rank.apply(safe_normalize, axis=0)

                metricas_menor_melhor = ["Consistência (Desvio Padrão)", "Custo por Ponto (Partidas/Score)"]
                for col in metricas_menor_melhor:
                    if col in df_normalized.columns:
                        df_normalized[col] = 1.0 - df_normalized[col]
                
                df_normalized = df_normalized.fillna(0)
                
                pesos = presets[preset_selecionado]
                df_normalized['SCORE_FINAL'] = sum(df_normalized[metrica] * pesos.get(metrica, 0) for metrica in df_normalized.columns if metrica != 'SCORE_FINAL')
                
                score_min, score_max = df_normalized['SCORE_FINAL'].min(), df_normalized['SCORE_FINAL'].max()
                if score_max - score_min > 0:
                    df_normalized['SCORE_FINAL'] = 100 * (df_normalized['SCORE_FINAL'] - score_min) / (score_max - score_min)
                else:
                    df_normalized['SCORE_FINAL'] = 100.0
                df_ranked_final = df_normalized.sort_values(by="SCORE_FINAL", ascending=False)
                
                st.markdown("---")
                st.subheader(f"Classificação Final:")
                
                medals = ["🥇", "🥈", "🥉"]
                for i, (agente, row) in enumerate(df_ranked_final.iterrows()):
                    medal = medals[i] if i < len(medals) else f"**{i+1}º**"
                    st.markdown(f"### {medal} {agente}")
                    col1, col2, col3 = st.columns(3)
                    #  Parâmetro 'help' a cada st.metric
                    col1.metric(
                        label="Score Final Ponderado", 
                        value=f"{row['SCORE_FINAL']:.2f}",
                        help="Pontuação final calculada com base na estratégia de ranking selecionada. Varia de 0 a 100."
                    )
                    col2.metric(
                        label=f"Atingiu Limiar de {score_threshold} Pontos?", 
                        value=df_leaderboard.loc[agente, f"Atingiu Limiar de {score_threshold} Pontos?"],
                        help="Indica se o agente conseguiu atingir o limiar de performance definido no slider."
                    )
                    
                    # Verifica se o custo é infinito antes de formatar.
                    custo_valor = df_leaderboard.loc[agente, 'Custo por Ponto (Partidas/Score)']
                    custo_display = "∞" if np.isinf(custo_valor) else f"{custo_valor:.2f}"
                    col3.metric(
                        label="Custo por Ponto",
                        value = custo_display,
                        help="Mede a eficiência do agente (Partidas até o limiar / Pontuação Média). Um custo menor indica que o agente é mais eficiente para atingir sua performance."
                    )
        else:
            st.info("Selecione pelo menos dois agentes para gerar o ranking final.")
            
    if st.checkbox("Mostrar dados brutos"):
        st.dataframe(df_filtrado)