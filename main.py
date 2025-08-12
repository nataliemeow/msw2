from parser import Parser
from parser.ext import Include, Aliases
from sys import stdin

print(Parser.use(Include, Aliases)(stdin.read()).parse().emit())