#!/usr/bin/python

import time;
import random;
import math;
from strip import *;

period = 60;
period13 = period / 3;
period23 = 2 * period / 3;
period16 = period / 6;
period26 = 2 * period / 6;
period36 = 3 * period / 6;
period46 = 4 * period / 6;
period56 = 5 * period / 6;

def getColorValue2(count):
  while count < 0:
    count += period;
  while count >= period:
    count -= period;

  if count < period16:
    return 255;
  if count < period26:
    count -= period16;
    return 255 * (period16 - count) / period16;
  if count < period46:
    return 0;
  if count < period56:
    count -= period46;
    return 255 * count / period16;
  if count < period:
    return 255;
  return 0;

def rainbow(count):
  r = getColorValue2(count);
  g = getColorValue2(count - period13);
  b = getColorValue2(count - period23);
  return [r, g, b];


class Weird2(Effect):
  colors = [ \
    [255, 0, 0],
    [255, 102, 0],
    [255, 255, 0],
    [0, 255, 0],
    [0, 0, 255],
    [128, 0, 255], #[72, 0, 130],
    [255, 0, 255], #[134, 0, 255],
  ];
  #f = [.20 * math.sin(math.pi * i / 26) for i in range(1, 12)];
  f = [0.02, 0.03, 0.05, 0.09, 0.10, 0.11, 0.12, 0.13, 0.17, 0.19, 0.20];
  
  bg = [[0, 50, 0], [50, 50, 50]];

  def __init__(self, strip2D):
    super(Weird2, self).__init__(strip2D);
    self.strip2D.strip.clear();
    self.strip2D.send();
    print self.f;

  def step(self, count):
    #if count % 8 != 0:
    #  return;
    self.bg = [self.bg[1], self.bg[0]];
    for i in range(11):
      #c = self.colors[(count - i) % len(self.colors)];
      #c = [255, 0, 0];
      c = rainbow((count - i) % period);
      #c = self.bg[(count + i) % 2];
      c = [int(c[0] * self.f[i]), int(c[1] * self.f[i]), int(c[2] * self.f[i])];
      
      for x in range(7):
        self.strip2D.set(x, 10 + i, c);
        self.strip2D.set(x, 10 - i, c);
        

if __name__ == "__main__":
  e = Weird2(Strip2D(7, 21));
  e.run();


