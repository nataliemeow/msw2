from parser import ListNode, Parser, TokenKind, StringNode, CallListNode, ConcatListNode

def Flags(base: type[Parser]):
	class _Flags(base):
		_flags: set[str]

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self._flags = set()

		def parse(self):
			result = ConcatListNode()
			while self._token.kind != TokenKind.EOF:
				item = self._parse_node()

				if (
					not isinstance(item, CallListNode) or
					len(item) == 0 or
					item[0] != '#set'
				):
					result.append(item)
					continue

				assert len(item) == 2
				assert isinstance(item[1], StringNode)
				
				self._flags.add(str(item[1]))

			return result
		
		def _parse_list(self, list_type):
			lst = super()._parse_list(list_type)

			if list_type != CallListNode: return lst
			if len(lst) == 0: return lst
			if lst[0] != '#if': return lst
			assert len(lst) == 3
			assert isinstance(lst[1], StringNode)
			
			if str(lst[1]) in self._flags:
				return lst[2]
			else:
				return ConcatListNode()

	return _Flags