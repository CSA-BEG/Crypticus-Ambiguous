import pygame, sys
from pygame.locals import *
import glob, os
import time
import random
'''-----------------------------------------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------'''
#Crypticus Ambiguous v. 0.7
#not necessarily the best, but complete
global currentLocation
currentLocation=os.path.dirname(os.path.realpath(__file__))

WHITE = (255, 255, 255)
GRAY = (211,211,211)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)

class playercharacter():
    def __init__(self):#sets up inv and health and such
        global health
        global inv
        global atk
        global armor
        atk=[2,'']
        armor=[0,'']
        health=20
        inv={"key":0}
    def getitem(self):#when you open a chest or kill an enemy it will give you random drops
        itemlist=[]
        os.chdir(currentLocation+"/items")
        for file in glob.glob("*.txt"):
            itemlist.append(file)
        rand=random.randint(1,len(itemlist))
        rand-=1
        itemget=str(itemlist[rand])
        file=open(itemget,'r')
        line=int(file.readline())
        if line==1:
            line=file.readline()
            itemget=itemget.replace(".txt",'')
            inv[itemget]=[1,int(line)]
            print(inv)
        elif line==2:
            line=file.readline()
            itemget=itemget.replace(".txt",'')
            inv[itemget]=[2,int(line)]
            print(inv)
        elif line==3:
            line=file.readline()
            itemget=itemget.replace(".txt",'')
            inv[itemget]=[3,int(line)]
            print(inv)
        os.chdir(currentLocation)
    def attack(self):#animations are going to be a hassle
        global enemyhp
        global atk
        slash = pygame.mixer.Sound('attack.wav')
        slash.play()
        enemyhp-=atk[0]
    def inventory(self):#just prints the inv for now, will have a menu in final product
        global health
        global way
        global atk
        global armor
        global text
        global m
        strinv=str(inv)
        strinv=strinv.replace("'","")
        tempinv=removekey(inv,'key')
        temp2=list(tempinv.keys())
        cursor=1
        newtempdict={}
        x=0
        for i in temp2:
            x+=1
            newtempdict[x]=i
        while m==True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
                    if cursor<=1:
                        pass
                    else:
                        cursor-=1
                elif event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                    if cursor>=x:
                        pass
                    else:
                        cursor+=1
                elif event.type == pygame.KEYDOWN and event.key == K_z:
                    try:
                        thing=inv[newtempdict[cursor]]
                        if thing[0]==1:
                            health+=thing[1]
                            del inv[newtempdict[cursor]]
                            player.inventory()
                        if thing[0]==2:
                            armor=[thing[1],str(newtempdict[cursor])]
                            del inv[newtempdict[cursor]]
                            player.inventory()
                        if thing[0]==3:
                            atk=[thing[1],str(newtempdict[cursor])]
                            del inv[newtempdict[cursor]]
                            player.inventory()
                    except:
                        text2 = text.render("Inventory empty", 6, WHITE)
                elif event.type == pygame.KEYDOWN and event.key == K_x:
                    m=False
            try:
                text2 = text.render(str(newtempdict[cursor]), 6, WHITE)
            except:
                text2 = text.render("Inventory empty", 6, WHITE)
            text3 = text.render("Inventory", 6, WHITE)
            text4 = text.render(armor[1], 6, WHITE)
            text5 = text.render(atk[1], 6, WHITE)
            screen.blit(text2, (20, 240))
            screen.blit(text3, (200, 10))
            screen.blit(text4, (20, 50))
            screen.blit(text5, (20, 80))
            pygame.display.flip()
            screen.fill(BLACK)
            clock.tick(30)
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

class mapstuffs():#makes a dictionary of coordinates and tiles based on map file
    def __init__(self):
        global user
        global tiles
        file=open("map.txt",'r')
        line=file.readline()
        tiles={}
        temp=[]
        x=0
        y=0
        user=[]
        while line:
            line=line.strip()
            line=line.split(' ')
            temp.append(line)
            line=file.readline()
        for f in temp:
            y+=1
            while f:
                x+=1
                tile=f[0]#haha, get it, F-Zero, haha
                del f[0]
                if tile=='P':
                    user.append(x)
                    user.append(y)
                    current=(x,y)
                    tiles[current]=tile
                else:
                    current=(x,y)
                    tiles[current]=tile
            x=0
        file.close()
    def move(self,where):#moves player and checks what each tile does
        global direction
        temp=user
        if where == pygame.K_RIGHT:#turning left and right
            if direction=='n':
                direction='e'
            elif direction=='e':
                direction='s'
            elif direction=='s':
                direction='w'
            elif direction=='w':
                direction='n'
        if where == pygame.K_LEFT:#for some weird reason, when i first put in this code, you could only turn right, despite copy paste
            if direction=='n':
                direction='w'
            elif direction=='w':
                direction='s'
            elif direction=='s':
                direction='e'
            elif direction=='e':
                direction='n'
        if where == pygame.K_DOWN:#moving forward and backward
            tiles[tuple(temp)]='-'
            if direction=='n':
                temp[1]+=1
                if tiles[tuple(temp)]=='-':#all the actions from gridspaces are handled here
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[1]-=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[1]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[1]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'
            if direction=='e':
                temp[0]-=1
                if tiles[tuple(temp)]=='-':
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[0]+=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[0]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[0]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'
            if direction=='s':
                temp[1]-=1
                if tiles[tuple(temp)]=='-':
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[1]+=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[1]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[1]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'
            if direction=='w':
                temp[0]+=1
                if tiles[tuple(temp)]=='-':
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[0]-=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[0]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[0]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'
        if where == pygame.K_UP:#man i love copy & paste
            tiles[tuple(temp)]='-'
            if direction=='n':
                temp[1]-=1
                if tiles[tuple(temp)]=='-':
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[1]+=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[1]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[1]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'
            if direction=='e':
                temp[0]+=1
                if tiles[tuple(temp)]=='-':
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[0]-=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[0]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[0]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'
            if direction=='s':
                temp[1]+=1
                if tiles[tuple(temp)]=='-':
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[1]-=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[1]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[1]-=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'
            if direction=='w':
                temp[0]-=1
                if tiles[tuple(temp)]=='-':
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'X':
                    temp[0]+=1
                    tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'E':
                    fight()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'C':
                    player.getitem()
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)] == 'D':
                    if inv['key']>=1:
                        inv['key']-=1
                        tiles[tuple(temp)] = 'P'
                    else:
                        temp[0]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'K':
                    inv['key']+=1
                    tiles[tuple(temp)] = 'P'
                elif tiles[tuple(temp)]=='L':
                    if inv['greatkey']>=1:
                        inv['greatkey']-=1
                        win()
                    else:
                        temp[0]+=1
                        tiles[tuple(temp)]='P'
                elif tiles[tuple(temp)] == 'G':
                    inv['greatkey']=1
                    tiles[tuple(temp)] = 'P'

class enemyclass():
    def __init__(self):# generates random enemy from a list of possible enemies
        global enemyhp
        global enemyatk
        global enemyspeed
        global enemyimg
        enemieslist=[]
        os.chdir(currentLocation+"/enemies")
        for file in glob.glob("*.txt"):
            enemieslist.append(file)
        rand=random.randint(1,len(enemieslist))
        rand-=1
        enemy=str(enemieslist[rand])
        enemyimg=enemy
        enemyimg=enemyimg.replace('.txt','.png')
        file=open(enemy,'r')
        line=file.readline()
        line=line.strip()
        enemyhp=int(line)
        line=file.readline()
        line=line.strip()
        enemyatk=int(line)
        line=file.readline()
        line=line.strip()
        enemyspeed=int(line)
        file.close()
        enemy=enemy.replace(".txt",'')
        os.chdir(currentLocation)
    def attack(self):#NYA-HA-HA--
        global health
        global armor
        slash = pygame.mixer.Sound('enemyatk.wav')
        slash.play()
        health-=(enemyatk-armor[0])

def fight():
    global player
    global way
    global enemyhp
    global enemyimg
    global text
    global health
    pygame.mixer.music.load('battle.wav')
    pygame.mixer.music.play(-1, 0.0)
    shield = pygame.mixer.Sound('shield.wav')
    x=0
    y=0
    eatk=pygame.image.load('eatk.png')
    playerattack=pygame.image.load('bam.png')
    defendo=pygame.image.load('sheild.png')#yes i am aware shield is spelled wrong
    enemy = enemyclass()
    os.chdir(currentLocation+"/enemies")
    enemypic=pygame.image.load(enemyimg)
    os.chdir(currentLocation)
    while True:#you can attack and defend, the enemy can only attack, however you can only attack once every second
        screen.blit(enemypic, (0, 0))
        if health<=0:
            pygame.mixer.music.stop()
            break
        if enemyhp<=0:
            pygame.mixer.music.stop()
            player.getitem()
            break
        x+=1
        y+=1
        if x%enemyspeed==0:
            screen.blit(eatk, (0, 0))
        if x % enemyspeed == 0 and defend==True:
            shield.play()
        if x%enemyspeed==0 and defend==False:#enemy attacks ever so often
            enemy.attack()
        keys = pygame.key.get_pressed()#checking pressed keys
        if keys[pygame.K_x]:
            defend=True
        else:
            defend=False
        if defend==True:
            screen.blit(defendo, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == K_x:
                defend=True
            elif event.type == pygame.KEYDOWN and event.key==K_z:
                if y<30:
                    pass
                elif defend==True:
                    pass
                else:
                    player.attack()
                    screen.blit(playerattack, (0, 0))
                    y=0

        text2 = text.render(str(health) + " HP", 6, WHITE)
        screen.blit(text2, (0, 0))
        text3 = text.render(str(enemyhp), 6, WHITE)
        screen.blit(text3, (550, 0))
        pygame.display.flip()
        screen.fill(BLACK)
        clock.tick(30)

def win():
    pygame.mixer.music.load('victory.wav')
    pygame.mixer.music.play(-1, 0.0)
    leave=pygame.image.load('done.png')
    while True:
        screen.blit(leave,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        screen.fill(WHITE)
        clock.tick(30)

pygame.init()
pygame.display.set_caption("Crypticus Ambiguous")
clock = pygame.time.Clock()
window_width = 600
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))

map=mapstuffs()
player=playercharacter()

r1=pygame.image.load('r1.png')
r2=pygame.image.load('r2.png')
l1=pygame.image.load('l1.png')
l2=pygame.image.load('l2.png')
hall=pygame.image.load('hall.png')
wall=pygame.image.load('wall.png')
worldkey=pygame.image.load('key.png')
greatkey=pygame.image.load('greatkey.png')
door=pygame.image.load('door.png')
chest=pygame.image.load('chest2.png')
genericenemything=pygame.image.load('enemy.png')
greatdoor=pygame.image.load('greatdoor.png')

direction='n'
text=pygame.font.Font(None, 60)

step=pygame.mixer.Sound('step.wav')
pygame.mixer.music.load('ambient sound.wav')
pygame.mixer.music.play(-1, 0.0)
while True:
    global direction
    global tiles
    global user
    if health<=0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            text5=text.render("GAME OVER",6,WHITE)
            screen.blit(text5,(170,175))
            text6=text.render("Esc to quit",6,WHITE)
            screen.blit(text6,(193,220))
            pygame.display.flip()
            screen.fill(BLACK)
            clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key==K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key==K_i:
            m = True
            player.inventory()
        elif event.type == pygame.KEYDOWN:
            step.play()
            map.move(event.key)

    if direction=='n':#and thus begins the blit tree of death
        r01=[user[0]+1,user[1]]
        r02=[user[0]+1,user[1]-1]
        l01=[user[0]-1,user[1]]
        l02=[user[0]-1,user[1]-1]
        up=[user[0],user[1]-1]
        if tiles[tuple(r01)]!='X':
            screen.blit(r1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(r02)]!='X':
            screen.blit(r2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l01)]!='X':
            screen.blit(l1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l02)]!='X':
            screen.blit(l2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(up)]=='X':
            screen.blit(wall,(0,0))
        elif tiles[tuple(up)]=='E':
            screen.blit(genericenemything,(0,0))
        elif tiles[tuple(up)]=='C':
            screen.blit(chest, (0, 0))
        elif tiles[tuple(up)]=='D':
            screen.blit(door, (0, 0))
        elif tiles[tuple(up)]=='K':
            screen.blit(worldkey, (0, 0))
        elif tiles[tuple(up)]=='G':
            screen.blit(greatkey, (0, 0))
        elif tiles[tuple(up)]=='L':
            screen.blit(greatdoor, (0, 0))
        else:
            screen.blit(hall,(0,0))
    if direction=='s':
        r01=[user[0]-1,user[1]]
        r02=[user[0]-1,user[1]+1]
        l01=[user[0]+1,user[1]]
        l02=[user[0]+1,user[1]+1]
        up=[user[0],user[1]+1]
        if tiles[tuple(r01)]!='X':
            screen.blit(r1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(r02)]!='X':
            screen.blit(r2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l01)]!='X':
            screen.blit(l1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l02)]!='X':
            screen.blit(l2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(up)]=='X':
            screen.blit(wall,(0,0))
        elif tiles[tuple(up)]=='E':
            screen.blit(genericenemything,(0,0))
        elif tiles[tuple(up)]=='C':
            screen.blit(chest, (0, 0))
        elif tiles[tuple(up)]=='D':
            screen.blit(door, (0, 0))
        elif tiles[tuple(up)]=='K':
            screen.blit(worldkey, (0, 0))
        elif tiles[tuple(up)]=='G':
            screen.blit(greatkey, (0, 0))
        elif tiles[tuple(up)]=='L':
            screen.blit(greatdoor, (0, 0))
        else:
            screen.blit(hall,(0,0))
    if direction=='e':
        r01=[user[0],user[1]+1]
        r02=[user[0]+1,user[1]+1]
        l01=[user[0],user[1]-1]
        l02=[user[0]+1,user[1]-1]
        up=[user[0]+1,user[1]]
        if tiles[tuple(r01)]!='X':
            screen.blit(r1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(r02)]!='X':
            screen.blit(r2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l01)]!='X':
            screen.blit(l1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l02)]!='X':
            screen.blit(l2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(up)]=='X':
            screen.blit(wall,(0,0))
        elif tiles[tuple(up)]=='E':
            screen.blit(genericenemything,(0,0))
        elif tiles[tuple(up)]=='C':
            screen.blit(chest, (0, 0))
        elif tiles[tuple(up)]=='D':
            screen.blit(door, (0, 0))
        elif tiles[tuple(up)]=='K':
            screen.blit(worldkey, (0, 0))
        elif tiles[tuple(up)]=='G':
            screen.blit(greatkey, (0, 0))
        elif tiles[tuple(up)]=='L':
            screen.blit(greatdoor, (0, 0))
        else:
            screen.blit(hall,(0,0))
    if direction=='w':
        r01=[user[0],user[1]-1]
        r02=[user[0]-1,user[1]-1]
        l01=[user[0],user[1]+1]
        l02=[user[0]-1,user[1]+1]
        up=[user[0]-1,user[1]]
        if tiles[tuple(r01)]!='X':
            screen.blit(r1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(r02)]!='X':
            screen.blit(r2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l01)]!='X':
            screen.blit(l1,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(l02)]!='X':
            screen.blit(l2,(0,0))
        else:
            screen.blit(hall,(0,0))
        if tiles[tuple(up)]=='X':
            screen.blit(wall,(0,0))
        elif tiles[tuple(up)]=='E':
            screen.blit(genericenemything,(0,0))
        elif tiles[tuple(up)]=='C':
            screen.blit(chest, (0, 0))
        elif tiles[tuple(up)]=='D':
            screen.blit(door, (0, 0))
        elif tiles[tuple(up)]=='K':
            screen.blit(worldkey, (0, 0))
        elif tiles[tuple(up)]=='G':
            screen.blit(greatkey, (0, 0))
        elif tiles[tuple(up)]=='L':
            screen.blit(greatdoor, (0, 0))
        else:
            screen.blit(hall,(0,0))

    text2=text.render(str(health)+" HP",6,BLACK)
    screen.blit(text2,(0,0))
    pygame.display.flip()
    screen.fill(WHITE)
    clock.tick(30)