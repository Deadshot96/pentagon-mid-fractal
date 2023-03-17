import time
import math
import random
import pygame
import operator
from settings import *
from colors import *    


class Main():
    
    def __init__(self, sides=5):
        self.width = WIDTH
        self.height = HEIGHT
        self.xoff = X_OFF
        self.yoff = Y_OFF
        self.gameWinWidth = GAMEWIN_WIDTH
        self.gameWinHeight = GAMEWIN_HEIGHT
        self.fps = FPS
        self.win = None
        self.clock = None
        self.sides = sides
        self.points = []
        self.centre = (self.gameWinWidth // 2, self.gameWinHeight // 2)
        self.currPoint = None
        self.sidePoint = None
        self.angle = 2 * math.pi * (self.sides - 2) / self.sides
        self.angle = 2 * math.pi / self.sides
        
    
    def grid_init(self):
        pygame.init()
        pygame.font.init()
        
        self.win = pygame.display.set_mode((self.width, self.height))
        title = "{0}-side Fractal".format(self.sides)
        pygame.display.set_caption(title)
        
        self.gameWinRect = pygame.Rect(self.xoff, self.yoff, self.gameWinWidth, self.gameWinHeight)
        self.gameWin = self.win.subsurface(self.gameWinRect)
        
        self.win.fill(MID_BLACK)
        self.gameWin.fill(BLACK)
        
        self.titleFont = pygame.font.SysFont(TITLE_FONT, FONT_SIZE)
        title = self.titleFont.render(title, 1, GOLD)
        w, h = title.get_size()
        blitX = (self.width - w) // 2
        blitY = (self.yoff - h) // 2
        self.win.blit(title, (blitX, blitY))
        
        self.clock = pygame.time.Clock()
        
        self.draw_shape()
        
        pygame.display.update()


    def close(self):
        pygame.font.quit()
        pygame.quit()


    def draw_shape(self):
        shapeSize = min(self.gameWinHeight, self.gameWinWidth) * 4 // 10
        
        startDeltaAngle = 0 if self.sides % 2 != 0 else self.angle / 2
        
        point = self.rotate((0, -shapeSize), startDeltaAngle)
        self.currPoint = point
        self.sidePoint = point
        self.points.append(point)
        
        self.pixel(point)
        for _ in range(self.sides - 1):
            point = self.rotate(point, self.angle)
            self.pixel(point)
            self.points.append(point)
            
        for i in range(len(self.points)):
            j = (i + 1) % len(self.points)
            start = self.translate(self.points[i])
            end = self.translate(self.points[j])
            pygame.draw.line(self.gameWin, LAWN_GREEN, start, end)
        
    
    def translate(self, point, tranlation=None):
        if not tranlation:
            translation = self.gameWinWidth // 2, self.gameWinHeight // 2
        return self.point_op(point, translation, operator.add) 
    
    
    def rotate(self, point, angle):
        x, y = point
        rx = int(x * math.cos(angle) - y * math.sin(angle))
        ry = int(x * math.sin(angle) + y * math.cos(angle))

        return rx, ry    
    
    
    def point_op(self, left, right, operation):
        x = operation(left[0], right[0])
        y = operation(left[1], right[1])
        
        return x, y


    def draw(self):
        newPoint = self.sidePoint
        while newPoint == self.sidePoint:
            newPoint = random.choice(self.points)
        
        self.sidePoint = newPoint
        point = self.point_op(self.sidePoint, self.currPoint, operator.add)
        point = self.point_op(point, (2, 2), operator.floordiv)
        self.currPoint = point

        self.pixel(self.currPoint)
        
        pygame.display.update()
    
    
    def pixel(self, point, color=LAWN_GREEN):
          
        point = self.translate(point)
                
        self.gameWin.set_at(point, color)


    def run(self):
        if not pygame.display.init():
            self.grid_init()

        run = True
        while run:
            # self.clock.tick(self.fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE]:
                self.draw()
                
                    
        self.close()        


if __name__ == "__main__":
    X = Main(sides=5)
    X.run()














