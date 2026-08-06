"""
Achievement Tracker — desktop app
----------------------------------
A small desktop app (built with pywebview) that gives your team a friendly
interface for logging milestones and gives upper management a ranking view —
with data stored in a plain JSON file that lives inside a OneDrive/SharePoint
synced folder, so everyone's app reads and writes the SAME shared file.

No Claude access needed to use this once it's set up. No server needed either.

Run it with:  python app.py
"""

import json
import os
import time
import uuid
from pathlib import Path

import webview

APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "config.json"
DATA_FILENAME = "achievements_data.json"


# ---------------------------------------------------------------------------
# Config: remembers which shared folder this PC should read/write to
# ---------------------------------------------------------------------------
def load_config():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Data file helpers (this IS the "backend" — a JSON file synced by
# OneDrive/SharePoint so every machine pointed at the same folder shares data)
# ---------------------------------------------------------------------------
def read_data_file(path: Path, retries=3, delay=0.3):
    """Read the shared data file, retrying briefly if OneDrive has it locked
    mid-sync. Returns a fresh list every time — never trust cached state."""
    if not path.exists():
        return []
    for attempt in range(retries):
        try:
            raw = path.read_text(encoding="utf-8")
            return json.loads(raw) if raw.strip() else []
        except (json.JSONDecodeError, OSError):
            if attempt == retries - 1:
                raise
            time.sleep(delay)
    return []


def write_data_file(path: Path, entries):
    """Write atomically: write to a temp file then replace, so a sync
    picking up the file mid-write never sees a half-written JSON file."""
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    os.replace(tmp_path, path)


# ---------------------------------------------------------------------------
# API exposed to the HTML/JS front end
# ---------------------------------------------------------------------------
class Api:
    def __init__(self):
        self.window = None
        cfg = load_config()
        self.data_folder = cfg.get("data_folder")

    def _data_path(self):
        if not self.data_folder:
            return None
        return Path(self.data_folder) / DATA_FILENAME

    # ---- setup ----
    def get_status(self):
        """Tells the UI whether a shared folder is configured yet, and shows
        the current data path so the user can confirm it's the right one."""
        path = self._data_path()
        return {
            "configured": bool(self.data_folder),
            "folder": self.data_folder or "",
            "data_path": str(path) if path else "",
        }

    def choose_folder(self):
        """Opens a native folder picker. Point this at a folder INSIDE your
        OneDrive/SharePoint synced library so it shares across machines."""
        result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        if not result:
            return self.get_status()
        chosen = result[0]
        self.data_folder = chosen
        save_config({"data_folder": chosen})
        # Make sure the data file exists so sync picks it up immediately
        path = self._data_path()
        if not path.exists():
            write_data_file(path, [])
        return self.get_status()

    # ---- data ----
    def load_entries(self):
        path = self._data_path()
        if not path:
            return []
        try:
            return read_data_file(path)
        except Exception as e:
            return {"error": str(e)}

    def add_entry(self, entry):
        path = self._data_path()
        if not path:
            return {"ok": False, "error": "No shared folder configured yet."}
        entries = read_data_file(path)
        entry["id"] = uuid.uuid4().hex[:10]
        entry["submittedAt"] = time.time()
        entry.setdefault("score", None)
        entries.append(entry)
        write_data_file(path, entries)
        return {"ok": True, "entries": entries}

    def update_score(self, entry_id, score):
        path = self._data_path()
        if not path:
            return {"ok": False, "error": "No shared folder configured yet."}
        entries = read_data_file(path)
        found = False
        for e in entries:
            if e.get("id") == entry_id:
                e["score"] = score
                found = True
                break
        if not found:
            return {"ok": False, "error": "Entry not found — someone may have removed it. Refreshing.",
                     "entries": entries}
        write_data_file(path, entries)
        return {"ok": True, "entries": entries}

    def delete_entry(self, entry_id):
        path = self._data_path()
        if not path:
            return {"ok": False, "error": "No shared folder configured yet."}
        entries = read_data_file(path)
        entries = [e for e in entries if e.get("id") != entry_id]
        write_data_file(path, entries)
        return {"ok": True, "entries": entries}


def main():
    api = Api()
    window = webview.create_window(
        "Achievement Tracker",
        str(APP_DIR / "ui.html"),
        js_api=api,
        width=1100,
        height=780,
        min_size=(820, 600),
    )
    api.window = window
    webview.start()


if __name__ == "__main__":
    main()
