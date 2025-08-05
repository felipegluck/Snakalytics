import json
import random

def gerar_dados_falsos(nome_arquivo, num_partidas=1000, perfil="balanceado"):
    """
    Gera um arquivo JSON com dados falsos, simulando diferentes perfis de IA.
    Perfis: 'cauteloso', 'balanceado', 'agressivo'
    """
    print(f"Gerando {num_partidas} partidas para o agente '{nome_arquivo}' com perfil '{perfil}'...")
    
    lista_de_partidas = []

    for i in range(num_partidas):
        partida_id = i + 1
        
        # --- Lógica de perfil ---
        if perfil == "cauteloso":
            # Aprende devagar, mas é consistente (pouca variação)
            pontuacao_maxima_possivel = 3 + (i // 100)
            score = random.randint(0, pontuacao_maxima_possivel)
            moves = score * random.randint(15, 25) + random.randint(20, 40) # Mais movimentos por ponto
        elif perfil == "agressivo":
            # Tenta scores altos, mas falha mais (muita variação)
            pontuacao_maxima_possivel = 8 + (i // 30)
            # Chance maior de ter score baixo (morreu arriscando) ou alto
            score = int(random.triangular(0, pontuacao_maxima_possivel, 2))
            moves = score * random.randint(5, 15) + random.randint(10, 30) # Menos movimentos por ponto
        else: # Balanceado (lógica original)
            pontuacao_maxima_possivel = 5 + (i // 50) 
            score = random.randint(0, pontuacao_maxima_possivel)
            moves = score * random.randint(8, 20) + random.randint(10, 50)

        time_seconds = int(moves * random.uniform(0.3, 0.8))
                
        nova_partida = {"id": partida_id, "score": score, "moves": moves, "time_seconds": time_seconds}
        lista_de_partidas.append(nova_partida)

    try:
        with open(nome_arquivo, 'w') as f:
            json.dump(lista_de_partidas, f, indent=4)
        print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo: {e}")

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    # Aqui você pode gerar dados para múltiplos agentes com uma única execução
    gerar_dados_falsos("stats_agente_cauteloso.json", num_partidas=500, perfil="cauteloso")
    gerar_dados_falsos("stats_agente_balanceado.json", num_partidas=500, perfil="balanceado")
    gerar_dados_falsos("stats_agente_agressivo.json", num_partidas=500, perfil="agressivo")
    print("\nTodos os arquivos de dados foram gerados.")