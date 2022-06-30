import os, sys, pathlib
import asyncio
from enum import Enum
import datetime
from math import fmod

# from database import table_namer

NOW = datetime.datetime.utcnow()

def pythonpath(file):
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

async def snooze_calc(start_utc:int=None, end_utc:int=None, interval:int=None):
    """Simple timer delay based on interval.
    :: params :: interval: int in seconds
    Produces:
        start_utc:
        end_utc: not aptly named as this is the slice     
    """

    now = NOW
    start_offset_in_minutes = (interval / 60) * 24

    nowminute = int(now.minute / interval) * interval
    print(f"{nowminute = }")

    if start_utc:
        pass
    else:
        # start_utc = datetime.datetime.utcnow() - timedelta(minutes=mins) 
        start_utc = now - timedelta(minutes=start_offset_in_minutes) 
        print(f"{start_utc}")

    if end_utc:
        pass
    else:
        try:
            end_utc = now.replace(minute=nowminute, second=10, microsecond=0) # nowminute + 1
            print(f"{end_utc = }")
        except Exception as e:
            print(e)
    freq = f'{interval}m' 

    # print(f"{start_utc = } {end_utc = }")

    # convert to unix time
    start = pd.Timestamp(start_utc).value // 10e8
    end = pd.Timestamp(end_utc).value // 10e8
    
    return start, end


class side(Enum):

    # BUY, SELL, EXIT = Buy, Sell, Exit = range(3)

    BUY = 0, 'buy'
    SELL = 1, 'sell'
    EXIT = 2, 'exit'
 
    def __int__(self):
        return self.value[0]
    
    def __str__(self):
        return self.value[1] 

async def timeframe_valences():
    """All the modular clock recursions needed."""
    microsecond = 1000000 # 1/1000th of a millisecond, 1/1000000 of a second
    millisecond = microsecond * .001 # 1/1000th of a second
    # the above categories expressed in decimal notation, below zero
    second = millisecond * .001 # 1000 / millisecond
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    week = day * 7 
    month = week * 30
    year = month * 12

    *valence_values, = millisecond, second, minute, hour, day, week, month, year
    # index = [ i-1 for i,n in enumerate(valence_values) if n < interval ][0]
    *valence_labels, = 'millisecond', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year'
    valences = dict(zip(valence_values, valence_labels))
    # print(valences)
    return valences

async def timeframe_finder(interval:int):
    """Assuming all intervals are in seconds, unless or until a good algo or enum is employed, find the timeframe's scope."""
    valences = await timeframe_valences()

    index = [(v, k) for k, v in valences.items() if k <= interval]
    # index = [(v, k) for k, v in valences.items() if k <= interval]
    # print(f"{index[-1][0]}s = {interval / index[-1][1]}")
    
    return {f"{index[-1][0]}": f"{interval / index[-1][1]:.0f}"}

    # print(f"\
        # {second = },\
        # {minute = },\
        # {hour = },\
        # {day = },\
        # {week = },\
        # {month = }\
        # {year = }\
        # ")


async def clocktops_in_minutes(interval:int):
    """Clocktops in minutes as targets for local conversion to seconds for loop delay recalculations."""
    # let's say I have a minute of 196, and I want to know, assuming the clock starts at 0 preceding all other preceding intervals, what time in hour minutes that is
    # 196 % 60 = 16
    # 150 % 60 = 30
    # 120 % 60 = 0

    valences = await timeframe_valences()
    mode = await timeframe_finder(interval)  
    # print(f"mode:{mode = } {int(list(mode.values())[0])}")
    clocktops = [i for i in range(60+1) if fmod(60*60, interval) == 0.0] #fmod
    return mode, interval, clocktops, 

async def symbol_slice(symbol):
    base, *sep, quote = symbol.split("/")
    print(base, sep, quote)
    return base, sep, quote

if __name__ == "__main__":
    pythonpath(__file__)
    from itertools import chain
    ones = [1, 60, 3600, 86400, 604800, 18144000, 217728000]
    *odds, = .000999, .999, 2, 61, 3601, 86401, 1200, 36000, 2200, 1234567891211
    # asyncio.run(symbol_slice("BTC/USD"))
    # for i in chain(ones, odds):
        # print(asyncio.run(timeframe_finder(i)))
    for i in chain(ones, odds):
        print(asyncio.run(clocktops_in_minutes(i)))
