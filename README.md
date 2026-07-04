# Deep Work Timer

A lightweight terminal app to time, log, and visualize your deep work sessions. Built with Python.

---

## What it does

1. **Menu** — running the app drops you into an interactive menu: start a session, view your logs, or quit.
2. **Timer** — you enter a duration in minutes and an optional theme, a green progress bar counts down in your terminal, and a sound + desktop notification fires when time is up. You can pause/resume or quit early from the keyboard.
3. **Logger** — after each session you choose whether to save it. Sessions are stored in a local SQLite database (`database.db`).
4. **Visualizer** — the "See the logs" menu option reads the database and plots your total work minutes per day as a line chart for the last 7 recorded days.

---

## Project structure

```
deep_work/
├── main.py                # Entry point — launches the interactive main menu
├── deep_work.py           # Core app logic: menu, timer, countdown, pause/resume, notifications
├── database.py            # SQLite persistence layer (creates/queries database.db)
├── graph.py                # Reads sessions from the database and plots a 7-day chart
├── timer_over               # Audio file played when a session ends
└── database.db             # SQLite database, created automatically on first saved session
```

---

## Requirements

- **Python 3.12** (strictly — see installation notes below)
- An audio file named exactly **`timer_over`** placed in the project root

---

## Installation

> Python 3.12 is required regardless of what version is installed globally on your machine. The steps below explain how to set up an isolated virtual environment pinned to 3.12.

### Windows

```powershell
# Install Python 3.12 from https://python.org or the Microsoft Store
# Then, inside the project folder:
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install pygame plyer pynput pywinctl tqdm matplotlib
```

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev libdbus-1-dev libglib2.0-dev

# Inside the project folder:
python3.12 -m venv venv
source venv/bin/activate
pip install pygame plyer pynput pywinctl dbus-python tqdm matplotlib
```

> `dbus-python` is Linux-only and **optional**. `plyer` uses it for desktop notifications when it's installed, but falls back to the `notify-send` binary (present on most Linux desktops by default) when it isn't. Skip it unless `notify-send` is unavailable on your system or you specifically want the direct D-Bus path — it requires `python3.12-dev` and the dbus system libraries to compile.

### macOS

```bash
brew install python@3.12

# Inside the project folder:
python3.12 -m venv venv
source venv/bin/activate
pip install pygame plyer pynput pywinctl tqdm matplotlib
```

> On the first run, macOS will prompt you to allow the terminal to send notifications and access the speakers. Click **Allow**.

---

## Usage

### Launch the app

```bash
python main.py
```

You'll see the main menu:

```
What is it you desire?

 1. Launch a Deep Work session.
 2. See the logs.
 3. Quit
```

### 1. Launch a Deep Work session

You'll be asked for a duration in minutes and, optionally, a theme (what you're working on). After confirming, a green progress bar fills as time passes:

- Press **`p`** to pause, **`r`** to resume
- Press **`esc`** to stop the timer early

Pause/resume/quit key presses are only picked up while the terminal window you launched the app from is focused, so typing in other windows won't accidentally affect the timer.

When the timer reaches 100%:
- A sound plays from `timer_over`
- A desktop notification appears
- You're asked whether to save the session — saved sessions are written to `database.db`

After saving, you can immediately start another session or exit.

### 2. See the logs

Plots a line chart of total deep work minutes per day for your most recent days. If there are fewer than 7 recorded days of data, the raw session data is printed to the terminal instead of a chart.

### 3. Quit

Exits the app.

---

## Data storage

Sessions are stored in a SQLite database (`database.db`), in a `deep_work_sessions` table:

| Column       | Description                                  |
|--------------|-----------------------------------------------|
| `session_id` | Auto-incrementing primary key                |
| `minutes`    | Duration of the session in minutes           |
| `theme`      | Optional label for what you worked on        |
| `date`       | Timestamp the session was saved (defaults to now) |

The database file and table are created automatically the first time you save a session — no manual setup required.

---

## Dependencies

| Library      | Purpose                             |
|--------------|-------------------------------------|
| `tqdm`       | Terminal progress bar               |
| `pygame`     | Audio playback at session end       |
| `plyer`      | Cross-platform desktop notification |
| `pynput`     | Pause/resume/quit the timer via keyboard |
| `pywinctl`   | Detects the active window so pause/resume/quit only react while the app's terminal is focused |
| `matplotlib` | Line chart for the logs view        |

`sqlite3` is part of the Python standard library, so no separate install is needed for the database layer.

Install all at once using the provided `requirements.txt` (after activating your venv):

```bash
pip install -r requirements.txt
```

On Linux, `dbus-python` is commented out in `requirements.txt` since it's optional (see the [Linux install notes](#linux-ubuntu--debian) above). Uncomment it, or install separately, only if `notify-send` isn't available on your system:

```bash
pip install -r requirements.txt dbus-python
```
