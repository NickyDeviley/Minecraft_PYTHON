import pygame


class Camera(pygame.sprite.Group):

    def __init__(self, *sprites):
        super().__init__(*sprites)

        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        #status
        self.width = self.display.get_width()
        self.height = self.display.get_height()
        self.mid = 2
        self.tile = 32


    def costume_draw(self, player):

        if -1000 < player.rect.x < 1000:
            self.offset.x = player.rect.centerx - self.width // 2
        if -500 < player.rect.y < 500:
            self.offset.y = player.rect.centery - self.height // 2

        for sprite in self.sprites():
            pos_copy = sprite.rect.copy()
            pos_copy.center -= self.offset

            if pos_copy.right < (self.width + self.tile) and pos_copy.left > -self.tile:
                self.display.blit(sprite.image, pos_copy)

    def update(self, *args, **kwargs):

        for sprite in self.sprites():
            pos_copy = sprite.rect.copy()
            pos_copy.center -= self.offset

            if pos_copy.right < (self.width + self.tile) and pos_copy.left > -self.tile:
                sprite.update(*args, **kwargs)