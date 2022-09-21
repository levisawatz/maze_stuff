
import random
from time import sleep
from PIL import Image
import numpy as np
import pygame
import time
CWD="C:\\Users\\levis\\OneDrive\\Documents\\Python projects\\Personal\\maze\\"
image1 = Image.open(CWD+"Whiteboard.png")
if image1.size[1]>900:
    image1=image1.reduce(image1.size[1]//900+1)
image1.save(CWD+"program.png")
imagearr=np.array(image1)
pygame.init()
disp=pygame.display.set_mode((1280,850))
while 1:
    for event in pygame.event.get():
       if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.scancode==41):
                pygame.quit()
                quit()
    disp.fill((random.randint(0,155),random.randint(0,155),random.randint(0,155)))
    color=np.random.randint(0,255,(4,),np.ubyte)
    x=random.randint(0,imagearr.shape[0]-6)
    y=random.randint(0,imagearr.shape[1]-6)
    imagearr[x:x+5,y:y+5]=np.full((5,5,4),color)
    Image.fromarray(imagearr).save(CWD+"program.png")
    
    mazething=pygame.image.load(CWD+"program.png")
    rect=mazething.get_rect()
    rect.center=(1280//2,850//2)
    disp.blit(mazething,rect)
    pygame.display.update()
