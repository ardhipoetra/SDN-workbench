# SDN-workbench

## Introduction
SDN workbench for ET4285 course in TU Delft.

In this project, we use POX as the controller. Please refer to its repository how to get this controller.

Currently, we run POX 0.2.0 (carp) with CPython (2.7.4)

`yes we still stuck on python 2.7!`


## Installation

* Copy `ext/` folder into `ext/` in your `pox` library. These files is needed to run several _profile_ in POX. 
* Overwrite `l2_learning.py` with its corresponding file in `pox/pox/forwarding`. This file is necessary to tell POX what is its role in the initialization.
* Check if you already have package `iptables` in your python environment. In a simple way, you can install it with : 

```
sudo apt-get install python-pip
sudo pip install --upgrade python-iptables
```

* Make sure the constants inside file `sch*.py` is matched with your environment. If you're using my .ova file, you don't have to do anything.


Cheers!
