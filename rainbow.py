#!/usr/bin/python

import time
from strip import *;

class Rainbow(Effect):

  def __init__(self, strip2D):
    super(Rainbow, self).__init__(strip2D);
  
  def run(self, runtime = sys.maxint):
    self.strip2D.pattern([ \
      [255, 0, 0], [255, 96, 0], [255, 255, 0], \
      [0, 255, 0], [0, 255, 255], \
      [0, 0, 255], [255, 0, 255] \
     ],  0);
    self.strip2D.send();
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      time.sleep(0.1);
      self.strip2D.rotr();
      self.strip2D.send();

    self.quit = False;


"""
./rainbow.py 'addr=[("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Rainbow(Strip2D(7, 21));
  e.run();


