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


Using the proxy
===============
export ADDR='[("192.168.94.106", 6454), ("192.168.94.104", 6454), ("192.168.94.100", 6454), ("192.168.94.105", 6454), ("192.168.94.103", 6454), ("192.168.94.102", 6454), ("192.168.94.101", 6454)]'

./proxy.py

This defines the addresses of the sleeves at the 192.168.94.* addresses. The
proxy listens at ports 8000 to 8006 respectively. The proxy will send data it 
receives at the ports to the corresponding sleeve.

export 'ADDR=[("192.168.94.2", 8000), ("192.168.94.2", 8001),("192.168.94.2", 8002),("192.168.94.2", 8003),("192.168.94.2", 8004),("192.168.94.2", 8005),("192.168.94.2", 8006)]'



