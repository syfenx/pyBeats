import pygame
class Playhead(object):
    def __init__(self, location, screen, color):
        self.start = 0
        self.screen = screen
        self.color = color
        self.r = pygame.Rect(location,0,1,pygame.Surface.get_height(self.screen))
    def draw(self, x):
        
        self.x = x
        self.r = pygame.Rect(self.x,0,1,pygame.Surface.get_height(self.screen))
        self.topbar = pygame.Rect(0,0,pygame.Surface.get_width(self.screen),20)
        pygame.draw.rect(self.screen, (33,33,33), self.topbar)
        pygame.draw.rect(self.screen, self.color, self.r)