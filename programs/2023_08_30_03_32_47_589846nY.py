# Python Code Editor

a, b = input().split()
a,b = int(a), int(b)
print("Even" if a*b%2==0 else "Odd")
import json
_vars = dict()
_global_vars = list(globals().items())
for _n, _v in _global_vars:
    if _n in []:
        _vars[_n] = _v
with open("/home/programming/mysite/programs/2023_08_30_03_32_47_589846nY_vars.json", mode="w") as f:
    json.dump(_vars, f)
