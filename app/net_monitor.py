import platform
import subprocess
import time
import psutil
import pandas as pd
from io import StringIO

from mega_proc import get_matching_procs
def net_usage():
    old_value = 0    

    while True:
        new_value =psutil.net_io_counters().bytes_recv

        if old_value:
            yield (new_value - old_value)/1024

        old_value = new_value


def process_net_usage():
    old_usage = -1
    procs = []
    check_procs = True
    while True:
        if check_procs:
            procs = get_matching_procs("MEGAclient")
           
        if len(procs)>0:
            if not procs[0].is_running():
                check_procs=True
                continue
            if platform.system() == 'Darwin':
                out = subprocess.run( f"nettop -Pp {procs[0].pid} -J bytes_in -L 1 -x -d".split(" "),capture_output=True)
                output = out.stdout.decode('ascii')
                df = pd.read_table(StringIO(output,newline='\n'),sep=',')
                bytes = df['bytes_in'].to_list()
                if len(bytes)>0:
                    usage =  int(bytes[0])/1024
                    if old_usage ==-1:
                        old_usage = usage
                    if abs(usage-old_usage)<10:
                        yield 0
                    else:
                        yield usage
                    old_usage = usage
                else:
                    continue
                
            else:
                raise Exception(f"Not implemented for {platform.system()}")
            check_procs = False
        else:
            check_procs = True
def process_net_usage_sample(n=5):
    usage_gen  = process_net_usage()
    for i in range(n-1):
        next(usage_gen)
    return next(usage_gen)


if __name__ == '__main__':
    print(process_net_usage_sample())