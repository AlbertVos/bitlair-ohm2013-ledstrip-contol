#!/usr/bin/python

import time
import math

import sys
sys.path.append('../lib')
from strip import *;

class Plasma(Effect):

  plasma_counter = 0.0;
  #plasma_step_width = 10;
  plasma_step_width = 30;
  plasma_cell_size_x = 6;
  plasma_cell_size_y = 6;
  num_col1 = 1536 / 2;
  num_col2 = 768 / 2;

  def __init__(self, strip2D):
    super(Plasma, self).__init__(strip2D);
    self.strip2D.strip.clear();
    self.color = self.color1;
    self.num_col = self.num_col1;
  
  def run(self, runtime = sys.maxint):
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      self.draw();
      time.sleep(0.1);
      self.strip2D.send();

    self.quit = False;

  def draw(self):
    self.plasma_counter = self.plasma_counter \
      + float(self.plasma_step_width) / 10.0;
    calc1 = math.sin(self.plasma_counter * 0.006);
    calc2 = math.sin(self.plasma_counter * -0.06);
    xc = 25.0;
    for x in range(self.strip2D.lenx):
      xc += float(self.plasma_cell_size_x) / 10.0;
      yc = 25.0;
      s1 = self.num_col + self.num_col * math.sin(xc) * calc1;
      for y in range(self.strip2D.leny):
        yc += float(self.plasma_cell_size_y) / 10.0;
        s2 = self.num_col + self.num_col * math.sin(yc) * calc2;
        s3 = self.num_col + self.num_col \
          * math.sin((xc + yc + float(self.plasma_counter / 10.0)) / 2.0);
        pixel = int((s1 + s2 + s3) / 3.0);
        c = self.color(pixel);
        self.strip2D.set(x, y, c);

  def color1(self, count):
    if (count < 256):
      count -= 0;
      return [255, 128 - count / 2, 0];
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


  def color2(self, count):
    if (count < 256):
      count -= 0;
      return [count, count / 2, 0];
    if (count < 512):
      count -= 256;
      return [255, (255 + 2 * count) / 3, count];
    if (count < 768):
      count = 767 - count;
      return [count, count, count];


"""
./plasma.py 'addr=[("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Plasma(Strip2D(7, 21));
  e.run();


