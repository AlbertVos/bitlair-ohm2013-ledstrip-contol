#!/usr/bin/python

import time;
import random;
from strip import *;


class Matrix(Effect):
  stars = [];
  numStars = 14;
  bgcolor = 8;
  color = [255, 130, 65, 30, 15];

  def __init__(self, strip2D):
    super(Matrix, self).__init__(strip2D);
    # x, y, len 
    self.stars = [[random.randint(0, 6), random.randint(0, 20), \
      random.randint(0, 6) + 3, random.randint(0, 4)] for i in range(self.numStars)];
    self.strip2D.strip.clear([0, self.bgcolor, 0]);

  def step(self, count):
    if (count % 4) != 0:
      return;

    for i in range(150):
      c = self.strip2D.strip.get(i);
      #c[1] -= 5;
      #if c[1] < self.bgcolor:
      #  c[1] = self.bgcolor;
      #self.strip2D.strip.set(i, c);
      c[1] = self.bgcolor;
      self.strip2D.strip.set(i, c);

    for i in range(len(self.stars)):
      if self.stars[i][1] <= -self.stars[i][2]:
        self.stars[i] = [random.randint(0, 6), 20, \
         random.randint(0, 6) + 3, random.randint(0, 4)]; 
        s = self.stars[i]
      else:
        s = self.stars[i]
      s[1] -= 1;
      for y in range(s[2]):
        y += s[1];
        self.strip2D.set(s[0], y, [0, self.color[s[3]], 0]);


if __name__ == "__main__":
  e = Matrix(Strip2D(7, 21));
  e.run();


