import compute_graph
import requests 
import pickle

class ComputeIO:
  def __init__(self):
    self._await_callbacks = {}
    self._async_callbacks = {}
    self._await_outputs = {}
    self._async_outputs = {}

  def set_async_callback(self, name: str, callback):
    self._async_callbacks[name] = callback

  def set_await_callback(self, name: str, callback):
    self._await_callbacks[name] = callback

  def _validate_callbacks(self, node_name : str, cg : compute_graph.ComputeGraph):
    # Validate all graph callbacks set.
    for c in cg.connections:
      if c.dest_name == node_name:
        if c.type == compute_graph.ConnectionType.AWAIT:
          cb = self._await_callbacks.get(c.name, None)
          if cb is None:
            print("Missing await callback for compute graph connection", c.name)
            return False
          if c.dest_name != node_name:
            print("Callback set for connection", c.name, " but", node_name, "is not the destination")
            return False
        else:
          cb = self._async_callbacks.get(c.name, None)
          if cb is None:
            print("Missing async callback for compute graph connection", c.name)
            return False
          if c.dest_name != node_name:
            print("Callback set for connection", c.name, " but", node_name, "is not the destination")
            return False
    return True

  def setup(self, node_name : str, cg : compute_graph.ComputeGraph):
    if not cg.consistent:
      print("ComputeGraph not consistent")
      return
    if not self._validate_callbacks(node_name, cg):
      return

    # Setup lambdas for all outgoing connections
    for c in cg.connections:
      if c.src_name == node_name:
        if c.type == compute_graph.ConnectionType.AWAIT:
          self._await_outputs[c.name] = "http://{}:{}".format(c.dest.ip, c.port)
        else:
          self._async_outputs[c.name] = "http://{}:{}".format(c.dest.ip, c.port)


  def send_await(self, name: str, data):
    print(self._await_outputs)
    url = self._await_outputs[name]
    datas = pickle.dumps(data)
    try:
      res = requests.post(url=url, data=datas)
    except requests.exceptions.ConnectionError:
      return False, None
    print(res)
    

