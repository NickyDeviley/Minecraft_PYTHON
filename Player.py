import pygame

class player(pygame.sprite.Sprite):

    def __init__(self, img, pos, collision, *groups):
        super().__init__(*groups)

        # Bag
        self.bag = [{"grass": 5, "rock": 0, "sand": 0, "water": 0, "wood": 0, "leaf": 0, "metal": 0, "coal": 0}]

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

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

        # Damage Time
        self.damage_time = 0
        self.damage = False

    def verify_damage(self):
        if self.damage:
            self.damage_time += 1
            self.image.fill("red", special_flags=pygame.BLEND_RGB_MULT)
            if self.damage_time >= 60:
                self.damage_time = 0
                self.damage = False

    def x_collision(self):
        for block in self.all_collision:
#            if self.rect.colliderect(block):
            if pygame.sprite.collide_mask(self, block) and block.rigid:
                if self.direction.x > 0:
                    self.rect.right = block.rect.left
                elif self.direction.x < 0:
                    self.rect.left = block.rect.right

    def y_collision(self):
        for block in self.all_collision:
            if pygame.sprite.collide_mask(self, block):
                if block.rigid:
                    if self.direction.y > 0:
                        self.rect.bottom = block.rect.top
                        self.on_ground = True
                        self.jump_force = -15
                        self.direction.y = 0
                    elif self.direction.y < 0:
                        self.rect.top = block.rect.bottom
                        self.direction.y = 0
                else:
                    if block.style == "water":
                        self.on_ground = True
                        if self.direction.y < 0:
                            self.status = "jump"
                        elif self.direction.y > 0:
                            self.jump_force = -10
                            self.status = "swim"
                            self.direction.y = 0
                            self.animation(12, 3)

    def animation(self, speed, limit):
        self.ticks += 1
        if self.ticks >= speed:
            self.ticks = 0
            self.frame += 1

        if self.frame >= limit:
            self.frame = 0

        self.image = pygame.image.load("Assets/Player/" + self.status + str(self.frame) + ".png")
        self.image = pygame.transform.flip(self.image, self.flip, False)


    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.direction.x = -self.speed
            self.status = "walk"
            self.flip = True
        elif key[pygame.K_d]:
            self.direction.x = +self.speed
            self.flip = False
            self.status = "walk"
        else:
            self.direction.x = 0
            self.status = "idle"

        if key[pygame.K_SPACE]:
            if self.on_ground:
#               self.status = "jump"
                self.on_ground = False
                self.direction.y = -10

        self.rect.x += self.direction.x

#        if key[pygame.K_w]:
#            self.rect.y -= self.speed
#        elif key[pygame.K_s]:
#            self.rect.y += self.speed


    def animation_status(self):
        if self.status == "idle":
            self.animation(16, 3)
        elif self.status == "walk":
            self.animation(12, 3)
#       elif self.status == "jump":
#           self.animation(60, 1)
        if not self.on_ground:
            self.image = pygame.image.load("assets/player/jump0.png")
            self.image = pygame.transform.flip(self.image, self.flip, False)

    def gravity(self):
        self.direction.y += self.force
        self.rect.y +=  self.direction.y

#        if self.rect.y >= 650:
#           self.rect.y = 650
#            self.on_ground = True
#        else:
#            self.on_ground = False
#            self.image = pygame.image.load("assets/player/jump0.png")
#            self.image = pygame.transform.flip(self.image, self.flip, False)
#
#        if self.on_ground:
#            self.direction.y = 0
#        else:
#            self.image = pygame.image.load("assets/player/jump0.png")
#            self.image = pygame.transform.flip(self.image, self.flip, False)



    def update(self):
        self.movement()
        self.x_collision()
        self.animation_status()
        self.gravity()
        self.y_collision()
        self.verify_damage()

#        print(self.direction.y, self.status, self.on_ground)



#    def events(self, event):
#       if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_a:
#                self.rect.x -= 1
#            if event.key == pygame.K_d:
#                self.rect.x += 1