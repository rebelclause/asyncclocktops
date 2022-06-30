import os, sys, pathlib
import asyncio
from enum import Enum
# Async generators
# https://peps.python.org/pep-0525/
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import time
import math
from math import floor, fmod

import tzlocal

NOW = datetime.datetime.now()

def pythonpath(file):
    """Set PYTHONPATH in the top module, or in modules under testing.
    # TODO: sys.path.insert(0, basepath), for cases where imports need a little tenderness.
    """
    #########################
    basepath = str(pathlib.Path(file).parent)
    print(f"{basepath = }")
    directory = str(pathlib.Path('.').resolve())
    print(f"{directory = }")
    parent = str(pathlib.Path('..').resolve())
    print(f"{parent = }")
    #########################
    os.environ["PYTHONPATH"] = basepath
    print("PYTHONPATH ", os.environ.get("PYTHONPATH"))

class i(Enum):
    MICROSECOND = .000001, 'us'
    MILLISECOND = MICROSECOND[0] * 1000, 'ms' 
    MSECOND = MILLISECOND[0] * 1000, 'msS'
    SECOND = 1, 'S' # Referene (1)
    MINUTE = SECOND[0] * 60, 'M'
    HOUR = MINUTE[0] * 60, 'H'
    DAY = HOUR[0] * 24, 'd'
    WEEK = DAY[0] * 7, 'w'
    MONTH = WEEK[0] * 30, 'm'
    YEAR = MONTH[0] * 12, 'y'

    def __str__(self):
        return self.value[1]

    def __int__(self):
        if self.value[0] == .000001:
            return 1000000
        else:
            return self.value[0]

    def __mul__(self, factor):
        return self.value[0] * factor 

    def __div__(self, denominator):
        return float(self.value[0] / denominator)

MICROSECONDS = i.MICROSECOND
MILLISECONDS = i.MILLISECOND
MSECONDS = i.MSECOND
SECONDS = int(i.SECOND)
MINUTES= int(i.MINUTE)
HOURS = int(i.HOUR)
DAYS = int(i.DAY)
WEEKS = int(i.WEEK)
MONTHS = int(i.MONTH)
YEARS = int(i.YEAR)


print(MICROSECONDS)

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


async def timeframe_valences():
    """All the modular clock recursions needed."""
    microsecond = float(0.000001) # 1/1000th of a millisecond, 1/1000000 of a second
    millisecond = float(microsecond * 1000) # 1/1000th of a second
    # the above categories expressed in decimal notation, below zero
    # will only work for mods in seconds having 60 regular divisions, and up the chain
    msecond = float(millisecond * 1000) # / millisecond
    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    week = day * 7 
    month = week * 30
    year = month * 12

    *valence_values, = microsecond, millisecond, msecond, second, minute, hour, day, week, month, year
    # index = [ i-1 for i,n in enumerate(valence_values) if n < interval ][0]
    *valence_labels, = 'microsecond', 'millisecond', 'msecond', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year'
    numeric_valences = dict(zip(valence_values, valence_labels))
    label_valences = {}
    for k, v in numeric_valences.items():
        label_valences[str(v)] = int(k)
    # print(valences)
    return numeric_valences, label_valences

async def timeframe_finder(interval:int):
    """Assuming all intervals are in seconds, unless or until a good algo or enum is employed, find the timeframe's scope, returning 'mode'."""
    numeric_valences, label_valences = await timeframe_valences()

    index = [i-1 for i, k in enumerate(list(numeric_valences.keys())) if k >= interval+1]
    key = list(numeric_valences.keys())[index[0]]
    # index = [(v, k) for k, v in valences.items() if k <= interval]
    # print(f"{index[-1][0]}s = {interval / index[-1][1]}")
    print()
    return numeric_valences[key]
    # return numeric_valences[index[0]]
    # return {f"{index[-1][0]}": f"{interval / index[-1][1]:.0f}"}



# def valid_interval_list(clock_len=60, interval=None):
async def valid_interval_list(interval:int):
    """Generate a 'now_unit' aware list of seconds, minutes, hours, or days on the clock spanning an interval's range until its coincident with the lowest common multiple of the clock mode."""

    clock_len=60
    num_valences, lbl_valences = await timeframe_valences()
    mode = await timeframe_finder(interval) 
    # mode = str(list(mode.keys())[0])

    print(f"{mode =}")
    if mode == 'second':
        # clock_mod = lbl_valences[mode] * 1000 #* 60 1000
        now_val = datetime.datetime.now().microsecond / 1000
        clock_len = 60 #int(clock_mod / 1000)

        *args, = clock_len, interval
        lm = await lowest_multiple(*args)
        genlist = [x for x in range(0, lm + 1, interval) if fmod(x, interval) == 0]
        
        # print(f"All clocktops: {list(clocktops)}")


        # genlist = [int(x%clock_len) for x in clocktops]
        print(f"All clocktops: {list(genlist)}")
        print()

    elif mode == 'minute':
        # clock_mod = int(lbl_valences[mode])
        now_val = datetime.datetime.now().minute # / 60
        clock_len = 60

        print(interval/MINUTES)
        interval = int(interval / MINUTES)

        *args, = clock_len, interval
        lm = await lowest_multiple(*args)
        clocktops = [x for x in range(0, lm + 1, interval) if fmod(x, interval) == 0]
        print(f"All clocktops: {list(clocktops)}")

        genlist = [int(x%clock_len) for x in clocktops]
        print(f"All clocktops: {list(genlist)}")
        print()

    elif mode == 'hour':
        # clock_mod = lbl_valences[mode]
        now_val = datetime.datetime.now().hour
        clock_len = 24

        print(interval/HOURS)
        interval = int(interval / HOURS)
        *args, = clock_len, interval
        lm = await lowest_multiple(*args)
        clocktops = [x for x in range(0, lm + 1, interval) if fmod(x, interval) == 0]
        print(f"All clocktops: {list(clocktops)}")


        genlist = [int(x%clock_len) for x in clocktops]
        print(f"All clocktops: {list(genlist)}")
        print()

    elif mode == 'day':

        # clock_mod = lbl_valences[mode]
        delta = datetime.timedelta(seconds=interval)
        now = datetime.datetime.now() #+ datetime.timedelta(days=31)
        now_val = now.day
        month = now.month
        year = now.year
        next = now + delta
        # if year < next.year: # TODO:
        #     ...
        if month < next.month:
            spanning = True
        

        def is_leap(year):
            """Determine whether a year is a leap year."""
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

        leap = 31 if is_leap(year) else 30        
        
        clock_len = 31

        # if month in [1]: # 28 or 29, which year?
        #     clock_len += leap # TODO:?
        #     real_len = 31
        if month in [1, 3, 5, 7, 8, 10, 12]: #31
            clock_len -= 31
            # real_len = 31
        elif month in [2, 4, 6, 9, 11]: #2, #30
            clock_len -= 30
            # real_len = 30
            if month in [2]:
                clock_len -= leap
        
        
        interval = int(interval / DAYS)

        # *args, = real_len, interval
        *args, = 66, interval
        lm = await lowest_multiple(*args)
        clocktops = [31-clock_len if x == 0 else x for x in range(1-clock_len, lm+1, interval)] # if fmod(x, interval) == 0]
        print(f"All clocktops: {list(clocktops)}")

        genlist = [abs(x%31-clock_len) for x in clocktops]
        genlist = [31-clock_len if x == 0 else x for x in genlist]
        print(f"All clocktops: {list(genlist)}")
        print()

    else:
        print(f"Not implemented for {mode = }")
        exit()

    t_min = genlist[min(range(len(genlist)), key = lambda i: abs(genlist[i]-now_val))]
    # t_max = genlist[max(range(len(genlist)), key = lambda i: abs(genlist[i]-now_val))]
    print(t_min)
    # print(t_max)
    # is the min closest
    tmi = genlist.index(t_min)
    # tmxi = genlist.index(t_max)
    # print(trunc_list)
    if genlist[tmi] > now_val:
        trunc_list = genlist[tmi::]
    else:
        trunc_list = genlist[tmi+1::]
    
    if mode == 'day':
        """Limit a day list to a week, then regenerate. Accommodates edge cases, including a possible later introduction of 'week'."""
        # end = int(interval/DAYS)
        trunc_list = trunc_list[0:]
    
    print(trunc_list)
    return (x for x in trunc_list), mode

    # # this gets complicated for mods beneath seconds and above hours, as the clock cycles differ, meaning inputs must be adjusted, and, well... if you're up for it, there is other work to be done first, so this is a TODO: week, month, year clock feature

    # elif mode == 'month':
    #     clock_mod = clock_mod = lbl_valences[mode] * 4
    #     now_val = datetime.datetime.utcnow().month
    # clocktops = [x for x in range(0, lm + 1, interval) if fmod(x, interval) == 0]
    # warming up to a generator
    # clocktops_pre = (x for x in range(0, lm + 1, interval) if fmod(x, interval) == 0)

    # ziptup = zip(list(genlist), [now_val for i in range(len(genlist)+ 1)])
    # closest = [abs(x+60)-y for x, y in ziptup ]
    # # print(closest)
    # nearest = [i - now_val for i in closest]
    # # print(nearest)
    # closenear = [x-y for x, y in zip(closest, nearest)]

async def lowest_multiple(*args):
    # https://stackoverflow.com/questions/147515/least-common-multiple-for-3-or-more-numbers/147539#147539
    async def lcm(x,y):
        tmp=x
        while (tmp%y)!=0:
            tmp+=x
        return tmp

    async def lcmm(*args):
        from functools import reduce
        return await reduce(lcm,args)

    return await lcmm(*args)


##################################
##################################

async def sleep_to_next_interval_clock_top(x, mode, interval):
        """setup to run schedule"""
        # a localization flaw: what if utcnow() and locale are not hour/minute compatible, ie. -4:30 instead of -5:00, yikes, this could wreak havoc if posted to the internet!!!
        now = datetime.datetime.now() # local
        next_top = x
        # mode = str(list(mode.keys())[0])
        # use delta to calculate the right hour on interval over interval hourly transitions, then swap in the calculated minute
        # except, this introduces an error if the next minute of the interval is within the hour, so calculation branches on this conditional

        # if x - interval > 0:
        #     # intervals are known to be in minutes
        #     end = now.replace(minute=x, second=3, microsecond=0)
        #     snore = end - now
        #     snore = snore.total_seconds()
        # else:
        #     # TODO: to accommodate seconds, milliseconds are necessary

        if mode == 'second':
            delta = datetime.timedelta(milliseconds=x)
            # delta = datetime.timedelta(microseconds=interval) 
            end = now + delta
            # end = end.replace(microsecond=x*1000)
            snore = end - now
            snore = snore.total_seconds()
            # snore = 
            print(f"{end =}-{now =}, {snore =}")
            print('second')

        elif mode == 'minute':
            # x = int(x / 60)
            delta = datetime.timedelta(seconds=interval)
            end = now + delta
            end = end.replace(minute=x, second=1, microsecond=0)
            snore = end - now
            snore = snore.total_seconds()
            print(f"{end =}-{now =}, {snore =}")
            print('minute')

        elif mode == 'hour':
            # x = int(x / 60)
            delta = datetime.timedelta(seconds=interval) 
            end = now + delta
            end = end.replace(hour=x, minute=0, second=1, microsecond=0)
            snore = end - now
            snore = snore.total_seconds()
            print(f"{end =}-{now =}, {snore =}")
            print('hour')

        elif mode == 'day':
            # still rather one dimensional, so if you want to choose an hour 
            # within the next start day rather than midnight, add it here
            # x = int(x / 60)
            delta = datetime.timedelta(seconds=interval) 
            end = now + delta
            end = end.replace(day=x, hour=0, minute=0, second=1, microsecond=0)
            snore = end - now
            snore = snore.total_seconds()
            print(f"{end =}-{now =}, {snore =}")
            print('day')

        else:
            raise NotImplementedError
            exit()
         # + 30
        # TODO: pass the right divisor, according to the clock_mod

        # snore_min = snore/60
        print(f"{next_top=} {snore=}")
        await asyncio.sleep(snore)

        # # problems?: started at 4:45 am...
            # it looks like the zero and sixty have been stripped... for this list should contain sixty as the final clocktop... where is it?
            # zero is clipped by virtue of it being part of the whole list, the first value, cut out by slicing... if the list running out regenerates a list having a zero and the calcs here run fine,
            # this could be the beta version...
        #     45
        #     [30, 15]
        #     next_top=30 snore=2618.85893


async def mygen(interval):
    genlist, mode = await valid_interval_list(interval)
    return genlist, mode


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


async def worker(x, mode, interval):
    from random import randint
    import random
    # x is next clocktop, the target minute for sleep
    # presently using the valid clocktop
    # TODO: reconcile seconds between start>begin to present a delta
    # FIXME:? could make this tzinfo aware and convert from utcnow() ts to tzlocal, but, for now, all times in this module, to avoid complications of internal timing, will be set relative to system local time, '.now()'
    # start = datetime.datetime.utcnow()
    start = datetime.datetime.now()
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
    await sleep_to_next_interval_clock_top(x, mode, interval)


async def itergen(interval:int):

    while True:
            # restart
        while True:
            async for x, mode in genframes(interval, mygen):

                try:
                    # i = x.send(None)
                    # print(i)
                    # await asyncio.sleep(1)
                    # task = asyncio.create_task(worker(x.send(None), interval))
                    # await task
                    # await asyncio.sleep(3)
                    await worker(x.send(None), mode, interval)

                except StopIteration as e:
                    break

async def other_generators():
    """Generators pending implementation"""
    lcm = "lowest common multiple, derived using Euclid's Algorithm"
    (x for x in range(0xAAAAAA, 0xEEEEEE, 0xBA))
    (x for x in range(0, lcm+1, interval))


if __name__ == "__main__":
    """Unit test fodder"""
    pythonpath(__file__)
    from itertools import chain
    ones = [1, 60, 3600, 86400, 604800, 18144000, 217728000]
    *odds, =  SECONDS*2,
    *odds, =  SECONDS*60, # a minute, same as MINUTES*1
    *odds, = MINUTES, #*1 #, 3601, # 1 min, 1 hour & 1 sec
    *odds, = MINUTES*60, #*1 #, 3601, # 1 min, 1 hour & 1 sec
    *odds, = HOURS, # 1 hour
    *odds, = HOURS*4, # 2 hours
    *odds, = HOURS*24, # 2 hours
    *odds, = DAYS, # 24 hours
    *odds, = DAYS*3, # 24 hours
    # *odds, = DAYS*4, # 24 hours
    *odds, = i.MINUTE*7,

    # asyncio.run(symbol_slice("BTC/USD"))
    # for i in chain(ones, odds):
        # print(asyncio.run(timeframe_finder(i)))
    # for i in chain(ones, odds):
        # print(asyncio.run(clocktops_in_minutes(i)))

    # for i in chain(ones, odds):
    for i in odds:
        print(asyncio.run(itergen(i)))


    # *args, = 24, 60, 60
    # lowest_multiple(*args) 

    # Set the stage to know what clock cycle an interval entered in seconds is, so corresponding interval list can be generated with snooze in seconds to the next interval on the job runner. Multiple jobs are supported without a queue as each is entered and started immedaitely, running on the event loop. No cancel is currently supported, which makes this a kind of on/off piece of software.

    interval = 13
    asyncio.run(itergen(interval))
    
    # i = 24
    # # print(f'with lcf {i = }: {valid_interval_list(60, i)}')
    # print(f'w/o lcf {i = }: {valid_interval_list(60, i)}')
    
    # i = 9
    # # print(f'with lcf {i = }: {valid_interval_list(60, i))}')
    # print(f'w/o lcf {i = }: {valid_interval_list(60, i)}')
    
    # print(valid_interval_list(60, 9))
    # # lcf of x and 60 is the interval for the purposes of producing a minutes list which repeats
    # print(valid_interval_list(60, 24))
    # print(valid_interval_list(240, 24))
    # print(valid_interval_list(24, 2))
    # l = valid_interval_list(31, 7) # but what if it starts on a different date???q song of the ages...
    # print(l)
    # l = [x * 5 for x in l]
    # print(l)
    # print(elapsed_time(30))
    # print(elapsed_time(60))
    # print(elapsed_time(90))
    # print(elapsed_time(3600))
    # print(elapsed_time(3720))
    # print(elapsed_time(36030))
    # print(elapsed_time(363063))
    # print(elapsed_time(436306200)) #, floor=False))
    # print(elapsed_time(436306200, floor=False))


