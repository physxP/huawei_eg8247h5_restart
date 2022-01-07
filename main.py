from typing import Iterator
from net_monitor import net_usage, process_net_usage
import time
from restart import restart_router
from mega_proc import start_mega, kill_mega

class StreamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0

    def process(self, value):
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)
        return float(self.sum) / len(self.values)

threshold_kb = 500
threshold_trigger_time = 0
max_trigger_tigger_time = 90
sleep_timer = 5
last_iter_time = time.time()



start_mega()
time.sleep(sleep_timer)
def wait_for_mega_downloading():
    avg_filt = StreamingMovingAverage(10)
    print('Waiting for mega to start downloading...')
    for usage in process_net_usage():
        avg_usage =  avg_filt.process(usage)

        if avg_usage>threshold_kb:
            print(f'Detected mega internet usage of {avg_usage} kb/s')
            break
        print(f'Net usage: ({int(usage)} kb/s) { int(avg_usage)} kb/s < {threshold_kb} kb/s',end='\r')
        time.sleep(sleep_timer)
    
wait_for_mega_downloading()
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
        wait_for_mega_downloading()
        print('Restarted monitoring...')

    
    time.sleep(sleep_timer)


    





