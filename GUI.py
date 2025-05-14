import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
class Close_Window(IOError): pass



class Globals:
    def __init__(self):
        self.sort_by = "volume"
globals = Globals()


class Button:
    def __init__(self, canvas, x, y, w, h, text, target):
        self.canvas = canvas
        self.target = target
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def Input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:                # IF left-click
                self.Clicked()
    def Update(self, data): pass
    def Render(self):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pygame.draw.rect(self.canvas, BLACK, (x, y, w, h), 0 )
        pygame.draw.rect(self.canvas, WHITE, (x, y, w, h), 1 )
        font = pygame.font.Font(None, int(w / len(self.text) * 0.8) )
        text_surface = font.render(self.text, True, WHITE)
        self.canvas.blit(text_surface, (x, y))

    def Clicked(self):
        print("<BUTTON PRESSED>")
        print("This is a virtual function that MUST be overwritten by all child classes")
        print("The button class used must be missing its \"Clicked(self):\" function!")
        print("</BUTTON PRESSED>")

class Button_Sort_1 (Button):
    def Clicked(self):
        print("Does something!")



class Graph:
    def __init__(self, canvas, x, y, w, h):
        self.canvas = canvas
        self.state = "bandwidth"
        self.scale = 1
        self.data = list()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def Input(self, key): pass
    def Update(self, data):
        self.data = data
    def Render(self):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        data = self.data
        if len(data) == 0:
            data_gap = 10
        else:
            data_gap = h / len(data)
        # 1. Draw border box
        pygame.draw.rect(self.canvas, BLACK, (x, y, w, h), 0 )
        pygame.draw.rect(self.canvas, WHITE, (x, y, w, h), 1 )
        # 2. draw a bar for every data point
        for i in range(len(data)):
            # 2.1. draw the bar
            x2 = x
            y2 = i * data_gap + y
            w2 = self.scale * data[i][1]
            h2 = data_gap
            x2 = int(x2)
            y2 = int(y2)
            w2 = int(w2)
            h2 = int(h2)
            pygame.draw.rect(self.canvas, WHITE, (x2, y2, w2, h2), 0 )
            # 2.2. draw/write the IP
            font = pygame.font.Font(None, int(data_gap * 0.8) )
            text_surface = font.render(self.data[i][0], True, WHITE)
            self.canvas.blit(text_surface, (x2+w2, y2))


class GUI_Class:
    # -----------------=================   Constructor and Destructor   =================-----------------
    def __init__(self, w, h):
         # 1. Create pygame Window
        self.screen = pygame.display.set_mode((w,h))   # Height and Width of window
        pygame.display.set_caption("Revenant")              # Title of window
        icon = pygame.image.load('RevenantIcon1.png')       # Icon of window
        pygame.display.set_icon(icon)
        # 2. Instantiate all agents inside the GUI
        self.agent_list = list()
        button_sort_1 = Button_Sort_1(self.screen, 10, 20, 30, 40, "sort", globals)
        table_1 = Graph(self.screen, 150,100, 700,300,)
        # 3. Save all agents for later use
        self.agent_list.append(button_sort_1)
        self.agent_list.append(table_1)
    def __del__(self):
        self.Close()
    def Close(self):
        print("Closing Window...")
        pygame.quit()
        print("Window closed.")
    # -----------------=================   Methods   =================-----------------
    def Input(self, data):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Close_Window()
            for agent in self.agent_list:
                agent.Input(event)
    def Update(self, ip_list):
        for agent in self.agent_list:
            agent.Update(ip_list)
            
    def Render(self):
        self.screen.fill((255,0,0))             # 1. Clear Window
        for agent in self.agent_list:           # 2. Draw items
            agent.Render()
        pygame.display.update()                 # 3. Update window



if __name__ == "__main__":
    gui = GUI_Class(1000, 600)
    try:
        while True:
            data = [
                ["ip1", 12],
                ["ip2", 22],
                ["ip3", 32],
                ["ip4", 5]]
            gui.Input(data)
            gui.Update(data)
            gui.Render()
    except Close_Window:
        gui.Close()
