import pyxel
hx = [50, 65, 80, 95, 110]
fx = [25,45,65,85]
px = [0, 30, 60, 90]


class Tile: #焼きマス
   def __init__(self):
      self.step = 0
      self.timer = 0
      self.wait = pyxel.rndi(120, 210) 
      self.burn = 60

   def start(self):#時間経過にかかわらず初回クリック時にのみ動く
      if self.step == 0:
         self.step = 1
         self.timer = 0
         self.wait = pyxel.rndi(120, 210)

   def click(self):#時間経過にかかわらず焼きと焦げのクリック時にのみ動く
      if self.step == 2:
         pyxel.play(0, 0)
         self.step = 0
         self.timer = 0
         return "score"
      elif self.step == 3:
         self.step = 0
         self.timer = 0
      return None
   
   def update(self):
      burned = False

      if self.step == 1: #生地を焼く段階
         self.timer += 1
         if self.timer >= self.wait:
            self.step = 2
            self.timer = 0

      elif self.step == 2: #上手く焼けた段階
         self.timer += 1
         if self.timer >= self.burn:
            self.step = 3
            self.timer = 0
            burned = True

      elif self.step == 3: #焦げてしまった段階
         self.timer += 1
         if self.timer >= 90:
            self.step = 0
            self.timer = 0

      return burned


class APP:
  def __init__(self):
      pyxel.init(128, 128, title="pyxel")
      pyxel.mouse(True) 
      pyxel.load('my_resource.pyxres')

      pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
      pyxel.sound(1).set(notes='C2', tones='N', volumes='3', effects='S', speed=30)

      self.tiles = [Tile() for _ in range(8)]
      
      self.score = 0
      self.burn_count = 0
      self.game_over = False

      self.time_limit = 60*30
      self.time_count = 0
      self.time_over = False

      pyxel.run(self.update, self.draw)

     
  def update(self):
    
      if self.game_over:
         return 
      
      if self.time_over:
         return

      if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        
         for i in range(len(fx)): 
            x = fx[i]

            if  x <= pyxel.mouse_x <= x+16 and 50 <= pyxel.mouse_y <=66: #上段
               self.tiles[i].start()
               if self.tiles[i].click() == "score":
                  self.score += 1
             

            if  x <= pyxel.mouse_x <= x+16 and 70 <= pyxel.mouse_y <=86: #下段
               index = i+4
               self.tiles[index].start()
               if self.tiles[index].click() == "score":
                  self.score += 1

      for tile in self.tiles:
         if tile.update():
            pyxel.play(0, 1)
            self.burn_count += 1

      if self.burn_count >= 8:
         self.game_over = True

      self.time_count += 1
      if self.time_count >= self.time_limit:
         self.time_over = True

      

  def draw(self):
      pyxel.cls(0)
      
      pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

      for i in range(5):#お客さん
         pyxel.blt(50+i*15, 20, 0, 0, i*16, 16, 16, 0)

      for i in range(0,len(fx)):#鉄板のフレーム
         pyxel.blt(fx[i],50,0,64,0,16,16,0)
         pyxel.blt(fx[i],70,0,64,0,16,16,0)

      for i in range(4): #上段
         x = fx[i]
         tile = self.tiles[i]

         if tile.step == 1:
          pyxel.blt(x,50,0,16,0,16,16,0)
         elif tile.step == 2:
          pyxel.blt(x,50,0,32,0,16,16,0)
         elif tile.step == 3:
          pyxel.blt(x,50,0,48,0,16,16,0)

      for i in range(4): #下段
         x = fx[i]
         tile = self.tiles[i+4]
         
         if tile.step == 1:
          pyxel.blt(x,70,0,16,0,16,16,0)
         elif tile.step == 2:
          pyxel.blt(x,70,0,32,0,16,16,0)
         elif tile.step==3:
          pyxel.blt(x,70,0,48,0,16,16,0)

      remaining = max(0, (self.time_limit - self.time_count) // 30)
      pyxel.text(5, 5, 'time:'+str(remaining),0)
      pyxel.text(5, 15, 'score: '+str(self.score), 0)
      pyxel.text(5, 25, 'burned: '+str(self.burn_count), 0)
      

      if self.game_over:
         pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

         for i in range(0,len(px)):
           pyxel.blt(px[i],0,0,80,0,32,32,0)
           pyxel.blt(px[i],90,0,80,0,32,32,0)

         pyxel.text(40, 60, "GAME OVER", 8)

      if self.time_over:
         pyxel.bltm(0, 0, 0, 0, 0, 128, 128)

         pyxel.text(45, 30, " FINISH!", 8)
         pyxel.text(35, 60, 'FINAL SCORE: '+str(self.score), 0)
         pyxel.text(35, 80, 'FINAL BURNED: '+str(self.burn_count), 0)

      
APP()
