#!/usr/bin/env python3
import random
import math
import time

import sys
sys.path.append('../lib')
from strip import *

import termios, fcntl

class Fire2(Effect):
  rdata = {}
  gdata = {}
  bdata = {}

  #pcount = 10 # set at init
  maxparticles = 300

  maxbrightness = 255  
  palette = 0
  restoretime = 0

  def __init__(self, strip2D):
    super(Fire2, self).__init__(strip2D)
    
    self.pcount = 10
    
    self.strip2D.strip.clear([0, 0, 0])
    self.strip2D.send()

    for i in range(150):
      self.rdata[i] = 0
      self.gdata[i] = 0
      self.bdata[i] = 0

  def run(self, runtime = None):
    if ( runtime == None ):
      if ( hasattr( sys, "maxint" ) ): # Python 2
        runtime = sys.maxint
      elif ( hasattr( sys, "maxsize" ) ): # Python 3
        runtime = sys.maxsize
      
    particles = [Particle(self, random.randint(0, self.strip2D.lenx - 1), \
      self.strip2D.leny) for each in range(self.maxparticles)]

    starttime = time.time()
     
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    heat = 0
    while (not self.quit or heat) and ((time.time() - starttime) < runtime):
      if ( self.quit ):
        if ( heat ):
          heat -= 1
        if ( self.maxbrightness ):
          self.maxbrightness -= 1
      elif (self.pcount < self.maxparticles):
        heat = int( 512 * self.pcount / self.maxparticles )

      if ( heat > 255 ):
        heat = 255

      try:
        c = sys.stdin.read(1)
        if c == "0":
          self.palette = 0
        elif c == "1":
          self.palette = 1
        elif c == "2":
          self.palette = 2
        elif c == "3":
          self.palette = 3
        elif c == "4":
          self.palette = 4
        elif c == "5":
          self.palette = 5
          
        elif c == "9":
          self.palette = 3
          self.restoretime = time.time() + 5
        elif c == "q":
          print( "quit" )
          self.quit = True
        elif c == "+" or c == "=":
          self.maxbrightness += 1
          if ( self.maxbrightness > 255 ):
            self.maxbrightness = 255
        elif c == "-" or c == "_":
          self.maxbrightness -= 1
          if ( self.maxbrightness < 1 ):
            self.maxbrightness = 1
        elif c == "h":
          self.pcount = self.maxparticles - 2
        elif c == "l":
          self.pcount = 20
            
      except IOError: pass
    
      if ( self.restoretime and self.restoretime < time.time() ):
        self.palette = 0
        self.restoretime = 0
      for i in range(self.pcount):
        particles[i].updateparticle( heat, True )
      for i in range(self.pcount, self.maxparticles):
        particles[i].updateparticle( 255, False )
        
      for i in range(150):
        self.strip2D.set((149 - i) % self.strip2D.lenx, int((149 - i) / self.strip2D.lenx), \
          [self.maxbrightness * self.rdata[i] / 255, self.maxbrightness * self.gdata[i] / 255, self.maxbrightness * self.bdata[i] / 255])

      self.strip2D.send()
      self.cleanarray()
      time.sleep(0.03)
      
      # Add new particle
      if( self.pcount < self.maxparticles and random.randint(0, 256 - heat) < 3 + heat ):
        self.pcount += 1

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)        
    self.quit = False

  def cleanarray(self):
    for i in range(150):
      self.rdata[i] = 0
      self.gdata[i] = 0
      self.bdata[i] = 0


class Particle:

  def __init__(self, fire, x, y):
    self.rgb = (0,0,0)
    self.fire = fire
    self.y = y
    self.x = x
    self.rnderp = id(self) % 9
    self.speed = 1#int(self.rnderp / 18) + 1
    self.life = random.uniform( 5, self.fire.strip2D.leny - 1 )
    self.palette = fire.palette

  def updateparticle(self, heat, alive):
    # Fire goes from white -> yellow -> deep orange
    life = heat * self.life / 255
    if ( life < 3 ):
        life = 3
    progress = int(heat * (self.fire.strip2D.leny - self.y) / life)
    color = heat - progress
    if ( color < 0 ):
        color = 0
    
    r = 5 + color * 2
    if ( r > 255 ):
        r = 255

    g = (color - 92) * 2
    if ( g > 255 ):
        g = 255
    if ( g < 0 ):
        g = 0

    b = (color - 191) * random.randint( 0, 4 )
    if ( b > 255 ):
        b = 255
    if ( b < 0 ):
        b = 0

    if ( self.palette == 1 ):
      # turqoise blue BGR
      temp = r
      r = b
      b = temp
    elif ( self.palette == 2 ):
      # yellow green GRB     
      temp = r
      r = g
      g = temp
    elif ( self.palette == 3 ):
      # pink blue GBR
      temp = r
      r = g
      g = b
      b = temp
    elif ( self.palette == 4 ):
      # purple red RBG
      temp = b
      b = g
      g = temp
    elif ( self.palette == 5 ):
      # turqoise green BRG
      temp = r
      r = b
      b = g
      g = temp
        
    self.rgb = ( r, g, b )
    self.y -= self.speed

    intx = int(self.x)
    inty = int(self.y)

    self.intoarray(intx, inty, self.rgb)
    
    # Reset if particle is done
    if (self.fire.strip2D.leny - self.y ) > life or self.y > self.fire.strip2D.leny:
      if (alive):
        self.__init__(self.fire, random.randint( 0, self.fire.strip2D.lenx - 1 ), self.fire.strip2D.leny)
      else:
        self.rgb = ( 0,0,0 )

  def intoarray(self, x, y, rgb):
    self.fire.rdata[y * self.fire.strip2D.lenx + x] = rgb[0]
    self.fire.gdata[y * self.fire.strip2D.lenx + x] = rgb[1]
    self.fire.bdata[y * self.fire.strip2D.lenx + x] = rgb[2]


"""
./fire.py addr=192.168.1.255
./fire.py 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./fire.py 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Fire2(Strip2D(7, 21))
  e.run()

