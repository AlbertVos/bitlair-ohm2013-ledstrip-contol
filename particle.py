#!/usr/bin/python

import time
from strip import *;

class Particle1(Effect):
  particles1 = [];
  particles2 = [];
  step = 0;

  def __init__(self, strip2D):
    super(Particle1, self).__init__(strip2D);
    self.strip = self.strip2D;
    self.particles1 = [[[0, 0] for y in range(self.strip.leny)] \
      for x in range(self.strip.lenx)];
    self.particles2 = [[[0, 0] for y in range(self.strip.leny)] \
      for x in range(self.strip.lenx)];
    self.color = self.color1;
  
  def run(self, runtime = sys.maxint):
    self.particles1[2][3] = [10, 10];
    self.print_();
    #self.particles1[0][4] = [10, 10];
    #self.particles1[1][3] = [10, 10];
    #self.particles1[1][4] = [10, 10];
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      for x in range(self.strip.lenx):
        for y in range(self.strip.leny):
          vx = self.particles1[x][y][0];
          vy = self.particles1[x][y][1];
          """
          if vx > 0:
            vx -= 1;
          if vx < 0:
            vx += 1;
          if vy > 0:
            vy -= 1;
          if vy < 0:
            vy += 1;
            """
          if vx > 0:
            xx = (x + 2) % self.strip.lenx;
            vxx = self.particles1[xx][y][0];
            if vxx < 0:
              vx += vxx;
          elif vx < 0:
            xx = (x - 2) % self.strip.lenx;
            vxx = self.particles1[xx][y][0];
            if vxx > 0:
              vx -= vxx;
            
          x1 = (x + 1) % self.strip.lenx;
          x2 = (x - 1) % self.strip.lenx;
          vx -= self.particles1[x1][y][0] / 2;
          vx += self.particles1[x2][y][0] / 2;
          if y + 1 < self.strip.leny:
            vy -= self.particles1[x][y + 1][1] / 2;
          if y - 1 >= 0:
            vy += self.particles1[x][y - 1][1] / 2;
          self.particles2[x][y] = [vx, vy];
      p = self.particles1;
      self.particles1, self.particles2 = self.particles2, self.particles1;
      self.print_();
      for x in range(self.strip.lenx):
        for y in range(self.strip.leny):
          self.strip.set(x, y, self.color(20 * self.particles1[x][y][1]));

      self.strip2D.send();
      time.sleep(1.1);

    self.quit = False;

  def color1(self, index):
    index = index / 2 + 127;
    if index < 0:
      index = 0;
    if index > 255:
      index = 255;
    return [index, 0, index];

  def print_(self):
    print self.particles1
    print "==================================="
    


"""
./particle.py 'addr=[("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Particle1(Strip2D(7, 21));
  e.run();


