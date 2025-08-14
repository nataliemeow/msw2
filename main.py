from parser import Parser
from parser.ext import Include, Aliases, OutJson, ShortLoad, HexLiterals
import sys

with open(sys.argv[1]) as f:
	print(
		Parser.use(Include, Aliases, ShortLoad, OutJson, HexLiterals)(
			# i did not want to have to do this but my silly ass mixin thing necessitates it i think
			f.read(), path=sys.argv[1] # type: ignore
		).parse().emit()
	)