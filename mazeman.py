import numpy as np
import random 
import math
from PIL import Image
import pygame
import time
from matplotlib import pyplot as plt
import matplotlib


DISPWIDTH,DISPHIGHT=(1200,850)
CWD="C:\\Users\\levis\\OneDrive\\Documents\\Python projects\\Personal\\completed\\maze\\"
class Plotter:
    def __init__(self) -> None:
        self.fig=plt.figure()
        self.ax1=self.fig.add_subplot()
        self.ax2=self.fig.add_subplot()
    def plot(self,radar):
        x=[i for i in range(len(radar))]
        dr=[radar[i+1]-radar[i]for i in range(len(radar)-1)]
        
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.plot((0,20),(np.mean(radar),np.mean(radar)))
        self.ax1.bar(x,radar)
        self.ax2.bar(x[:-1],dr)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.fig.show()


    


class Man:
    def __init__(self,data):
        self.gridp=np.array([80,80],float)
        self.direction=np.array([1,0],float)
        self.periferial=3.1
        self.nrays=10
        """angle of periferial vision, radians"""
        self.seelines=[]
        self.radar=[0 for _ in range(self.nrays)]
        self.xzero=DISPWIDTH//2-data.shape[0]//2
        self.yzero=DISPHIGHT//2-data.shape[1]//2
        self.weights=[pow((-math.cos(i*2*math.pi/self.nrays)+0.9),2) for i in range(self.nrays)]
        
    def weighted_choice(self):
        mean=np.mean(self.radar)
        choises=[self.radar[i]>mean for i in range(self.nrays)]
        for i in range(self.nrays):
            choises[i]=self.weights[i]*choises[i]
        return random.choices([i for i in range(self.nrays)],choises,k=1)
    def hugright(self):
        i=0
        
        while i<self.nrays:
            if self.radar[i]>10: break

            i+=1
        if i==self.nrays: i=self.nrays//2+1
        if i==0 and self.radar[self.nrays//2]>10: i=self.nrays//2
        


        return i    
    def __disppos__(self):
        return(tuple([round(self.gridp[0]+self.xzero),round(self.gridp[1]+self.yzero)]))
    def setpos(self,pos):
        self.gridp=np.array([pos[0]-self.xzero,pos[1]-self.yzero],float)

    def move(self,data):
        self.seeman(data)
        #self.gridp+=10*math.atan(self.seedist/30)*self.direction
        self.gridp+=self.direction*5
    def seeman(self,data):
        maxd=100
        self.seedist=0.0
        self.seelines=[]
        
        #angle-self.periferial/2,angle+self.periferial/2,self.periferial//30
        startangle=angle(self.direction)-self.periferial/2
        direction=np.copy(self.direction)
        #print(f"angle:{startangle}")
        for i in range(self.nrays):
            adder=np.array([math.cos(i*(self.periferial/self.nrays)+startangle),math.sin(i*self.periferial/self.nrays+startangle)],float)
            pos1=pos2=self.__disppos__()
            gridp2=np.array(self.gridp,float)
            j=0
            for j in range(maxd):
                gridp2+=adder
                try:
                    pos2=tuple([round(gridp2[0]+self.xzero),round(gridp2[1]+self.yzero)])
                    if data[round(gridp2[0]),round(gridp2[1])] or not inbounds(data,gridp2):
                        break
                except:
                    break
            line=[pos1,pos2]
            self.seelines.append(line)
            self.radar[i]=dist =j
            
            # if dist>self.seedist: 
            #     self.seedist=dist
            #     self.direction=adder/np.linalg.norm(adder)
        index=self.weighted_choice()[0]
        #index=self.hugright()
        self.seedist=self.radar[index]
        if self.seedist<=10:self.direction*=-1
        else:self.direction=np.array([math.cos(index*(self.periferial/self.nrays)+startangle),math.sin(index*self.periferial/self.nrays+startangle)],float)
def angle(vect):
    angle=math.atan(vect[1]/vect[0])
    if vect[0]<0:
        angle+=math.pi
    return angle
def inbounds(data,pos):
    return pos[0]>=0 and pos[1]>=0 and pos[0]<data.shape[0] and pos[1]<data.shape[1]

def NOOOseeman(mousepos,data):
    maxd=10
    xzero=DISPWIDTH//2-data.shape[0]//2
    yzero=DISPHIGHT//2-data.shape[1]//2
    gridp1=(mousepos[0]-xzero,mousepos[1]-yzero)
    lines=[]
    for i in range(32):
        adder=np.array([math.sin(i/5),math.cos(i/5)],float)/2
        pos2=mousepos
        gridp2=np.array(gridp1,float)
        for _ in range(maxd):
            gridp2+=adder
            try:
                pos2=tuple([round(gridp2[0]+xzero),round(gridp2[1]+yzero)])
                if data[round(gridp2[0]),round(gridp2[1])] or not inbounds(data,gridp2):
                    break
            except:
                break
      
        lines.append([mousepos,pos2])
    
    

    return lines

def displines(disp,color,lines):
    for line in lines:
        pygame.draw.line(disp,color,line[0],line[1],width=2)
def drawman(disp,man:Man):
    size=1
    pos=man.__disppos__()
    pygame.draw.circle(disp, (0,255,0), pos, 10*size)
    pygame.draw.circle(disp, (0,0,0), pos, 10*size,width=1)
    ang=angle(man.direction)
    i=ang+.35
    eye=np.array([math.cos(i),math.sin(i)],float)
    pygame.draw.circle(disp, (0,0,0), pos+eye*6*size,2)
    i=ang-.45
    eye=np.array([math.cos(i),math.sin(i)],float)
    pygame.draw.circle(disp, (0,0,0), pos+eye*6*size, 2)
def drawpath(disp,imagearr,pos):
    rad=3
    x,y=[round(i) for i in pos]
    color=np.array([200,20,10,255],np.ubyte)#ignore
    imagearr[y-rad:y+rad,x-rad:x+rad]=np.full((2*rad,2*rad,4),color,np.ubyte)
    Image.fromarray(imagearr).save(CWD+"programpath.png")
    mazething=pygame.image.load(CWD+"programpath.png")

    rect=mazething.get_rect()
    rect.center=(DISPWIDTH//2,DISPHIGHT//2)
    disp.blit(mazething,rect)

def main():
    pygame.init()
    disp=pygame.display.set_mode((DISPWIDTH,DISPHIGHT))
    pygame.display.set_caption('MAZE GRID!!!!!')
    #pygame.mouse.set_visible(False)
    clock= pygame.time.Clock()
    pmp=mousepos=(0,0)
    mousebutton=0
    begintime=time.time()
    image1 = Image.open(CWD+"megsmaze.png")
    plotter=Plotter()

    if image1.size[1]>900:
        image1=image1.reduce(image1.size[1]//900+1)
    image1.save(CWD+"program.png")
    data=np.array(image1)
    path=np.zeros((image1.size[1],image1.size[0],4),np.ubyte)
    data=np.array([[int(data[i,j,0]<100)for i in range(data.shape[0])]for j in range(data.shape[1])])
    print(data.shape)
    men=[Man(data) for _ in range(1)]
    man=men[0]
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.scancode==41):
                pygame.quit()
                quit()
            elif event.type==pygame.MOUSEMOTION: 
                mousepos=event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                man.setpos(mousepos)
            elif event.type == pygame.MOUSEBUTTONUP:
                mousebutton=0
        mazething=pygame.image.load(CWD+"program.png")
        rect=mazething.get_rect()    
        rect.center=(DISPWIDTH//2,DISPHIGHT//2)
        disp.blit(mazething,rect)
        displines(disp,(0,250,0),man.seelines)
        #pygame.draw.line(disp,(255,0,0),man.__disppos__(),man.__disppos__()+80*man.direction,width=2)
        for m in men:
            m.move(data)
            drawpath(disp,path,man.gridp)
            drawman(disp,m)
        pygame.display.update()
        plotter.plot(man.radar)
        #     if event.type==pygame.KEYDOWN:
        #         tasks.manage(grid,event.unicode)
        # tasks.execute()
if __name__ == "__main__":
    main()
