#!/usr/bin/env python3

import time
import random

import sys
sys.path.append('../lib')
from strip import Effect, Strip2D


class Weird3(Effect):

  colors = [
    [0, 255, 0],
    [0, 192, 64],
    [0, 128, 128],
    [0, 64, 192],
    [0, 0, 255]
  ]

  index = -1

  state = 0

  count = 0

  def __init__(self, strip2D):
    super(Weird3, self).__init__(strip2D)
    for i in range(150):
      self.strip2D.strip.set(i, self.colors[random.randint(0, len(self.colors) - 1)])
    self.strip2D.send()

  def run(self, runtime = None):
    if runtime is None:
      if hasattr( sys, "maxint" ): # Python 2
        runtime = sys.maxint
      elif hasattr( sys, "maxsize" ): # Python 3
        runtime = sys.maxsize
    while not self.quit:
      for i in range(150):
        self.strip2D.strip.set(i, self.colors[random.randint(0, len(self.colors) - 1)])
      self.strip2D.send()
      time.sleep(.5)

      for i in range(100):
        self.index = random.randint(0, 149)
        self.draw(self.index, [255, 255, 255])
        #self.strip2D.strip.set(self.index, [255, 255, 255])
        self.strip2D.send()
        time.sleep(.05)

        for j in range(5):
          self.draw(self.index, [255, 255 / (7 - j), 255 / (7 - j)])
          #self.strip2D.strip.set(self.index, [255, 255 / (7 - j), 255 / (7 - j)])
          self.strip2D.send()
          time.sleep(.02)

        self.draw(self.index, [255, 0, 0])
        #self.strip2D.strip.set(self.index, [255, 0, 0])
        self.strip2D.send()

  def draw(self, index, color):
    self.strip2D.strip.set(index, color)
    self.strip2D.strip.set(index + 1, color)
    self.strip2D.strip.set(index + 7, color)
    self.strip2D.strip.set(index + 8, color)


if __name__ == "__main__":
  e = Weird3(Strip2D(7, 21))
  e.run()
