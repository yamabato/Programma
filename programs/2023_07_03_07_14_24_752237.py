print("Hello\nHello"*10)
import json
_vars = dict()
_global_vars = list(globals().items())
for _n, _v in _global_vars:
    if _n in []:
        _vars[_n] = _v
with open("/home/programma/mysite/programs/2023_07_03_07_14_24_752237_vars.json", mode="w") as f:
    json.dump(_vars, f)
