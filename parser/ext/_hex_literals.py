from parser import Parser, StringNode, CallListNode
from typing import cast
import os.path

# TODO: detect circular includes, add limit

def HexLiterals(base: type[Parser]):
  '''Converts `0x...` and `-0x...` strings to decimal.'''

  class _HexLiterals(base):
    def _parse_node(self):
      node = super()._parse_node()
      if not isinstance(node, StringNode): return node
      if not node.startswith(('0x', '-0x')): return node
      if len(node) == 2: return node
      
      sign = -1 if node[0] == '-' else 1
      hex_str = node[1:] if sign == -1 else node
      return StringNode(sign * int(hex_str, 16))

  return _HexLiterals