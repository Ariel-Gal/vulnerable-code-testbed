from pathlib import Path
from flask import Flask, request

app = Flask(__name__)
BASE_DIR = Path("data").resolve()


@app.get("/safe-read")
def safe_read_file():
    filename = request.args.get("file", "note.txt")

    # False positive candidate: user input is validated to remain under BASE_DIR.
    target = (BASE_DIR / filename).resolve()
    if BASE_DIR not in target.parents and target != BASE_DIR:
        return {"error": "invalid path"}, 400

    if not target.exists() or not target.is_file():
        return {"error": "not found"}, 404

    return {"content": target.read_text(encoding="utf-8")}


if __name__ == "__main__":
    BASE_DIR.mkdir(exist_ok=True)
    (BASE_DIR / "note.txt").write_text("safe sample", encoding="utf-8")
    app.run(port=5013)
