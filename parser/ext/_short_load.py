from parser import Parser, StringNode, CallListNode
from typing import cast
import os.path

def ShortLoad(base: type[Parser]):
  '''Replace `.VAR` with `(get VAR)`.'''

  class _ShortLoad(base):
    def _parse_node(self):
      node = super()._parse_node()
      if not isinstance(node, StringNode): return node
      if not node.startswith('.'): return node
      if len(node) == 1: return node
      
      return CallListNode([StringNode('load'), StringNode(node[1:])])

  return _ShortLoad