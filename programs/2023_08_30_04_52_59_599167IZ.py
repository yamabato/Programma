a, b = map(int, input().split())
print("Even" if a*b%2==0 else "Odd")
    
import json
_vars = dict()
_global_vars = list(globals().items())
for _n, _v in _global_vars:
    if _n in []:
        _vars[_n] = _v
with open("/home/programming/mysite/programs/2023_08_30_04_52_59_599167IZ_vars.json", mode="w") as f:
    json.dump(_vars, f)
