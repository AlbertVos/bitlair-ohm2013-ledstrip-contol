#!/usr/bin/env python3

import time
import sys
import math
sys.path.append('../lib')
from strip import *


lenx = 7
leny = 21

addr = getAddr()

def globalStop(self):
  #print "globalStop"
  clock.quit = True
  time.sleep(.2)
  for i in range(len(addr)):
    self.artnet.addr = [addr[i]]
    self.clear()
    self.send()

class Clock1:
  count = 0
  quit = False
  
  def __init__(self, strip2D):
    self.strip2D = strip2D

  def showDigit(self, d):
    m = 1
    for i in range(6):
      if (d & m) > 0:
        for x in range(7):
          self.strip2D.set(x, i * 3 + 2, [255, 0, 0])
          self.strip2D.set(x, i * 3 + 3, [255, 0, 0])
      #else:
      #  for x in range(7):
      #    self.strip2D.set(x, i * 3 + 2, [5, 0, 0])
      #    self.strip2D.set(x, i * 3 + 3, [5, 0, 0])
      m <<= 1

  def run(self):
    while not self.quit:
      for i in range(7):
        self.strip2D.strip.artnet.addr = [addr[i]]
        c = int(13.0 + 10.0 * math.sin((-i * 3 + float(self.count)) / 10.0))
        self.strip2D.strip.clear([0, c, c])
        t = time.localtime()
        if i == 0:
          day = t.tm_mday
          self.showDigit(day)
        elif i == 1:
          month = t.tm_mon
          self.showDigit(month)
        elif i == 2:
          year = t.tm_year % 100
          self.showDigit(year)
        elif i == 3:
          pass
        elif i == 4:
          hour = t.tm_hour
          self.showDigit(hour)
        elif i == 5:
          minute = t.tm_min
          self.showDigit(minute)
        elif i == 6:
          sec = t.tm_sec
          self.showDigit(sec)
        self.strip2D.send()
      time.sleep(0.10)
      self.count += 1


class Clock2:
  count = 0
  quit = False
  
  def __init__(self, strip2D):
    self.strip2D = strip2D

  def showDigit(self, d):
    m = 1
    for i in range(6):
      if (d & m) > 0:
        for x in range(7):
          self.strip2D.set(x, i * 4 + 2, [255, 0, 0])
          self.strip2D.set(x, i * 4 + 3, [255, 0, 0])
          self.strip2D.set(x, i * 4 + 4, [255, 0, 0])
      m <<= 1

  def run(self):
    while not self.quit:
      for i in range(7):
        self.strip2D.strip.artnet.addr = [addr[i]]
        c = int(13.0 + 10.0 * math.sin((-i * 3 + float(self.count)) / 10.0))
        self.strip2D.strip.clear([0, c, c])
        t = time.localtime()
        if i == 0:
          pass
        elif i == 1:
          d = (t.tm_hour / 10) % 10
          self.showDigit(d)
        elif i == 2:
          d = t.tm_hour % 10
          self.showDigit(d)
        elif i == 3:
          d = (t.tm_min / 10) % 10
          self.showDigit(d)
        elif i == 4:
          d = t.tm_min % 10
          self.showDigit(d)
        elif i == 5:
          d = (t.tm_sec / 10) % 10
          self.showDigit(d)
        elif i == 6:
          d = t.tm_sec % 10
          self.showDigit(d)
        self.strip2D.send()
      time.sleep(0.10)
      self.count += 1


if __name__ == "__main__":
  s = Strip2D(lenx, leny)
  s.strip.globalStop = globalStop
  clock = Clock1(s)
  clock.run()


