print("Hello")
import json
_vars = dict()
_global_vars = list(globals().items())
for _n, _v in _global_vars:
    if _n in []:
        _vars[_n] = _v
with open("/home/programma/mysite/programs/2023_07_03_07_04_54_530780_vars.json", mode="w") as f:
    json.dump(_vars, f)
