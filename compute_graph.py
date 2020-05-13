import json
from typing import Dict
from enum import Enum

class ComputeNode:
  
  def __init__(self, cfg: Dict[str, str]):
    self.name = cfg["name"]
    self.ip = cfg["ip"]

  def __str__(self):
    return "(name: " + str(self.name) + ", ip: " + str(self.ip) + ")"


class ConnectionType(Enum):
  ASYNC = 0
  AWAIT = 1

class ComputeConnection:

  def __init__(self, nodes_lookup : Dict[str, ComputeNode], port : int, cfg: Dict[str, str]):
    self.consistent = True
    self.name = cfg["name"]
    self.src_name = cfg["src"]
    self.port = port
    try:
      self.src = nodes_lookup[self.src_name]
    except KeyError:
      print("Unknown src name:", self.src_name)
      self.consistent = False
    self.dest_name = cfg["dest"]
    try:
      self.dest = nodes_lookup[self.dest_name]
    except KeyError:
      print("Unknown dest name:", self.dest_name)
      self.consistent = False
    self.type = ConnectionType.ASYNC if cfg["type"] == "async" else ConnectionType.AWAIT

  def __str__(self):
    return "(name: " + self.name + ", src: " + self.src_name + ", dest: " + self.dest_name + ", type: " + str(self.type) + " port: " + str(self.port) +")"

class ComputeGraph:
  def __init__(self, cfg: Dict[str, str]):    
    kStartingPort = 8001
    self.nodes = [ComputeNode(n) for n in  cfg["nodes"]]
    self.nodes_lookup = {n.name : n for n in self.nodes}
    self.connections = [ComputeConnection(self.nodes_lookup, kStartingPort + idx, n) for idx, n in enumerate(cfg["connections"])]
    self.consistent = all([c.consistent for c in self.connections])

  def __str__(self):
    return "(consistent: " + str(self.consistent) + ", nodes: [" + ", ".join([str(n) for n in self.nodes]) + "], connections: [" + ", ".join([str(n) for n in self.connections]) + "])"


def load(filepath : str):
  with open(filepath) as f:
    cfg = json.load(f)
    return ComputeGraph(cfg)
    