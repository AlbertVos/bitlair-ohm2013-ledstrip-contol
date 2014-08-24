#!/usr/bin/python

import time;
import random;

import sys
sys.path.append('../lib')
from strip import *;


class Color:
  def __init__(self):
    self.getColor = self.getColor1;

  rainbow = [ \
    [255, 0, 0], [255, 96, 0], [255, 255, 0], \
    [0, 255, 0], [0, 255, 255], \
    [0, 0, 255], [255, 0, 255]];

  def getColor1(self):
    return [255, 255, 255];

  def getColor2(self):
    return [random.randint(0, 255), random.randint(0, 255) \
      , random.randint(0, 255)];

  def getColor3(self):
    return self.rainbow[random.randint(0, len(self.rainbow) - 1)];

  def colorFade(self, f):
    c = self.getColor();
    for i in range(len(c)):
      c[i] = int(c[i] * f);
    return c;

"""
  Random stars with strip fade.
"""
class Stars1(Effect):
  color = Color();

  def __init__(self, strip2D):
    super(Stars1, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def step(self, count):
    if (count % 5) != 0:
      return;
    self.strip2D.strip.fade(.8);
    for i in range(1):
      self.strip2D.set(random.randint(0, 6), random.randint(0, 20) \
        , self.color.getColor());

"""
  Stars with fading trails (strip fade).
"""
class Stars2(Effect):
  numstar = 4;
  stars = [];
  color = Color();

  def __init__(self, strip2D):
    super(Stars2, self).__init__(strip2D);
    self.stars = [[random.randint(0, 6), random.randint(0, 20) \
      , random.randint(-1, 1), -1, self.color.getColor(), 0] \
      for each in range(self.numstar)];
    self.strip2D.strip.clear();

  def step(self, count):
    if (count % 9) != 0:
      return;
    self.strip2D.strip.fade(.5);
    for i in range(self.numstar):
      x = self.stars[i][0];
      y = self.stars[i][1];
      vx = self.stars[i][2];
      vy = self.stars[i][3];
      c = self.stars[i][4];
      life = self.stars[i][5];
      self.stars[i][5] += 1;
      if vx == 0 and vy == 0:
        pass;
      else:
        if abs(vx) == 2 or abs(vy) == 2:
          self.strip2D.set(x + vx / 2, y + vy / 2, c);
        x = x + vx;
        y = y + vy;
        self.stars[i][0] = x;
        self.stars[i][1] = y;
        self.strip2D.set(x, y, c);
      if (y < 0) or (y >= 21) or (life >= 10):
        self.stars[i] = [random.randint(0, 6), random.randint(0, 20) \
          , random.randint(-1, 1), -1, self.color.getColor(), 0]


"""
  Stars with background color (particle fading).
"""
class Stars3(Effect):
  stars = [];
  numStars = 20;
  life = 30;
  color = Color();

  def __init__(self, strip2D):
    super(Stars3, self).__init__(strip2D);
    self.stars = [[random.randint(0, 6), random.randint(0, 20), \
      random.randint(0, self.life)] for i in range(self.numStars)];
    self.strip2D.strip.clear();

  def step(self, count):
    if (count % 4) != 0:
      return;
    self.strip2D.strip.clear([0, 0, 2]);
    for i in range(len(self.stars)):
      if self.stars[i][2] <= 0:
        self.stars[i] = [random.randint(0, 6), random.randint(0, 20) \
          , self.life / 2]; 
        s = self.stars[i]
      else:
        s = self.stars[i]
        s[2] -= 1;
      self.strip2D.set(s[0], s[1], self.color.colorFade( \
        float(s[2]) / float(self.life)));


if __name__ == "__main__":
  e = Stars3(Strip2D(7, 21));
  e.run();


