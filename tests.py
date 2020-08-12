#!/usr/bin/env python3

import sys
sys.path.append('./lib')
from strip import *;
import time;
import random;


def test1():
  print( "*** test1 ***" )

  strip = Strip(150);

  strip.clear([255, 0, 0]);
  strip.set(0, [0, 255, 0]);
  strip.set(strip.length - 1, [0, 0, 255]);
  strip.artnet.send(strip);
  time.sleep(3);

  strip.clear([0, 255, 0]);
  strip.set(0, [255, 0, 0]);
  strip.set(strip.length - 1, [0, 0, 255]);
  strip.artnet.send(strip);
  time.sleep(3);

  strip.clear([0, 0, 255]);
  strip.set(0, [255, 0, 0]);
  strip.set(strip.length - 1, [0, 255, 0]);
  strip.artnet.send(strip);
  time.sleep(3);

  strip.artnet.close();


def test2(count):
  print( "*** test2 ***" )

  lenx = 7;
  leny = 21;
  strip2D = Strip2D(lenx, leny);
  strip = strip2D.strip;
  while count > 0:
    
    strip2D.strip.clear([255, 255, 255]);
    for y in range(leny):
      strip2D.set(0, y, [255, 0, 0]);
    strip.artnet.send(strip2D.strip);
    
    for i in range(30):
      time.sleep(0.1);
      strip2D.rotl();
      strip.artnet.send(strip2D.strip);
    for i in range(30):
      time.sleep(0.1);
      strip2D.rotr();
      strip.artnet.send(strip2D.strip);
    
    strip2D.strip.clear([255, 255, 255]);
    for x in range(lenx):
      strip2D.set(x, 0, [255, 0, 0]);
    strip.artnet.send(strip2D.strip);
    
    for i in range(40):
      time.sleep(0.1);
      strip2D.rotu();
      strip.artnet.send(strip2D.strip);
    for i in range(40):
      time.sleep(0.1);
      strip2D.rotd();
      strip.artnet.send(strip2D.strip);
    count -= 1;
    
    strip2D.strip.clear([255, 255, 255]);
    for x in range(lenx):
      strip2D.set(x, 0, [255, 0, 0]);
    strip.artnet.send(strip2D.strip);
    for y in range(leny):
      strip2D.set(0, y, [255, 0, 0]);
    strip.artnet.send(strip2D.strip);
    
    for i in range(40):
      time.sleep(0.1);
      strip2D.rotu();
      strip2D.rotr();
      strip.artnet.send(strip2D.strip);
    count -= 1;
    
  strip.artnet.close();


def test3(count):
  print( "*** test3 ***" )

  lenx = 7;
  leny = 21;
  strip2D = Strip2D(lenx, leny);
  strip = strip2D.strip;
  #strip2D.strip.clear([0, 0, 0]);
  #for y in range(leny):
  #  strip2D.set(0, y, [255, 0, 0]);
  strip2D.strip.clear([255, 255, 255]);
  for y in range(leny):
    strip2D.set(y % lenx, y, [255, 0, 0]);
    strip2D.set((y + 1) % lenx, y, [255, 0, 0]);
    strip2D.set((y + 5) % lenx, y, [0, 0, 255]);
    strip2D.set((y + 6) % lenx, y, [0, 0, 255]);
  strip.artnet.send(strip2D.strip);
  while count > 0:
    for i in range(30):
      time.sleep(0.1);
      strip2D.rotl();
      strip.artnet.send(strip2D.strip);
    for i in range(30):
      time.sleep(0.1);
      strip2D.rotr();
      strip.artnet.send(strip2D.strip);
    for i in range(30):
      time.sleep(0.1);
      strip2D.rotu();
      strip.artnet.send(strip2D.strip);
    for i in range(30):
      time.sleep(0.1);
      strip2D.rotd();
      strip.artnet.send(strip2D.strip);
    count -= 1;

  strip.artnet.close();


def test4(count):
  print( "*** test4 ***" )

  lenx = 7;
  leny = 21;
  canvas = Canvas(lenx, leny);
  global strip
  strip = canvas.strip2D.strip;
  strip.clear([40, 40, 40]);

  while count > 0:
    strip.clear([0, 0, 0]);
    x = random.randint(0, 6);
    y = random.randint(0, 20);
    cr = random.randint(0, 255);
    cg = random.randint(0, 255);
    cb = random.randint(0, 255);
    for r in range(4):
      canvas.circle(x, y, r, [cr, cg, cb]);
      strip.artnet.send(canvas.strip2D.strip);
      time.sleep(1.0);
      count -= 1;
    #canvas.strip2D.rotl();
    #strip.artnet.send(canvas.strip2D.strip);

  strip.artnet.close();


def test5(count):
  print( "*** test5 ***" )

  lenx = 7;
  leny = 21;
  strip2D = Strip2D(lenx, leny);
  global strip
  strip = strip2D.strip;

  strip2D.pattern([ \
    [255, 0, 0], [255, 96, 0], [255, 255, 0], \
    [0, 255, 0], [0, 255, 255], \
    [0, 0, 255], [255, 0, 255] \
   ],  0);
  strip.artnet.send(strip);
  while count > 0:
    time.sleep(0.1);
    strip2D.rotr();
    strip.artnet.send(strip2D.strip);
    count -= 1;

  strip.artnet.close();


def testFade(count):
  print( "*** testFade ***" )

  strip = Strip(150);
  while count > 0:
    strip.clear([255, 0, 255]);
    strip.send();
    for i in range(10):
      time.sleep(1);
      strip.fade(0.6);
      strip.send();
    count -= 1;

  strip.artnet.close();


def discover(count):
  print( "*** discover ***" )
  print( "Discovery test (takes 520 seconds)" )

  artnet = Artnet();
  while count > 0:
    artnet.discover();
    count -= 1;

  artnet.close();


#thread = threading.Thread(target = discover, args = []);
#thread.daemon = True;
#thread.start();
#thread.join();

#discover(2);
#test1();
test2(3);
#test3(2);
#test4(30);
#test5(40);
#testFade(4);


