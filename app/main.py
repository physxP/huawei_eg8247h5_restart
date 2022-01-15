from typing import Iterator
from net_monitor import net_usage, process_net_usage
import time
from restart import restart_router
from mega_proc import start_mega, kill_mega
from wait_mega import wait_for_mega_downloading
from utils import StreamingMovingAverage

threshold_kb = 500
threshold_trigger_time = 0
max_trigger_tigger_time = 90
sleep_timer = 5
last_iter_time = time.time()



start_mega()
time.sleep(sleep_timer)

    
wait_for_mega_downloading(threshold_kb,sleep_timer)
print('\nStarted monitoring')
average_filter = StreamingMovingAverage(10)
for usage in process_net_usage():
    average_usage = average_filter.process(usage)
    print(f'Net usage: ({int(usage)} kb/s) { int(average_usage)} kb/s > {threshold_kb} kb/s',end='\r')
    if average_usage<threshold_kb:
        threshold_trigger_time += sleep_timer
    else:
        threshold_trigger_time = 0
    



    if threshold_trigger_time>max_trigger_tigger_time:
        print(f"Detected an average usage of {average_usage} kb/s < {threshold_kb} kb/s over a duration of " 
        f"{threshold_trigger_time}s")

        usage_data = []
        threshold_trigger_time = 0
        kill_mega()
        restart_router()
        
        start_mega()
        wait_for_mega_downloading(threshold_kb,sleep_timer)
        print('Restarted monitoring...')

    
    time.sleep(sleep_timer)


    





