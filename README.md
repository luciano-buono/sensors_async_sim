Sensor Simulation with AsyncIO
==============================

This is a simple example of how to use *asyncio* to simulate async reading from
sensors and write it to a database (either mongo or sqlite).

Requirements
------------
Mosquitto is needed for mqtt messaging.

SQLite3 is needed for managing the DB.

(Optional) MongoDB is needed for managing the DB.

Virtualenv provided:

* python 3.7
* asyncio 3.4.3
* numpy 1.16.2
* paho-mqtt 1.4.0
* pymongo 3.7.2

How it works
------------
There are 3 main files:

* `initsqlite.py` initializes the database and defines the schema to be used.
* `sensors.py` uses asyncio to simulate data from different sensors and
publishes those readings through mqtt.
* `subscriber.py` subscribes to the different topics and writes everything on a
database.

Always run `initsqlite.py` first to create or reset the database. Then, run
`subscriber.py` to start listening and don't lose any message and finally run
`sensors.py`to start publishing the data.

How to run
----------

### On Ubuntu

First install all the requirements:
```
apt-get install mosquitto
apt-get install sqlite3 mongodb-org
```

```
$ git clone https://github.com/HernanG234/sensors_async_sim.git
$ cd sensors_async_sim
$ source venv/bin/activate
# You should see (venv) at the beggining of your terminal
(venv) $ python initsqlite.py
(venv) $ python subscriber.py

# Open a new terminal
$ source venv/bin/activate
(venv) $ python sensors.py
```

If you are not using the virtualenv provided, install the requirements using pip and then run the steps above:

```
$ pip install -r requirements.txt
```

Check that everything worked from SQLite:
```
$ sqlite3 iot-sqlite.db
sqlite> .tables
frequency     pressure      temperature
sqlite> select * from pressure;
# You should see the readings here!
```

### On Windows

Install all the requirements:

* Download Mosquitto QuickInstall for Windows: http://www.steves-internet-guide.com/install-mosquitto-broker/
* Download Sqlite for Windows: https://sqlite.org/2019/sqlite-tools-win32-x86-3280000.zip
* `pip install requirements.txt`

Execute each in a separate PowerShell:

```
.\mosquitto

python initsqlite.py
python subscriber.py
python sensors.py
```

Once it is finished, you can check that it worked from sqlite:

```
sqlite3.exe
```
Inside Sqlite:
```
.open iot-sqlite.db
.tables
select * from pressure;
```

Upcoming features
----------------

- [x] ~~MQTT messaging~~
- [x] Implement writing to mongo.
- [x] Implement writing to sqlite.
- [x] Add "signals" to sensors (noise, step, ramp, etc.) to plot ant query sth nicer
- [ ] Accept arg to select mongo or sqlite.
- [ ] Plot
