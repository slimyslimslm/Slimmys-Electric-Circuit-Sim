import pygame

class CircuitComponentSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img) -> None:
        super().__init__()

        self.file_path = img
        loaded_img = pygame.image.load(self.file_path)
        self._image = pygame.transform.scale(loaded_img, (width, height))
        self._rect = self.image.get_rect()
        self._rect.topleft = x, y

    @property
    def rect(self) -> pygame.Rect:
        return self._rect
    
    @rect.setter
    def rect(self, other: pygame.Rect) -> pygame.Rect:
        self._rect = other

    @property
    def image(self) -> pygame.Surface:
        return self._image 
    
    @image.setter
    def image(self, other: pygame.Surface) -> None:
        self._image = other 
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, self.rect)

class CircuitComponent(CircuitComponentSprite):

    def __init__(self, x, y, width, height, img) -> None:
        """For the left and right couple states, a 0 indicates the couple is not attached to anyting, a 1 indicates it is collides with another couple and ready to attach
        and a 2 indicates that the couple is attached to a couple of another component."""
        super().__init__(x, y, width, height, img)
        self.name = "Component"

        self.left_components = []
        self.right_components = []

        self.selection_circle_radius = 8
        self.left_selection_circle_center = pygame.math.Vector2(self.rect.x - self.selection_circle_radius, self.rect.centery)
        self.right_selection_circle_center = pygame.math.Vector2(self.rect.x + self.rect.width + self.selection_circle_radius, self.rect.centery)

        self._left_rect = pygame.Rect(0, 0, self.selection_circle_radius, self.selection_circle_radius)
        self._right_rect = pygame.Rect(0, 0, self.selection_circle_radius, self.selection_circle_radius)

        self._left_rect.center = self.left_selection_circle_center
        self._right_rect.center = self.right_selection_circle_center

        self.left_color = (255, 0, 0)
        self.right_color = (255, 0, 0)

        self.left_circle_selected = False 
        self.right_circle_selected = False 

        self._rotation_state = 0

        self.being_dragged = False 

    @property
    def image(self) -> pygame.Surface:
        return self._image 
    
    @image.setter
    def image(self, other: pygame.Surface) -> None:
        old_center = self._rect.center
        self._image = other 
        self._rect = self._image.get_rect(center=old_center)

    @property 
    def left_rect(self) -> pygame.Rect:
        return self._left_rect
    
    @left_rect.setter
    def left_rect(self, other: pygame.Rect) -> None:
        self._left_rect = other 

    @property 
    def right_rect(self) -> pygame.Rect:
        return self._right_rect
    
    @right_rect.setter
    def right_rect(self, other: pygame.Rect) -> None:
        self._right_rect = other 

    @property
    def rotation_state(self) -> int:
        return self._rotation_state 
    
    @rotation_state.setter
    def rotation_state(self, other: int) -> None:
        target = other % 4
        while self._rotation_state != target:
            self._rotation_state = (self._rotation_state + 1) % 4
            self.image = pygame.transform.rotate(self.image, -90)
    
        # x_center, y_center = self.image.get_rect().centerx, self.image.get_rect().centery
        # self.update_circle_positions(x_center, y_center) 

    def move_component(self):

        if self.being_dragged:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x_diff, y_diff = mouse_x - self.rect.centerx, mouse_y - self.rect.centery

            self.rect.centerx += x_diff
            self.rect.centery += y_diff    
            self.update_circle_positions(self.rect.centerx, self.rect.centery)
            
            stack = []
            visited = {self}

            for component in self.left_components:
                stack.append(component)
            for component in self.right_components:
                stack.append(component)

        else:
            return 
        
        while stack != []:
                node = stack.pop()
                if node not in visited:
                    node.rect.centerx += x_diff
                    node.rect.centery += y_diff 
                    node.update_circle_positions(node.rect.centerx, node.rect.centery)
            
                    for component in node.left_components:
                        if component not in visited:
                            stack.append(component)
                    for component in node.right_components:
                        if component not in visited:
                            stack.append(component)

                    visited.add(node)


    def check_circle_selection(self, cursor):
        # Use rotation states and component circles to figure out the components orientation
        if self.left_rect.collidepoint(pygame.mouse.get_pos()) and cursor == "Default Cursor":
            self.left_circle_selected = True
        elif self.right_rect.collidepoint(pygame.mouse.get_pos()) and cursor == "Default Cursor":
            self.right_circle_selected = True 

    def split_component(self) -> None:
        """Split the component from other components and move it slightly depending on rotations state"""
        for component in self.left_components + self.right_components:
            if self in component.left_components:
                component.left_components.remove(self)
            if self in component.right_components:
                component.right_components.remove(self)

        self.left_components = []
        self.right_components = []

        increment = 4 * self.selection_circle_radius

        if self.rotation_state == 0:
            self.left_rect.y += increment 
            self.rect.y += increment
            self.right_rect.y += increment
        elif self.rotation_state == 1:
            self.left_rect.x += increment
            self.rect.x += increment
            self.right_rect.x += increment 
        elif self.rotation_state == 2:
            self.left_rect.y -= increment 
            self.rect.y -= increment 
            self.right_rect.y -= increment
        else: # self.rotation_state == 3
            self.left_rect.x -= increment 
            self.rect.x -= increment 
            self.right_rect.x -= increment 

    def check_selection(self, cursor):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and cursor == "Default Cursor":
            self.being_dragged = True 
        elif self.rect.collidepoint(pygame.mouse.get_pos()) and cursor == "Rotate Cursor" \
            and (self.left_components == [] and self.right_components == []): # Makes sure component is not connected to anything

            self.rotation_state += 1
            self.update_circle_positions(self.rect.centerx, self.rect.centery)

        elif self.rect.collidepoint(pygame.mouse.get_pos()) and cursor == "Scissors Cursor":
            if len(self.left_components) > 0 or len(self.right_components) > 0: 
                self.split_component()

    def update_circle_positions(self, new_center_x, new_center_y):
        if self.rotation_state == 0:
            self.left_rect.center = pygame.math.Vector2(new_center_x - self.rect.width//2 - self.selection_circle_radius, 
                                                                                new_center_y)
            self.right_rect.center = pygame.math.Vector2(new_center_x + self.rect.width//2 + self.selection_circle_radius, 
                                                                                new_center_y)
        elif self.rotation_state == 1:
            # self.left_rect.center = pygame.math.Vector2(new_center_x - 13, new_center_y - self.rect.height//2 - self.selection_circle_radius)
            # self.right_rect.center = pygame.math.Vector2(new_center_x - 13, new_center_y + self.rect.height//2 + self.selection_circle_radius + 28)

            self.left_rect.center = pygame.math.Vector2(new_center_x, new_center_y - self.rect.height//2 - self.selection_circle_radius)
            self.right_rect.center = pygame.math.Vector2(new_center_x, new_center_y + self.rect.height//2 + self.selection_circle_radius)
        
        elif self.rotation_state == 2:
            self.left_rect.center = pygame.math.Vector2(new_center_x + self.rect.width//2 + self.selection_circle_radius, 
                                                                                new_center_y)
            self.right_rect.center = pygame.math.Vector2(new_center_x - self.rect.width//2 - self.selection_circle_radius, 
                                                                                new_center_y)
            
        elif self.rotation_state == 3:
            self.left_rect.center = pygame.math.Vector2(new_center_x, new_center_y + self.rect.height//2 + self.selection_circle_radius)
            self.right_rect.center = pygame.math.Vector2(new_center_x, new_center_y - self.rect.height//2 - self.selection_circle_radius)
        
        else:
            pass

    def draw(self, window):
        super().draw(window)

        self.left_rect = pygame.draw.circle(window, self.left_color, self.left_rect.center, self.selection_circle_radius, 2)
        self.right_rect = pygame.draw.circle(window, self.right_color, self.right_rect.center, self.selection_circle_radius, 2)

class Battery(CircuitComponent):
    def __init__(self, x, y, width, height, img) -> None: 
        super().__init__(x, y, width, height, img)
        self.name = "Battery"

class Wire(CircuitComponent):
    def __init__(self, x, y, width, height, img) -> None: 
        super().__init__(x, y, width, height, img)
        self.name = "Wire"

class Resistor(CircuitComponent):
    def __init__(self, x, y, width, height, img) -> None: 
        super().__init__(x, y, width, height, img)
        self.name = "Resistor"

class Capacitor(CircuitComponent):
    def __init__(self, x, y, width, height, img) -> None: 
        super().__init__(x, y, width, height, img)

class Switch(CircuitComponent):
    def __init__(self, x, y, width, height, img) -> None: 
        super().__init__(x, y, width, height, img)
        self.is_closed = False 

class Inductor(CircuitComponent):
    def __init__(self, x, y, width, height, img) -> None: 
        super().__init__(x, y, width, height, img)
        