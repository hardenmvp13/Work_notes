'''

开启一个线程

python
计时器：

import threading
import time

CRANE_WORK_TIME = {crane.name: 0 for crane in io.crane_io.devices}


def crane_work_time():
    while True:
        for crane in io.crane_io.devices:
            if crane.status:
                CRANE_WORK_TIME[crane.name] += 1
        time.sleep(1)


threading.Thread(target=crane_work_time).start()


def get_crane(request):
    for crane in cranes:
        crane_dict = {}
        # 天车名称
        crane_dict["no"] = crane.name
        # 工作时间
        crane_dict["work_time"] = CRANE_WORK_TIME[crane.name]



'''

