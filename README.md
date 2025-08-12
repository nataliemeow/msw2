# MSW

LISP-like language that compiles to Robot is Chill's macro language called MacroScript.

## Examples

### Print squares

```
(set i 0)
,(repeat 10 '[
	(int (* (get i) (get i))) " "
	(set+ i 1)
])
```

## Extensions

See [parser/ext/__init__.py](parser/ext/__init__.py)