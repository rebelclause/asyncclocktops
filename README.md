# Async Clocktops Task Runner (ACTR)

First beta release of ACTR.

Some uses for ACTR may include:

  - Scheduling and running recurring tasks in millisecond, second, minute, hour and day intervals.  which don't require cancellation at any point.

If you find a bug, please report it.


## Feature Possibilities

  - Thorough tests.

  - As with possible uses, from above:
    - cancel inner task(s);
    - cancel outer generator.

  - Integrations
    - framework plugin;
    - or, modular import elsewise.


## Extra Verbiage

ACTR presents a method for creating and using an async generator and its corresponding consuming async for loop to run tasks on recurring intervals.

Its overkill presumptively presents the next valid clock top for delay adjustments to a post-task `asyncio.sleep()`, aptly named 'snooze' in the code.

A simpler use of the generator, in list form perhaps, might be to check if a task is late, comparing its completion minute; however, that logic also spins out with respect to other contextual conditionals, not the least of which is then having to know which is the valid minute, which is the next...

If the task is late, the snooze will be negative, kicking off another run immediately...

So, there is no real load balancing act stub available here; if there is a kludge, tasks will blindly dive into it, possibly exacerbating whatever timing issue there is. 

It's not likely to happen if long running io, or long running processing are parallelized. Asyncio makes this possible with Python's concurrent futures Executor class, simplifying thread and multiprocessing task runs while the remainder of a concurrent program ticks along, stopping in those parts only where results from long running tasks are expected.

At least two major points of data flow constriction are present despite there being room for parallelism. These aren't discussed in great detail, though it can be said they mainly arise around how your dependencies stack up against each other, and whether separation of concerns takes into account long delays if there is tight coupling. 

Async used here schedules tasks of a similar nature concurrently, entering them onto the event loop so the chaining of sequences can then await results from other coroutines in a chain before continuing to an end, making it easier to schedule multiple categories of tasks simultaneously, and have some move forward if others are held back waiting on results. As earlier mentioned, parallelism can be included within the generator's looping through tasks. 

Since tasks which may use parallelism in this way will be on the event loop together, and interprocess and thread communications are well handled by Python's async implementation, any specifying of microprocessors to the multiprocessing executor might require awareness of how many multiprocessing sessions have been started at the same time.


## Userful Resources

[Conditional list comprehensions and other examples](https://towardsdatascience.com/lets-learn-list-comprehension-with-a-lots-of-examples-efficient-python-programming-98fb41813d7)

[Python Docs: Sorting HOWTO:](https://docs.python.org/3.10/howto/sorting.html#sortinghowto)

[List compreshension - find a given k in list using min](https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/)

[Lowest Common Multiple: Euclid's Algorithm](https://stackoverflow.com/questions/147515/least-common-multiple-for-3-or-more-numbers/147539#147539)

[Leap Year on Wikipedia](https://en.wikipedia.org/wiki/Leap_year)

[How to do math on the Linux command line](https://www.networkworld.com/article/3268964/how-to-do-math-on-the-linux-command-line.html)
