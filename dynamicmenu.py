import pygame 
from button import Button

class DynamicMenu:
    """Meant to model the dynamic menu shown on the 
    bottom of the screen and updates depending on what the user does/clicks on"""

    
    def __init__(self, rect: pygame.Rect, font: pygame.font):
        self.rect = rect
        self.color = 0, 0, 0
        self.border = 2

        self.font = font
        self.select_state = "Default"


        scissors_button = Button(self.rect.centerx, self.rect.centery - self.rect.height//4, 50, 50, "Scissors Button", r"assets\Scissors Button-1.png.png")
        scissors_button.rect.center = self.rect.centerx, self.rect.centery - self.rect.height//4

        # key is state, value is a tuple where 0th element is list of buttons, 1st element is the text render to be printed below the buttons 
        self.selection_states = {"Default": (pygame.sprite.Group(), self.font.render("", True, (0, 0, 0))), 
                       "Connected Circle": (pygame.sprite.Group([scissors_button]), 
                                            self.font.render(self._connected_circle_text(), True, (0, 0, 0)))}
    

    def _connected_circle_text(self) -> str:
        """Returns connected circle text"""
        return "something"

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, self.rect, self.border)

        # Note that the buttons in the menu are drawn in the main file since they will be included in the simulation's button sprite group

        text = self.selection_states[self.select_state][1]

        text_rect = text.get_rect()
        text_rect.center = self.rect.centerx, self.rect.centery + self.rect.height//4
        window.blit(text, text_rect)
    
