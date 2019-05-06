import asyncio
import json
import time
import math

from numpy import random
from contextlib import suppress
import paho.mqtt.publish as publish

host = "localhost"

class PeriodicTimer:
    def __init__(self, timeout, func):
        self.func = func
        self.timeout = timeout
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            await asyncio.sleep(self.timeout)
            await self.func()

global_tick = 0.03
modifiers = ["none", "step", "ramp", "sin"]
sensors_list = []

async def tick_func():
    if (len(sensors_list) == 0):
        await asyncio.sleep(0.01)
    else:
        for sensor in sensors_list:
            if sensor._modifier == "none":
                 continue
            if sensor._modifier == "step":
                 await sensor.Step()
            if sensor._modifier == "ramp":
                 await sensor.Ramp()
            if sensor._modifier == "sin":
                 await sensor.Sin()

    await asyncio.sleep(0.01)


class Sensor:

    def __init__(self, name, timeout, unit, mu, sigma):
        self._name = name
        self._timer = PeriodicTimer(timeout, self._get_results)
        self._modifier = "none"
        self._offset = 0
        self._frequency = 0
        print("\nTimer Inited")
        self._unit = unit
        print(self._unit)
        self._mu = mu #mean value
        self._orig_mu = mu
        print(self._mu)
        self._sigma = sigma #standard deviation
        self._orig_sigma = sigma
        print(self._sigma)
        sensors_list.append(self)
        self.day = 86400 # seconds in a day for modifying posix time
        self.n = 0 # number of days in the past | quick trick to do the job

    def set_day(self, day):
        self.n = day

    async def _get_results(self):
        reading = random.normal(self._mu, self._sigma)
        dict_msg = {"value": reading, "unit": self._unit, "timestamp": time.time() - self.n*self.day}
        msg = json.dumps(dict_msg)
        print (self._name + ": " + str(reading) + " " + self._unit + "timestamp: " + str(time.time() - self.n*self.day))
        publish.single(topic=self._name, payload=msg, hostname=host)
        await asyncio.sleep(0.1)

    async def start(self):
        await self._timer.start()

    async def stop(self):
        sensors_list.pop()
        await self._timer.stop()

    async def modifier(self, mod_string, offset=0, duration=0, freq=0):
        if mod_string in modifiers:
            self._modifier = mod_string
            self._offset = offset
            self._duration = duration
            self._frequency = freq
            self._counter = 0
        else:
            print ("Modifier function not recognized\n")

    async def Step(self):
        self._mu = self._mu + self._offset
        self._orig_mu = self._mu
        self._modifier = "none"
        self._offset = 0

    async def Ramp(self):
        if ((self._mu < (self._orig_mu + self._offset) and self._offset > 0) or (self._offset < 0 and self._mu > (self._orig_mu + self._offset))):
            self._mu = self._mu + (self._offset * global_tick / self._duration)
        else:
            self._modifier = "none"
            self._orig_mu = self._mu
            self._offset = 0

    async def Sin(self):
        if (self._counter < 1):
            self._end_time = loop.time() + self._duration*1000
            self._counter += 1
        elif (loop.time() < self._end_time):
            self._mu = self._orig_mu + self._offset * math.sin(2*math.pi/self._frequency*self._counter)
            self._counter += 1
        else:
            self._mu = self._orig_mu
            self._modifier = "none"
            self._offset = 0
            self._counter = 0

async def main():
    global_clock = PeriodicTimer(global_tick, tick_func)
    await global_clock.start()
    print('\nfirst example:')
    sensor = Sensor("frequency", 0.5, "Hz", 5000, 0.1)  # set timer for two seconds
    sensor2 = Sensor("pressure", 2, "hPa", 120, 0.1)  # set timer for two seconds
    await sensor.start()
    await sensor2.start()
    await asyncio.sleep(10) # wait to see timer works
    print('\nfirst example:')
    sensor.set_day(1)
    await sensor.modifier("sin", 10, 5, 500)
    await asyncio.sleep(10) # wait to see timer works
    await sensor.modifier("ramp", 1000, 5)
    print('\nfirst example:')
    sensor.set_day(2)
    await asyncio.sleep(10) # wait to see timer works
    await sensor.modifier("ramp", -1000, 5)
    print('\nfirst example:')
    sensor.set_day(3)
    await asyncio.sleep(10) # wait to see timer works
    await sensor.stop()

#    sensor2 = Sensor("temperature", 1, "C", 100, 0.3)  # set timer for one seconds
#    sensor3 = Sensor("pressure", 2, "hPa", 120, 0.1)  # set timer for two seconds
#    sensor4 = Sensor("moreTemperature", 3, "K", 5000, 0.5)  # set timer for three seconds

#    print('\nsecond example:')
#    await asyncio.gather(
#        sensor2.start(),
#        sensor3.start(),
#        sensor4.start()
#    )
#    await asyncio.sleep(10)  # and wait to see it won't call callback
#    await asyncio.gather(
#        sensor2.stop(),
#        sensor3.stop(),
#        sensor4.stop()
#    )

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
loop.close()
