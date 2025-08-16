from parser import Parser, StringNode, CallListNode, ListNode
from typing import cast
import glob
import os.path

# TODO: detect circular includes, add limit

def Include(base: type[Parser]):
	'''Replace `(#include FILE)` with the contents of FILE.'''

	class _Include(base):
		_dir_path: str

		def __init__(self, *args, path=None, **kwargs):
			super().__init__(*args, **kwargs)
			self._dir_path = os.path.abspath('.' if path is None else os.path.dirname(path))

		def _load(self, rel_path: str):
			parser = None
			with open(os.path.join(self._dir_path, rel_path)) as f:
				parser = self.__class__(f.read())
			parser._dir_path = self._dir_path
			return parser.parse()
		
		def _modify_list(self, lst: ListNode):
			new_lst = lst.__class__()

			for item in lst:
				if (
					not isinstance(item, CallListNode) or
					len(item) == 0 or
					item[0] != '#include_merge'
				):
					new_lst.append(item)
					continue

				assert len(item) == 2
				assert isinstance(item[1], StringNode)

				for path in glob.iglob(item[1], root_dir=self._dir_path):
					new_lst.extend(self._load(path))
			
			return new_lst
		
		def parse(self):
			return self._modify_list(super().parse())

		def _parse_list(self, list_type):
			lst = self._modify_list(super()._parse_list(list_type))

			if list_type != CallListNode: return lst
			if len(lst) == 0: return lst
			if lst[0] != '#include': return lst
			assert len(lst) == 2
			assert isinstance(lst[1], StringNode)

			return self._load(lst[1])


	return _Include