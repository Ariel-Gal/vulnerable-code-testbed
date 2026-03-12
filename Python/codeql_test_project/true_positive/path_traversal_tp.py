from pathlib import Path
from flask import Flask, request

app = Flask(__name__)
BASE_DIR = Path("data")


@app.get("/read")
def read_file():
    filename = request.args.get("file", "note.txt")

    # True positive: user controls path and traversal is not prevented.
    target = BASE_DIR / filename

    if not target.exists():
        return {"error": "not found"}, 404

    return {"content": target.read_text(encoding="utf-8")}


if __name__ == "__main__":
    BASE_DIR.mkdir(exist_ok=True)
    (BASE_DIR / "note.txt").write_text("safe sample", encoding="utf-8")
    app.run(port=5003)
