import pygame
from obj import Obj
from text import Text

class Hud:

    def __init__(self):

        self.display = pygame.display.get_surface()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.blocks_groups = pygame.sprite.Group()
        self.hearths_groups = pygame.sprite.Group()
        self.texts_group = pygame.sprite.Group()

        # Hud Image
        self.hud_bar = pygame.image.load("assets/hud/hud.png") # ItemHud("grass", "assets/hud/hud.png", [440, 650], self.all_sprites )
        self.rect = self.hud_bar.get_rect(topleft = (440,650))

        # Blocks
        self.block_grass = ItemHud("grass", "assets/hud/block_grass.png", [460, 670], self.all_sprites, self.blocks_groups)
        self.block_sand = ItemHud("sand", "assets/hud/block_sand.png", [512, 670], self.all_sprites, self.blocks_groups)
        self.block_water = ItemHud("water", "assets/hud/block_water.png", [563, 670], self.all_sprites, self.blocks_groups)
        self.block_wood = ItemHud("wood", "assets/hud/block_wood.png", [615, 670], self.all_sprites, self.blocks_groups)
        self.block_rock = ItemHud("rock", "assets/hud/block_rock.png", [667, 670], self.all_sprites, self.blocks_groups)
        self.block_leaf = ItemHud("leaf", "assets/hud/block_leaf.png", [720, 670], self.all_sprites, self.blocks_groups)
        self.block_metal = ItemHud("metal", "assets/hud/block_metal.png", [770, 670], self.all_sprites, self.blocks_groups)
        self.block_coal = ItemHud("coal", "assets/hud/block_coal.png", [822, 670], self.all_sprites, self.blocks_groups)


        # Properties
        self.block_over = pygame.image.load("assets/hud/block_select.png")
        self.block_select = "grass"
        self.hud_area = False

        # Player Properties
        self.life = 9

        # Hearths Properties
        self.hearth_pos_x = 445
        self.hearth_pos_y = 630
        self.distance_hearth = 30

        self.generator_hearths()
        self.generator_texts()

    def verify_text(self, block_status, new_text):
        for text in self.texts_group:
            if text.status == block_status:
                text.update_text(new_text)

    def generator_texts(self):
        for block in self.blocks_groups:
            Text( block.status, [block.rect.x + 20, block.rect.y + 20], self.all_sprites, self.texts_group)

    def generator_hearths(self):
        for sprite in range(self.life):
            Obj("Assets/hud/empty_hearth.png", [self.hearth_pos_x, self.hearth_pos_y], self.all_sprites)
            Obj("Assets/hud/hearth.png", [self.hearth_pos_x, self.hearth_pos_y], self.all_sprites, self.hearths_groups)
            self.hearth_pos_x += self.distance_hearth

    def lost_life(self):
        if len(self.hearths_groups) > 0:
            last_hearth = self.hearths_groups.sprites()[-1]
            last_hearth.kill()
            self.life -= 1

    def regen_life(self):
        if len(self.hearths_groups) < 9:
            last_hearth = self.hearths_groups.sprites()[-1]
            Obj("Assets/hud/hearth.png", [last_hearth.rect.x + self.distance_hearth, self.hearth_pos_y], self.all_sprites, self.hearths_groups)
            self.life += 1

    def mouse_over(self):

        mouse_pos = pygame.mouse.get_pos()
        mouse_key = pygame.mouse.get_pressed()

        # Hud area
        if self.rect.collidepoint(mouse_pos):
            self.hud_area = True
        else:
            self.hud_area = False

        # Blocks Area
        for sprite in self.blocks_groups:
            if sprite.rect.collidepoint(mouse_pos):
                sprite.image.blit(self.block_over, (0, 0))
                if mouse_key[0]:
                    self.block_select = sprite.status
            else:
                sprite.image = pygame.image.load("assets/hud/block_" + sprite.status + ".png")


    def draw(self):
        self.display.blit(self.hud_bar, (440,650))
        self.all_sprites.draw(self.display)

    def update(self):
        self.all_sprites.update()
        self.mouse_over()

class ItemHud(pygame.sprite.Sprite):

    def __init__(self, status, img, pos, *groups):
        super().__init__(*groups)

        # Status
        self.status = status


        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(topleft = pos)
