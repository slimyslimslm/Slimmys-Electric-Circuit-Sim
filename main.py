import pygame
from button import Button
from circuit_component import CircuitComponentSprite, CircuitComponent, Wire
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
        # self.components = []
        self.component_menu = DragDropMenu(SIDE_BAR_COLOR, pygame.font.SysFont("comicsans", 10), 
                                  pygame.Rect(1200, 5, 295, HEIGHT - 10), COMPONENTS_LIST)
        

        # Only meant to create self.dynamic_menu's rectangle, not used again
        temp_rect = pygame.Rect(0, 0, 600, 125)
        temp_rect.center = (WIDTH - 295)//2, HEIGHT - 75

        self.dynamic_menu = DynamicMenu(temp_rect, pygame.font.SysFont("comicsans", 10))
        
        self.circuits = []

        self.buttons = pygame.sprite.Group([Button(30, 30, 50, 50, "Default Cursor", r"assets\Cursor Button-1.png.png"),
                        Button(30, 90, 50, 50, "Rotate Cursor", r"assets\Rotate Button-1.png.png"), 
                        Button(30, 150, 50, 50, "Scissors Cursor", r"assets\Scissors Button-1.png.png")])
        self.cursor = "Default Cursor"

        self.arrow_cursor_image = pygame.image.load(ROTATE_CURSOR_IMAGE_FILE)
        self.scissors_cursor_image = pygame.image.load(SCISSORS_CURSOR_IMAGE_FILE)

    @property
    def all_components(self):
        return [c for circuit in self.circuits for c in circuit.components]
    
    def all_circle_rects(self, component):
        rects = []
        for other_component in self.all_components:
            if component is not other_component:
                rects.append(other_component.left_rect)
                rects.append(other_component.right_rect)
        return rects
    
    def update_cursor(self) -> None:
        """Handles switching the cursor when needed"""
        if self.cursor == "Rotate Cursor" or self.cursor == "Scissors Cursor":
            pygame.mouse.set_visible(False)
        elif self.cursor == "Default Cursor":
            pygame.mouse.set_visible(True)

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

    def _attach3(self, component, index, components_minus_one, circle_center, side):
        other_component = components_minus_one[index//2]

        if other_component in component.left_components or other_component in component.right_components:
            return
        
        if side == "Left":
            component.left_components.append(other_component)
        else:
            component.right_components.append(other_component)

        if index % 2 == 0 and component not in other_component.left_components:
            other_x, other_y = other_component.left_rect.center
            other_component.left_components.append(component)
            for c in other_component.left_components:
                if c is not component and other_component in c.left_components and component not in c.left_components:
                    c.left_components.append(component)
                elif c is not component and other_component in c.right_components and component not in c.right_components:
                    c.right_components.append(component)
    
        elif index % 2 == 1 and component not in other_component.right_components: # Attach to other's right side 
            other_x, other_y = other_component.right_rect.center
            other_component.right_components.append(component)

            for c in other_component.right_components:
                if c is not component and other_component in c.left_components and component not in c.left_components:
                    c.left_components.append(component)
                elif c is not component and other_component in c.right_components and component not in c.right_components:
                    c.right_components.append(component)
        else:
            other_x, other_y = other_component.right_rect.center
            return 
        

        circuit = component.find_circuit(self.circuits)
        other_circuit = other_component.find_circuit(self.circuits)

        if circuit is not other_circuit:
            self.circuits.remove(circuit)
            self.circuits.remove(other_circuit)
            self.circuits.append(circuit + other_circuit)

        x, y = circle_center
        x_difference = x - other_x
        y_difference = y - other_y

        stack = []
        visited = {other_component, component}

        for component in other_component.left_components:
            stack.append(component)
        for component in other_component.right_components:
            stack.append(component)

        other_component.left_rect.x += x_difference
        other_component.left_rect.y += y_difference 
        other_component.rect.centerx += x_difference 
        other_component.rect.centery += y_difference 
        other_component.right_rect.x += x_difference
        other_component.right_rect.y += y_difference 
        
        while stack != []:
            node = stack.pop()
            if node not in visited:
                node.left_rect.x += x_difference
                node.left_rect.y += y_difference 
                node.rect.centerx += x_difference 
                node.rect.centery += y_difference 
                node.right_rect.x += x_difference
                node.right_rect.y += y_difference 

                for component in node.left_components:
                    if component not in visited:
                        stack.append(component)
                for component in node.right_components:
                    if component not in visited:
                        stack.append(component)

                visited.add(node)
        

    def attach3(self):
        components = self.all_components
        for component in self.all_components:
            if not component.being_dragged:
                continue 
                pass
    
            components = self.all_components
            components.remove(component)
            all_circle_rects = self.all_circle_rects(component)
            
            left_collided_indices = component.left_rect.collidelistall(all_circle_rects)
            right_collided_indices = component.right_rect.collidelistall(all_circle_rects) 
        
            # print(f"All Circle Rects: {all_circle_rects}")
            for index in left_collided_indices:
                other_rect = all_circle_rects[index]
                # print(f"Thingy {component.left_rect is not other_rect}")
                if component.left_rect is not other_rect:
                    self._attach3(component, index, components, component.left_rect.center, "Left")
                    pass 
            
            for index in right_collided_indices:
                other_rect = all_circle_rects[index]
                if component.right_rect is not other_rect:
                    self._attach3(component, index, components, component.right_rect.center, "Right")
        
        for circuit in self.circuits:
            # print(circuit.is_closed())
            pass

    def _attach(self, component, other_component, index, circle_center):
        """"
        self.circuits.remove(circuit)
        self.circuits.remove(other_circuit)
        self.circuits.append(circuit + other_circuit)
        """

        if index % 2 == 0: # Attach to other's left side
            other_x, other_y = other_component.left_rect.center
           # other_component.left_components.append(component) 
        else: # Attach to other's right side 
            other_x, other_y = other_component.right_rect.center
           # other_component.right_components.append(component)

        x, y = circle_center
        x_difference = x - other_x
        y_difference = y - other_y

        stack = []
        visited = {other_component}

        for component in other_component.left_components:
            stack.append(component)
        for component in other_component.right_components:
            stack.append(component)

        other_component.left_rect.x += x_difference
        other_component.left_rect.y += y_difference 
        other_component.rect.centerx += x_difference 
        other_component.rect.centery += y_difference 
        other_component.right_rect.x += x_difference
        other_component.right_rect.y += y_difference 

        
        while stack != []:
            node = stack.pop()
            if node not in visited:
                node.left_rect.x += x_difference
                node.left_rect.y += y_difference 
                node.rect.centerx += x_difference 
                node.rect.centery += y_difference 
                node.right_rect.x += x_difference
                node.right_rect.y += y_difference 

                for component in node.left_components:
                    if component not in visited:
                        stack.append(component)
                for component in node.right_components:
                    if component not in visited:
                        stack.append(component)

                visited.add(node)
        
        if index % 2 == 0: # Attach to other's left side
            other_component.left_components.append(component) 
        else: # Attach to other's right side 
            other_component.right_components.append(component)

    def attach2(self):
        """WORK HERE"""
        all_circle_rects = []
        circuits_to_combine = []

        for component in self.all_components:
            all_circle_rects.append(component.left_rect)
            all_circle_rects.append(component.right_rect)

        for component in self.all_components:
                left_collided_rect_indices = component.left_rect.collidelistall(all_circle_rects)
                # right_collided_rect_indices = component.right_rect.collidelistall(all_circle_rects)
                
                for index in left_collided_rect_indices:
                    if all_circle_rects[index] == component.left_rect or all_circle_rects == component.right_rect:
                        left_collided_rect_indices.remove(index)
                    
                for index in left_collided_rect_indices:
                    other_component = self.all_components[index//2]
                    if (all_circle_rects[index] is not component.left_rect and other_component not in component.left_components and other_component not in component.right_components 
                        and other_component is not component):

                        circuit = component.find_circuit(self.circuits)
                        other_circuit = other_component.find_circuit(self.circuits)
                        circuits_to_combine.append((circuit, other_circuit))
                        self._attach(component, other_component, index, component.left_rect.center)
                        component.left_components.append(other_component)
                        if component.name == "Resistor":
                            
                            pass 
                        

                right_collided_rect_indices = component.right_rect.collidelistall(all_circle_rects)

                for index in right_collided_rect_indices:
                    
                    if all_circle_rects[index] is component.left_rect or all_circle_rects is component.right_rect:
                        right_collided_rect_indices.remove(index)
                
                for index in right_collided_rect_indices:

                    other_component = self.all_components[index//2]
                    if (all_circle_rects[index] is not component.right_rect and other_component not in component.left_components and other_component not in component.right_components 
                        and other_component is not component):

                        if component.name == "Resistor":
                 
                            pass 

                        circuit = component.find_circuit(self.circuits)
                        other_circuit = other_component.find_circuit(self.circuits)
                        circuits_to_combine.append((circuit, other_circuit))
                        self._attach(component, other_component, index, component.right_rect.center)
                        component.right_components.append(other_component)
                        if component.name == "Resistor":
                          
                            pass 

        for circuit, other_circuit in circuits_to_combine:
            if circuit in self.circuits and other_circuit in self.circuits:
                self.circuits.remove(circuit)
                self.circuits.remove(other_circuit)
                self.circuits.append(ElectricCircuit(circuit.components + other_circuit.components))
        

    def mouse_button_down_events(self) -> None:
        """
        Handles all events where the mouse is clicked
        Events include:
            - Checking if component menu is selected
            - Checking if a field component is selected
            - Checking if a button is selected
        """
        if self.cursor == "Default Cursor":
            self.component_menu.check_menu_selection(self.circuits)

        self.check_buttons_selection()

        all_components = self.all_components
        for component in all_components.copy():
            # Check component selection
            component.check_selection(self.cursor, self.circuits)
            component.check_circle_selection(self.cursor)
            if not component.left_rect.collidepoint(pygame.mouse.get_pos()):
                component.left_circle_selected = False
            if not component.right_rect.collidepoint(pygame.mouse.get_pos()):
                component.right_circle_selected = False 

    def mouse_button_up_events(self) -> None:
        """TO DO"""
        self.attach3()

        for circuit in self.circuits:
            for component in circuit.components:
                if component.being_dragged:
                    component.being_dragged = False 
                    break 

    def event_loop(self) -> None: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False 
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up_events()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down_events()
    
    def circuit_has_dragging_component(self, component) -> None:
        """WORKING HERE"""
        stack = component.left_components + component.right_components
        visited = {component}

        while stack != []:
            node = stack.pop()
            if node not in visited:
                if node.being_dragged:
                    return True 
                
                visited.add(node)
                stack.extend(node.left_components + node.right_components)

        return False 
        
    def update_component_position(self) -> None:
        for circuit in self.circuits:
            for component in circuit.components:
                component.move_component()

                if component.being_dragged is False and self.component_menu.rect.contains(component.rect):
                    if component.being_dragged:
                        circuit.components.remove(component)
                    elif not self.circuit_has_dragging_component(component):
                        for neighbor in component.left_components + component.right_components:
                            if component in neighbor.left_components:
                                neighbor.left_components.remove(component)
                                
                            elif component in neighbor.right_components:
                                neighbor.right_components.remove(component)
                    
                        circuit.components.remove(component)


        self.circuits = [c for c in self.circuits if len(c.components) != 0]

    def update_component_circle_color(self) -> None:
        """all_circle_rects has twice as many elements as self.components, so given any index and rect in all_circle_rects, the corresponding component is at 
        self.components[index//2]"""
        all_circle_rects = []
        for component in self.all_components:
                all_circle_rects.append(component.left_rect)
                all_circle_rects.append(component.right_rect)

        for component in self.all_components:
            left_collided_rect_indices = component.left_rect.collidelistall(all_circle_rects)
            right_collided_rect_indices = component.right_rect.collidelistall(all_circle_rects)

            for index in left_collided_rect_indices:
                if component.being_dragged and all_circle_rects[index] != component.left_rect:
                    
                    # rect_index = all_circle_rects.index(all_circle_rects[index])
                    other_component = self.all_components[index//2] # other component in preconnected state 
                    component.left_color = GREEN
                    
                    if index % 2 == 0:
                        other_component.left_color = GREEN  
                        
                    else:
                        other_component.right_color = GREEN 

                    for index in right_collided_rect_indices:    
                        if component.being_dragged and all_circle_rects[index] != component.right_rect:
                            other_component = self.all_components[index//2]  # other component in preconnected state 
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
                    other_component = self.all_components[index//2]  # other component in preconnected state 
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

        for circuit in self.circuits:
            for component in circuit.components:
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

        for circuit in self.circuits:
            for component in circuit.components:
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

    def debug(self) -> None:
        """Method to print stuff to help me debug"""
        for circuit in self.circuits:
            for component in circuit.components:
                if component.name == "Resistor":
                    print(circuit.is_closed("Left", component), circuit.is_closed("Right", component))

    def run_sim(self) -> None:
        while self.run:
            CLOCK.tick(FPS)
            self.event_loop() # Includes events that occur when mouse button down or up 
            self.update_cursor()
            self.update_component_position()
            self.update_component_circle_color()
            self.update_dynamic_menu_state()
            self.draw()
            # self.debug()

            """
            for circuit in self.circuits:
                if circuit.is_closed():
                    print(circuit.calculate_current())
            """

        pygame.quit()

if __name__ == "__main__":
    sim = Simulation()
    sim.run_sim()