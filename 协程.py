'''
```python
import asyncio
def test(i):
    time.sleep(i)
    return i
import time
def test(i):
    print(f'test {i} start sleeping')
    time.sleep(i)
    print(f'test {i} finish sleeping')
    return i
loop = asyncio.get_event_loop()
tasks = [loop.run_in_executor(None, test, i) for i in range(3)]
test 0 start sleeping
test 0 finish sleeping
test 1 start sleeping
test 2 start sleeping
test 1 finish sleeping
test 2 finish sleeping
tasks = [loop.run_in_executor(None, test, i) for i in [4,6,8]]
test 4 start sleeping
test 6 start sleeping
test 8 start sleeping
test 4 finish sleeping
test 6 finish sleeping
test 8 finish sleeping
tasks
[<Future pending cb=[_chain_future.<locals>._call_check_cancel() at d:\python3.6\Lib\asyncio\futures.py:403]>, <Future pending cb=[_chain_future.<locals>._call_check_cancel() at d:\python3.6\Lib\asyncio\futures.py:403]>, <Future pending cb=[_chain_future.<locals>._call_check_cancel() at d:\python3.6\Lib\asyncio\futures.py:403]>]
asyncio.gather(tasks)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "d:\python3.6\Lib\asyncio\tasks.py", line 600, in gather
    for arg in set(coros_or_futures):
TypeError: unhashable type: 'list'
asyncio.gather(*tasks)
<_GatheringFuture pending>
loop.run_until_complete(asyncio.gather(*tasks))
[4, 6, 8]
loop.run_until_complete(asyncio.gather(*tasks))
[4, 6, 8]
```


'''