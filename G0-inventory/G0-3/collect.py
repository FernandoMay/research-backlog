import json, subprocess, os, sys, time
targets=json.load(open("raw/wave2-targets.json"))
out={}
def gh(path):
    p=subprocess.run(["gh","api",path],capture_output=True,text=True)
    return p.returncode, p.stdout
done=0
for i,n in enumerate(targets,1):
    if n in out: continue
    rc,o=gh(f"repos/FernandoMay/{n}")
    if rc!=0:
        out[n]={"error":"repo api failed"}; continue
    meta=json.loads(o); br=meta.get("default_branch")
    rec={"default_branch":br,"visibility":meta.get("visibility"),
         "size":meta.get("size"),"language":meta.get("language"),
         "created_at":meta.get("created_at"),"pushed_at":meta.get("pushed_at")}
    rc,o=gh(f"repos/FernandoMay/{n}/git/trees/{br}?recursive=1")
    if rc==0:
        t=json.loads(o)
        rec["truncated"]=t.get("truncated",False)
        blobs=[b["path"] for b in t.get("tree",[]) if b["type"]=="blob"]
        rec["files"]=blobs
    else:
        rec["files"]=[]
    # fetch README (or largest .md) — read-only content
    cand=[f for f in rec["files"] if f.lower()=="readme.md"] or \
         [f for f in rec["files"] if f.lower().endswith(".md")]
    rec["readme_path"]=cand[0] if cand else None
    if rec["readme_path"]:
        rc2,o2=gh(f"repos/FernandoMay/{n}/contents/{rec['readme_path']}")
        if rc2==0:
            import base64
            rec["readme"]=base64.b64decode(json.loads(o2)["content"]).decode("utf-8","replace")
    out[n]=rec
    done+=1
    if i%25==0: print(f"  {i}/{len(targets)} collected", flush=True)
json.dump(out, open("raw/wave2-observed.json","w"), indent=1)
print(f"collected {len(out)}")
