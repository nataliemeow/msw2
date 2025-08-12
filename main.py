from parser import Parser
from parser.ext import Include, Aliases, OutJson
from sys import stdin

print(Parser.use(Include, Aliases, OutJson)(stdin.read()).parse().emit())