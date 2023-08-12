from ast import Break
from binhex import binhex
from os import system
from pprint import pprint
import random

import pygame
import numpy as np
import math
import time
import copy
import os

DISPWIDTH=1200
DISPHIGHT=850
black=(0,0,0)
white=(255,255,230)
grey=(100,100,100)
green =(0,255,0)
red = (255,0,50)
blue=(5,5,255)
yellow=(255,255,10)
orange=(255,160,5)
offwhite=(220,220,190)
FILENAME='maze_19.mzg'
DIRECTIONS=['north','west','south','east']
GRIDSIZE=(60,50)
TILESIZE=15
gridoffset=(20,20)

class Tile:
    
    def __init__(self,x:int,y:int):
        self.stepped=False
        self.deadend=False
        self.availmoves=[]
        self.trail=[]
        self.distance=0
        self.x=x
        self.y=y
        self.coords=(x,y)
        self.cn,self.cw,self.cs,self.ce=((x,y-1),(x-1,y),(x,y+1),(x+1,y))
        
    def checkwalls(self,wgrid):
        """returns: (N,W,S,E)  
        0: No wall 
        1: wall"""
        n,w,s=(wgrid[self.x,2*self.y],wgrid[self.x,2*self.y+1],wgrid[self.x,2*self.y+2])
        e=wgrid[self.x+1,2*self.y+1]
        self.walls= [n,w,s,e]
    def __repr__(self) -> str:
        return f'T-{self.coords}\n\tstepped:{self.stepped}\n\tdistance:{self.distance}'
    def getneighbours(self,grid):
        self.neighbours:list[Tile]=[grid[self.cn] for _ in range(4)]
        if not self.walls[0] and self.y>0:
            self.neighbours[0]=grid[self.cn]
            self.availmoves.append(0)

        if not self.walls[1] and self.x>0:
            self.neighbours[1]=grid[self.cw]
            self.availmoves.append(1)

        if not self.walls[2] and self.y<GRIDSIZE[1]-1:
            self.neighbours[2]=grid[self.cs]
            self.availmoves.append(2)

        if not self.walls[3] and self.x<GRIDSIZE[0]-1:
            self.neighbours[3]=grid[self.ce]
            self.availmoves.append(3)


    def progress(self, grid):
        
        if self.coords[0]==GRIDSIZE[0]-1 and self.coords[1] == GRIDSIZE[1]-1:
            #print("end of maze")
            return None
        
        nchoices=len(self.availmoves)
        if nchoices==0 :
            #print("going back")
            if len(self.trail)==0:
                #print("no trail")

                return None
            self.deadend=True
            
            return self.neighbours[(self.trail[-1]+2)%4]
        self.stepped=True
        

        #print("availmoves: ",self.availmoves)
        choice = self.availmoves.pop(random.randint(0,nchoices-1))
        nexttile=self.neighbours[choice]
        #print("going",DIRECTIONS[choice],self.walls, self.neighbours)
        #print("current trail: ",self.trail)
        if nexttile.stepped:
            return self
        # if len(self.trail)==0:
        #     nexttile.trail=[choice]
        nexttile.trail=[i for i in self.trail]+[choice]
        #print("next trail: ",nexttile.trail)
        nexttile.availmoves.remove((choice+2)%4)
        return nexttile
    def buildmaze(self,grid,backtrack):
            
            nchoices=len(self.availmoves)
            if nchoices==0 or backtrack:
                if len(self.trail)==0:
                    #print("no trail")
                    return None
                self.deadend=True
                
                return self.neighbours[(self.trail[-1]+2)%4]
            if len(self.trail)>0:

                if self.trail[-1]==0: grid.walls[self.x,2*self.y+2]=0
                if self.trail[-1]==1: grid.walls[self.x+1,2*self.y+1]=0
                if self.trail[-1]==2: grid.walls[self.x,2*self.y]=0
                if self.trail[-1]==3: grid.walls[self.x,2*self.y+1]=0
            self.stepped=True
            #print("availmoves: ",self.availmoves)
            choice = self.availmoves.pop(random.randint(0,nchoices-1))
            nexttile=self.neighbours[choice]
            #print("going",DIRECTIONS[choice],self.walls, self.neighbours)
            #print("current trail: ",self.trail)
            if nexttile.stepped:
                return self
            # if len(self.trail)==0:
            #     nexttile.trail=[choice]
            nexttile.trail=[i for i in self.trail]+[choice]
            #print("next trail: ",nexttile.trail)
            nexttile.availmoves.remove((choice+2)%4)
            return nexttile

class Grid:
    ######______INITIALIZATION______######
    def __init__(self,gridsize:tuple) -> None:
        self.tilesx,self.tilesy=gridsize
        self.wallsx,self.wallsy=(gridsize[0]+1,2*gridsize[1]+1)
        self.tiles=np.array([[Tile(x,y) for y in range(self.tilesy)]for x in range(self.tilesx)],Tile)
        self.walls=np.array([[1 for _ in range(self.wallsy)] for _ in range(self.wallsx)],int)
        self.fillwalls(1)
        self.wallsdisp=None

        # for i in range(0,self.wallsy,2):
        #     self.walls[self.wallsx-1,i]=0
    def fillwalls(self,n):
        print(self.wallsx,self.wallsy)
        for i in range(self.wallsx):
            for j in range(self.wallsy):
                self.walls[i,j]=n
        for i in range(0,self.wallsy,2):
            self.walls[self.wallsx-1,i]=0
    def inittiles(self):
        for row in self.tiles:
            for j in row:
                j.__init__(j.x,j.y)
                j.checkwalls(self.walls)
        for i in self.tiles:
            for tile in i:
                tile.getneighbours(self.tiles)

    def buildwalls(self,mousepos):
        pos=((mousepos[0]-gridoffset[0])/TILESIZE, (mousepos[1]-gridoffset[1])/TILESIZE)
        if pos[0]>0 and pos[0]< self.tilesx-1 and pos[1]>0 and pos[1]<self.tilesy/2:
            if abs(pos[0]-round(pos[0]))<.2:
                self.walls[round(pos[0]),round(pos[1]-.5)*2+1]=0
            if abs(pos[1]-round(pos[1]))<.2:#horiz
                self.walls[round(pos[0]-.5),round(pos[1])*2]=0

    #######______.mzg file______######
    def customgrid(self,name):
        with open("mzg_files/"+name,'r') as f:
            for i,line in enumerate(f):
                for j, chr in enumerate(line[:-1]):
                    self.walls[i,j]=int(chr)

    def clearpaths(self):
        for row in self.tiles:
            for i in row:
                if i.deadend:
                    i.deadend=False
                    i.stepped=False



    def random_maze(self):
        for i in range(self.wallsx):
            for j in range(self.wallsy):
                self.walls[i,j]=random.randint(0,1)
    def savemaze(self, name = None):
        # print(f'{GRIDSIZE[1]} {GRIDSIZE[0]}')
        binary='\n'.join([''.join([str(tile) for tile in line])for line in self.walls])
        # binary=int(binary,base=2)
        # print(hex(binary))
        filenumbermax=0
        #search cwd
        if name is None:
            for subdir, dirs, files in os.walk('./mzg_files'):
                
                for file in files:
                    if file[-4:]=='.mzg':
                        try:
                            if int(file[-6:-4])>filenumbermax:
                                filenumbermax=int(file[-6:-4])
                        except: pass
            filenumbermax+=1
            if filenumbermax<10:
                filenum=f'0{filenumbermax}'
            else: filenum=str(filenumbermax)
            name = f"maze_{filenum}.mzg"
        
        with open("./mzg_files/"+name,'w') as f:
            f.write(binary)
            f.close()
class Solveparams:
    def __init__(self,grid,iterations=10):
        grid.inittiles()
        self.tile=grid.tiles[0,0]
        self.x=0
        self.n=0
        self.backtrack=0
        self.iterations=iterations
    pass


class Tasks:
    iterations=50
    def __init__(self,grid:Grid):
        self.solvestatus=0
        self.solveparams=Solveparams(grid)
        self.makemaze=0
        self.makemazeparams=Solveparams(grid)
    def manage(self,grid:Grid,input):
        if input=="g":
            self.solveparams.__init__(grid)
            self.solvestatus=1
        if input=="m":
            grid.fillwalls(0)
            self.makemazeparams.__init__(grid,1000)
            grid.fillwalls(1)
            self.makemaze=1
        if input=="r":grid.random_maze()
        if input=="s": grid.savemaze()
        if input=="l": grid.customgrid(FILENAME)

    def execute(self,grid):
        if self.solvestatus: 
            self.solve(grid)
        if self.makemaze: 
            self.iterations=1000
            
            self.make(grid)

    def solve(self,grid):
        for _ in range(self.solveparams.iterations):
            if self.solveparams.tile == None:
                grid.clearpaths()
                break

            self.solveparams.tile=self.solveparams.tile.progress(grid)
    def make(self,grid:Grid):
        
        for _ in range(self.makemazeparams.iterations):
            if self.makemazeparams.tile is None: 
                self.solveparams.__init__(grid)
                self.makemaze=0

                break
            self.makemazeparams.tile=self.makemazeparams.tile.buildmaze(grid,self.makemazeparams.backtrack)
            if random.randint(0,50)==0 and self.makemazeparams.backtrack==0:
                self.makemazeparams.backtrack=1
                self.makemazeparams.x=0
            self.makemazeparams.x+=1
            self.makemazeparams.x%=10
            if self.makemazeparams.x==0:
                self.makemazeparams.backtrack=0
            grid.wallsdisp=None

        


        
        



def display(disp,grid:Grid):
    disp.fill(offwhite)
    
    for i in range(grid.tilesx):
        for j in range(grid.tilesy):
            if grid.tiles[i,j].stepped:
                color=green
                if grid.tiles[i,j].deadend: color=red
                pygame.draw.rect(disp, color, (gridoffset[0]+i*TILESIZE,gridoffset[1]+j*TILESIZE,TILESIZE,TILESIZE), width=0)
                #pygame.draw.rect(disp, color, (1+gridoffset[0]+i*TILESIZE,1+gridoffset[1]+j*TILESIZE,TILESIZE-1,TILESIZE-1), width=0)
    pygame.draw.rect(disp, blue, (gridoffset[0]+(grid.tilesx-1)*TILESIZE,gridoffset[1]+(grid.tilesy-1)*TILESIZE,TILESIZE,TILESIZE), width=0)
    #pygame.draw.rect(disp, blue, (1+gridoffset[0]+(grid.tilesx-1)*TILESIZE,1+gridoffset[1]+(grid.tilesy-1)*TILESIZE,TILESIZE-1,TILESIZE-1), width=0)
    if grid.wallsdisp is None or True:
        for i in range(grid.wallsx):
            xpos=TILESIZE*i
            #horixontal
            for j in range(0,grid.wallsy,2):
                if grid.walls[i,j]:
                    if grid.walls[i,j]==2: color=green
                    else: color=black
                    pygame.draw.line(disp, color,(xpos+gridoffset[0],gridoffset[1]+TILESIZE*(j//2)),(gridoffset[0]+xpos+TILESIZE,gridoffset[1]+TILESIZE*(j//2)), width=2)
            for j in range(1,grid.wallsy,2):
                if grid.walls[i,j]:
                    if grid.walls[i,j]==2: color=green
                    else: color=black
                    pygame.draw.line(disp, color,(xpos+gridoffset[0],gridoffset[1]+TILESIZE*(j//2)),(gridoffset[0]+xpos,gridoffset[1]+TILESIZE*(j//2+1)), width=2)
        grid.wallsdisp=disp.copy()
    else: disp.blit(grid.wallsdisp,(0,0))


    pygame.display.update()


    
def main():
    pygame.init()
    disp=pygame.display.set_mode((DISPWIDTH,DISPHIGHT))
    pygame.display.set_caption('MAZE GRID!!!!!')
    #pygame.mouse.set_visible(False)
    clock= pygame.time.Clock()
    pmp=mousepos=(0,0)
    mousebutton=0
    begintime=time.time()
    grid=Grid(GRIDSIZE)
    tasks=Tasks(grid)
    
    #print(wgrid)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.scancode==41):
                pygame.quit()
                quit()
            elif event.type==pygame.MOUSEMOTION: 
                mousepos=event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousebutton=1
            elif event.type == pygame.MOUSEBUTTONUP:
                mousebutton=0
            if event.type==pygame.KEYDOWN:
                tasks.manage(grid,event.unicode)
        tasks.execute(grid)
        if mousebutton:
            grid.buildwalls(mousepos)
        display(disp,grid)
        

if __name__ == "__main__":
    main()
