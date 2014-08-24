#!/usr/bin/python

import time

import sys
sys.path.append('../lib')
from strip import *;

# Orange flasher

class Flash(Effect):

  def __init__(self, strip2D):
    super(Flash, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def step(self, count):
    self.strip2D.strip.clear([255, 60, 0]);
    self.strip2D.send();
    time.sleep(0.10);
    self.strip2D.strip.clear([0, 0, 0]);
    self.strip2D.send();
    time.sleep(0.90);


if __name__ == "__main__":
  e = Flash(Strip2D(7, 21));
  e.run();


