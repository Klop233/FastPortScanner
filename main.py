# coding = utf-8

import socket
import time
import threading
import sys
import os
import traceback

lock = threading.Lock()
unscanned_port = []
scanned_port = []
open_port = {}  # port : thread num


# If the port is open return true
def scan(host: str, port: int, timeout=1000) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout / 1000)
    # Connect
    try:
        result = sock.connect_ex((host, port))
    except Exception as e:
        print(f"Error while scanning port {port}")
        traceback.print_exc()
    return result == 0


def pick_task(host: str, thread_num: int):
    port = 0  # Port that is being scanned
    while True:
        if len(unscanned_port) == 0:
            return
        with lock:
            # Pick a port to scan and remove it from unscanned port list
            port = unscanned_port[0]
            unscanned_port.remove(port)
        if (scan(host, port)):
            # print(f"Thread {thread_num} discovered an open port: {port}")
            open_port[port] = thread_num
        scanned_port.append(port)


def run():
    print("Fast Port Scanner by Klop233")
    host = input("Host: ")
    threads = input("Threads(default=100): ")  # Default is 100
    threads = 100 if threads == "" else int(threads)
    timeout = input("Timeout(ms, default=1000): ")
    timeout = 1000 if timeout == "" else int(timeout)  # Default is 1000

    t = time.time()

    print("Creating threads")
    thread_pool = []
    for i in range(threads):
        thread_pool.append(
            threading.Thread(target=pick_task, args=(host, i))
        )

    for i in range(65535):
        unscanned_port.append(i+1)

    print("Staring Threads")
    for i in thread_pool:
        i.start()

    print("Threads started")
    while True:
        if len(unscanned_port) == 0:
            print(f"Complete! Spent {time.time() - t:.3f} sec")
            print(f"Summary: Open ports: {len(open_port)}")
            print(f"{open_port.keys()}")
            sys.exit()

        # Clear terminal
        os.system("cls||clear")
        print(f"Host: {host} | Threads: {threads} | Timeout: {timeout}")
        print(
            f"Unscanned: {len(unscanned_port)} | Scanned: {len(scanned_port)} | Open: {len(open_port)}")
        for i in open_port.keys():
            print(f"Open Port | Thread: {open_port[i]} | Port: {i}")

        time.sleep(1)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        sys.exit()
else:
    print("Sorrt, this is the entry of a program")
