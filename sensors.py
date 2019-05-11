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
        print (self._name + ": " + str(reading) + " " + self._unit + " timestamp: " + str(time.time() - self.n*self.day))
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
    print('\nDay 0!:\n')
    sensor1 = Sensor("bedroom/temperature", 0.3, "C", 24, 0.5)
    sensor2 = Sensor("bedroom/humidity", 0.3, "%", 70, 1)
    sensor3 = Sensor("bedroom/noisemeter", 2, "dBA", 50, 5)
    sensor4 = Sensor("kitchen/temperature", 0.5, "C", 26, 4)
    sensor5 = Sensor("kitchen/humidity", 0.5, "%", 50, 5)
    sensor6 = Sensor("livingroom/temperature", 0.8, "C", 22, 2)
    sensor7 = Sensor("livingroom/humidity", 0.8, "%", 80, 1)
    sensors = [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7]
    await asyncio.gather(
        sensor1.start(),
        sensor2.start(),
        sensor3.start(),
        sensor4.start(),
        sensor5.start(),
        sensor6.start(),
        sensor7.start()
    )
    await asyncio.sleep(20) # wait to see timer works
    print('\nDay 1:')
    for sensor in sensors:
        sensor.set_day(1)
    await sensor1.modifier("sin", 5, 5, 0.5)
    await sensor2.modifier("ramp", 10, 5)
    await sensor3.modifier("step", 10)
    await sensor4.modifier("sin", 5, 5, 0.5)
    await sensor5.modifier("ramp", 15, 5)
    await sensor6.modifier("step", -5)
    await sensor7.modifier("sin", 5, 5, 0.5)
    await asyncio.sleep(10) # wait!
    await sensor7.modifier("sin", 5, 5, 0.5)
    await sensor6.modifier("ramp", 10, 5)
    await sensor5.modifier("step", 10)
    await sensor4.modifier("sin", 5, 5, 0.5)
    await sensor3.modifier("ramp", 15, 5)
    await sensor2.modifier("step", -5)
    await sensor1.modifier("sin", 5, 5, 0.5)
    await asyncio.sleep(10) # wait!

    print('\nDay 2:')
    for sensor in sensors:
        sensor.set_day(2)
    await sensor1.modifier("sin", 7, 5, 1)
    await sensor2.modifier("ramp", -8, 5)
    await sensor3.modifier("step", 10)
    await sensor4.modifier("sin", 3, 5, 1)
    await sensor5.modifier("ramp", -18, 5)
    await sensor6.modifier("step", 4)
    await sensor7.modifier("sin", 4, 5, 1)
    await asyncio.sleep(10) # wait!
    await sensor7.modifier("sin", 8, 5, 1)
    await sensor6.modifier("ramp", -10, 5)
    await sensor5.modifier("step", -8)
    await sensor4.modifier("sin", 1, 5, 1)
    await sensor3.modifier("ramp", -12, 5)
    await sensor2.modifier("step", 7)
    await sensor1.modifier("sin", 3, 5, 1)
    await asyncio.sleep(10) # wait!

    print('\nDay 3:')
    for sensor in sensors:
        sensor.set_day(3)
    await sensor3.modifier("sin", 5, 5, 0.5)
    await sensor4.modifier("ramp", 10, 5)
    await sensor2.modifier("step", 10)
    await sensor5.modifier("sin", 5, 5, 0.5)
    await sensor7.modifier("ramp", 15, 5)
    await sensor1.modifier("step", -5)
    await sensor6.modifier("sin", 5, 5, 0.5)
    await asyncio.sleep(10) # wait
    await sensor4.modifier("sin", 8, 5, 1)
    await sensor2.modifier("ramp", -10, 5)
    await sensor7.modifier("step", -8)
    await sensor4.modifier("sin", 1, 5, 1)
    await sensor5.modifier("ramp", -12, 5)
    await sensor3.modifier("step", 7)
    await sensor1.modifier("sin", 3, 5, 1)
    await asyncio.sleep(10) # wait!

    await asyncio.gather(
        sensor1.stop(),
        sensor2.stop(),
        sensor3.stop(),
        sensor4.stop(),
        sensor5.stop(),
        sensor6.stop(),
        sensor7.stop()
    )
    await global_clock.stop()
    print('\nThe end')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
loop.close()
