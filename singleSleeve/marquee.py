#!/usr/bin/env python3

import time
import os
import sys
sys.path.append('../lib')
from strip import Effect, Strip2D

os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

pygame.init()

color = [64, 192, 255]
# You might need to experiment with different fonts since rendering is slightly skewed
# and the pixels are pretty far apart horizontally
font = pygame.font.Font("SairaCondensed-ExtraLight.ttf", 10 )

class Marquee(Effect):

  def __init__(self, strip2D):
    self.text = "Hello World"
    super(Marquee, self).__init__(strip2D)
    self.strip2D.strip.clear()

  def run(self, runtime = None):
    if runtime is None:
      if hasattr( sys, "maxint" ): # Python 2
        runtime = sys.maxint
      elif hasattr( sys, "maxsize" ): # Python 3
        runtime = sys.maxsize

    self.strip2D.strip.clear()

    self.text = " ".join(self.text[i:i+1] for i in range(0, len(self.text), 1))
    text = font.render( self.text, False, color)

    screen = pygame.display.set_mode((text.get_width() + 14, 21))
    screen.fill((0, 0, 0))
    screen.blit(text, ( 7 , (screen.get_height() - text.get_height()) // 2))

    pygame.display.flip()

    now = time.time()

    offset = 0
    while (not self.quit) and ((time.time() - now) < runtime):
      time.sleep(0.1)

      for y in range(self.strip2D.leny):
        for x in range(self.strip2D.lenx):
          renderedcolor = screen.get_at( (x + offset, y) )[0:3]
          self.strip2D.set(x + 1, self.strip2D.leny - y, renderedcolor )
          #self.strip2D.set(x, 2 * y + 1, color )
      offset += 1
      if  offset > screen.get_width() - 7 :
        offset = 0

      self.strip2D.send()

    self.quit = False

"""
./marquee.py "Hello world" addr=192.168.1.255
./marquee.py "Hello world" 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./marquee.py "Hello world" 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  print( sys.argv )
  e = Marquee(Strip2D(7, 21))
  if len(sys.argv) > 2:
    e.text = sys.argv[1]
  e.run()
