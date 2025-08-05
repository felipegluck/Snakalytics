import pygame
import sys
import random
import json
from datetime import datetime

# --- 1. FUNÇÕES AUXILIARES ---

def save_stats_to_json(score, moves, time_seconds):
    """
    Lê um arquivo JSON de estatísticas, adiciona os novos dados da partida com um ID sequencial
    e salva o arquivo novamente.
    """
    filename = "game_stats.json"
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
        
    # Get the ID of the last entry, or 0 if the list is empty.
    last_id = data[-1]['id'] if data else 0
    
    # The new ID is the last ID plus one.
    new_id = last_id + 1

    # Cria o dicionário com os dados da partida atual, incluindo o novo ID
    new_entry = {
        "id": new_id, 
        "score": score,
        "moves": moves,
        "time_seconds": time_seconds
    }
    
    data.append(new_entry)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Estatísticas da Partida #{new_id} salvas em '{filename}'")


# --- 2. FUNÇÃO PRINCIPAL QUE CONTROLA O JOGO ---
def run_game():
    # --- Inicialização e Configurações ---
    pygame.init()
    
    BLOCK_SIZE = 20
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo da Cobrinha")
    
    # Cores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 155, 0)
    GRAY = (40, 40, 40)
    BUTTON_COLOR = (0, 100, 200)

    fps_controller = pygame.time.Clock()

    # --- Função para resetar o estado do jogo ---
    def reset_game_state():
        return {
            "snake_pos": [WIDTH / 2, HEIGHT / 2],
            "snake_body": [[WIDTH / 2, HEIGHT / 2], [WIDTH / 2 - BLOCK_SIZE, HEIGHT / 2], [WIDTH / 2 - (2 * BLOCK_SIZE), HEIGHT / 2]],
            "direction": 'RIGHT',
            "food_pos": [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE],
            "score": 0,
            "moves": 0,
            "start_time": pygame.time.get_ticks(),
            "total_paused_time": 0,
            "time_at_pause": 0,
            "game_over": False,
            "paused": False
        }

    # --- Tela de Fim de Jogo ---
    def game_over_screen(final_score, final_moves, final_time_seconds):
        replay_button_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_button_rect.collidepoint(event.pos):
                        return # Reinicia o jogo

            # Desenho da tela de game over
            screen.fill(BLACK)
            font_large = pygame.font.SysFont('arial', 50)
            font_small = pygame.font.SysFont('arial', 30)
            title_surface = font_large.render('FIM DE JOGO', True, WHITE)
            screen.blit(title_surface, title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 4)))
            minutes, seconds = divmod(final_time_seconds, 60)
            stats_text = f'Pontos: {final_score} | Movimentos: {final_moves} | Tempo: {minutes:02d}:{seconds:02d}'
            stats_surface = font_small.render(stats_text, True, WHITE)
            screen.blit(stats_surface, stats_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 20)))
            pygame.draw.rect(screen, BUTTON_COLOR, replay_button_rect)
            replay_text_surface = font_small.render('Jogar Novamente', True, WHITE)
            screen.blit(replay_text_surface, replay_text_surface.get_rect(center=replay_button_rect.center))
            pygame.display.update()
            fps_controller.tick(15)

    # --- Inicialização do Primeiro Jogo ---
    game_state = reset_game_state()
    change_to = game_state["direction"]
    
    # --- Loop Principal (Gerenciador de Estados) ---
    while True:
        # --- Processamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    game_state["paused"] = not game_state["paused"]
                    if game_state["paused"]:
                        # Guarda o momento em que o jogo foi pausado
                        game_state["time_at_pause"] = pygame.time.get_ticks()
                    else:
                        # Ao despausar, calcula quanto tempo ficou parado e acumula
                        game_state["total_paused_time"] += pygame.time.get_ticks() - game_state["time_at_pause"]
                
                if not game_state["paused"]:
                    # Lógica de controle de direção
                    if event.key == pygame.K_UP and game_state["direction"] != 'DOWN': change_to = 'UP'; game_state["moves"] += 1
                    if event.key == pygame.K_DOWN and game_state["direction"] != 'UP': change_to = 'DOWN'; game_state["moves"] += 1
                    if event.key == pygame.K_LEFT and game_state["direction"] != 'RIGHT': change_to = 'LEFT'; game_state["moves"] += 1
                    if event.key == pygame.K_RIGHT and game_state["direction"] != 'LEFT': change_to = 'RIGHT'; game_state["moves"] += 1
        
        # --- Lógica do Jogo ---
        if not game_state["paused"] and not game_state["game_over"]:
            game_state["direction"] = change_to
            if game_state["direction"] == 'UP': game_state["snake_pos"][1] -= BLOCK_SIZE
            if game_state["direction"] == 'DOWN': game_state["snake_pos"][1] += BLOCK_SIZE
            if game_state["direction"] == 'LEFT': game_state["snake_pos"][0] -= BLOCK_SIZE
            if game_state["direction"] == 'RIGHT': game_state["snake_pos"][0] += BLOCK_SIZE
            game_state["snake_body"].insert(0, list(game_state["snake_pos"]))
            if game_state["snake_body"][0] == game_state["food_pos"]:
                game_state["score"] += 1
                game_state["food_pos"] = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
            else:
                game_state["snake_body"].pop()
            if (game_state["snake_pos"][0] < 0 or game_state["snake_pos"][0] >= WIDTH or game_state["snake_pos"][1] < 0 or game_state["snake_pos"][1] >= HEIGHT or game_state["snake_body"][0] in game_state["snake_body"][1:]):
                game_state["game_over"] = True

        # --- Renderização ---
        screen.fill(BLACK)
        
        if game_state["game_over"]:
            # Calcula o tempo final ANTES de entrar na tela de game over
            final_time = (pygame.time.get_ticks() - game_state["start_time"] - game_state["total_paused_time"]) // 1000
            # Salva as estatísticas no arquivo JSON
            save_stats_to_json(game_state["score"], game_state["moves"], final_time)
            # Mostra a tela de fim de jogo
            game_over_screen(game_state["score"], game_state["moves"], final_time)
            # Se a função retornar, reinicia o jogo
            game_state = reset_game_state()
            change_to = game_state["direction"]
        else:
            # Desenha os elementos do jogo
            for x in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE): pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
            for pos in game_state["snake_body"]: pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, DARK_GREEN, pygame.Rect(game_state["snake_body"][0][0], game_state["snake_body"][0][1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, RED, pygame.Rect(game_state["food_pos"][0], game_state["food_pos"][1], BLOCK_SIZE, BLOCK_SIZE))
            
            # --- LÓGICA DO TIMER ---
            # O tempo decorrido é calculado aqui para ser exibido no cabeçalho
            if game_state["paused"]:
                # Se pausado, o tempo "congela" no momento da pausa
                current_ticks = game_state["time_at_pause"]
            else:
                # Se rodando, o tempo continua a contar
                current_ticks = pygame.time.get_ticks()
            
            elapsed_time = (current_ticks - game_state["start_time"] - game_state["total_paused_time"]) // 1000
            minutes, seconds = divmod(elapsed_time, 60)
            
            # Desenha o cabeçalho
            font = pygame.font.SysFont('arial', 24)
            score_surface = font.render(f'Pontos: {game_state["score"]}', True, WHITE)
            screen.blit(score_surface, score_surface.get_rect(topleft=(10, 10)))
            moves_surface = font.render(f'Movimentos: {game_state["moves"]}', True, WHITE)
            screen.blit(moves_surface, moves_surface.get_rect(topright=(WIDTH - 10, 10)))
            timer_surface = font.render(f'Tempo: {minutes:02d}:{seconds:02d}', True, WHITE)
            screen.blit(timer_surface, timer_surface.get_rect(midtop=(WIDTH / 2, 10)))

            if game_state["paused"]:
                pause_surface = pygame.font.SysFont('arial', 50).render('PAUSADO', True, WHITE)
                screen.blit(pause_surface, pause_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

        pygame.display.update()
        fps_controller.tick(15)

# Executa o jogo
run_game()
