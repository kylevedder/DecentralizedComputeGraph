#!/usr/bin/env python3

import compute_graph
import compute_io
import incoming_handler
import time

cg = compute_graph.load("compute_graph.json")
cio = compute_io.ComputeIO()
cio.setup("node1", cg)

d =  {"dict" : "ionary"}
print(cio.send("block", d))
print(cio.send("non_block", d))