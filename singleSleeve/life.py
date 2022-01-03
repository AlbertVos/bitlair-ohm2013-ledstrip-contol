#!/usr/bin/env python3

import time
import random
import copy
import math

import sys
sys.path.append('../lib')
from strip import *

# Conrad's game of life

class Life(Effect):
  
  def __init__(self, strip2D):
    super(Life, self).__init__(strip2D)
    self.strip2D.strip.clear()
    self.strip2D.send()
    self.reset()

  def step(self, count):
    self.strip2D.strip.clear([0, 0, 0])
    #if (count % 200) == 0:
    #  self.reset()
    if (count % 20) == 0:
      for i in range(int(20 / (math.log(self.getCount() + 1) + 1))):
        self.plane[random.randint(0, 6)][random.randint(0, 20)] = 1
    else:
      self.updatePlane()
    self.draw(count)
    self.strip2D.send()
    time.sleep(0.10)

  def reset(self):
    self.plane = [[0 for y in range(21)] for x in range(7)]
    for i in range(30):
      self.plane[random.randint(0, 6)][random.randint(0, 20)] = 1

  def updatePlane(self):
    p = copy.deepcopy(self.plane)
    for y in range(21):
      for x in range(7):
        count = 0
        for dy in range(-1, 2):
          for dx in range(-1, 2):
            if dx == 0 and dy == 0:
              pass
            else:
              xx = x + dx
              if xx < 0: xx += 7
              if xx >= 7: xx -= 7
              yy = y + dy
              if yy < 0: yy += 21
              if yy >= 21: yy -= 21
              if self.plane[xx][yy] == 1:
                count += 1
        if self.plane[x][y] == 0:
          # cell is dead
          if count == 3:
            p[x][y] = 1
          else:
            p[x][y] = 0
        else:
          # cell is alive
          if (count == 2) or (count == 3):
            p[x][y] = 1
          else:
            p[x][y] = 0
    self.plane = p

  def draw(self, count):
    for y in range(21):
      for x in range(7):
        if self.plane[x][y] == 0:
          self.strip2D.set(x, y, rainbow(count + x + y))

  def getCount(self):
    c = 0
    for y in range(21):
      for x in range(7):
        if self.plane[x][y] == 1: c += 1
    return c


period = 36
period13 = period / 3
period23 = 2 * period / 3

period16 = period / 6
period26 = 2 * period / 6
period36 = 3 * period / 6
period46 = 4 * period / 6
period56 = 5 * period / 6


def getColorValue2(count):
  while count < 0:
    count += period
  while count >= period:
    count -= period

  if count < period16:
    return 255
  if count < period26:
    count -= period16
    return 255 * (period16 - count) / period16
  if count < period46:
    return 0
  if count < period56:
    count -= period46
    return 255 * count / period16
  if count < period:
    return 255
  return 0

def rainbow(count):
  r = getColorValue2(count)
  g = getColorValue2(count - period13)
  b = getColorValue2(count - period23)
  return [r, g, b]

if __name__ == "__main__":
  e = Life(Strip2D(7, 21))
  e.run()


