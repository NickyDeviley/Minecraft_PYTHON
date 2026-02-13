
# Objeto player:
posicao_x = 0 # posição inicial do jogador
posicao_y = 0 # posição inicial do jogador
width = 50 # tamanho do jogador (Largura)
height = 50 # tamanho do jogador (altura)
rect = pygame.Rect([posicao_x, posicao_y, width, height]) # Objeto que armazena os dados do jogador (tamanho e posição)
direction = pygame.math.Vector2()


if evento.type == pygame.KEYDOWN:
    if evento.key == pygame.K_d:
        direction.x = 1
    elif evento.key == pygame.K_a:
        direction.x = -1
    else:
        direction.x = 0

    if evento.key == pygame.K_w:
        direction.y = -1
    elif evento.key == pygame.K_s:
        direction.y = 1
    else:
        direction.y = 0
if evento.type == pygame.KEYUP:
    if evento.key == pygame.K_d:
        direction.x = 0
    elif evento.key == pygame.K_a:
        direction.x = 0

    if evento.key == pygame.K_w:
        direction.y = 0
    elif evento.key == pygame.K_s:
        direction.y = 0


rect.center += direction
    pygame.draw.rect(surface=tela, color="red", rect=rect)
    # pygame.draw.rect(surface=tela, color="red", rect=[posicao_x, posicao_y, width, height])
    #criando uma superfície na variáel tela, adicionando a cor vermelha e a posição 100, posição 50, com 50 de largura e 50 de altura.