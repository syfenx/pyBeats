import pygame
class MainLines(object):
    def __init__(self, screen_width, screen):
        self.lines = []
        self.space = 8
        self.snap_thresh = self.space -1
        self.start = 0
        self.amt = screen_width / self.space
        self.screen = screen
        for x in range(0,int(self.amt)):
                l = pygame.Rect(self.start,0,1,pygame.Surface.get_height(screen))
                self.lines.append(l)
                self.start+=self.space

    def drawlines(self):
      c = 4
      v = 16
      for x in range(0,len(self.lines)):
        if c==0:
            pygame.draw.rect(self.screen, (44,44,44), self.lines[x], 2)
            c = 4
        if v == 0:
            pygame.draw.rect(self.screen, (44,44,44), self.lines[x], 4)
            v = 16
        else:
            pygame.draw.rect(self.screen, (29,29,29), self.lines[x], 1)
        c-=1
        v-=1
    def setLines(self):
        pass