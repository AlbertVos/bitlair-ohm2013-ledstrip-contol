#!/usr/bin/env python3

import time
import math

import sys
sys.path.append('../lib')
from strip import Strip2D, Effect

period = 1800
period13 = period / 3
period23 = 2 * period / 3

period16 = period / 6
period26 = 2 * period / 6
period36 = 3 * period / 6
period46 = 4 * period / 6
period56 = 5 * period / 6


def getColorValue1(count):
  while count < 0:
    count += period
  while count >= period:
    count -= period
  if count >= period23:
    return 0
  return 255 * math.sin(count * math.pi / period23)

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

class Rainbowslow(Effect):

  def __init__(self, strip2D):
    super(Rainbowslow, self).__init__(strip2D)
    self.strip2D.strip.clear()

  def run(self, runtime = None):
    if runtime is None:
      if hasattr( sys, "maxint" ): # Python 2
        runtime = sys.maxint
      elif hasattr( sys, "maxsize" ): # Python 3
        runtime = sys.maxsize
    count = 0
    self.strip2D.strip.clear()
    self.strip2D.send()
    now = time.time()
    while (not self.quit) and ((time.time() - now) < runtime):
      self.strip2D.strip.clear(rainbow(count))
      self.strip2D.send()
      count += 1
      if count >= period:
        count -= period
      time.sleep(.1)

    self.quit = False


"""
./rainbowSlow.py addr=192.168.1.255
./rainbowSlow.py 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./rainbowSlow.py 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Rainbowslow(Strip2D(7, 21))
  e.run()
