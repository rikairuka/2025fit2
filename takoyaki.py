# -*- coding: utf-8 -*-

import pyxel
hx = [50, 65, 80, 95, 110]
fx = [15,35,55,75,95]
px = [0, 30, 60, 90]


class Tile:
   def __init__(self):
      self.step = 0
      self.timer = 0
      self.wait = pyxel.rndi(90, 150) 
      self.burn = 60

   def start(self):#時間経過にかかわらず初回クリック時にのみ動く
      if self.step == 0:
         self.step = 1
         self.timer = 0
         self.wait = pyxel.rndi(90, 150)

   def click(self):
      if self.step == 2:
         self.step = 0
         self.timer = 0
         return "score"
      elif self.step == 3:
         self.step = 0
         self.timer = 0
      return None
   
   def update(self):
      burned = False

      if self.step == 1:
         self.timer += 1
         if self.timer >= self.wait:
            self.step = 2
            self.timer = 0

      elif self.step == 2:
         self.timer += 1
         if self.timer >= self.burn:
            self.step = 3
            self.timer = 0
            burned = True

      elif self.step == 3:
         self.timer += 1
         if self.timer >= 90:
            self.step = 0
            self.timer = 0

      return burned

class APP:
  def __init__(self):
      pyxel.init(128, 128, title="pyxel")
      pyxel.mouse(True) #マウスを使えるようにする
      pyxel.load('my_resource.pyxres')

      self.tiles = [Tile() for _ in range(10)]
      
      self.score = 0
      self.burn_count = 0
      self.game_over = False

      pyxel.run(self.update, self.draw)

     
  def update(self):
      if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
      if self.game_over:
         return #game overになったらreturn以降の処理がストップする

      if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
         
         for i in range(len(fx)): #上段
            x = fx[i]

            if  x <= pyxel.mouse_x <= x+16 and 50 <= pyxel.mouse_y <=66:
               self.tiles[i].start()
               if self.tiles[i].click() == "score":
                  self.score += 1
             

            if  x <= pyxel.mouse_x <= x+16 and 70 <= pyxel.mouse_y <=86: #下段
               index = i+5
               self.tiles[index].start()
               if self.tiles[index].click() == "score":
                  self.score += 1

      for tile in self.tiles:
         if tile.update():
            self.burn_count += 1

      if self.burn_count >= 10:
         self.game_over = True

      

  def draw(self):
      pyxel.cls(0)

      pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

      for i in range(0, len(hx)):#待ち列の客
       pyxel.blt(hx[i], 20, 0, 0, 0, 16, 16, 0)  

      for i in range(0,len(fx)):#鉄板のフレーム
         pyxel.blt(fx[i],50,0,64,0,16,16,0)
         pyxel.blt(fx[i],70,0,64,0,16,16,0)


      for i in range(5): #上段
         x = fx[i]
         tile = self.tiles[i]

         if tile.step == 1:
          pyxel.blt(x,50,0,16,0,16,16,0)
         elif tile.step == 2:
          pyxel.blt(x,50,0,32,0,16,16,0)
         elif tile.step == 3:
          pyxel.blt(x,50,0,48,0,16,16,0)

      for i in range(5): #下段
         x = fx[i]
         tile = self.tiles[i+5]
         
         if tile.step == 1:
          pyxel.blt(x,70,0,16,0,16,16,0)
         elif tile.step == 2:
          pyxel.blt(x,70,0,32,0,16,16,0)
         elif tile.step==3:
          pyxel.blt(x,70,0,48,0,16,16,0)


      pyxel.text(5, 5, 'score: '+str(self.score), 0)
      pyxel.text(5, 15, 'burned: '+str(self.burn_count), 0)

      if self.game_over:
         pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

         for i in range(0,len(px)):
           pyxel.blt(px[i],0,0,80,0,32,32,0)
           pyxel.blt(px[i],90,0,80,0,32,32,0)

         pyxel.text(40, 60, "GAME OVER", 8)
      
APP()
