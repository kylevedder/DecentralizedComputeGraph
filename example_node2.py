#!/usr/bin/env python3

import signal
import compute_graph
import compute_io
import time

cg = compute_graph.load("compute_graph.json")
cio = compute_io.ComputeIO()


def async_callback(data):
    print(data)
    data["goodbye"] = "world"


def await_callback(data):
    print(data)
    data["hello"] = "world"
    return data


cio.set_callback("non_block", async_callback)
cio.set_callback("block", await_callback)
cio.setup("node2", cg)

is_running = True


def handler(signum, frame):
    global is_running
    is_running = False


signal.signal(signal.SIGINT, handler)

while is_running:
  time.sleep(0.1)

cio.shutdown()
