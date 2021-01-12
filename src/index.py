from pyglet.gl import *;from pyglet.window import key;from math import sin, cos, pi, sqrt;from PIL import Image, ImageDraw;import random;import os



class Block:
    def __init__(self,name,pos,map_):
        if name=='wall':self.w=self.s=self.e=self.n=self.u=self.d=self.get_tex(f'img_perspective/{name}.png',wall=True,name=name)
        self.name=name
        self.tex_coords=('t2f',(0,0,1,0,1,1,0,1))
        self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
        self.map_=map_
        self.map_[tuple(self.pos)]=self
        self.update()
    def draw(self):self.batch.draw()
    def get_tex(self,file,wall=False,name=None):
        if wall:
            img=Image.open(f'img_perspective/{name}.png');imgd=ImageDraw.Draw(img)
            pixels=[];[[pixels.append((x,y))for x in range(64)]for y in range(64)];random.shuffle(pixels)
            dark=random.randint(154,214);imgd.point(pixels[:dark],(163,154,114));imgd.point(pixels[dark+1:dark+1+random.randint(154,214)],(176,168,135))
            img.save(f'img_perspective/{name}_tmp.png')
        if wall:tex=pyglet.image.load(f'img_perspective/{name}_tmp.png').texture;os.remove(f'img_perspective/{name}_tmp.png')
        else:tex=pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)
    def update(self,call=True,map_=None):
        map_=map_ if map_ else self.map_
        l,l2=[(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)],[False]*6
        for crds in l:
            x2,y2,z2=self.pos[0]+crds[0],self.pos[1]+crds[1],self.pos[2]+crds[2]
            if (x2,y2,z2) in list(map_.keys()):
                if map_[(x2,y2,z2)].name=='air':l2[l.index(crds)]=True
                elif call:map_[(x2,y2,z2)].update(False,map_)
            else:l2[l.index(crds)]=True
        x,y,z,X,Y,Z,n=self.pos[0],self.pos[1],self.pos[2],self.pos[0]+1,self.pos[1]+1,self.pos[2]+1,1/16
        self.batch=pyglet.graphics.Batch()
        if l2[0]:self.batch.add(4,GL_QUADS,self.w,('v3f',(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tex_coords)
        if l2[1]:self.batch.add(4,GL_QUADS,self.s,('v3f',(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tex_coords)
        if l2[2]:self.batch.add(4,GL_QUADS,self.d,('v3f',(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tex_coords)
        if l2[3]:self.batch.add(4,GL_QUADS,self.u,('v3f',(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tex_coords)
        if l2[4]:self.batch.add(4,GL_QUADS,self.e,('v3f',(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tex_coords)
        if l2[5]:self.batch.add(4,GL_QUADS,self.n,('v3f',(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tex_coords)
class Log:
    def __init__(self,pos,type_,lmap,p2=None):
        self.edge_top=self.get_tex(f'img_perspective/log_top.png')
        if type_!=[-1]:self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
        else:self.pos=[float(pos[0]),float(pos[1]),float(pos[2])]
        self.type=[False]*13
        for ti in type_:self.type[int(ti)]=True
        self.tex_coords=('t2f',(0,0,1,0,1,1,0,1))
        self.pos2=p2
        self.lmap=lmap
        if type_!=[-1]:self.lmap[(int(pos[0]),int(pos[1]),int(pos[2]))]=self
    def draw(self):self.batch.draw()
    def get_tex(self,file,wall=False,name=None):
        tex=pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)
    def update(self,map_):
        t,x,y,z,X,Y,Z,x_,y_,z_,n,lm=self.type,self.pos[0],self.pos[1],self.pos[2],self.pos[0]+1,self.pos[1]+1,self.pos[2]+1,self.pos[0]-1,self.pos[1]-1,self.pos[2]-1,1/16,self.lmap;self.batch=pyglet.graphics.Batch()
        def rand_log_tex():return self.get_tex(f'img_perspective/log{random.randint(1,2)}.png')
        def checkL(pos,type_,invert=False):return invert if pos not in list(lm.keys()) else not(lm[pos].type[type_])==invert
        def checkB(pos):return pos in list(map_.keys())
        if t[0]:
            if checkL((x,y_,z),0,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,y,z+n,x-n,y,z+n,x-n,y,z-n,x+n,y,z-n)),self.tex_coords)
            if checkL((x,Y,z),0,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,Y,z+n,x-n,Y,z+n,x-n,Y,z-n,x+n,Y,z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x_,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y,z+n,x-n,y,z+n,x-n,Y,z+n,x+n,Y,z+n)),self.tex_coords)
            if not(checkB((x_,y,z)) and checkB((x_,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,y,z-n,x-n,y,z+n,x-n,Y,z+n,x-n,Y,z-n)),self.tex_coords)
            if not(checkB((x,y,z_)) and checkB((x_,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y,z-n,x-n,y,z-n,x-n,Y,z-n,x+n,Y,z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y,z-n,x+n,y,z+n,x+n,Y,z+n,x+n,Y,z-n)),self.tex_coords)
        if t[1]:
            if checkL((x,y_,z),1,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X+n,y,z+n,X-n,y,z+n,X-n,y,z-n,X+n,y,z-n)),self.tex_coords)
            if checkL((x,Y,z),1,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X+n,Y,z+n,X-n,Y,z+n,X-n,Y,z-n,X+n,Y,z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((X,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,y,z+n,X-n,y,z+n,X-n,Y,z+n,X+n,Y,z+n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,y,z-n,X-n,y,z+n,X-n,Y,z+n,X-n,Y,z-n)),self.tex_coords)
            if not(checkB((x,y,z_)) and checkB((X,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,y,z-n,X-n,y,z-n,X-n,Y,z-n,X+n,Y,z-n)),self.tex_coords)
            if not(checkB((X,y,z)) and checkB((X,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,y,z-n,X+n,y,z+n,X+n,Y,z+n,X+n,Y,z-n)),self.tex_coords)
        if t[2]:
            if checkL((x,y_,z),2,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X+n,y,Z+n,X-n,y,Z+n,X-n,y,Z-n,X+n,y,Z-n)),self.tex_coords)
            if checkL((x,Y,z),2,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X+n,Y,Z+n,X-n,Y,Z+n,X-n,Y,Z-n,X+n,Y,Z-n)),self.tex_coords)
            if not(checkB((x,y,Z)) and checkB((X,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,y,Z+n,X-n,y,Z+n,X-n,Y,Z+n,X+n,Y,Z+n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,y,Z-n,X-n,y,Z+n,X-n,Y,Z+n,X-n,Y,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((X,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,y,Z-n,X-n,y,Z-n,X-n,Y,Z-n,X+n,Y,Z-n)),self.tex_coords)
            if not(checkB((X,y,z)) and checkB((X,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,y,Z-n,X+n,y,Z+n,X+n,Y,Z+n,X+n,Y,Z-n)),self.tex_coords)
        if t[3]:
            if checkL((x,y_,z),3,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,y,Z+n,x-n,y,Z+n,x-n,y,Z-n,x+n,y,Z-n)),self.tex_coords)
            if checkL((x,Y,z),3,True):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,Y,Z+n,x-n,Y,Z+n,x-n,Y,Z-n,x+n,Y,Z-n)),self.tex_coords)
            if not(checkB((x,y,Z)) and checkB((x_,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y,Z+n,x-n,y,Z+n,x-n,Y,Z+n,x+n,Y,Z+n)),self.tex_coords)
            if not(checkB((x_,y,z)) and checkB((x_,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,y,Z-n,x-n,y,Z+n,x-n,Y,Z+n,x-n,Y,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x_,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y,Z-n,x-n,y,Z-n,x-n,Y,Z-n,x+n,Y,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y,Z-n,x+n,y,Z+n,x+n,Y,Z+n,x+n,Y,Z-n)),self.tex_coords)
        if t[4]:
            if not(checkL((x,y,z),0) and checkL((x,y_,z),0)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,y-n,z-n,x+n,y+n,z-n,x+n,y+n,z+n,x+n,y-n,z+n)),self.tex_coords)
            if not(checkL((x,y,z),1) and checkL((x,y_,z),1)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,y-n,z-n,X-n,y+n,z-n,X-n,y+n,z+n,X-n,y-n,z+n)),self.tex_coords)
            if not(checkB((x,y,z_)) and checkB((x,y_,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y-n,z-n,x+n,y+n,z-n,X-n,y+n,z-n,X-n,y-n,z-n)),self.tex_coords)
            if not(checkB((x,y_,z)) and checkB((x,y_,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y-n,z-n,x+n,y-n,z+n,X-n,y-n,z+n,X-n,y-n,z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y+n,z-n,x+n,y+n,z+n,X-n,y+n,z+n,X-n,y+n,z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y-n,z+n,x+n,y+n,z+n,X-n,y+n,z+n,X-n,y-n,z+n)),self.tex_coords)
        if t[5]:
            if not(checkL((x,y,z),1) and checkL((x,y_,z),1)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,y-n,z+n,X-n,y+n,z+n,X+n,y+n,z+n,X+n,y-n,z+n)),self.tex_coords)
            if not(checkL((x,y,z),2) and checkL((x,y_,z),2)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,y-n,Z-n,X-n,y+n,Z-n,X+n,y+n,Z-n,X+n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,y-n,z+n,X-n,y+n,z+n,X-n,y+n,Z-n,X-n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y_,z)) and checkB((X,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,y-n,z+n,X+n,y-n,z+n,X+n,y-n,Z-n,X-n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((X,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,y+n,z+n,X+n,y+n,z+n,X+n,y+n,Z-n,X-n,y+n,Z-n)),self.tex_coords)
            if not(checkB((X,y,z)) and checkB((X,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,y-n,z+n,X+n,y+n,z+n,X+n,y+n,Z-n,X+n,y-n,Z-n)),self.tex_coords)
        if t[6]:
            if not(checkL((x,y,z),2) and checkL((x,y_,z),2)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,y-n,Z-n,x+n,y+n,Z-n,x+n,y+n,Z+n,x+n,y-n,Z+n)),self.tex_coords)
            if not(checkL((x,y,z),3) and checkL((x,y_,z),3)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,y-n,Z-n,X-n,y+n,Z-n,X-n,y+n,Z+n,X-n,y-n,Z+n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y-n,Z-n,x+n,y+n,Z-n,X-n,y+n,Z-n,X-n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y-n,Z-n,x+n,y-n,Z+n,X-n,y-n,Z+n,X-n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y_,z)) and checkB((x,y_,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y+n,Z-n,x+n,y+n,Z+n,X-n,y+n,Z+n,X-n,y+n,Z-n)),self.tex_coords)
            if not(checkB((x,y,Z)) and checkB((x,y_,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y-n,Z+n,x+n,y+n,Z+n,X-n,y+n,Z+n,X-n,y-n,Z+n)),self.tex_coords)
        if t[7]:
            if not(checkL((x,y,z),3) and checkL((x,y_,z),3)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x-n,y-n,z+n,x-n,y+n,z+n,x+n,y+n,z+n,x+n,y-n,z+n)),self.tex_coords)
            if not(checkL((x,y,z),0) and checkL((x,y_,z),0)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x-n,y-n,Z-n,x-n,y+n,Z-n,x+n,y+n,Z-n,x+n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x_,y,z)) and checkB((x_,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,y-n,z+n,x-n,y+n,z+n,x-n,y+n,Z-n,x-n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y_,z)) and checkB((x_,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,y-n,z+n,x+n,y-n,z+n,x+n,y-n,Z-n,x-n,y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x_,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,y+n,z+n,x+n,y+n,z+n,x+n,y+n,Z-n,x-n,y+n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y_,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,y-n,z+n,x+n,y+n,z+n,x+n,y+n,Z-n,x+n,y-n,Z-n)),self.tex_coords)
        if t[8]:
            if not(checkL((x,y,z),0) and checkL((x,Y,z),0)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,Y+n,z-n,x+n,Y-n,z-n,x+n,Y-n,z+n,x+n,Y+n,z+n)),self.tex_coords)
            if not(checkL((x,y,z),1) and checkL((x,Y,z),1)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,Y+n,z-n,X-n,Y-n,z-n,X-n,Y-n,z+n,X-n,Y+n,z+n)),self.tex_coords)
            if not(checkB((x,y,z_)) and checkB((x,Y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y-n,z-n,x+n,Y+n,z-n,X-n,Y+n,z-n,X-n,Y-n,z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y-n,z-n,x+n,Y-n,z+n,X-n,Y-n,z+n,X-n,Y-n,z-n)),self.tex_coords)
            if not(checkB((x,Y,z)) and checkB((x,Y,z_))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y+n,z-n,x+n,Y+n,z+n,X-n,Y+n,z+n,X-n,Y+n,z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y-n,z+n,x+n,Y+n,z+n,X-n,Y+n,z+n,X-n,Y-n,z+n)),self.tex_coords)
        if t[9]:
            if not(checkL((x,y,z),1) and checkL((x,Y,z),1)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,Y+n,z+n,X-n,Y-n,z+n,X+n,Y-n,z+n,X+n,Y+n,z+n)),self.tex_coords)
            if not(checkL((x,y,z),2) and checkL((x,Y,z),2)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,Y+n,Z-n,X-n,Y-n,Z-n,X+n,Y-n,Z-n,X+n,Y+n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,Y-n,z+n,X-n,Y+n,z+n,X-n,Y+n,Z-n,X-n,Y-n,Z-n)),self.tex_coords)
            if not(checkB((x,Y,z)) and checkB((X,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,Y-n,z+n,X+n,Y-n,z+n,X+n,Y-n,Z-n,X-n,Y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((X,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X-n,Y+n,z+n,X+n,Y+n,z+n,X+n,Y+n,Z-n,X-n,Y+n,Z-n)),self.tex_coords)
            if not(checkB((X,y,z)) and checkB((X,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(X+n,Y-n,z+n,X+n,Y+n,z+n,X+n,Y+n,Z-n,X+n,Y-n,Z-n)),self.tex_coords)
        if t[10]:
            if not(checkL((x,y,z),2) and checkL((x,Y,z),2)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x+n,Y+n,Z-n,x+n,Y-n,Z-n,x+n,Y-n,Z+n,x+n,Y+n,Z+n)),self.tex_coords)
            if not(checkL((x,y,z),3) and checkL((x,Y,z),3)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(X-n,Y+n,Z-n,X-n,Y-n,Z-n,X-n,Y-n,Z+n,X-n,Y+n,Z+n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y-n,Z-n,x+n,Y+n,Z-n,X-n,Y+n,Z-n,X-n,Y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y-n,Z-n,x+n,Y-n,Z+n,X-n,Y-n,Z+n,X-n,Y-n,Z-n)),self.tex_coords)
            if not(checkB((x,Y,z)) and checkB((x,Y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y+n,Z-n,x+n,Y+n,Z+n,X-n,Y+n,Z+n,X-n,Y+n,Z-n)),self.tex_coords)
            if not(checkB((x,y,Z)) and checkB((x,Y,Z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y-n,Z+n,x+n,Y+n,Z+n,X-n,Y+n,Z+n,X-n,Y-n,Z+n)),self.tex_coords)
        if t[11]:
            if not(checkL((x,y,z),3) and checkL((x,Y,z),3)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x-n,Y+n,z+n,x-n,Y-n,z+n,x+n,Y-n,z+n,x+n,Y+n,z+n)),self.tex_coords)
            if not(checkL((x,y,z),0) and checkL((x,Y,z),0)):self.batch.add(4,GL_QUADS,self.edge_top,('v3f',(x-n,Y+n,Z-n,x-n,Y-n,Z-n,x+n,Y-n,Z-n,x+n,Y+n,Z-n)),self.tex_coords)
            if not(checkB((x_,y,z)) and checkB((x_,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,Y-n,z+n,x-n,Y+n,z+n,x-n,Y+n,Z-n,x-n,Y-n,Z-n)),self.tex_coords)
            if not(checkB((x,Y,z)) and checkB((x_,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,Y-n,z+n,x+n,Y-n,z+n,x+n,Y-n,Z-n,x-n,Y-n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x_,y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x-n,Y+n,z+n,x+n,Y+n,z+n,x+n,Y+n,Z-n,x-n,Y+n,Z-n)),self.tex_coords)
            if not(checkB((x,y,z)) and checkB((x,Y,z))):self.batch.add(4,GL_QUADS,rand_log_tex(),('v3f',(x+n,Y-n,z+n,x+n,Y+n,z+n,x+n,Y+n,Z-n,x+n,Y-n,Z-n)),self.tex_coords)
        if t[12]:
            self.batch.add(2,GL_LINES,None,('v2f',(x,y,z,*self.pos2)))
class Camera:
    def __init__(self,pos=(0,0,0),rot=(0,0)):self.pos,self.rot=list(pos),list(rot)
    def check_colission_box(self,pos):
        return True
    def mouse_motion(self,dx,dy):
    	dx/=8
    	dy/=8
    	self.rot[0]+=dy
    	self.rot[1]-=dx
    	self.rot[0]=90 if self.rot[0]>90 else self.rot[0]
    	self.rot[0]=-90 if self.rot[0]<-90 else self.rot[0]
    def update(self,dt,keys):
    	dx,dz=dt*5*sin(-self.rot[1]/180*pi),dt*5*cos(-self.rot[1]/180*pi)
    	self.pos=[self.pos[0]+dx,self.pos[1],self.pos[2]-dz] if keys[key.W] and self.check_colission_box([self.pos[0]+dx,self.pos[1],self.pos[2]-dz]) else self.pos
    	self.pos=[self.pos[0]-dx,self.pos[1],self.pos[2]+dz] if keys[key.S] and self.check_colission_box([self.pos[0]-dx,self.pos[1],self.pos[2]+dz]) else self.pos
    	self.pos=[self.pos[0]-dz,self.pos[1],self.pos[2]-dx] if keys[key.A] and self.check_colission_box([self.pos[0]-dz,self.pos[1],self.pos[2]-dx]) else self.pos
    	self.pos=[self.pos[0]+dz,self.pos[1],self.pos[2]+dx] if keys[key.D] and self.check_colission_box([self.pos[0]+dz,self.pos[1],self.pos[2]+dx]) else self.pos
    	self.pos=[self.pos[0],self.pos[1]+dt*5,self.pos[2]] if keys[key.SPACE] and self.check_colission_box([self.pos[0],self.pos[1]+dt*5,self.pos[2]]) else self.pos
    	self.pos=[self.pos[0],self.pos[1]-dt*5,self.pos[2]] if keys[key.LSHIFT] and self.check_colission_box([self.pos[0],self.pos[1]-dt*5,self.pos[2]]) else self.pos
class Main(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        try:
            super().__init__(width=1366,height=768,caption='Perspective',resizable=False,fullscreen=True)
        except Exception as e:
            print(str(e))
        glClearColor(0,0,0,0)
        glEnable(GL_DEPTH_TEST)
        self.set_minimum_size(1366,768)
        self.mouse=True
        self.models=[]
        self.map_={}
        self.lmap={}
        FILE='perspective_tst'
        def get_name(seq):
            end,i=1,0
            while seq[i].isalpha():end+=1;i+=1
            return end
        with open(FILE+'.wrld','r') as f:
            for l in f:
                l=l.replace(' ','').replace('\n','')
                if not l.startswith('##'):
                    if l[0]=='B':self.models.append(Block(l[1:get_name(l[1:])],tuple(l[get_name(l[1:]):].split(',')),self.map_));self.map_=self.models[-1].map_
                    if l[0]=='L':
                        p2=None if len(l[1:].split(';'))==2 else l[1:].split(';')[2];self.models.append(Log(l[1:].split(';')[0].split(','),l[1:].split(';')[1].split(','),self.lmap,p2=p2));self.lmap=self.models[-1].lmap
        for lg in list(self.lmap.values()):lg.update(self.map_)
        self.cam=Camera((0,3,0),(-90,180))
        self.keys=key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.fps=pyglet.clock.ClockDisplay()
        pyglet.app.run()
    def on_mouse_motion(self,x,y,dx,dy):self.cam.mouse_motion(dx,dy)
    def on_key_press(self,KEY,MOD):self.close() if KEY==key.ESCAPE else 0;self.mouse=not self.mouse if KEY==key.P else self.mouse
    def update(self,dt):self.cam.update(dt,self.keys)
    def on_draw(self):
        self.clear()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70,self.width/self.height,0.05,1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glRotatef(-self.cam.rot[0],1,0,0)
        glRotatef(-self.cam.rot[1],0,1,0)
        glTranslatef(-self.cam.pos[0],-self.cam.pos[1],-self.cam.pos[2])
        [mdl.draw() for mdl in self.models]
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0,self.width,0,self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.fps.draw()
        self.set_exclusive_mouse(1) if self.mouse else self.set_exclusive_mouse(0)
if __name__=='__main__':Main()
