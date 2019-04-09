import asyncio
import random
from contextlib import suppress

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

    def __init__(self, timeout, units, min_value, max_value):
        self._timer = PeriodicTimer(timeout, self._get_results)
        print("\nTimer Inited")
        self._units = units
        print(self._units)
        self._min_value = min_value
        print(self._min_value)
        self._max_value = max_value
        print(self._max_value)

    async def _get_results(self):
        print ("Result: " + str(random.uniform(self._min_value, self._max_value)) + " " + self._units)
        await asyncio.sleep(0.1)

    async def start(self):
        await self._timer.start()

    async def stop(self):
        await self._timer.stop()

async def main():
    print('\nfirst example:')
    sensor = Sensor(2, "Hz", 10, 10000)  # set timer for two seconds
    await sensor.start()
    await asyncio.sleep(10)  # wait to see timer works
    await sensor.stop()

    sensor2 = Sensor(1, "°C", -30, 150)  # set timer for two seconds
    sensor3 = Sensor(2, "hPa", -100, 100)  # set timer for two seconds
    sensor4 = Sensor(3, "K", 0, 270)  # set timer for two seconds

    print('\nsecond example:')
    await asyncio.gather(
        sensor2.start(),
        sensor3.start(),
        sensor4.start()
    )
    await asyncio.sleep(2.5)  # and wait to see it won't call callback
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
