bitlair-ohm2013-ledstrip-contol
===============================

Control Bitlair Ohm2013 RGB ledstrips with python

You can run a file seperately like ./police1.py or combine them like in the 
effects*.py files.

The default (broadcast) address is 192.168.89.255; the default port is 6454.

You can specify the address on the command-line:

./police.py [1|2|3] addr=192.168.1.255
./police.py [1|2|3] 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./police.py [1|2|3] 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'

or you can define an environment variable:

export ADDR=192.168.1.255
export ADDR=[("192.168.1.255", ), ("localhost", 7000)]
export ADDR=[("192.168.1.255", 6454), ("localhost", 7000)]

You can use a non-broadcast address to control one strip.



