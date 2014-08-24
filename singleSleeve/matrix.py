#!/usr/bin/python

import time;
import random;

import sys
sys.path.append('../lib')
from strip import *;


class Particle():
  def __init__(self, matrix, level):
    if level == 0:
      self.x = random.randint(0, 6);
      self.y = 21;
      self.len = random.randint(0, 4) + 3;
      self.color = level;
      self.speed = 2 * random.randint(0, 1) + 2;
      self.speedCount = 0;
    if level == 1:
      self.x = random.randint(0, 6);
      self.y = 21;
      self.len = random.randint(0, 3) + 2;
      self.color = level;
      self.speed = 2 * random.randint(0, 3) + 4;
      self.speed = 4;
      self.speedCount = 0;
    if level == 2:
      self.x = random.randint(0, 6);
      self.y = 21;
      self.len = random.randint(0, 2) + 2;
      self.color = level;
      self.speed = 2 * random.randint(0, 3) + 4;
      self.speed = 6;
      self.speedCount = 0;

class Matrix(Effect):
  particles = [[], [], []];
  numParticles = [35, 35, 8];
  bgcolor = 0;
  colors = [7, 55, 160];

  def __init__(self, strip2D):
    super(Matrix, self).__init__(strip2D);
    self.strip2D.strip.clear([0, self.bgcolor, 0]);
    self.strip2D.send();
    for level in range(len(self.numParticles)):
      for i in range(self.numParticles[level]):
        p = Particle(self, level);
        p.y = random.randint(0, 20);
        self.particles[level].append(p);

  def step(self, count):
    self.strip2D.strip.clear([0, self.bgcolor, 0]);

    for level in range(len(self.numParticles)):
      for i in range(self.numParticles[level]):
        p = self.particles[level][i];
        if p.y <= -p.len:
          p = Particle(self, level);
          self.particles[level][i] = p;
        if p.speedCount <= 0:
          p.y -= 1;
          p.speedCount = p.speed;
        else:
          p.speedCount -= 1;
        for y in range(p.len):
          c = ((4 * p.len - 3 * y) * self.colors[p.color]) / (4 * p.len);
          #cc = self.strip2D.get(p.x, p.y + y)[1];
          #if cc > c:
          #  c = cc;
          self.strip2D.set(p.x, p.y + y, [0, c, 0]);


if __name__ == "__main__":
  e = Matrix(Strip2D(7, 21));
  e.run();


