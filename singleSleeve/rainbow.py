#!/usr/bin/python

import time

import sys
sys.path.append('../lib')
from strip import *;

"""
Rainbow colors:
RED      255,0,0
ORANGE   255,165,0
YELLOW   255,255,0
GREEN    0,255,0
BLUE     0,0,255
INDIGO   72,0,130
VIOLET   134,0,255
"""


class Rainbow(Effect):

  def __init__(self, strip2D):
    super(Rainbow, self).__init__(strip2D);
    self.strip2D.strip.clear();
  
  def run(self, runtime = sys.maxint):
    """
    self.strip2D.pattern([ \
      [255, 0, 0],   # red
      [255, 96, 0],  # orange
      [255, 255, 0], # yellow
      [0, 255, 0],   # green
      [0, 255, 255], # cyan
      [0, 0, 255],   # blue
      [255, 0, 255], # magenta
    ],  0);
    """
    self.strip2D.pattern([ \
      [255, 0, 0],
      [255, 102, 0],
      [255, 255, 0],
      [0, 255, 0],
      [0, 0, 255],
      [128, 0, 255], #[72, 0, 130],
      [255, 0, 255], #[134, 0, 255],
    ],  0);
    self.strip2D.send();
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      time.sleep(0.1);
      self.strip2D.rotr();
      self.strip2D.send();

    self.quit = False;


"""
./rainbow.py addr=192.168.1.255
./rainbow.py 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./rainbow.py 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Rainbow(Strip2D(7, 21));
  e.run();


