import hashlib
import json
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

# releases folder is next to this file
releases_dir = Path(__file__).parent / "releases"


def latest_version():
    with open(releases_dir / "manifest.json") as f:
        data = json.load(f)
    return data["latest"]


def file_hash(path):
    # sha256 so board can check download isn't corrupted
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


@app.get("/health")
def health():
    return {"status": "ok"}


# has to be above /{version}
@app.get("/api/v1/firmware/latest")
def get_latest():
    version = latest_version()
    path = releases_dir / (version + ".bin")

    if not path.exists():
        raise HTTPException(status_code=500, detail="missing firmware file")

    return {
        "version": version,
        "size": path.stat().st_size,
        "sha256": file_hash(path),
    }


@app.get("/api/v1/firmware/{version}")
def get_firmware(version: str):
    # only allow stuff like 1.2.3
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise HTTPException(status_code=400, detail="bad version")

    path = releases_dir / (version + ".bin")
    if not path.exists():
        raise HTTPException(status_code=404, detail="version not found")

    return FileResponse(path, media_type="application/octet-stream")