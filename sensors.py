import asyncio
import json
import time

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

class Sensor:

    def __init__(self, name, timeout, unit, mu, sigma):
        self._name = name
        self._timer = PeriodicTimer(timeout, self._get_results)
        print("\nTimer Inited")
        self._unit = unit
        print(self._unit)
        self._mu = mu #mean value
        print(self._mu)
        self._sigma = sigma #standard deviation
        print(self._sigma)

    async def _get_results(self):
        reading = random.normal(self._mu, self._sigma)
        dict_msg = {"value": reading, "unit": self._unit, "timestamp": time.time()}
        msg = json.dumps(dict_msg)
        print (self._name + ": " + str(reading) + " " + self._unit)
        publish.single(topic=self._name, payload=msg, hostname=host)
        await asyncio.sleep(0.1)

    async def start(self):
        await self._timer.start()

    async def stop(self):
        await self._timer.stop()

async def main():
    print('\nfirst example:')
    sensor = Sensor("frequency", 2, "Hz", 5000, 0.1)  # set timer for two seconds
    await sensor.start()
    await asyncio.sleep(10)  # wait to see timer works
    await sensor.stop()

    sensor2 = Sensor("temperature", 1, "C", 100, 0.3)  # set timer for one seconds
    sensor3 = Sensor("pressure", 2, "hPa", 120, 0.1)  # set timer for two seconds
    sensor4 = Sensor("moreTemperature", 3, "K", 5000, 0.5)  # set timer for three seconds

    print('\nsecond example:')
    await asyncio.gather(
        sensor2.start(),
        sensor3.start(),
        sensor4.start()
    )
    await asyncio.sleep(10)  # and wait to see it won't call callback
    await asyncio.gather(
        sensor2.stop(),
        sensor3.stop(),
        sensor4.stop()
    )

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
loop.close()
