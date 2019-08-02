# sdnify

inside your virtual environment:

``pip install -r requirements.txt``

Copy ``config.default`` to ``.config.yml`` and fill out with the appropriate username and password (coughautomationcough). For the love of God, ``chmod 400`` that file. Like, for real. It has a plaintext password in it.

for help /path/to/python sdnify.py -h

You can add the following to your .bashrc:

``alias sdnify='/path/to/env/bin/python /path/to/sdnify/sdnify.py'``

Then ``source ~/.bashrc`` and you can do the following:

``sdnify lw-dc3-core1-nexus.rtr -i e1/1 -p nexus``

The following results will be generated:

```
[erochow@beardofprey ~]$ sdnify lw-dc3-core1-nexus.rtr -i e1/1 -p nexus

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

!Command: show running-config interface Ethernet1/1
!Time: Wed Oct 19 20:16:32 2016

version 6.2(14)

interface Ethernet1/1
  description Connection to lw-dc3-core1.rtr.liquidweb.com
  channel-group 5 mode active
  no shutdown

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           SFP Detail Diagnostics Information (internal calibration)
  ----------------------------------------------------------------------------
                Current              Alarms                  Warnings
                Measurement     High        Low         High          Low
  ----------------------------------------------------------------------------
  Temperature   32.73 C        75.00 C     -5.00 C     70.00 C        0.00 C
  Voltage        3.32 V         3.63 V      2.97 V      3.46 V        3.13 V
  Current        5.44 mA       10.50 mA     2.50 mA    10.50 mA       2.50 mA
  Tx Power      -2.41 dBm       1.69 dBm  -11.30 dBm   -1.30 dBm     -7.30 dBm
  Rx Power      -2.50 dBm       2.00 dBm  -13.90 dBm   -1.00 dBm     -9.90 dBm
  Transmit Fault Count = 0
  ----------------------------------------------------------------------------
  Note: ++  high-alarm; +  high-warning; --  low-alarm; -  low-warning

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    input rate 3.00 Mbps, 618 pps; output rate 2.26 Mbps, 1.44 Kpps
  RX
    0 input error  0 short frame  0 overrun   0 underrun  0 ignored
  TX
    0 output error  0 collision  0 deferred  0 late collision
lw-dc3-core1-nexus#
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

```
