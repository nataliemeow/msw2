import re
import base64
from typing import Iterator, Callable
from enum import Enum
from dataclasses import dataclass

class TokenKind(Enum):
	EOF = 0
	STRING = 1
	VERBATIM_STRING = 2
	PAREN = 3
	BRACKET = 4
	QUOTE = 5
	COMMENT = 6

@dataclass
class Token:
	kind: TokenKind
	value: str

type Node = StringNode | QuotedNode | ListNode

class StringNode(str):
	def __repr__(self):
		if _symbol_re.search(self):
			return f'"{bytes(self, encoding='unicode_escape').decode('utf-8')}"'
		return str(self)
	
	def emit(self):
		return str(self)

def _b64_encode(src: str):
	trail = len(src) % 3
	if trail == 1: src += '[/  ]'
	elif trail == 2: src += '[/ ]'
	return base64.b64encode(bytes(src, 'utf-8')).decode('utf-8')

@dataclass
class QuotedNode():
	quote: str
	value: Node

	def __repr__(self):
		return f'{self.quote}{self.value}'
	
	def emit(self):
		if self.quote == '\'':
			return _b64_encode(self.value.emit())
		elif self.quote == ',':
			return f'[base64.decode/{self.value.emit()}]'
		raise ValueError

class ListNode(list):
	OPEN: str
	CLOSE: str

	def __repr__(self):
		return f'{self.OPEN}{' '.join(repr(child) for child in self)}{self.CLOSE}'
	
	def emit(self) -> str: ...

class CallListNode(ListNode):
	OPEN, CLOSE = '(', ')'

	def emit(self):
		return f'[{'/'.join(child.emit() for child in self)}]'

class ConcatListNode(ListNode):
	OPEN, CLOSE = '[', ']'

	def emit(self):
		return ''.join(child.emit() for child in self)

_token_re = re.compile(
	r'''\s*(?:
		# comment
		(;[^\n]*$) |
		# symbol
		([^\s()\[\]',"@]+) |
		# string
		("(?:\\.|[^"\\])*") |
		# verbatim string
		(@"(?:\\["\n\\]|[^"])*") |
		# paren
		([()]) |
		# bracket
		([\[\]]) |
		# quote
		([',]) |
	)''', re.VERBOSE | re.MULTILINE
)
_verbatim_re = re.compile(r'\\(["\n\\])')
_symbol_re = re.compile(r'[\s()\[\]\',"@]')

def _tokenize(s: str) -> Iterator[Token]:
	pos = 0
	while pos < len(s):
		m = _token_re.match(s, pos)
		if not m:
			raise SyntaxError(f'unexpected character at position {pos}: {s[pos]!r}')

		comment, symbol, string, verbatim_string, paren, bracket, quote = \
			m[1], m[2], m[3], m[4], m[5], m[6], m[7]
		pos = m.end()

		if comment:
			continue
		elif symbol:
			yield Token(TokenKind.STRING, symbol)
		elif string:
			yield Token(TokenKind.STRING, bytes(string[1:-1], 'utf-8').decode('unicode_escape'))
		elif verbatim_string:
			yield Token(TokenKind.VERBATIM_STRING, _verbatim_re.sub(r'\g<1>', verbatim_string[2:-1]))
		elif paren:
			yield Token(TokenKind.PAREN, paren)
		elif bracket:
			yield Token(TokenKind.BRACKET, bracket)
		elif quote:
			yield Token(TokenKind.QUOTE, quote)

	yield Token(TokenKind.EOF, '')

class Parser:
	tokens: Iterator[Token]
	_token: Token

	def __init__(self, src: str):
		self.tokens = _tokenize(src)
		self._advance()

	def _advance(self):
		self._token = next(self.tokens)

	def parse(self):
		result = ConcatListNode()
		while self._token.kind != TokenKind.EOF:
			result.append(self._parse_node())
		return result

	def _parse_node(self) -> Node:
		match self._token.kind, self._token.value:
			case TokenKind.STRING | TokenKind.VERBATIM_STRING, value:
				self._advance()
				return StringNode(value)
			case TokenKind.PAREN, '(':
				return self._parse_list(CallListNode)
			case TokenKind.BRACKET, '[':
				return self._parse_list(ConcatListNode)
			case TokenKind.QUOTE, value:
				self._advance()
				return QuotedNode(value, self._parse_node())
			case token:
				raise SyntaxError(f'unexpected {token}')

	def _parse_list(self, list_type: type[ListNode]):
		# consume '('
		self._advance()

		lst = list_type()
		while self._token.value != list_type.CLOSE:
			if self._token.kind == TokenKind.EOF:
				raise SyntaxError(f'unclosed {list_type.__name__}')
			lst.append(self._parse_node())
		
		# consume ')'
		self._advance()
		return lst

	@staticmethod
	def use(*exts: Callable[[type['Parser']], type['Parser']]):
		parser_t = Parser
		for ext in exts:
			parser_t = ext(parser_t)
		return parser_t