from parser import Parser, CallListNode, ConcatListNode, StringNode
from typing import cast
import json

def OutJson(base: type[Parser]):
	'''Convert `(#out_json [key value]...)` lists to `{"key": "value"...}` strings. Meant to facilitate importing into natta-ric.'''

	class _OutJson(base):
		def _parse_list(self, list_type):
			lst = super()._parse_list(list_type)
			if list_type != CallListNode: return lst
			if len(lst) == 0: return lst
			if lst[0] != '#out_json': return lst
			
			out = {}
			for defn in lst[1:]:
				assert isinstance(defn, ConcatListNode)
				assert len(defn) == 2
				name, value = defn
				assert isinstance(name, StringNode)
				out[str(name)] = repr(value)
			return StringNode(json.dumps(out))

	return _OutJson