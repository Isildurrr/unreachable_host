import subprocess
import concurrent.futures
import time
import sys
import os
import threading
import io


file_lock = threading.Lock()

def ping_host(host):
    is_unsuccessful_file = "problemuri_hosti.txt"


    if not os.path.exists(is_unsuccessful_file):
        with open(is_unsuccessful_file, "w"):
            pass

    command = ["ping", "-t", host]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

    start_time = time.time()
    elapsed_time = 0
    timeout = 300  # 5 wuti wamebshi
    is_host_responding = True

    try:
        while True:
            output = process.stdout.readline()
            if not output:
                break
            print(f"{host}: {output.strip()}", flush=True)


            if "Request timed out" in output or "Destination host unreachable" in output:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    is_host_responding = False
    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()

    if not is_host_responding:
        with file_lock:
            with io.open(is_unsuccessful_file, "a", buffering=1) as file:
                file.write(f"{current_time}: {host}\n")

if __name__ == "__main__":
    hosts = ["10.1.1.1", "10.1.1.1", "10.1.1.1"]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ping_host, host) for host in hosts]


        concurrent.futures.wait(futures)