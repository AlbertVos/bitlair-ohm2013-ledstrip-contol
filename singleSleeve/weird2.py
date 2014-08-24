#!/usr/bin/python

import time;
import random;
import math;

import sys
sys.path.append('../lib')
from strip import *;

period = 60;
period13 = (1 * period) / 3;
period23 = (2 * period) / 3;
period16 = (1 * period) / 6;
period26 = (2 * period) / 6;
period36 = (3 * period) / 6;
period46 = (4 * period) / 6;
period56 = (5 * period) / 6;

def getColorValue2(count):
  count %= period;
  if count < 0:
    count += period;

  if count < period16:
    return 255;
  if count < period26:
    count -= period16;
    return 255 * (period16 - count) / period16;
  if count < period46:
    return 0;
  if count < period56:
    count -= period46;
    return (255 * count) / period16;
  return 255;


def getColorValue3(count):
  count %= 1536;
  if (count < 256):
    count -= 0;
    return [255, 0, 255 - count];
  if (count < 512):
    count -= 256;
    return [255, count, 0];
  if (count < 768):
    count -= 512;
    return [255 - count, 255, 0];
  if (count < 1024):
    count -= 768;
    return [0, 255, count];
  if (count < 1280):
    count -= 1024;
    return [0, 255 - count, 255];
  if (count < 1536):
    count -= 1280;
    return [count, 0, 255];


def rainbow(count):
  r = getColorValue2(count);
  g = getColorValue2(count - period13);
  b = getColorValue2(count - period23);
  #[r, g, b] = getColorValue3(count);
  return [r, g, b];


class Weird2(Effect):

  def __init__(self, strip2D):
    super(Weird2, self).__init__(strip2D);
    self.strip2D.strip.clear();
    self.strip2D.send();

  def step(self, count):
    #if count % 8 != 0:
    #  return;
    for i in range(11):
      #c = rainbow((count - i) % period);
      c = rainbow(count);
      
      for x in range(7):
        self.strip2D.set(x, 10 + i, c);
        self.strip2D.set(x, 10 - i, c);
        
    self.strip2D.coneFade(10);
    #self.strip2D.fade(.5);
    self.strip2D.send();

if __name__ == "__main__":
  e = Weird2(Strip2D(7, 21));
  e.run();


