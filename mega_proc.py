import psutil
import subprocess
import platform
import time

def get_matching_procs(PROCNAME = "MEGAclient"):
    return [proc for proc in psutil.process_iter() if PROCNAME.lower() in proc.name().lower()]
def kill_mega(PROCNAME = "MEGAclient"):
    print(f'Trying to kill process: {PROCNAME}')
    for proc in get_matching_procs(PROCNAME):
            print(f'Killing {proc.name()}')
            proc.kill()

def start_mega():
    print('Starting mega')
    if platform.system() == 'Darwin':
        subprocess.call(['open', '-a', 'MEGAsync'])
    else:
        raise Exception(f"Starting mega not implemented for platform{platform.system()}")
    print('Done!')
if __name__ == '__main__':
    kill_mega()
    time.sleep(3)
    start_mega()
    time.sleep(3)
    kill_mega()