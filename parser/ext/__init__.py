'''
Parser extensions. These are modules containing factory functions that take a :class:`parser.Parser` type, extend it in some way and return a new subclass; in other words, `(type[Parser]) -> type[Parser]` functions.

These are applied to the base class sequentially, like `ParserExt2(ParserExt1(Parser))` (see :meth:`parser.Parser.use`). The order is specified by the user, meaning the extension is not guaranteed to be passed the base `Parser` class.

They usually look like this::

	def Something(base: type[Parser]):
		class _Something(base):
			# overrides, etc., like:
			def _parse_list(self, *args):
				lst = super()._parse_list(*args)
				if lst[0] != '#something': return lst

				# custom logic for `(#something ...)`

		return _Something

The extension may modify the AST, log to the console, etc.; however, the regex tokenizer is explicitly left outside of `Parser` to prevent any changes.
'''

from ._include import Include
from ._aliases import Aliases
from ._out_json import OutJson
from ._short_load import ShortLoad
from ._hex_literals import HexLiterals
__all__ = ['Include', 'Aliases', 'OutJson', 'ShortLoad', 'HexLiterals']