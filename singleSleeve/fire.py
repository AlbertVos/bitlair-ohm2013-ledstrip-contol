#!/usr/bin/python
import random
import math
import time

import sys
sys.path.append('../lib')
from strip import *;


class Fire(Effect):
  rdata = {}
  gdata = {}
  bdata = {}

  pcount = 300

  def __init__(self, strip2D):
    super(Fire, self).__init__(strip2D);
    
    self.strip2D.strip.clear([0, 0, 0]);
    self.strip2D.send();

    for i in range(150):
      self.rdata[i] = 0
      self.gdata[i] = 0
      self.bdata[i] = 0

  def run(self, runtime = sys.maxint):
      
    particles = [Particle(self, random.randint(0, self.strip2D.lenx - 1), \
      random.randint(0, self.strip2D.leny)) for each in range(self.pcount)]

    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      for i in range(self.pcount):
        particles[i].updateparticle()

      for i in range(150):
        self.strip2D.set((149 - i) % 7, (149 - i) / 7, \
          [self.rdata[i], self.gdata[i], self.bdata[i]]);

      self.strip2D.send();
      self.cleanarray()
      time.sleep(0.02)    

    self.quit = False;

  def cleanarray(self):
    for i in range(150):
      self.rdata[i] = 0
      self.gdata[i] = 0
      self.bdata[i] = 0


class Particle:

  def __init__(self, fire, x, y):
    self.rgb = (255, 255, random.randint(0, 255))
    self.fire = fire;
    self.y = y
    self.x = x
    self.rnderp = id(self) % 9
    self.speed = (self.rnderp / 18) + 1
    self.life = random.uniform(1, self.fire.strip2D.leny - 5)

  def updateparticle(self):
    # Fire goes from white -> yellow -> deep orange
    if self.rgb[2] > self.rnderp + 30:
      self.rgb = (255, 255, self.rgb[2] - int(self.rnderp + 30))
    else:
      if self.rgb[1] > self.rnderp + 32:
        self.rgb = (255, self.rgb[1] - int(self.rnderp + 30), 0)
      else:
        if self.rgb[0] > self.rnderp + 5:
          self.rgb = (self.rgb[0] - int(self.rnderp + 1), self.rgb[1], 0)

    self.y -= self.speed

    intx = int(self.x)
    inty = int(self.y)

    self.intoarray(intx, inty, self.rgb)
    if self.y < self.life or self.y < 0.5:
      self.__init__(self.fire, self.x, self.fire.strip2D.leny)
              
  def intoarray(self, x, y, rgb):
    self.fire.rdata[y * 7 + x] = rgb[0]
    self.fire.gdata[y * 7 + x] = rgb[1]
    self.fire.bdata[y * 7 + x] = rgb[2]


"""
./fire.py addr=192.168.1.255
./fire.py 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./fire.py 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Fire(Strip2D(7, 21));
  e.run();


