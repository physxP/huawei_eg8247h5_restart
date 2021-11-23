from typing import Iterator
from net_monitor import net_usage
import time
from restart import restart_router
from mega_proc import start_mega, kill_mega

threshold_kb = 500
threshold_trigger_time = 0
max_trigger_tigger_time = 30
sleep_timer = 5
last_iter_time = time.time()
usage_data = []



start_mega()
time.sleep(sleep_timer)

for usage in net_usage():
    usage_data.append(usage)
    average_usage = sum(usage_data)/len(usage_data)
    if average_usage<threshold_kb:
        threshold_trigger_time += sleep_timer
    else:
        threshold_trigger_time = 0



    if threshold_trigger_time>max_trigger_tigger_time:
        print(f"Detected an average usage of {average_usage} kb/s over a duration of " 
        f"{threshold_trigger_time}s")

        usage_data = []
        threshold_trigger_time = 0
        kill_mega()
        restart_router()
        start_mega()
        time.sleep(120)
        print('Restarted monitoring...')

    
    time.sleep(sleep_timer)


    





