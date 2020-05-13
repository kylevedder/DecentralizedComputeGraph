#!/usr/bin/env python3

import compute_graph
import compute_io

cg = compute_graph.load("compute_graph.json")
cio = compute_io.ComputeIO()
cio.setup("node1", cg)

d =  {"dict" : "ionary"}
cio.send_await("block", d)