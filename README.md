# DmaaS Achievement Tracker — desktop app

A desktop app: the same friendly interface you've seen throughout, now backed
by a real shared data file instead of manual CSV shuffling — Vodafone red/black
branding, DmaaS Team 1–6 + Spirit Ambassadors dropdown, a management access
code, and euro budget figures all included.

Data lives in a JSON file inside a OneDrive/SharePoint synced folder. Everyone
who runs this app pointed at the same synced folder shares the same data —
OneDrive/SharePoint's own sync handles moving it between machines. No Azure
app registration, no server, no Claude access needed to use it day-to-day.

## Setup (each person does this once)

1. Install Python 3.9+ if not already on the machine.
2. Open a terminal in this folder and run:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python app.py
   ```
4. First launch: click **"Choose shared folder"** and pick a folder *inside*
   your OneDrive/SharePoint-synced library, e.g.
   `OneDrive - Vodafone\DmaaS\Achievement Tracker`
   Everyone on the team should point at the exact same folder.
5. Done — the app remembers this choice for next time.

## Management access

Click "Management view" and enter the access code (default: `Dmaas2026`,
set near the top of `ui.html` — search for `MANAGEMENT_PASSCODE` and change
it before rollout). This is a soft deterrent, not real security: anyone who
opens `ui.html` in a text editor can read the code. It stops casual
browsing, not a determined look. If you need real access separation later,
the next step up is a SharePoint List with column-level permissions.

## Packaging as a real .exe — two ways to do this

I can't produce a working Windows `.exe` myself from this environment (Linux
sandbox, no way to compile or test a Windows binary). But you only need
**one person to build it once** — everyone else just receives the finished
file and double-clicks it, exactly like the `caffeine64.exe`-style tool you
showed me.

### Option A — build it locally (needs one Windows PC with Python, once)

1. Copy this whole folder onto a Windows machine.
2. Double-click `build.bat`.
3. It installs the build tools, builds the app, and tells you where the
   finished `DmaaS-Achievement-Tracker.exe` landed (in a new `dist` folder).
4. Share that single `.exe` file with the team. They don't need Python —
   only the machine that ran `build.bat` did.

### Option B — build it with zero local installs anywhere (needs a free GitHub account)

This uses GitHub's own Windows cloud machines to do the build, so nobody —
not even you — installs Python locally.

1. Create a free account at github.com if you don't have one.
2. Create a new repository and upload this entire folder to it (drag-and-drop
   works fine on github.com — no command line needed), including the hidden
   `.github` folder with the workflow file inside it.
3. On the repository page, click the **Actions** tab.
4. Click **"Build DmaaS Achievement Tracker .exe"** in the left list, then
   the **"Run workflow"** button.
5. Wait a minute or two for it to finish (green checkmark).
6. Click into the finished run, scroll to **Artifacts**, and download
   `DmaaS-Achievement-Tracker-exe` — that's your `.exe`, built and zipped,
   ready to share with the team.

Option B is the more reliable of the two, since it builds on an actual
Windows machine Microsoft runs, not a guess from this sandbox.

## Honest limitations

- **File-sync sharing, not a real database.** Two people saving at the exact
  same moment can create a OneDrive conflict copy. Low risk for a team
  logging a few milestones a week; not zero.
- **No login system.** Anyone with the app can submit or (if they have the
  access code) score. If that boundary needs to be enforced rather than
  just deterred, that's the signal to move to a SharePoint List or a real
  backend.
- **Everyone's synced folder must be set to sync locally** (not
  "online-only") for reliable read/write.

## What's inside

- `app.py` — backend: reads/writes the shared JSON file, exposes methods to the UI
- `ui.html` — the interface (Vodafone-branded, team dropdown, management gate)
- `requirements.txt` — one dependency (pywebview)
- `config.json` — created automatically after your first folder choice (per-machine, not shared)
