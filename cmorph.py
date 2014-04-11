#!/usr/bin/python

import time
from strip import *;

class CMorph(Effect):
  color1 = [255, 15, 0];
  #color2 = [200, 200, 200];
  #color2 = [15, 0, 255];
  #color2 = [15, 255, 0];
  #color2 = [0, 255, 255];
  #color2 = [30, 9, 0];
  color2 = [40, 34, 15];

  dr = float(color2[0] - color1[0]);
  dg = float(color2[1] - color1[1]);
  db = float(color2[2] - color1[2]);

  def __init__(self, strip2D):
    super(CMorph, self).__init__(strip2D);

  def color(self, count):
    [r, g, b] = self.color1;
    if (count < 20):
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];
    if (count < 30):
      count = (count - 20) + 10;
      r += int(count * self.dr / 30);
      g += int(count * self.dg / 30);
      b += int(count * self.db / 30);
      return [r, g, b];
    if (count < 50):
      count = (count - 30) + 40;
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];
    if (count < 70):
      count = 19 - (count - 50) + 40;
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];
    if (count < 80):
      count = 9 - (count - 70) + 10;
      r += int(count * self.dr / 30);
      g += int(count * self.dg / 30);
      b += int(count * self.db / 30);
      return [r, g, b];
    if (count < 100):
      count = 19 - (count - 80) + 0;
      r += int(count * self.dr / 60);
      g += int(count * self.dg / 60);
      b += int(count * self.db / 60);
      return [r, g, b];

  def run(self, runtime = sys.maxint):
    count = 0;
    count2 = 0;
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      for i in range(self.strip2D.lenx):
        c = self.color(count2);
        self.strip2D.strip.clear(c);
        self.strip2D.send();
        time.sleep(0.03);
        count2 += 3;
        count2 = count2 % 100;

    self.quit = False;


