#!/usr/bin/python

import time;
import threading;
from strip import *;

from police import *;
from rainbow import *;
from bump import *;
from cmorph import *;
from lemmings import *;


lenx = 7;
leny = 21;

strip2D = Strip2D(lenx, leny);
effect = Rainbow(strip2D);
effect.run();


