#!/usr/bin/python

import time

import sys
sys.path.append('../lib')
from strip import *;

select = 1

class CMorph(Effect):
    
  color1 = [255, 15, 0];
  color2 = [40, 34, 15];
  #color2 = [200, 200, 200];
  #color2 = [15, 0, 255];
  #color2 = [15, 255, 0];
  #color2 = [0, 255, 255];
  #color2 = [30, 9, 0];

  def __init__(self, strip2D):
    super(CMorph, self).__init__(strip2D);
    self.strip2D.strip.clear();
    
    if select == 2:
      self.color1 = [255, 255, 255];
      self.color2 = [0, 0, 0];
    elif select == 3:
      self.color1 = [255, 15, 0];
      self.color2 = [0, 15, 255];
    
    self.dr = float(self.color2[0] - self.color1[0]);
    self.dg = float(self.color2[1] - self.color1[1]);
    self.db = float(self.color2[2] - self.color1[2]);


  def color(self, count):
    [r, g, b] = self.color1;
    if (count < 20):
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];
    if (count < 30):
      count = (count - 20) + 10;
      r += int(count * self.dr / 30);
      g += int(count * self.dg / 30);
      b += int(count * self.db / 30);
      return [r, g, b];
    if (count < 50):
      count = (count - 30) + 40;
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];
    if (count < 70):
      count = 19 - (count - 50) + 40;
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];
    if (count < 80):
      count = 9 - (count - 70) + 10;
      r += int(count * self.dr / 30);
      g += int(count * self.dg / 30);
      b += int(count * self.db / 30);
      return [r, g, b];
    if (count < 100):
      count = 19 - (count - 80) + 0;
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];

  def run(self, runtime = sys.maxint):
    count = 0;
    count2 = 0;
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      for i in range(self.strip2D.lenx):
        c = self.color(count2);
        self.strip2D.strip.clear(c);
        self.strip2D.send();
        time.sleep(0.05);
        count2 += 3;
        count2 = count2 % 100;

    self.quit = False;


"""
./cmorph.py addr=192.168.1.255
./cmorph.py 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./cmorph.py 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  if len(sys.argv) >= 2:
    select = int(sys.argv[1])
  e = CMorph(Strip2D(7, 21));
  e.run();


