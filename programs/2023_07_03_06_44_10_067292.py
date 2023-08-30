# print("Hello World!")を実行してみましょう
print("Hello World!")
import json
_vars = dict()
for _n, _v in globals().items():
    if _n in []:
        _vars[_n] = _v
with open("/home/programma/mysite/programs/2023_07_03_06_44_10_067292_vars.json", mode="w") as f:
    json.dump(_vars, f)
