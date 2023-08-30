# print("Hello World!")を実行してみましょう
print("Hello World!")
import json
_vars = dict()
_global_vars = globals()
for _n, _v in _global_vars.items():
    if _n in []:
        _vars[_n] = _v
with open("/home/programma/mysite/programs/2023_07_03_06_45_01_129980_vars.json", mode="w") as f:
    json.dump(_vars, f)
