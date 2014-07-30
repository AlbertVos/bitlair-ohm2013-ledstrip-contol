#!/usr/bin/python

import time;
import math;
from strip import *;

period = 1800;
period13 = period / 3;
period23 = 2 * period / 3;

period16 = period / 6;
period26 = 2 * period / 6;
period36 = 3 * period / 6;
period46 = 4 * period / 6;
period56 = 5 * period / 6;


def getColorValue1(count):
  while count < 0:
    count += period;
  while count >= period:
    count -= period;
  if count >= period23:
    return 0;
  return 255 * math.sin(count * math.pi / period23);

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

count = 0;
strip = Strip(150);
strip.clear();
strip.send();
while True:
  strip.clear(rainbow(count));
  strip.send();
  count += 1;
  if count >= period:
    count -= period;
  time.sleep(.1);



