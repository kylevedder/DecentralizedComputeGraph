#!/usr/bin/env python3

import signal
import compute_graph
import compute_io
import time

cg = compute_graph.load("compute_graph.json")
cio = compute_io.ComputeIO()


stored_info = []


def update_callback(data):
    global stored_info
    if data is not None:
      stored_info += data


def compute_callback(data):
    return stored_info


cio.set_callback("update", update_callback)
cio.set_callback("compute", compute_callback)
cio.setup("node2", cg)

is_running = True


def handler(signum, frame):
    global is_running
    is_running = False


signal.signal(signal.SIGINT, handler)

while is_running:
    time.sleep(0.1)

cio.shutdown()
