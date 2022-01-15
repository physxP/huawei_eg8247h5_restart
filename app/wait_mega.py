import time
import sys
from utils import StreamingMovingAverage
from net_monitor import process_net_usage
def wait_for_mega_downloading(threshold_kb,sleep_timer):
    avg_filt = StreamingMovingAverage(10)
    print('Waiting for mega to start downloading...')
    for usage in process_net_usage():
        avg_usage =  avg_filt.process(usage)

        if avg_usage>threshold_kb:
            print(f'Detected mega internet usage of {avg_usage} kb/s')
            break
        print(f'Net usage: ({int(usage)} kb/s) { int(avg_usage)} kb/s < {threshold_kb} kb/s',end='\r')
        time.sleep(sleep_timer)
if __name__=='__main__':
    wait_for_mega_downloading(500,5)
    print('Mega started download')
