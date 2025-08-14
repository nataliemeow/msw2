from parser import Parser, StringNode, CallListNode

# TODO: modularize this further?

_assign_ops = {
	'+': 'add',
	'-': 'subtract',
	'*': 'multiply',
	'/': 'divide',
	'%': 'mod',
	'**': 'pow',
	'&&': 'and',
	'||': 'or'
}

def Aliases(base: type[Parser]):
	'''Random aliases.'''

	class _Aliases(base):
		def _parse_list(self, list_type):
			lst = super()._parse_list(list_type)
			if list_type != CallListNode: return lst
			if len(lst) == 0: return lst

			base = lst[0]
			if not isinstance(base, StringNode): return lst
			
			new = base
			match base:
				case 'set': new = 'store'
				case 'get': new = 'load'
				case 'get_or': new = 'get'
				case 'del': new = 'drop'
				case '==': new = 'equal'
				case '<': new = 'less'
				case '>':
					new = 'greater'
					lst[1], lst[2] = lst[2], lst[1]
				case '!': new = 'not'
				case ',': new = 'unescape' # after lisp
				case _:
					op = _assign_ops.get(base)
					if op is not None:
						new = op

			lst[0] = StringNode(new)
			return lst

	return _Aliases