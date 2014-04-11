#!/usr/bin/python

import time
from strip import Strip2D;


def color(count):
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


def fade1(loopcnt = 2000000000):
  lenx = 7;
  leny = 21;
  strip2D = Strip2D(lenx, leny);

  count = 0;
  count2 = 0;
  while loopcnt > 0:
    for i in range(lenx):
      strip2D.strip.fade(.6);
      strip2D.rotr();
      for y in range(leny):
        strip2D.set(count, y, color(count2));
      strip2D.send();
      time.sleep(0.02);
      count2 += 1;
      count2 = count2 % 1536;
    count += 1;
    count = count % lenx;
    loopcnt -= 1;

  strip2D.strip.stop();


fade1();


