import json, sys, griffe
from griffe import ExprName
pkg = griffe.load("gswa", search_paths=[sys.argv[1]], resolve_aliases=True, resolve_external=False)
def ty(e):
    if e is None: return None
    names = sorted({n.canonical_path for n in e.iterate(flat=True) if isinstance(n, ExprName)}) if not isinstance(e,str) else []
    return {"text": str(e), "refs": [n for n in names if n.startswith("gswa.")]}
def ops(cls):
    out=[]
    for name, m in cls.all_members.items() if False else cls.members.items():
        if m.is_alias or m.kind.value!="function" or name.startswith("_"): continue
        if {"classmethod","staticmethod","property"} & set(m.labels): continue
        ps=[p for p in m.parameters if p.name not in ("self","cls")]
        out.append({"op":name,"async":"async" in m.labels,"line":m.lineno,
          "params":[{"name":p.name,"kind":p.kind.value,"type":ty(p.annotation)} for p in ps],
          "returns":ty(m.returns)})
    return out
targets=sys.argv[2:]
res={t:{"file":str(pkg[t.removeprefix("gswa.")].relative_filepath),"bases":[str(b) for b in pkg[t.removeprefix("gswa.")].bases],"operations":ops(pkg[t.removeprefix("gswa.")])} for t in targets}
print(json.dumps(res,indent=1))
