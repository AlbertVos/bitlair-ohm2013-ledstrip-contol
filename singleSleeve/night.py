#!/usr/bin/python

import time;
import random;

import sys
sys.path.append('../lib')
from strip import *;


class Night(Effect):
  top = [];
  active = [];
  bottom = [];
  numpart = 125;
  numlayer = 5;
  initcnt = -1;
  gold = [255, 215, 0];
  white = [255, 255, 255];
  blue = [50, 50, 255];
  dblue = [5, 5, 55];
  colors = [dblue, white];

  def __init__(self, strip2D):
    super(Night, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def init(self):
    for i in range(0, self.numlayer):
      for j in range(self.numpart / self.numlayer):
        self.top.append([random.randint(0, 6), i, i]);
    self.active = [];
    self.bottom = [];
    self.initcnt = -1;

  def step(self, count):
    self.strip2D.strip.clear(self.colors[0]);

    if self.initcnt == 0:
      self.init();
      self.initcnt = -1;
      return;
    elif self.initcnt > 0: 
      self.initcnt -= 1;
      for i in range(self.numlayer):
        for j in range(7):
          self.strip2D.set(j, 20 - (self.initcnt / 3 + i), self.colors[1]);
      return;

    # check for end
    if ((len(self.top) == 0) and (len(self.active) == 0)):
      self.initcnt = 21 - self.numlayer;
      self.initcnt *= 3;
    # drop next one
    if ((len(self.top) > 0) and (count % 9 == 0)):
      p = self.top.pop();
      p[1] = 20 - (self.numlayer - 1 - p[1]);
      self.active.insert(0, p);
    
    for i in reversed(range(len(self.active))):
      self.active[i][2] += 1;
      if (self.active[i][2] >= self.active[i][1]):
        p = self.active.pop(i);
        self.bottom.append(p);

    for i in range(len(self.top)):
      self.strip2D.set(self.top[i][0], 20 - self.top[i][2], self.colors[1]);

    for i in range(len(self.bottom)):
      self.strip2D.set(self.bottom[i][0], 20 - self.bottom[i][2], self.colors[1]);

    for i in range(len(self.active)):
      self.strip2D.set(self.active[i][0], 20 - self.active[i][2], self.colors[1]);

    m = 129 - (count / 50) % 7;
    a = -1;
    if self.strip2D.strip.get(m - 0) == self.colors[1]:
      a = 180;
    self.strip2D.strip.set(m - 0 , self.gold, a);
    a = -1;
    if self.strip2D.strip.get(m - 13) == self.colors[1]:
      a = 180;
    self.strip2D.strip.set(m - 13, self.gold, a);
    a = -1;
    if self.strip2D.strip.get(m - 20) == self.colors[1]:
      a = 180;
    self.strip2D.strip.set(m - 20, self.gold, a);
    a = -1;
    if self.strip2D.strip.get(m - 27) == self.colors[1]:
      a = 180;
    self.strip2D.strip.set(m - 27, self.gold, a);
    a = -1;
    if self.strip2D.strip.get(m - 28) == self.colors[1]:
      a = 180;
    self.strip2D.strip.set(m - 28, self.gold, a);

  def setColors(self, colors):
    self.colors = colors;


if __name__ == "__main__":
  e = Night(Strip2D(7, 21));
  e.run();


