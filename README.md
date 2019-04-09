Sensor Simulation with AsyncIO
==============================

This is a simple example of how to use *asyncio* to simulate async reading from
sensors. Future objectives will consist on writing and reading to a database
(either mongo or sqlite), do some queries and plot something.

Requirements
------------
Virtualenv provided:

* python 3.7
* asyncio 3.4.3

How to run
----------

```
$ git clone https://github.com/HernanG234/sensors_async_sim.git
$ cd sensors_async_sim
$ source venv/bin/activate
#You should see (venv) at the beggining of your terminal#
(venv) $ python main.py
```

Upcoming features
----------------

* Implement writing to mongo.
* Implement writing to sqlite.
* Plot

