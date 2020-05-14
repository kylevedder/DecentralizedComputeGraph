#!/usr/bin/env python3

import compute_graph
import compute_io
import incoming_handler
import time

cg = compute_graph.load("compute_graph.json")
cio = compute_io.ComputeIO()
cio.setup("node1", cg)

print(cio.send("update", [1, 2, 3]))
print(cio.send("update", [4, 5, 6]))
print(cio.send("update", [7, 8, 9]))
print(cio.send("compute"))
