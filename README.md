HamsterEmu
==========

A (very slow) Gameboy emulator written entirely in python

This came from a desire for an easily modifiable gameboy emulator for analyzing
gameboy games. I also realized that an emulator in python would run very slowly
and I wondered how slowly. This answers that question. Running in pypy, I get
speeds only 2 or 3 times slower than real time. Perhaps with a sufficiently
fast processor it will run in real time.

The first version of this code was written between 3/25/2013 and 3/29/2013, at
which point there was support for MBC 0/1/3 (0 being no MBC), and in particular
it was possible to run Pokemon Blue. Note that there is currently no saving.
