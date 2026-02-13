import pygame

class Text(pygame.sprite.Sprite):

    def __init__(self, status, pos, *groups):
        super().__init__(*groups)

        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render("0", False, "white")
        self.rect = self.image.get_rect(topleft = pos)

        self.status = status

    def update_text(self, text):
        self.image = self.font.render(text, False, "white")