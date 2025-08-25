import argparse
import hashlib
import json
import pathlib
import sys
from typing import Dict

# 确保本项目根目录优先于 site-packages，避免被 PyPI 的 `app` 包遮蔽
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.chroma_utils import init_chroma, add_documents


STATE_FILE = pathlib.Path("data/.index_state.json")


def file_sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state() -> Dict[str, str]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: Dict[str, str]):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def scan_data_dir(root: pathlib.Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".txt", ".md", ".pdf"}:
            continue
        yield p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="re-index all .md/.txt regardless of hash state")
    args = parser.parse_args()

    data_root = pathlib.Path("data")
    prev = {} if args.force else load_state()
    curr = {}
    docs = []

    for f in scan_data_dir(data_root):
        sha = file_sha256(f)
        curr[str(f)] = sha
        if args.force or prev.get(str(f)) != sha:
            # changed/new or force
            try:
                text = f.read_text(encoding="utf-8") if f.suffix.lower() != ".pdf" else None
            except Exception:
                text = None
            if text:
                docs.append((str(f), text))

    if docs:
        client = init_chroma()
        add_documents(client, "resume_mvp", docs)
        print(f"indexed {len(docs)} files ({'force' if args.force else 'delta'})")
    else:
        print("no changes detected")

    save_state(curr)


if __name__ == "__main__":
    main()


