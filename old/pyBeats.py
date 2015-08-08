import pygame
from pygame.locals import *
import playhead
import random
import time
import math
pygame.init()
screen = pygame.display.set_mode((1024, 768))
playhead = playhead.Playhead(0, screen, (255,60,99))
clock = pygame.time.Clock()
tick = 0
font = pygame.font.Font('coders_crux.ttf', 16)
pygame.display.set_caption("pyBeats - syfenx@gmail.com")

pygame.key.set_repeat (50, 5)

#speed = 100

clicked_point = []

playback = True


hit = 0
orange = (255,112,60)

from pybass import *
BASS_Init(-1, 44100, 0, 0, 0)

bpm = 160
timer_seconds = 0

sample_dir = "samples\\"


screen_width = pygame.Surface.get_width(screen)
screen_height = pygame.Surface.get_height(screen)

current_instrument = "samples\\kick.wav"


if pygame.mouse.get_pressed()[2]: 
    clicked_point.append((mpos[0],mpos[1]))
    clicked_point[0] = (mpos[0]-mpos_rel[0],mpos[1]-mpos_rel[1])


def drawText(x, y, text="text", size=16):
    mpos = pygame.mouse.get_pos()
    
    #text = str(mpos)
    size = font.size(text)
    fg = 255, 255, 255
    
    wincolor = 40, 40, 90
    ren = font.render(text, 1, fg, 255)
    
    screen.blit(ren, (x, y))

class MainLines(object):
    def __init__(self):
        self.lines = []
        self.space = 8
        self.snap_thresh = self.space -1
        self.start = 0
        self.amt = screen_width / self.space
        for x in range(0,int(self.amt)):
                l = pygame.Rect(self.start,0,1,pygame.Surface.get_height(screen))
                self.lines.append(l)
                self.start+=self.space

    def drawlines(self):
      c = 4
      v = 16
      for x in range(0,len(self.lines)):
        if c==0:
            pygame.draw.rect(screen, (44,44,44), self.lines[x], 2)
            c = 4
        if v == 0:
            pygame.draw.rect(screen, (44,44,44), self.lines[x], 4)
            v = 16
        else:
            pygame.draw.rect(screen, (29,29,29), self.lines[x], 1)
        c-=1
        v-=1
    def setLines(self):
        pass

class AudioItem(object):
    def __init__(self, x, y, w, h, color, filename, volume):
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
            drawText(self.x + self.w / 2 - 12, self.y - 10,str(float("{0:.2f}".format(self.volume))),8)

        #pygame.draw.rect(screen, self.color, self.block, 0)
        #pygame.draw.rect(screen, (55,55,55), self.block, 1)

        a = pygame.draw.rect(screen, self.color, self.block, 0)
        b = pygame.draw.rect(screen, (55,55,55), self.block, 1)
        #pygame.display.update(a)
        #pygame.display.update(b)
        #screen.blit(screen,a)
        #screen.blit(screen,b)
        drawText(self.x + self.w / 2 - 22 , self.y + self.h / 2 - 4,self.name, 8)
    def play(self):
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

#depends on line spacing -1
def checkSnap(n=0):
    if not len(audioitems) == 0:
        print('snap')
        try:
            for j in range(0, len(main_lines.lines)):
                if audioitems[selected_item].x >= main_lines.lines[j][0] and audioitems[selected_item].x <= main_lines.lines[j][0]+main_lines.snap_thresh :
                    audioitems[selected_item].x = main_lines.lines[j][0]
        except IndexError as e:
            print("index error (checksnap)", e)

running = 1

mouse_middle = 2
mouse_left = 1
mouse_right = 3
mouse_wheel_up = 4
mouse_wheel_down = 5

mouse_left_down = False
mouse_right_down = False
mouse_middle_down = False

audioitems = []
selected_item = 0
selected = False

isItemSelected = False

main_lines = MainLines()

def loadproject(project):
    f = open(project, 'r')
    data = f.readlines()
    if len(data) == 0:
        pass
    else:
        for x in range(0, len(data)):
            d = data[x].rstrip('\n').split(';')
            print(d[0])
            audioitems.append(AudioItem(int(d[0]),int(d[1]),int(d[2]),int(d[3]),(33,33,33),d[4],float(d[5])))


#print(data)
#print(data[0])
#print(data[1])
#print(data[2])
#print(data[3])
#print(data[4])
#color = data[5].lstrip('(').rstrip(')').split(',')
#audioitems.append(AudioItem(int(data[0]),int(float(data[1])),int(data[2]),int(data[3]),(33,33,33),data[4],0))
loadproject('project.txt')

while running:
  pygame.display.update()
  dt = clock.tick(60)
  speed = 1 / float(dt)
  for event in pygame.event.get():
    mpos = pygame.mouse.get_pos()
    mpos_rel = pygame.mouse.get_rel()
    if event.type == QUIT:
      running = 0
    elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()  

    #set playhead
    if pygame.mouse.get_pressed()[0] and mpos[1] <=20:
        for j in range(0, len(main_lines.lines)):
            if mpos[0] >= main_lines.lines[j][0] and mpos[0] <= main_lines.lines[j][0]+main_lines.snap_thresh :
                tick = main_lines.lines[j][0]

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == mouse_right:
            mouse_right_down = True
        if event.button == mouse_left:
            mouse_left_down = True
            for item in range(0, len(audioitems)):
                if audioitems[item].block.collidepoint(mpos[0],mpos[1]):
                    selected = True
                    selected_item = item
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == mouse_right:
            mouse_right_down = False
        if event.button == mouse_left:
            mouse_left_down = False
            selected = False
            checkSnap()

# Drag audio item with LEFT click 
    if pygame.mouse.get_pressed()[0]:
            if selected == True:
                try:
                    if audioitems[selected_item].x <0:
                        audioitems[selected_item].x
                    audioitems[selected_item].x = mpos[0] - audioitems[selected_item].w / 2
                    audioitems[selected_item].y = mpos[1] - audioitems[selected_item].h /2
                    current_instrument = audioitems[selected_item].file
                except IndexError as e:
                    print(e, "drag audio func")
                checkSnap()
            if selected == False:
                if not mpos[1] <= 25:
                    for j in range(0, len(main_lines.lines)):
                        if mpos[0] >= main_lines.lines[j][0] and mpos[0] <= main_lines.lines[j][0]+main_lines.snap_thresh :
                            #audioitems[selected_item].x = lines[j][0]
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == mouse_left:
                                    audioitems.append(AudioItem(main_lines.lines[j][0], mpos[1],50,20,(55,55,55), current_instrument, 1.0))

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == mouse_wheel_up:
            print("+ volume - mousewheelup")
            for item in range(0, len(audioitems)):
                if audioitems[item].block.collidepoint(mpos[0],mpos[1]):
                    audioitems[item].volume+=0.1
                    audioitems[item].set_volume(audioitems[item].volume)
        if event.button == mouse_wheel_down:
            print("- volume - mousewheeldown")
            for item in range(0, len(audioitems)):
                if audioitems[item].block.collidepoint(mpos[0],mpos[1]):
                    audioitems[item].volume-=0.1
                    audioitems[item].set_volume(audioitems[item].volume)
        if event.button == mouse_middle:
            mouse_middle_down = True
            print(mouse_middle_down)
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == mouse_middle:
            mouse_middle_down = False
            print(mouse_middle_down)
            print('middle up')
            checkSnap()

    if pygame.mouse.get_pressed()[2]:       #RIGHT Click

        for item in range(0, len(audioitems)):
            try:
                if audioitems[item].block.collidepoint(mpos[0],mpos[1]):
                    del audioitems[item]
            except IndexError as e:
                    print(e, 'remove item')



  screen.fill((20, 20, 20))

 

 

  #drawLines()
  main_lines.drawlines()
  '''
  loop_left = pygame.Rect([200,0,2,screen_height])
  loop_right = pygame.Rect([400,0,2,screen_height])
  pygame.draw.rect(screen, orange, loop_left, 1)
  pygame.draw.rect(screen, orange, loop_right, 1)
  '''

  for item in range(0, len(audioitems)):
    audioitems[item].draw(audioitems[item].x,audioitems[item].y,audioitems[item].w,audioitems[item].h)
    #print(audioitems[item].x)
    #if playhead.r.colliderect(audioitems[item].block):
    if playhead.r.colliderect(audioitems[item].block):
        audioitems[item].color=(255,90,99)
    else:
        audioitems[item].color=(33,33,33)
    #if playhead.x == audioitems[item].x:
    if playhead.r.colliderect(audioitems[item].block):
        time_to_play = True
    else:
        time_to_play = False

    if time_to_play == True:
        #print('hit', item)
        audioitems[item].play()
    #pygame.draw.rect(screen, audioitems[item].color, audioitems[item].block,0)


  if not playback == True:
    print('playback stopped, playback is', playback)
  else:
      if tick >= pygame.Surface.get_width(screen) - main_lines.space /2:
        tick = 0
      else:
        tick += 50 * (60000 / bpm / 4 * 0.001)
  #print(dt)


  playhead.draw(tick)
  drawText(6,6, str(bpm))

  #MOUSE SELECTION CODE
  #if mouse_right_down == True:
  if pygame.mouse.get_pressed()[2]:
    clicked_point.append(1) 
    clicked_point[0]=(mpos[0],mpos[1])
    #clicked_point[0] = (mpos[0]-mpos_rel[0],mpos[1]-mpos_rel[1])
    a = pygame.Rect(0,0,0,0)
    a.topleft = (clicked_point[0][0],clicked_point[0][1])
    #a.bottom = (mpos[0])
    #a.w = mpos[0]
    a.h = mpos[1]
    pygame.draw.rect(screen, (144,74,186),a, 1)

  

  if( pygame.key.get_pressed()[pygame.K_EQUALS] != 0 ): # + speed
    if bpm >= 999:
        bpm=999
    else:
        bpm+=1

  if( pygame.key.get_pressed()[pygame.K_MINUS] != 0 ): # - speed
    if bpm <= 10:
        bpm=10
    else:
        bpm-=1

  if( pygame.key.get_pressed()[pygame.K_1] != 0 ):
    current_instrument = "samples\\kick.wav"
  if( pygame.key.get_pressed()[pygame.K_2] != 0 ):
    current_instrument = "samples\\sd1.wav"
  if( pygame.key.get_pressed()[pygame.K_3] != 0 ):
    current_instrument = "samples\\sd2.wav"
  if( pygame.key.get_pressed()[pygame.K_4] != 0 ):
    current_instrument = "samples\\hh.wav"
  if( pygame.key.get_pressed()[pygame.K_5] != 0 ):
    current_instrument = "samples\\ohh.wav"
  if( pygame.key.get_pressed()[pygame.K_6] != 0 ):
    current_instrument = "samples\\clap.wav"
  if( pygame.key.get_pressed()[pygame.K_7] != 0 ):
    current_instrument = "samples\\cymbal.wav"
  if( pygame.key.get_pressed()[pygame.K_8] != 0 ):
    current_instrument = "samples\\cb.wav"
  if( pygame.key.get_pressed()[pygame.K_9] != 0 ):
    current_instrument = "samples\\rs.wav"
  if( pygame.key.get_pressed()[pygame.K_0] != 0 ):
    current_instrument = "samples\\hc.wav"

  #clock.tick(1000)
f = open('project.txt', 'w')
for x in range(0, len(audioitems)):
    ai = audioitems
    f.write(str(ai[x].x) + ';')
    f.write(str(ai[x].y) + ';')
    f.write(str(ai[x].w) + ';')
    f.write(str(ai[x].h) + ';')
    f.write(str(ai[x].file) + ';')
    f.write(str(ai[x].volume) + '\n')
    #float("{0:.2f}".format(self.volume))
pygame.quit()