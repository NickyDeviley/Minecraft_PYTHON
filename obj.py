import pygame
import random

class Obj(pygame.sprite.Sprite):

    def __init__(self, img, pos, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)


class Block(pygame.sprite.Sprite):

    def __init__(self, rigid, style, pos, *groups):
        super().__init__(*groups)

        #status
        self.resist = 3
        self.style = style
        self.rigid = rigid

        #image
        self.cracks = pygame.image.load("assets/cracks/crack.png")
        self.image = pygame.image.load("assets/blocks/block_" + self.style + ".png")
        self.rect = self.image.get_rect(topleft = pos)

        # Mask
#        self.mask = pygame.mask.from_surface(self.image)

        # Time
        self.ticks = 0

    def update(self):

        if self.resist < 3:
            self.ticks += 1
            self.image.blit(self.cracks, (0, 0))
            if self.ticks >= 120:
                self.ticks = 0
                self.resist = 3
                self.image = pygame.image.load("assets/blocks/block_" + self.style + ".png")

class Mouse_look(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((10, 10))
        self.image.fill("green")
        self.rect = self.image.get_rect()

    def mouse_look_update(self, camera):
        mouse_pos = pygame.mouse.get_pos()
        pos_x = mouse_pos[0]
        pos_y = mouse_pos[1]
        x = pos_x + camera.offset.x
        y = pos_y + camera.offset.y

        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2




class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)

        self.colors = ("green", "brown")
        self.choose_color = random.randint(0, 1)

        self.image = pygame.Surface((5, 5))
        self.image.fill(self.colors[self.choose_color])
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.direction.x = random.randint(-10, 10)
        self.direction.y = random.randint(-10, 10)

        self.ticks = 0

    def update(self, *args, **kwargs):

        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        self.ticks += 1
        if self.ticks >= 60:
            self.kill()


class Enemies(pygame.sprite.Sprite):

    def __init__(self, player, path, pos, collision, *groups):
        super().__init__(*groups)

        self.path = path
        self.player = player
        self.life = 3

        self.image = pygame.image.load(self.path + "stay0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

        # Collision groups
        self.all_collision = collision

        # Direction Walk
        self.speed = 5
        self.direction = pygame.math.Vector2()

        # Animation
        self.flip = False
        self.ticks = 0
        self.frame = 0
        self.status = "idle"

        # gravity
        self.force = 1
        self.on_ground = False

        # walk_time
        self.walk_time = 0

        # Distance
        self.distance = 0
        self.limit_distance = 200

        # Damage Time
        self.damage_time = 0
        self.damage = False

    def death(self):
        if self.life <= 0:
            self.kill()

    def verify_damage(self):
        if self.damage:
            self.damage_time += 1
            self.image.fill("red", special_flags=pygame.BLEND_RGB_MULT)
            if self.damage_time >= 20:
                self.damage_time = 0
                self.damage = False

    def near_player(self):
        distance = ((self.player.rect.x - self.rect.x) ** 2 + (self.player.rect.y - self.rect.y) ** 2) ** 0.5
        self.distance = distance
        if distance <= self.limit_distance:
            if self.rect.x < self.player.rect.x:
                self.direction.x = 1
                self.status = "walk"
                self.flip = True
            else:
                self.direction.x = -1
                self.status = "walk"
                self.flip = False

    def x_collision(self):
        for block in self.all_collision:
            if self.rect.colliderect(block.rect) and block.rigid:
#            if pygame.sprite.collide_mask(self, block) and block.rigid:
                if self.direction.x > 0:
                    self.rect.right = block.rect.left
                elif self.direction.x < 0:
                    self.rect.left = block.rect.right

    def y_collision(self):
        for block in self.all_collision:
            if self.rect.colliderect(block.rect) and block.rigid:
#            if self.rect.colliderect(block) and block.rigid:
                if self.direction.y > 0:
                    self.rect.bottom = block.rect.top
                    self.on_ground = True
                    self.direction.y = 0
                elif self.direction.y < 0:
                    self.rect.top = block.rect.bottom
                    self.direction.y = 0

    def animation(self, speed, limit):
        self.ticks += 1
        if self.ticks >= speed:
            self.ticks = 0
            self.frame += 1

        if self.frame >= limit:
            self.frame = 0

        self.image = pygame.image.load(self.path + self.status + str(self.frame) + ".png")
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def movement(self):

        if self.distance > self.limit_distance:
            self.walk_time += 1
            if self.walk_time >= random.randint(60, 180):
                self.walk_time = 0
                self.direction.x = random.randint(-1, 1)

        self.rect.x += self.direction.x

    def animation_status(self):
        if self.status == "stay":
            self.animation(16, 3)
        elif self.status == "walk":
            self.animation(12, 3)

        if self.direction.x == 0:
            self.status = "stay"
        elif self.direction.x == 1:
            self.status = "walk"
            self.flip = True
        elif self.direction.x == -1:
            self.status = "walk"
            self.flip = False

    def gravity(self):
        self.direction.y += self.force
        self.rect.y += self.direction.y

    def update(self):
        self.movement()
        self.x_collision()
        self.animation_status()
        self.gravity()
        self.y_collision()
        self.near_player()
        self.verify_damage()
        self.death()

class Animal(pygame.sprite.Sprite):

    def __init__(self, path, pos, collision, *groups):
        super().__init__(*groups)

        self.path = path

        self.image = pygame.image.load(self.path + "stay0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

        # Collision groups
        self.all_collision = collision

        # Direction Walk
        self.speed = 5
        self.direction = pygame.math.Vector2()

        # Animation
        self.flip = False
        self.ticks = 0
        self.frame = 0
        self.status = "idle"

        # gravity
        self.force = 1
        self.on_ground = False

        # walk_time
        self.walk_time = 0

    def x_collision(self):
        for block in self.all_collision:
            if self.rect.colliderect(block.rect) and block.rigid:
#            if pygame.sprite.collide_mask(self, block) and block.rigid:
                if self.direction.x > 0:
                    self.rect.right = block.rect.left
                elif self.direction.x < 0:
                    self.rect.left = block.rect.right

    def y_collision(self):
        for block in self.all_collision:
            if self.rect.colliderect(block.rect) and block.rigid:
#            if self.rect.colliderect(block) and block.rigid:
                if self.direction.y > 0:
                    self.rect.bottom = block.rect.top
                    self.on_ground = True
                    self.direction.y = 0
                elif self.direction.y < 0:
                    self.rect.top = block.rect.bottom
                    self.direction.y = 0

    def animation(self, speed, limit):
        self.ticks += 1
        if self.ticks >= speed:
            self.ticks = 0
            self.frame += 1

        if self.frame >= limit:
            self.frame = 0

        self.image = pygame.image.load(self.path + self.status + str(self.frame) + ".png")
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def movement(self):

        self.walk_time += 1
        if self.walk_time >= random.randint(60, 180):
            self.walk_time = 0
            self.direction.x = random.randint(-1, 1)

        self.rect.x += self.direction.x

    def animation_status(self):
        if self.status == "stay":
            self.animation(16, 3)
        elif self.status == "walk":
            self.animation(12, 3)

        if self.direction.x == 0:
            self.status = "stay"
        elif self.direction.x == 1:
            self.status = "walk"
            self.flip = True
        elif self.direction.x == -1:
            self.status = "walk"
            self.flip = False

    def gravity(self):
        self.direction.y += self.force
        self.rect.y += self.direction.y

    def update(self):
        self.movement()
        self.x_collision()
        self.animation_status()
        self.gravity()
        self.y_collision()