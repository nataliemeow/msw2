from parser import Parser, CallListNode, ConcatListNode, StringNode
from typing import cast
import json

def OutJson(base: type[Parser]):
	'''Convert `#out_json [KEY VALUE]...` files to `{KEY: VALUE...}` JSON strings. Meant to facilitate importing into natta-ric.'''

	class _OutJson(base):
		def parse(self):
			lst = super().parse()
			if len(lst) == 0: return lst
			if lst[0] != '#out_json': return lst
			
			out = {}
			for defn in lst[1:]:
				assert isinstance(defn, ConcatListNode)
				assert len(defn) == 2
				name, value = defn
				assert isinstance(name, StringNode)
				out[str(name)] = value.emit()
			return StringNode(json.dumps(out, indent=2))

	return _OutJson