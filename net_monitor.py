import time
import psutil

def net_usage():
    old_value = 0    

    while True:
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        if old_value:
            yield (new_value - old_value)/1024

        old_value = new_value



if __name__ == '__main__':
    for i in net_usage():
        print(i)
        time.sleep(1)