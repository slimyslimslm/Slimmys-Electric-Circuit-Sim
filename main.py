import pygame
from button import Button
from circuitcomponent import CircuitComponentSprite, CircuitComponent, Wire
from dragdropmenu import DragDropMenu
from dynamicmenu import DynamicMenu
from electric_circuit import ElectricCircuit

pygame.init()

CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 1500, 700

FPS = 60

# Colors:
WHITE = 255, 255, 255
BLACK = 0, 0, 0
SIDE_BAR_COLOR = 50, 140, 240

BUFFER = 5

# "Wire": CircuitComponentSprite(0, 0, ELEMENT_SIZE, ELEMENT_SIZE, r"assets\Based Wire-1.png.png"),

ELEMENT_SIZE = (HEIGHT - 5 - BUFFER)//5 - BUFFER
COMPONENTS_LIST = {"Battery": CircuitComponentSprite(0, 0, ELEMENT_SIZE, ELEMENT_SIZE, r"assets\Based Battery-1.png.png"),
                   "Wire": CircuitComponentSprite(0, 0, ELEMENT_SIZE, ELEMENT_SIZE, r"assets\Based Wire-1.png.png"),
                  "Resistor": CircuitComponentSprite(0, 0, ELEMENT_SIZE, ELEMENT_SIZE, r"assets\Based Resistor-1.png.png"),
                  "Capacitor": CircuitComponentSprite(0, 0, ELEMENT_SIZE, ELEMENT_SIZE, r"assets\Based Capacitor-1.png.png"),
                  "Switch": CircuitComponentSprite(0, 0, ELEMENT_SIZE, ELEMENT_SIZE, r"assets\Based Open Switch-1.png.png"),
                  "Inductor": CircuitComponentSprite(0, 0, ELEMENT_SIZE, ELEMENT_SIZE, r"assets\Based Inductor-1.png.png")}

ROTATE_CURSOR_IMAGE_FILE = r"assets\Arrow Cursor-1.png.png"
SCISSORS_CURSOR_IMAGE_FILE = r"assets\Scissors Cursor-1.png.png"

RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
    
class Simulation:
    
    def __init__(self):
        self.run = True 
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.components = []
        self.component_menu = DragDropMenu(SIDE_BAR_COLOR, pygame.font.SysFont("comicsans", 10), 
                                  pygame.Rect(1200, 5, 295, HEIGHT - 10), COMPONENTS_LIST)
        

        # Only meant to create self.dynamic_menu's rectangle, not used again
        temp_rect = pygame.Rect(0, 0, 600, 125)
        temp_rect.center = (WIDTH - 295)//2, HEIGHT - 75

        self.dynamic_menu = DynamicMenu(temp_rect, pygame.font.SysFont("comicsans", 10))
        
        self.circuit = ElectricCircuit()

        self.buttons = pygame.sprite.Group([Button(30, 30, 50, 50, "Default Cursor", r"assets\Cursor Button-1.png.png"),
                        Button(30, 90, 50, 50, "Rotate Cursor", r"assets\Rotate Button-1.png.png"), 
                        Button(30, 150, 50, 50, "Scissors Cursor", r"assets\Scissors Button-1.png.png")])
        self.cursor = "Default Cursor"

        self.arrow_cursor_image = pygame.image.load(ROTATE_CURSOR_IMAGE_FILE)
        self.scissors_cursor_image = pygame.image.load(SCISSORS_CURSOR_IMAGE_FILE)
    
    def update_cursor(self) -> None:
        """Handles switching the cursor when needed"""
        if self.cursor == "Rotate Cursor" or self.cursor == "Scissors Cursor":
            pygame.mouse.set_visible(False)
        elif self.cursor == "Default Cursor":
            pygame.mouse.set_visible(True)

    def split_components(self) -> None:
        """Split the selected components"""
        for component in self.components:
            if component.left_circle_selected:
                component.left_components = [] 

            elif component.right_circle_selected:
                component.right_components = []
        
    def check_buttons_selection(self):
        """Handles events where a button is selected. Assume the user pressed down on their mouse."""
        for button in self.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if button.name == "Default Cursor":
                    self.cursor = "Default Cursor"
                elif button.name == "Rotate Cursor":
                    self.cursor = "Rotate Cursor"
                elif button.name == "Scissors Cursor":
                    self.cursor = "Scissors Cursor" 

    def _attach(self, component, index, circle_center):
        other_component = self.components[index//2]
        if index % 2 == 0: # Attach to other's left side
            other_x, other_y = other_component.left_rect.center
            other_component.left_components.append(component) 
        else: # Attach to other's right side 
            other_x, other_y = other_component.right_rect.center
            other_component.right_components.append(component)

        x, y = circle_center
        x_difference = x - other_x
        y_difference = y - other_y
        other_component.left_rect.x += x_difference
        other_component.left_rect.y += y_difference 
        other_component.rect.centerx += x_difference 
        other_component.rect.centery += y_difference 
        other_component.right_rect.x += x_difference
        other_component.right_rect.y += y_difference 
         
    def attach2(self):
        all_circle_rects = []
        for component in self.components:
            all_circle_rects.append(component.left_rect)
            all_circle_rects.append(component.right_rect)

        for component in self.components: 
            left_collided_rect_indices = component.left_rect.collidelistall(all_circle_rects)
            right_collided_rect_indices = component.right_rect.collidelistall(all_circle_rects)

            for index in left_collided_rect_indices: 
                if all_circle_rects[index] is not component.left_rect:
                    self._attach(component, index, component.left_rect.center)
                    component.left_components.append(self.components[index//2])

            for index in right_collided_rect_indices:
                if all_circle_rects[index] is not component.right_rect:
                    self._attach(component, index, component.right_rect.center)
                    component.right_components.append(self.components[index//2])

    def mouse_button_down_events(self) -> None:
        """
        Handles all events where the mouse is clicked
        Events include:
            - Checking if component menu is selected
            - Checking if a field component is selected
            - Checking if a button is selected
        """
        if self.cursor == "Default Cursor":
            self.component_menu.check_menu_selection(self.components)

        self.check_buttons_selection()

        for component in self.components:
            # Check component selection
            component.check_selection(self.cursor)
            component.check_circle_selection(self.cursor)
            if not component.left_rect.collidepoint(pygame.mouse.get_pos()):
                component.left_circle_selected = False
            if not component.right_rect.collidepoint(pygame.mouse.get_pos()):
                component.right_circle_selected = False 

    def mouse_button_up_events(self) -> None:
        for component in self.components:
            if component.being_dragged:
                component.being_dragged = False 
                break 

        """TO DO"""
        self.attach2()

    def event_loop(self) -> None: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False 
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up_events()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down_events()
            
            for component in self.components:
                if (component.left_circle_selected or component.right_circle_selected):
                    pass 

    def add_wire(self, component, key) -> None:
        """NOT USING THIS METHOD"""
        """Adds a wire when an arrow key is selected"""
        """BASE THE METHOD OFF OF THE _ATTACH METHOD"""

        new_wire = Wire(0, 0, ELEMENT_SIZE, ELEMENT_SIZE,  r"assets\Based Wire-1.png.png")
        
        if component.left_circle_selected:
            component.left_components.append(new_wire)
            circle_rect = component.left_rect
        else:
            component.right_components.append(new_wire)
            circle_rect = component.right_rect

        centerx, centery = circle_rect.centerx, circle_rect.centery

        if key == pygame.K_UP:
            new_wire.rotation_state += 1
            new_wire.update_circle_positions(new_wire.rect.centerx, new_wire.rect.centery)
            x_difference = centerx - new_wire.right_rect.centerx 
            y_difference = centery - new_wire.right_rect.centery
            new_wire.right_components.append(component)
        elif key == pygame.K_DOWN:
            new_wire.rotation_state += 1 
            new_wire.update_circle_positions(new_wire.rect.centerx, new_wire.rect.centery)
            x_difference = centerx - new_wire.left_rect.centerx 
            y_difference = centery - new_wire.left_rect.centery
            new_wire.left_components.append(component)
        elif key == pygame.K_RIGHT:
            x_difference = centerx - new_wire.left_rect.centerx 
            y_difference = centery - new_wire.left_rect.centery
            new_wire.left_components.append(component)
        else: # key == pygame.K_LEFT
            x_difference = centerx - new_wire.right_rect.centerx 
            y_difference = centery - new_wire.right_rect.centery
            new_wire.right_components.append(component)
    
       #  new_wire.left_rect.x += x_difference
        # new_wire.left_rect.y += y_difference 
        new_wire.rect.centerx += x_difference 
        new_wire.rect.centery += y_difference 
        # new_wire.right_rect.x += x_difference
        # new_wire.right_rect.y += y_difference   
        new_wire.update_circle_positions(new_wire.rect.centerx, new_wire.rect.centery)
        self.components.append(new_wire)
        
    def check_arrow_input_valid(self, component, key) -> bool:
        """Returns true or false"""
        if component.left_circle_selected:
            for other_component in component.left_components:
                if key == "up":
                    if component.rotation_state == 0 or component.rotation_state == 2:
                        if other_component.rotation_state == 1 and component in other_component.right_components:
                            return False 
                        elif other_component.rotation_state == 3 and component in other_component.left_components:
                            return False 
                    elif component.rotation_state == 1: # Note that rotation state 3 is not possible
                        if other_component.rotation_state == 1 or other_component.rotation_state == 3:
                            return False 
                    elif component.rotation_state == 3:
                        return False 
                    
                if key == "down":
                    if component.rotation_state == 0 or component.rotation_state == 2:
                        if other_component.rotation_state == 1 and component in other_component.left_components:
                            return False 
                        elif other_component.rotation_state == 3 and component in other_component.right_components:
                            return False
                    elif component.rotation_state == 3:
                        if other_component.rotation_state == 1 or other_component.rotation_state == 3:
                            return False
                    elif component.rotation_state == 1:
                        return False 
                    
                if key == "right":
                    if component.rotation_state == 2: # Note that rotation state 2 is not possible:
                        if other_component.rotation_state == 0 or other_component.rotation_state == 2:
                            return False 
                    elif component.rotation_state == 0:
                        return False
                    elif component.rotation_state == 1 or component.rotation_state == 3:
                        if other_component.rotation_state == 0 and component in other_component.left_components:
                            return False 
                        elif other_component.rotation_state == 2 and component in other_component.right_components:
                            return False 
                    
                if key == "left":
                    if component.rotation_state == 0:
                        if other_component.rotation_state == 0 or other_component.rotation_state == 2:
                            return False 
                    elif component.rotation_state == 2:
                        return False 
                    elif component.rotation_state == 1 or component.rotation_state == 3:
                        if other_component.rotation_state == 0 and component in other_component.right_components:
                            return False 
                        elif other_component.rotation_state == 2 and component in other_component.left_components:
                            return False                         
     
            return True 
        
        else: 
            """TO IMPLEMENT"""
            for other_component in component.right_components:
                if key == pygame.K_UP:
                    if component.rotation_state == 1:
                        return False 
                    elif component.rotation_state == 3:
                        if other_component.rotation_state == 1 or other_component.rotation_state == 3:
                            return False 
                    elif component.rotation_state == 0 or component.rotation_state == 2:
                        if other_component.rotation_state == 1 and component in other_component.right_components:
                            return False 
                        elif other_component.rotation_state == 3 and component in other_component.left_components:
                            return False 

                elif key == pygame.K_DOWN:
                    if component.rotation_state == 0 or component.rotation_state == 2:
                        if other_component.rotation_state == 1 and component in other_component.left_components:
                            return False 
                        elif other_component.rotation_state == 3 and component in other_component.right_components:
                            return False  
                    elif component.rotation_state == 3:
                        return False 
                    elif component.rotation_state == 1:
                        if other_component.rotation_state == 1 or other_component.rotation_state == 3:
                            return False 
                        
                elif key == pygame.K_RIGHT:
                    if component.rotation_state == 0:
                        return False 
                    elif component.rotation_state == 2:
                        if other_component.rotation_state == 1 or other_component.rotation_state == 3:
                            return False 
                    elif component.rotation_state == 1 or component.rotation_state == 3:
                        if other_component.rotation_state == 0 and component in other_component.left_components:
                            return False 
                        if other_component.rotation_state == 2 and component in other_component.right_components:
                            return False 
                        
                elif key == pygame.K_LEFT:
                    if component.rotation_state == 2:
                        return False 
                    elif component.rotation_state == 0:
                        if other_component.rotation_state == 1 or other_component.rotation_state == 3:
                            return False 
                    elif component.rotation_state == 1 or component.rotation_state == 3:
                        if other_component.rotation_state == 0 and component in other_component.right_components:
                            return False 
                        elif other_component.rotation_state == 2 and component in other_component.left_components:
                            return False 
                    
            return True 

    def handle_component_circle_selection(self, component, event) -> None:
        """Handle when component end circle points are selected"""
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                if self.check_arrow_input_valid(component, event.key):
                    self.add_wire(component, event.key)
                    return True 
        return False 

    def update_component_position(self) -> None:
        for component in self.components:
            component.move_component()

            if component.being_dragged is False and self.component_menu.rect.contains(component.rect):
                self.components.remove(component)

    def _update_one_circle_side_color(self, component: CircuitComponent, all_circle_rects: list, side: str) -> None:
        if side == "left":
            side_rect = component.left_rect
        else: # side == "right"
            side_rect = component.right_rect

        collided_rect_indices = side_rect.collidelistall(all_circle_rects)

        for index in collided_rect_indices:
            if component.being_dragged and all_circle_rects[index] != side_rect:

                other_component = self.components[index//2]
                if side == "left":
                    component.left_color == GREEN 
                else:
                    component.right_color == GREEN

                if index % 2 == 0:
                    other_component.left_color = GREEN
                    return True 
                else:
                    other_component.right_color = GREEN
                    return True 

        if side == "left" and component.left_components == []:
            component.left_color == RED 
        elif side == "right" and component.right_components == []:
            component.right_color == RED 
        elif side == "left":
            component.left_color == BLUE
        elif side == "right":
            component.right_color == BLUE 

        return False 


    def update_component_circle_color(self) -> None:
        """all_circle_rects has twice as many elements as self.components, so given any index and rect in all_circle_rects, the corresponding component is at 
        self.components[index//2]"""
        all_circle_rects = []
        for component in self.components:
            all_circle_rects.append(component.left_rect)
            all_circle_rects.append(component.right_rect)

        for component in self.components:
            left_collided_rect_indices = component.left_rect.collidelistall(all_circle_rects)
            right_collided_rect_indices = component.right_rect.collidelistall(all_circle_rects)

            for index in left_collided_rect_indices:
                if component.being_dragged and all_circle_rects[index] != component.left_rect:
                    
                    # rect_index = all_circle_rects.index(all_circle_rects[index])
                    other_component = self.components[index//2] # other component in preconnected state 
                    component.left_color = GREEN
                    
                    if index % 2 == 0:
                        other_component.left_color = GREEN
                        
                        
                    else:
                        other_component.right_color = GREEN 

                    for index in right_collided_rect_indices:    
                        if component.being_dragged and all_circle_rects[index] != component.right_rect:
                            other_component = self.components[index//2]  # other component in preconnected state 
                            component.right_color = GREEN
                            if index % 2 == 0:
                                other_component.left_color = GREEN
                            else:
                                other_component.right_color = GREEN 
                    return
                
                elif component.left_components == []:
                    component.left_color = RED 
  
                else: # If the component is connected with another one 
                    component.left_color = BLUE
            
            for index in right_collided_rect_indices:    
                if component.being_dragged and all_circle_rects[index] != component.right_rect:
                    other_component = self.components[index//2]  # other component in preconnected state 
                    component.right_color = GREEN
                    if index % 2 == 0:
                        other_component.left_color = GREEN
                        return 
                    else:
                        
                        other_component.right_color = GREEN 
                        return
                    
                elif component.right_components == []:
                    component.right_color = RED
                else:
                    component.right_color = BLUE 
                
                #all_circle_rects.append(component.left_rect)
                #all_circle_rects.append(component.right_rect)
        
    def _update_simulation_buttons(self, new_state: str) -> None:
        """Adds the new_state's buttons from the dynamic menu to self.buttons while removing the buttons from the old state"""
        old_state = self.dynamic_menu.select_state

        """Remove the old buttons except for those not contained in self.dynamic_menu like the cursor and arrow buttons"""
        for button in self.buttons:
            if button in self.dynamic_menu.selection_states[old_state][0]:
                self.buttons.remove(button)
        
        """Add the new buttons to self.buttons"""
        for button in self.dynamic_menu.selection_states[new_state][0]:
            self.buttons.add(button)
        
    def update_dynamic_menu_state(self) -> None:
        for component in self.components:
            if component.left_circle_selected or component.right_circle_selected:
                new_state = "Connected Circle"
                self._update_simulation_buttons(new_state)
                self.dynamic_menu.select_state = new_state 
                break
        else:
            new_state = "Default"
            self._update_simulation_buttons(new_state)
            self.dynamic_menu.select_state = new_state

    def draw(self) -> None:
        self.window.fill(WHITE)
        self.component_menu.draw(self.window)
        for component in self.components:
            component.draw(self.window)

        self.buttons.draw(self.window)

        if self.cursor == "Rotate Cursor":
            arrow_cursor_image_rect = self.arrow_cursor_image.get_rect()
            arrow_cursor_image_rect.center = pygame.mouse.get_pos()
            self.window.blit(self.arrow_cursor_image, arrow_cursor_image_rect)
        elif self.cursor == "Scissors Cursor":
    
            scissors_cursor_image_rect = self.scissors_cursor_image.get_rect()
            scissors_cursor_image_rect.center = pygame.mouse.get_pos()
            self.window.blit(self.scissors_cursor_image, scissors_cursor_image_rect)

        self.dynamic_menu.draw(self.window)

        pygame.display.update()

    def run_sim(self) -> None:
        while self.run:
            CLOCK.tick(FPS)
            self.event_loop() # Includes events that occur when mouse button down or up 
            self.update_cursor()
            self.update_component_position()
            self.update_component_circle_color()
            self.update_dynamic_menu_state()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    sim = Simulation()
    sim.run_sim()