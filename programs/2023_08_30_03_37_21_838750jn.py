
import json
_vars = dict()
_global_vars = list(globals().items())
for _n, _v in _global_vars:
    if _n in []:
        _vars[_n] = _v
with open("/home/programming/mysite/programs/2023_08_30_03_37_21_838750jn_vars.json", mode="w") as f:
    json.dump(_vars, f)
