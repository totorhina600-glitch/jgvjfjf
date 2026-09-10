#!/usr/bin/env python3
"""Sync v2-live fixes -> PERTURABO via GitHub REST API (blobs, tree, commit, ref)."""
import base64, json, subprocess, sys, os
from pathlib import Path

REPO = "kioka8877-ux/PERTURABO"
BRANCH = "v2-live"
PAT = os.environ["PAT"]
ROOT = Path("MONDES_FORGES")  # faux, on le recalcule ci-dessous

# Racine du miroir local = ce script est a la racine du repo
ROOT = Path(__file__).resolve().parent

def api(method, url, payload=None):
    cmd = ["curl", "-s", "-H", f"Authorization: token {PAT}",
           "-H", "Accept: application/vnd.github+json"]
    if method in ("POST", "PUT", "PATCH"):
        cmd += ["-X", method, "-H", "Content-Type: application/json",
                "--data-binary", "@-"]
        data = json.dumps(payload).encode() if payload is not None else b"{}"
    else:
        data = None
    cmd.append(url)
    r = subprocess.run(cmd, input=data, capture_output=True)
    out = r.stdout.decode()
    if not out.strip():
        return {}
    return json.loads(out)

# 1. Etat actuel de PERTURABO
print("=== 1. Etat PERTURABO ===")
ref = api("GET", f"https://api.github.com/repos/{REPO}/git/ref/heads/{BRANCH}")
if "object" not in ref:
    print("ERREUR branche:", ref)
    sys.exit(1)
current_sha = ref["object"]["sha"]
base_tree = api("GET", f"https://api.github.com/repos/{REPO}/commits/{current_sha}")["commit"]["tree"]["sha"]
print(f"HEAD {BRANCH}: {current_sha[:10]} | tree: {base_tree[:10]}")

# 2. Fichiers a pousser (local -> distant)
FILES = {
    "MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/CODEBASE/libs/chat_pulse.py": "fix",
    "MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/CODEBASE/libs/helix_clipper.py": "fix",
    "MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/CODEBASE/libs/campaign_gate.py": "add",
    "MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/CODEBASE/f00b_vox_live.py": "fix",
    "MONDES_FORGES/CLIPPING/ARCHIVUM/campaign/live_campaigns.json": "add",
    "MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/IN/live_input.example.json": "fix",
    "MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/CODEBASE/refresh_twitch_token.py": "add",
    "MONDES_FORGES/CLIPPING/F00_IRON_SENTINEL/F00B_VOX/TRACKING/F00B_LOG.md": "fix",
    "MONDES_FORGES/CLIPPING/GUIDE_UTILISATION/18_MODE_LIVE_V2.md": "fix",
    "README_V2.md": "fix",
    "CONTINUATION_F00.md": "fix",
    ".github/workflows/perturabo_live_radar.yml": "fix",
    ".github/workflows/perturabo_oracle_watch.yml": "fix",
    "docs/index.html": "fix",
    "docs/data/.gitkeep": "add",
}

tree_items = []
for rel, kind in FILES.items():
    local = ROOT / rel
    if not local.exists():
        print(f"  !! absent en local, skip: {rel}")
        continue
    b64 = base64.b64encode(local.read_bytes()).decode()
    blob = api("POST", f"https://api.github.com/repos/{REPO}/git/blobs",
               {"content": b64, "encoding": "base64"})
    if "sha" not in blob:
        print(f"  !! blob fail {rel}: {blob}")
        sys.exit(1)
    mode = "100644"
    tree_items.append({"path": rel, "mode": mode, "type": "blob", "sha": blob["sha"]})
    print(f"  blob OK ({kind}): {rel} -> {blob['sha'][:10]}")

# 3. Suppression de l'ancien dossier BOARD_LIVE
existing = api("GET", f"https://api.github.com/repos/{REPO}/git/trees/{base_tree}?recursive=1")
for item in existing.get("tree", []):
    if item["path"].startswith("BOARD_LIVE/"):
        tree_items.append({"path": item["path"], "mode": "100644",
                           "type": "blob", "sha": None})
        print(f"  suppression: {item['path']}")

# 4. Tree + commit + ref
print("=== 2. Tree ===")
new_tree = api("POST", f"https://api.github.com/repos/{REPO}/git/trees",
               {"base_tree": base_tree, "tree": tree_items})
if "sha" not in new_tree:
    print("ERREUR tree:", new_tree)
    sys.exit(1)
print(f"tree: {new_tree['sha'][:10]}")

print("=== 3. Commit ===")
msg = ("fix(v2-live): radar SSL repare (session #1 = 0 msg), refresh auto token, board -> docs/\n\n"
       "- chat_pulse : wrap_socket sans server_hostname -> 22 echecs TLS sur la\n"
       "  session #1 (0 message recu en 60 min). Corrige + teste en direct\n"
       "  (47 msgs en 30s sur fps_shaka).\n"
       "- refresh_twitch_token.py : les workflows echangent le refresh token\n"
       "  contre un token frais a chaque run (token user ~4h).\n"
       "- Oracle + Radar : step 'Rafraichir le token' + fallback secret brut.\n"
       "- f00b_vox_live : snapshot statut AVANT arret du radar (connected=false\n"
       "  errone dans le statut final).\n"
       "- BOARD_LIVE -> docs/ : GitHub Pages n'accepte que / ou /docs.\n"
       "  Pages = v2-live + /docs, board sur kioka8877-ux.github.io/PERTURABO.\n"
       "- Docs : README_V2 (4 secrets, piege cron), guide 18, CONTINUATION.\n\n"
       "Session #1 (e11ysa, 60 min) : pipeline OK, capteur muet -> tout corrige.\n\n"
       "🤖 Generated with Codebuff\n"
       "Co-Authored-By: Codebuff <noreply@codebuff.com>")
new_commit = api("POST", f"https://api.github.com/repos/{REPO}/git/commits",
                 {"message": msg, "tree": new_tree["sha"], "parents": [current_sha]})
if "sha" not in new_commit:
    print("ERREUR commit:", new_commit)
    sys.exit(1)
print(f"commit: {new_commit['sha'][:10]}")

print("=== 4. Ref update ===")
upd = api("PATCH", f"https://api.github.com/repos/{REPO}/git/refs/heads/{BRANCH}",
          {"sha": new_commit["sha"], "force": False})
if "object" in upd:
    print(f"✅ SYNC TERMINEE -> {BRANCH} = {new_commit['sha'][:10]}")
else:
    print("ERREUR ref:", upd)
    sys.exit(1)
