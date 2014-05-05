#!/usr/bin/python

import time;
import random;
from strip import *;


class Stars1(Effect):

  def __init__(self, strip2D):
    super(Stars1, self).__init__(strip2D);
    self.getColor = self.getColor3

  def step(self, count):
    if (count % 5) != 0:
      return;
    self.strip2D.strip.fade(.8);
    for i in range(1):
      self.strip2D.set(random.randint(0, 6), random.randint(0, 20) \
        , self.getColor());

  def getColor1(self):
    return [255, 255, 255];

  def getColor2(self):
    return [random.randint(0, 255), random.randint(0, 255) \
      , random.randint(0, 255)];

  rainbow = [ \
    [255, 0, 0], [255, 96, 0], [255, 255, 0], \
    [0, 255, 0], [0, 255, 255], \
    [0, 0, 255], [255, 0, 255]];

  def getColor3(self):
    return self.rainbow[random.randint(0, len(self.rainbow) - 1)];


class Stars2(Effect):
  numstar = 4;
  stars = [];

  def __init__(self, strip2D):
    super(Stars2, self).__init__(strip2D);
    self.getColor = self.getColor3
    self.stars = [[random.randint(0, 6), random.randint(0, 20) \
      , random.randint(-1, 1), -1, self.getColor(), 0] \
      for each in range(self.numstar)];

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
          , random.randint(-1, 1), -1, self.getColor(), 0]

  def getColor1(self):
    return [255, 255, 255];

  def getColor2(self):
    return [random.randint(0, 255), random.randint(0, 255) \
      , random.randint(0, 255)];

  rainbow = [ \
    [255, 0, 0], [255, 96, 0], [255, 255, 0], \
    [0, 255, 0], [0, 255, 255], \
    [0, 0, 255], [255, 0, 255]];

  def getColor3(self):
    return self.rainbow[random.randint(0, len(self.rainbow) - 1)];


if __name__ == "__main__":
  e = Stars2(Strip2D(7, 21));
  e.run();


