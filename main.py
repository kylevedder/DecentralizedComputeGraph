#!/usr/bin/env python3

import compute_graph
import argparse

def make_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("node_name")
  return parser.parse_args()
args = make_args()
print(args.node_name)

cg = compute_graph.load("compute_graph.json")

print(cg)

