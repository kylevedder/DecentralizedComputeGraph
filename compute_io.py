import compute_graph
import outgoing_handler
import incoming_handler

class ComputeIO:
    def __init__(self):
        self._callbacks = {}

        self._outgoing = {}
        self._incoming = {}

    def set_callback(self, name: str, callback):
        self._callbacks[name] = callback

    def _validate_callbacks(self, node_name: str, cg: compute_graph.ComputeGraph):
        # Validate all graph callbacks set.
        for c in cg.connections:
            if c.dest_name == node_name:
                cb = self._callbacks.get(c.name, None)
                if cb is None:
                    print(
                        "Missing callback for compute graph connection", c.name)
                    return False
                if c.dest_name != node_name:
                    print("Callback set for connection", c.name,
                          " but", node_name, "is not the destination")
                    return False
        return True

    def _setup_outgoing(self, node_name: str, cg: compute_graph.ComputeGraph):
        for c in cg.connections:
            if c.src_name == node_name:
              self._outgoing[c.name] = outgoing_handler.OutgoingHandler(c.dest.ip, c.port)
                
    def _setup_incoming(self, node_name: str, cg: compute_graph.ComputeGraph):
        for c in cg.connections:
            if c.dest_name == node_name:
              self._incoming[c.name] = incoming_handler.IncomingHandler(c.dest.ip, c.port, self._callbacks[c.name])
              self._incoming[c.name].start()

    def setup(self, node_name: str, cg: compute_graph.ComputeGraph):
        if not cg.consistent:
            print("ComputeGraph not consistent")
            return
        if not self._validate_callbacks(node_name, cg):
            return

        self._setup_outgoing(node_name, cg)
        self._setup_incoming(node_name, cg)

    def shutdown(self):
      for ih in self._incoming.values():
        ih.stop()

    def send(self, connection_name: str, data):
      return self._outgoing[connection_name].send(data)

