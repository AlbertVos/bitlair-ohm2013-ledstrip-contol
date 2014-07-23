#!/usr/bin/python

import time
from strip import *;


class RainbowSlow(Effect):
  xcount = 0;

  def __init__(self, strip2D):
    super(RainbowSlow, self).__init__(strip2D);
    self.strip2D.strip.clear();
  
  def run(self, runtime = sys.maxint):
    self.strip2D.send();
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      self.strip2D.strip.clear(self.rainbow(self.xcount));
      self.strip2D.strip.send();
      self.xcount += 1;
      time.sleep(0.1);

    self.quit = False;

  def rainbow(self, count):
    count %= 1536;
    if count < 256:
      count -= 0;
      return [255, count, 0];
    if count < 512:
      count -= 256;
      return [255 - count, 255, 0];
    if count < 768:
      count -= 512;
      return [0, 255, count];
    if count < 1024:
      count -= 768;
      return [0, 255 - count, 255];
    if count < 1280:
      count -= 1024;
      return [count, 0, 255];
    if count < 1536:
      count -= 1280;
      return [255, 0, 255 - count];
    return [0, 0, 0];


"""
./rainbow.py addr=192.168.1.255
./rainbow.py 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./rainbow.py 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = RainbowSlow(Strip2D(7, 21));
  e.run();


