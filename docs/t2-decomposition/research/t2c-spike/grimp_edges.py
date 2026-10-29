import sys, json, time; sys.path.insert(0, sys.argv[1]); import grimp
t=time.time(); g=grimp.build_graph("gswa", cache_dir=None); bt=time.time()-t
svc={"AccountManager":"gswa.accounts.manager","AuthnManager":"gswa.authn.manager","AuthzManager":"gswa.authz.manager",
 "AccountsEngines":"gswa.accounts.engines","AuthnEngines":"gswa.authn.engines","AuthzEngines":"gswa.authz.engines",
 "UserAccess":"gswa.access.user","UserInviteAccess":"gswa.access.user_invite","OutboxAccess":"gswa.access.outbox",
 "RoleAccess":"gswa.access.role","ScopeAccess":"gswa.access.scope","RoleScopeAccess":"gswa.access.role_scope",
 "UserScopeAccess":"gswa.access.user_scope","EmailAccess":"gswa.access.external"}
def mods(p): return {p}|g.find_descendants(p)
edges=[]
for a,pa in svc.items():
    ma=mods(pa)
    for b,pb in svc.items():
        if a==b: continue
        mb=mods(pb); lines=[]
        for m in ma:
            for d in g.find_modules_directly_imported_by(m) & mb:
                det=g.get_import_details(importer=m, imported=d)
                lines+= [f"{m}->{d}:{x['line_number']}" for x in det]
        if lines: edges.append({"from":a,"to":b,"imports":sorted(lines)[:2],"n":len(lines)})
print("build_s",round(bt,3),"modules",len(g.modules))
for e in edges: print(e["from"],"->",e["to"],e["n"],e["imports"][0])
