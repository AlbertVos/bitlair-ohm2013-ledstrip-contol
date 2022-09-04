#!/usr/bin/env python3

import time

import sys
sys.path.append('../lib')
from strip import Effect, Strip2D

defaultColors = [
  [0,0,0],    # idle (color before 5 minute mark)
  [1,1,1],    # active (when the 5 minute progress starts)
  [0,255,0],  # 5 minutes progress
  [255,255,0],# 1 minute progress
  [255,0,0],  # 10 seconds progress
  [255,0,1],  # timeout (color after 0 second mark)
]
class Countdown(Effect):
  endtime = None
  direction = None

  def __init__(self, strip2D, colors=None, epoch=None, direction="up"):
    super(Countdown, self).__init__(strip2D)
    self.strip2D.strip.clear()
    self.colors = colors or defaultColors
    self.endtime = epoch or (time.time() + 300)
    self.direction = direction

  def run(self, runtime = None):
    if runtime is None:
      if hasattr( sys, "maxint" ): # Python 2
        runtime = sys.maxint
      elif hasattr( sys, "maxsize" ): # Python 3
        runtime = sys.maxsize

    now = time.time()
    leny = self.strip2D.leny

    while (not self.quit) and ((time.time() - now) < runtime):
      remainder = self.endtime - time.time()

      if remainder <= 0:
        # timeout
        for y in range(leny):
          v = self.direction == "down" and y or leny - y - 1
          for x in range(self.strip2D.lenx):
            self.strip2D.set( x, v, self.colors[5]) # timeout color
      elif remainder <= 10:
        # last 10 seconds
        for y in range(leny):
          v = self.direction == "down" and y or leny - y - 1
          for x in range(self.strip2D.lenx):
            # differentiate length over 10 sec
            if y > remainder / 10 * leny:
              self.strip2D.set( x, v, self.colors[4]) # 10 second color
            else:
              self.strip2D.set( x, v, self.colors[3]) # 1 minute color
      elif remainder <= 60:
        # last minute
        for y in range(leny):
          v = self.direction == "down" and y or leny - y - 1
          for x in range(self.strip2D.lenx):
            # differentiate length over 60-10 sec
            if y > (remainder - 10) / 50 * leny:
              self.strip2D.set( x, v, self.colors[3]) # 1 minute color
            else:
              self.strip2D.set( x, v, self.colors[2]) # 5 minute color
      elif remainder <= 300:
        # last 5 minutes
        for y in range(leny):
          v = self.direction == "down" and y or leny - y - 1
          for x in range(self.strip2D.lenx):
            # differentiate length over red/green 5-1 min
            if y > (remainder - 60) / 240 * leny:
              self.strip2D.set( x, v, self.colors[2]) # 5 minute color
            else:
              self.strip2D.set( x, v, self.colors[1]) # normal color
      else:
        # initial coloring (before 5 minute mark and timeout)
        for y in range(leny):
          for x in range(self.strip2D.lenx):
            self.strip2D.set( x, y, self.colors[0]) # idle color

      self.strip2D.send()
      time.sleep(1.0)

    self.quit = False



"""
./countdown.py addr=192.168.1.255
./countdown.py [epoch] [up/down] 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./countdown.py [epoch] [up/down] 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""
if __name__ == "__main__":
  argDirection = None
  argEpoch = None

  if len(sys.argv) > 2:
    if sys.argv[1] == "down" or sys.argv[1] == "up":
      argDirection = sys.argv[1]
    else:
      argEpoch = int( sys.argv[1] )
  if len(sys.argv) > 3:
    if sys.argv[2] == "down" or sys.argv[2] == "up":
      argDirection = sys.argv[2]
    else:
      argEpoch = int( sys.argv[2] )

  e = Countdown(Strip2D( 7, 21 ), defaultColors, argEpoch, argDirection )

  #e = Countdown(Strip2D( 21, 18, 15, 17, 15, 17 ), colors, 1640991600 ) # New year tz 1
  e.run()
