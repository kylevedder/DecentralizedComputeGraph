#!/usr/bin/env python3
import sys
sys.path.append("..")

import time
import incoming_handler
import compute_io
import compute_graph


cg = compute_graph.load("compute_graph.json")
cio = compute_io.ComputeIO()
cio.setup("node1", cg)


def check_success(res):
    success, payload = res
    if not success:
        print("Send failed!")
    else:
        print(payload)


check_success(cio.send("update", {"key1": "value1"}))
check_success(cio.send("update", {"key2": "value2"}))
check_success(cio.send("update", {"key3": "value3"}))
check_success(cio.send("compute"))
