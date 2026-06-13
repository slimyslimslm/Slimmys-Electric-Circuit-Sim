from circuit_component import CircuitComponentSprite, CircuitComponent, Battery, Wire, Resistor, Inductor, Switch, Capacitor
from electric_circuit import ElectricCircuit
import pygame 

class DragDropMenu:
    """Class that stores attributes of a drag and drop menu in pygame"""
    def __init__(self, color: tuple[int, int, int], font: pygame.font.Font, rect: pygame.Rect, 
                 components: dict[str, CircuitComponentSprite]) -> None:
        self._color = color
        self._rect = rect 
        self._font = font
        self._components = components 

    @property
    def color(self) -> tuple[int, int, int]:
        return self._color
    
    @color.setter
    def color(self, other) -> None:
        self._color = other 

    @property
    def rect(self) -> pygame.Rect:
        return self._rect
    
    @rect.setter
    def rect(self, other) -> None:
        self._rect = other 

    @property
    def font(self) -> pygame.font.Font:
        return self._font 
    
    @font.setter
    def font(self, other) -> pygame.font.Font:
        self._font = other 

    @property
    def components(self) -> dict[str, CircuitComponentSprite]:
        return self._components 
    
    @components.setter
    def components(self, other) -> None:
        self._components = other 

    def create_component(self, name, sprite, mouse_x, mouse_y) -> CircuitComponent:
        rectangle = pygame.Rect(0, 0, sprite.rect.width, sprite.rect.height)
        rectangle.center = mouse_x, mouse_y
        if name == "Battery":
            return Battery(rectangle.x, rectangle.y, sprite.rect.width, sprite.rect.height, sprite.file_path)
        
        elif name == "Wire":
            return Wire(rectangle.x, rectangle.y, sprite.rect.width, sprite.rect.height, sprite.file_path)
        
        elif name == "Resistor":
            return Resistor(rectangle.x, rectangle.y, sprite.rect.width, sprite.rect.height, sprite.file_path)
        
        elif name == "Capacitor":
            return Capacitor(rectangle.x, rectangle.y, sprite.rect.width, sprite.rect.height, sprite.file_path)
        
        elif name == "Switch":
            return Switch(rectangle.x, rectangle.y, sprite.rect.width, sprite.rect.height, sprite.file_path)
        
        elif name == "Inductor":
            return Inductor(rectangle.x, rectangle.y, sprite.rect.width, sprite.rect.height, sprite.file_path)

    def check_menu_selection(self, circuits_list: list[ElectricCircuit]):
        """Checks if user selects element in the menu"""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for name, component_sprite in self.components.items():
            if component_sprite.rect.collidepoint((mouse_x, mouse_y)):
                new_component = self.create_component(name, component_sprite, mouse_x, mouse_y)
                if new_component is not None:
                    new_component.being_dragged = True 
                    circuits_list.append(ElectricCircuit([new_component]))


    def draw(self, window) -> None:
        """Draws menu onto the given window"""
        y = self.rect.y
        buffer = 4
        element_size = (self.rect.height - buffer)/len(self.components.items()) - buffer

        pygame.draw.rect(window, self.color, self.rect)
        for name, component, in self.components.items():
            """Draw name, draw component sprite"""
            y += buffer 
            component.rect.centerx = self.rect.centerx
            component.rect.y = y
            component.rect.height = element_size - 5
            component.draw(window)
            y += component.rect.height 
            
            name_render = self.font.render(name, True, (0, 0, 0))
            name_rect = name_render.get_rect()
            name_rect.centerx = self.rect.centerx # x value specifically
            name_rect.y = y
            window.blit(name_render, name_rect)
            y += buffer 