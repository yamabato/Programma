# print("Hello World!")を実行してみましょう
print("Hello World!")
import json
_vars = dict()
_global_vars = list(globals().items())
for _n, _v in _global_vars:
    if _n in []:
        _vars[_n] = _v
with open("/home/programma/mysite/programs/2023_07_03_12_26_04_935052_vars.json", mode="w") as f:
    json.dump(_vars, f)
