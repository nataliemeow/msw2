from parser import Parser, StringNode
from typing import cast
import os.path

# TODO: detect circular includes, add limit

def Include(base: type[Parser]):
	'''Replace `(#include FILE)` with the contents of FILE.'''

	class _Include(base):
		path: str | None

		def __init__(self, *args, path=None, **kwargs):
			super().__init__(*args, **kwargs)
			self.path = os.path.abspath('.') if path is None else path
			self.parent = None

		def _parse_list(self, *args):
			lst = super()._parse_list(*args)
			if len(lst) < 2: return lst
			if not isinstance(lst[1], StringNode): return lst
			if lst[0] != '#include': return lst

			include_rel_path = cast(StringNode, lst[1])
			include_abs_path = os.path.join(
				'.' if self.path is None else os.path.dirname(self.path),
				include_rel_path
			)
			with open(include_abs_path) as f:
				parser = self.__class__(f.read())
				parser.path = include_abs_path

	return _Include