from parser import Parser
from parser.ext import Include, Aliases, OutJson
import pytest
from pytest import param
import re
import json

def ms_format(src: str):
  src = re.sub(r'\\(\s|[{}])|\s|(^|[^\\])\s', r'\g<1>\g<2>', src)
  src = re.sub(r'\{([^{}]*)\}', lambda m: re.sub(r'[\[\]/]', r'\\\g<0>', m[1]), src)
  return src

@pytest.mark.parametrize(['exts', 'src', 'out'], [
  param(
    [Include],
    r'(#include test.msw)',
    r'[yogurt]',
    id='include'
  ),
  param(
    [Aliases],
    r'''
      (set x 0)
      (set+ x 1)
      (+ 1 2)
    ''',
    r'''
      [store/x/0]
      [store/x/[add/[load/x]/1]]
      [add/1/2]
    ''',
    id='aliases'
  ),
])
def test_exts(exts, src, out):
  assert Parser.use(*exts)(src).parse().emit() == ms_format(out)

def test_json():
  assert json.loads(
    Parser.use(OutJson)(
      r'(#out_json [a (b)] [c (d)])'
    ).parse().emit()
  ) == {'a': '[b]', 'c': '[d]'}