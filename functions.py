import pygame
from pybass import *
import math
pygame.font.init()
font = pygame.font.Font('coders_crux.ttf', 16)




#---------------------------------------------------------------------

class AudioItem(object):
    def __init__(self,screen, x, y, w, h, color, filename, volume):
        self.file = filename
        self.volume = volume
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.volume_changed = False
        self.name = filename[8:]
        self.color = color
        self.block = pygame.Rect([self.x,self.y,self.w,self.h])
        self.filePlayerHandle = BASS_StreamCreateFile(False, bytes(filename,'utf-8'), 0, 0, 0)
        self.set_volume(self.volume)
        self.screen = screen
        #BASS_ChannelSetFX(self.filePlayerHandle,BASS_FX_DX8_GARGLE,1)
        #BASS_ChannelSetFX(self.filePlayerHandle,BASS_FX_DX8_FLANGER,1)
    def draw(self, x, y, w, h):
        self.x = int(math.floor(x))
        self.y = int(math.floor(y))
        self.w = int(math.floor(w))
        self.h = int(math.floor(h))
        self.block = pygame.Rect([self.x,self.y,self.w,self.h])
        #if self.block.collidepoint(mpos[0], mpos[1]):
        #    self.color = (43,43,43)
        #else:
        #    self.color = (33,33,33)
        #self.block2 = pygame.Rect([self.x,self.y,self.w + 10,self.h + 10])
        if self.volume_changed == True:
            drawText(self.screen, self.x + self.w / 2 - 12, self.y - 10,str(float("{0:.2f}".format(self.volume))),8)

        pygame.draw.rect(self.screen, self.color, self.block, 0)
        pygame.draw.rect(self.screen, (55,55,55), self.block, 1)

        drawText(self.screen, self.x + self.w / 2 - 22 , self.y + self.h / 2 - 4,self.name, 8)
    def play(self, playback):
        if playback == False:
            pass
        else:

            #filePlayerHandle = BASS_StreamCreateFile(False, b'kick.wav', 0, 0, 0)
            #BASS_ChannelSetAttribute(self.filePlayerHandle, BASS_ATTRIB_VOL, self.volume)
            BASS_ChannelPlay(self.filePlayerHandle, False)
            #BASS_ChannelSlideAttribute(self.filePlayerHandle, BASS_ATTRIB_VOL, 1, 50)
            #BASS_ChannelSlideAttribute(self.filePlayerHandle, BASS_ATTRIB_VOL, -1, 60)
            #print(self.get_length_seconds())
    def get_length_seconds(self):
        len = BASS_ChannelGetLength(self.filePlayerHandle, BASS_POS_BYTE)
        return BASS_ChannelBytes2Seconds(self.filePlayerHandle, len)
    def set_sample(self, sample_path):
        self.filePlayerHandle = BASS_StreamCreateFile(False, bytes(sample_path,'utf-8'), 0, 0, 0)
    def set_volume(self, volume):
        if volume < 0.1:
            self.volume = 0.0
        if volume >1.0:
            self.volume = 1.0
        #print
        BASS_ChannelSetAttribute(self.filePlayerHandle, BASS_ATTRIB_VOL, self.volume)
        self.volume_changed = True

#---------------------------------------------------------------------

def drawText(screen, x, y, text="text", size=16):
    
    #mpos = pygame.mouse.get_pos()
    
    #text = str(mpos)
    size = font.size(text)
    fg = 255, 255, 255
    
    wincolor = 40, 40, 90
    ren = font.render(text, 1, fg, 255)
    
    screen.blit(ren, (x, y))
    



#---------------------------------------------------------------------
#depends on line spacing -1
def checkSnap(audioitems,lines,n=0):
    if not len(audioitems) == 0:
        #print('snap')
        try:
            for j in range(0, len(main_lines.lines)):
                if audioitems[selected_item].x >= main_lines.lines[j][0] and audioitems[selected_item].x <= main_lines.lines[j][0]+main_lines.snap_thresh :
                    audioitems[selected_item].x = main_lines.lines[j][0]
        except IndexError as e:
            print("index error (checksnap)", e)

#---------------------------------------------------------------------


def loadproject(audioitems,screen,project):
    f = open(project, 'r')
    data = f.readlines()
    if len(data) == 0:
        pass
    else:
        for x in range(0, len(data)):
            d = data[x].rstrip('\n').split(';')
            #print(d[0])
            audioitems.append(AudioItem(screen, int(d[0]),int(d[1]),int(d[2]),int(d[3]),(33,33,33),d[4],float(d[5])))


#---------------------------------------------------------------------
def saveproject(audioitems):
    f = open('project.txt', 'w')
    for x in range(0, len(audioitems)):
        ai = audioitems
        f.write(str(ai[x].x) + ';')
        f.write(str(ai[x].y) + ';')
        f.write(str(ai[x].w) + ';')
        f.write(str(ai[x].h) + ';')
        f.write(str(ai[x].file) + ';')
        f.write(str(ai[x].volume) + '\n')