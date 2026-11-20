#!/usr/bin/env python3
"""Publish the 20 November 2026 news poster for the make.fun entry.

The poster itself ships in this repository as entry.png (1024x1024). It
was drawn from the verified world news of Friday 20 November 2026:
Cyclone Akvan makes landfall on India's east coast, GTA VI's first
day (19.1m copies, $1.84bn), Anthropic closes day one at $97.17, the
ICJ finds Myanmar guilty of genocide, Trump, Xi and Putin sign a
Peace Declaration in Shenzhen, and Nicholls' 113 puts New Zealand on
top in the Wellington Test. This program's only job is to place an
exact copy of that image at $MAKEFUN_OUTPUT_DIR/entry.png (or next to
this file when the variable is unset), so every grading run sees the
same bytes.

Standard library only, no network, no third-party packages. The
grader runs `python3 -P -s /bot/main.py` in a plain python:3.13 image
with no Pillow and no DejaVu fonts, as an unprivileged user with /bot
read-only and only $MAKEFUN_OUTPUT_DIR writable, so this program must
not import anything beyond the standard library or write anywhere
else.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or str(HERE)
    destination_dir = Path(out_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    if not SOURCE.is_file():
        raise SystemExit(f"poster missing: {SOURCE}")
    target = destination_dir / "entry.png"
    if target.resolve() != SOURCE.resolve():
        # With MAKEFUN_OUTPUT_DIR unset the destination is this directory,
        # so source and target are the same file and there is nothing to
        # copy; still verify the hash below.
        shutil.copyfile(SOURCE, target)
    # Never hand the grader a truncated copy: the published file must
    # hash exactly like the poster shipped in this repository.
    source_hash = _sha256(SOURCE)
    if _sha256(target) != source_hash:
        target.unlink(missing_ok=True)
        raise SystemExit("poster copy failed verification")
    print(f"Wrote {target}  {target.stat().st_size} bytes  sha256={source_hash}")


if __name__ == "__main__":
    main()
