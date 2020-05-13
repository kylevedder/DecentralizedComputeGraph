#!/usr/bin/env python3

import compute_graph
import compute_io

cg = compute_graph.load("compute_graph.json")
cio = compute_io.ComputeIO()

def async_callback():
  print("async_callback")

def await_callback():
  print("await_callback")

cio.set_async_callback("non_block", async_callback)
cio.set_await_callback("block", await_callback)
cio.setup("node2", cg)