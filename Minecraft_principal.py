import sys
import pygame
import json
from Player import player
from obj import Mouse_look, Particle, Block, Animal, Enemies
from camera import Camera
from hud import Hud
from text import Text

pygame.init() #inicializando a biblioteca pygame
pygame.mixer.init() #inicializando a ferramenta de aúdio da biblioteca pygame
pygame.font.init() #inicializando a ferramenta de texto da biblioteca pygame
pygame.display.set_caption("Minecraft 2D") #inicializando a ferramenta para adicionar título na aba do jogo

fps = pygame.time.Clock()
tela = pygame.display.set_mode((1280, 720))
# Objeto tela - Dentro da pasta "pygame" tem um arquivo chamado "display", nesse arquivo possuí uma função chamada "set_mode" que precisa de altura e largura.
# Isto é para criar a janela que será criada o jogo.

# Grupo
all_sprites = Camera()
all_collision = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()

#background
bg_image = pygame.image.load("assets/bg.png").convert()

# Hud
hud = Hud()

# text
# text = Text([0, 0], all_sprites)

# blocos modelos
# list_blocks = ["grass", "rock", "sand", "water"]
# list_choose = 0

# player
Player = player("Assets/Player/idle0.png", [0, 0], all_collision, all_sprites)
creative_mode = True

# Animals
pig1 = Animal("Assets/pig/pig_",[200, 0], all_collision, all_sprites)
Cow1 = Animal("Assets/cow/cow_",[200, 0], all_collision, all_sprites)

# Enemies
zombie = Enemies(Player, "Assets/zombie/zombie_",[50, 0], all_collision, all_sprites, all_enemies)
Skull = Enemies(Player, "Assets/skull/skull_",[50, 0], all_collision, all_sprites, all_enemies)

# Blocks
# block_1 = Obj("assets/blocks/block_grass.png", [0, 650], all_sprites, all_collision)
# block_2 = Obj("assets/blocks/block_grass.png", [31, 650], all_sprites, all_collision)
# block_3 = Obj("assets/blocks/block_grass.png", [62, 650], all_sprites, all_collision)
# block_4 = Obj("assets/blocks/block_grass.png", [93, 619], all_sprites, all_collision)

mouse = Mouse_look(all_sprites)

def verify_y_pos_player():
    if Player.rect.y > 1280:
        Player.rect.y = 0
        Player.rect.x = 200
        hud.lost_life()

def damage_enemies():
    key = pygame.mouse.get_pressed()

    if key[2]:
        for sprite in all_enemies:
            if mouse.rect.colliderect(sprite.rect):
                if not sprite.damage:
                    sprite.damage = True
                    sprite.life -= 1

def damage():
    if not Player.damage:
        for sprite in all_enemies:
            if sprite.rect.colliderect(Player.rect):
                Player.damage = True
                hud.lost_life()
                Player.direction.y -= 5
#                Player.image.fill("red")

def save_blocks(file_name):
    blocks = [(b.rect.x, b.rect.y, b.style, b.rigid) for b in all_collision]
    with open(file_name, "w") as file:
        json.dump(blocks, file)
        print("Blocos Salvos!")

    save_player_data()


def save_player_data():
    bag = Player.bag
    bag[1]["pos_x"] = Player.rect.x
    bag[1]["pos_y"] = Player.rect.y
    with open("player_data.json", "w") as file:
        json.dump(bag, file)
        print("Dados salvos!")


def load_blocks(file_name):
    with open(file_name, "r") as file:
        block_data = json.load(file)
        for pos_x, pos_y, style, rigid in block_data:
            Block(rigid, style, [pos_x, pos_y], all_sprites, all_collision)
#            if style == "water":
#                load_block.rigid = False
#            else:
#                load_block.rigid = True
    load_player_data()


def load_player_data():
    with open("player_data.json", "r") as file:
        bag_data = json.load(file)
        Player.bag = bag_data
        print(Player.bag)

        Player.rect.center = (Player.bag[1]["pos_x"], Player.bag[1]["pos_y"])

        for text in hud.texts_group:
            for item in bag_data:
                if text.status in item:
                    hud.verify_text(text.status, str(item[text.status]))


def event_keys():
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_i:
            save_blocks("data.json")

#        if evento.key == pygame.K_1:
#            list_choose = 0
#        if evento.key == pygame.K_2:
#            list_choose = 1
#        if evento.key == pygame.K_3:
#            list_choose = 2
#        if evento.key == pygame.K_4:
#            list_choose = 3


def interact_blocks():

    key = pygame.mouse.get_pressed()

    if not creative_mode:
        if not hud.hud_area:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if not Player.rect.collidepoint(mouse.rect.x, mouse.rect.y):
                    add_blocks()
                    Remove_Block()
    else:
        if not hud.hud_area:
            if key[0]:

                x = (mouse.rect.x // 32) * 32
                y = (mouse.rect.y // 32) * 32
                for block in all_collision:
                    if block.rect.collidepoint(mouse.rect.x, mouse.rect.y):
                        break
                else:
                    if hud.block_select == "water" or hud.block_select == "leaf":
                        Block(False, hud.block_select, [x, y], all_sprites, all_collision)
                    else:
                        Block(True, hud.block_select, [x, y], all_sprites, all_collision)

            elif key[2]:
                for block in all_collision:
                    if block.rect.collidepoint(mouse.rect.x, mouse.rect.y):
                        block.resist -= 1
                        if block.resist <= 0:
                            hud.block_select = block.style
                            for _particles in range(10):
                                Particle([block.rect.x, block.rect.y], all_sprites)
                            block.kill()

def add_blocks():
    if evento.button == 1:
#       hud.lost_life()
        x = (mouse.rect.x // 32) * 32
        y = (mouse.rect.y // 32) * 32
        for block in all_collision:
            if block.rect.collidepoint(mouse.rect.x, mouse.rect.y):
                break
        else:
            if Player.bag[0][hud.block_select] > 0:
                Player.bag[0][hud.block_select] -= 1
                hud.verify_text(hud.block_select, str(Player.bag[0][hud.block_select]))
                if hud.block_select == "water":
                    Block(False, hud.block_select, [x, y], all_sprites, all_collision)
                else:
                    Block(True, hud.block_select, [x, y], all_sprites, all_collision)

def Remove_Block():
    for block in all_collision:
        if block.rect.collidepoint(mouse.rect.x, mouse.rect.y):
            if evento.button == 3:
#               hud.regen_life()
                block.resist -= 1
                if block.resist <= 0:
                    hud.block_select = block.style
                    Player.bag[0][block.style] += 1
                    hud.verify_text(hud.block_select, str(Player.bag[0][hud.block_select]))
                    for _particles in range(10):
                        Particle([block.rect.x, block.rect.y], all_sprites)
                    block.kill()

load_blocks("data.json")

while True:
    # para cada item que eu tenho dentro de uma lista eu faço algo
    for evento in pygame.event.get(): # para cada evento ele entra na biblioteca "pygame" no arquivo "event" e encontra o evento "get"
        # cada vez que uma tecla é pressionada um evento é acionado
        if evento.type == pygame.QUIT: # Se o evento que eu tenho é do tipo "quit" ele fecha a janela
            pygame.quit() # acessa a biblioteca "pygame" e importa a função "quit"
            sys.exit() # Acessa a biblioteca "sys" e importa a função "exit" para fechar o terminal python

        event_keys()

        interact_blocks()


# Jeito errado de verificar colisão:
#
#    for item in all_collision:
#        if Player.rect.colliderect(item):
#            Player.rect.bottom = item.rect.top

    fps.tick(60)
    tela.fill("black") #Preenchendo a variável tela com a cor preta
    tela.blit(bg_image, (0, 0))
    all_sprites.costume_draw(Player)
    all_sprites.update()
    hud.draw()
    hud.update()
    damage()
    damage_enemies()
    verify_y_pos_player()
    mouse.mouse_look_update(all_sprites)
    pygame.display.flip()
    # Este comando serve para manter a janela constantemente aberta.
    # mas não é possível interagir com ela, pois ainda não foi configurado.

