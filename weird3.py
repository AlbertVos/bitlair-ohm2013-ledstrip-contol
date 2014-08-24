#!/usr/bin/python

import time;
import random;
import math;
from strip import *;


class Weird3(Effect):

  colors = [
    [0, 255, 0], 
    [0, 192, 64], 
    [0, 128, 128], 
    [0, 64, 192], 
    [0, 0, 255]
  ];

  index = -1;

  state = 0;

  count = 0;

  def __init__(self, strip2D):
    super(Weird3, self).__init__(strip2D);
    for i in range(150):
      self.strip2D.strip.set(i, self.colors[random.randint(0, len(self.colors) - 1)]);
    self.strip2D.send();

  def run(self):
    while self.quit == False:
      for i in range(150):
        self.strip2D.strip.set(i, self.colors[random.randint(0, len(self.colors) - 1)]);
      self.strip2D.send();
      time.sleep(.8);
     
      for i in range(300):
        self.index = random.randint(0, 149);
        self.strip2D.strip.set(self.index, [255, 255, 255]);
        self.strip2D.send();
        time.sleep(.05);

        for j in range(5):
          self.strip2D.strip.set(self.index, [255, 255 / (7 - j), 255 / (7 - j)]);
          self.strip2D.send();
          time.sleep(.02);
        
        self.strip2D.strip.set(self.index, [255, 0, 0]);
        self.strip2D.send();
        

if __name__ == "__main__":
  e = Weird3(Strip2D(7, 21));
  e.run();


