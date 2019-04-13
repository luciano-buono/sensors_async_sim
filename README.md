Sensor Simulation with AsyncIO
==============================

This is a simple example of how to use *asyncio* to simulate async reading from
sensors. Future objectives will consist on writing and reading to a database
(either mongo or sqlite), do some queries and plot something.

Requirements
------------
Mosquitto is needed for mqtt messaging. On Ubuntu:

```
apt-get install mosquitto
```

MongoDB is needed for using this DB:

```
apt-get install mongodb-org
```

Virtualenv provided:

* python 3.7
* asyncio 3.4.3
* numpy 1.16.2
* paho-mqtt 1.4.0
* pymongo 3.7.2

How to run
----------

```
$ git clone https://github.com/HernanG234/sensors_async_sim.git
$ cd sensors_async_sim
$ source venv/bin/activate
# You should see (venv) at the beggining of your terminal
(venv) $ python main.py
```

Upcoming features
----------------

- [x] ~~MQTT messaging~~
- [x] Implement writing to mongo.
- [x] Implement writing to sqlite.
- [ ] Initialize DBs on subscriber.
- [ ] Accept arg to select mongo or sqlite.
- [ ] Plot
- [ ] Add "signals" to sensors (noise, step, ramp, etc.) to plot ant query sth nicer
