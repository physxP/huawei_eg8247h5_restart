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
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        if old_value:
            yield (new_value - old_value)/1024

        old_value = new_value


def process_net_usage():
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
                out = subprocess.run( f"nettop -Pp {procs[0].pid} -J bytes_in -L 1 -x".split(" "),capture_output=True)
                output = out.stdout.decode('ascii')
                df = pd.read_table(StringIO(output,newline='\n'),sep=',')
                yield int(df['bytes_in'])/1024
                
            else:
                raise Exception(f"Not implemented for {platform.system()}")
            check_procs = False
        else:
            check_procs = True
    
if __name__ == '__main__':
    for i in process_net_usage():
    # while True:
        print(i)
        time.sleep(1)