import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name, file_path) -> None:

        super().__init__() 
        img = pygame.image.load(file_path)
        
        self.image = pygame.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.name = name
        self.file_path = file_path
