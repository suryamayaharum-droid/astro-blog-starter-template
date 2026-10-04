from __future__ import annotations
import json, subprocess
from pathlib import Path

BASE="https://suryamayaharum-droid.github.io/astro-blog-starter-template"
KEY="6973d74100b91d6ead3adf388b629848"
KEY_LOCATION=f"{BASE}/{KEY}.txt"

try:
    changed=subprocess.check_output(["git","diff","HEAD^","HEAD","--name-only"],text=True).splitlines()
except Exception:
    changed=[]

urls={BASE+"/"}

def add(path:str):
    urls.add(BASE+path)

for path in changed:
    p=Path(path)
    s=path.replace("\\","/")
    if s=="src/pages/index.astro":
        add("/")
    elif s.startswith("src/pages/en/"):
        add("/en/")
    elif s.startswith("src/pages/es/"):
        add("/es/")
    elif s.startswith("src/pages/") and s.endswith(".astro"):
        rel=s[len("src/pages/"):]
        if "[" in rel:
            parent=rel.split("/",1)[0]
            add(f"/{parent}/")
        elif rel.endswith("/index.astro"):
            add("/"+rel[:-len("index.astro")])
        else:
            add("/"+rel[:-len(".astro")]+"/")
    if "src/data/references" in s:
        add("/referencias/")
    if "src/data/artHistory" in s:
        add("/historia-da-arte/")
    if "src/data/imageBanks" in s:
        add("/bancos/"); add("/museus/"); add("/historia-da-arte/")
    if s.startswith(("src/components/","src/styles/")):
        for route in ("/","/en/","/es/","/referencias/","/historia-da-arte/","/bancos/","/biblioteca/"):
            add(route)
    if s in {"scripts/indexnow_payload.py",".github/workflows/indexnow.yml","public/robots.txt","public/llms.txt","public/site-knowledge.json"}:
        for route in ("/","/en/","/es/","/referencias/","/historia-da-arte/","/bancos/","/biblioteca/","/cadernos/","/percursos/","/bancos/bndigital/"):
            add(route)

payload={"host":"suryamayaharum-droid.github.io","key":KEY,"keyLocation":KEY_LOCATION,"urlList":sorted(urls)[:50]}
print(json.dumps(payload,ensure_ascii=False))
