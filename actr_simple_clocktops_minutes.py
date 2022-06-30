import asyncio
# Async generators
# https://peps.python.org/pep-0525/
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import time
import math
from math import floor, fmod

NOW = datetime.datetime.utcnow()

def elapsed_time(time_in_seconds=0, floor=True):
    if time_in_seconds != 0:
        years = fmod(time_in_seconds / (3600 * 24 * 7 * 4 * 12), 1)
        months = fmod(time_in_seconds / (3600 * 24 * 7 * 4), 12)
        weeks = fmod(time_in_seconds / (3600 * 24 * 7), 4)
        days = fmod(time_in_seconds / (3600 * 24), 7)
        hours = fmod(time_in_seconds / 3600, 24)
        minutes = fmod(time_in_seconds / 60, 60)
        seconds = fmod(time_in_seconds, 60)
        if floor:
            return math.floor(weeks), math.floor(days), math.floor(hours), math.floor(minutes), math.floor(seconds)
        return (years, months, weeks, days, hours, minutes, seconds)
    return None


def valid_interval_list(interval, clock_len=60):
    """Generate a 'now_minute' aware list of minutes on the clock spanning an interval's range until its coincident with the lowest common multiple of the clock"""
    *args, = 60, interval
    lm = lowest_multiple(*args)
    clocktops = [x for x in range(0, lm + 1, interval) if fmod(x, interval) == 0]
    print(f"All clocktops: {list(clocktops)}")
    genlist = [i%clock_len for i in clocktops]
   
    now_minute = datetime.datetime.utcnow().minute
    # https://docs.python.org/3.10/howto/sorting.html#sortinghowto
    # https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
    t_min = genlist[min(range(len(genlist)), key = lambda i: abs(genlist[i]-now_minute))]
    # t_max = genlist[max(range(len(genlist)), key = lambda i: abs(genlist[i]-now_minute))]
    print(t_min)
    # is the min closest
    tmi = genlist.index(t_min)
    # tmxi = genlist.index(t_max)
    if genlist[tmi] > now_minute:
        trunc_list = genlist[tmi::]
    else:
        trunc_list = genlist[tmi+1::]

    print(trunc_list)
    return (x for x in trunc_list)


def lowest_multiple(*args):
    """Lowest multiple."""
    def lcm(x,y):
        tmp=x
        while (tmp%y)!=0:
            tmp+=x
        return tmp

    def lcmm(*args):
        from functools import reduce
        return reduce(lcm,args)

    return lcmm(*args)


async def sleep_to_next_interval_clock_top(x, interval):
        """setup to run schedule"""
        now = datetime.datetime.now() # local
        next_top = x
        if x - interval > 0:
            end = now.replace(minute=x, second=3, microsecond=0)
        else:
            delta = datetime.timedelta(minutes=interval) 
            end = now + delta
            end = end.replace(minute=x, second=3, microsecond=0)
        snore = end - now
        snore = snore.total_seconds() # + 30
        snore_min = snore/60
        print(f"{next_top=} {snore=}")
        await asyncio.sleep(snore)


async def mygen(interval):
    return valid_interval_list(interval)


async def genframes(interval:int=None, func=None):
    while True:
        g = await func(interval)
        # print("{g = }")
        while g:
            try:
                yield g
            except StopIteration as e:
                # g.send(0)eration as e:
                # g.send(0)
                break


async def worker(x, interval):
    from random import randint
    import random
    # x is next clocktop, the target minute for sleep
    # presently using the valid clocktop
    # TODO: reconcile seconds between start>begin to present a delta
    start = datetime.datetime.utcnow()
    us = start.microsecond
    ms = us / 1000000
    s = start.second
    s_as_us = s / 1000000
    diff = (x/1000000) - us
    delta = datetime.timedelta(microseconds=diff)
    *fx, = f"{x =}", f"{start = }", f"{s_as_us = }", f"{s = }", f"{ms = }", f"{us = }", f"{diff = :.0f}", f"{diff = }", f"{delta = }"
    await asyncio.sleep(random.random())
    # print(fx)
    # await asyncio.sleep(5)
    await sleep_to_next_interval_clock_top(x, interval)


async def itergen(interval):

    while True:
            # restart
        while True:
            async for x in genframes(interval, mygen):
                try:
                    # i = x.send(None)
                    # print(i)
                    # await asyncio.sleep(1)
                    # task = asyncio.create_task(worker(x.send(None), interval))
                    # await task
                    # await asyncio.sleep(3)
                    await worker(x.send(None), interval)

                except StopIteration as e:
                    break


if __name__ == "__main__":
    # *args, = 24, 60, 60
    # lowest_multiple(*args)

    interval = 7
    asyncio.run(itergen(interval))
    

