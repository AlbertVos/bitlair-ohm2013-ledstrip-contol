#!/usr/bin/env python3

import time

import sys
sys.path.append('../lib')
from strip import Effect, Strip2D

# Cheesy version of a Jacob's Ladder
class JacobLadder(Effect):

  def __init__(self, strip2D):
    super(JacobLadder, self).__init__(strip2D)
    self.strip2D.strip.clear()

  def run(self, runtime = None):
    if runtime is None:
      if hasattr( sys, "maxint" ): # Python 2
        runtime = sys.maxint
      elif hasattr( sys, "maxsize" ): # Python 3
        runtime = sys.maxsize

    self.strip2D.strip.clear([0, 0, 0])

    for x in range(self.strip2D.lenx):
      self.strip2D.set(x, 0, [64, 192, 255])

    now = time.time()
    while (not self.quit) and ((time.time() - now) < runtime):

      for _i in range(self.strip2D.leny):
        time.sleep(0.05)
        self.strip2D.rotu()
        self.strip2D.send()

    self.quit = False


if __name__ == "__main__":
  e = JacobLadder(Strip2D(7, 21))
  e.run()
