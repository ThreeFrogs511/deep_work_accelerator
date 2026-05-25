# Deep Work Timer

A lightweight terminal app to time, log, and visualize your deep work sessions. Built with Python.

---

## What it does

1. **Timer** — you enter a duration in minutes, a green progress bar counts down in your terminal, and a sound + desktop notification fires when time is up.
2. **Logger** — after each session you choose whether to save it. Sessions are appended to a local CSV file (`deep_work_output.csv`).
3. **Visualizer** — a separate script reads the CSV and plots your total work time per day or per month as a line chart.

---

## Project structure

```
deep_work/
├── main.py                   # Entry point for the timer
├── deep_work.py              # Timer logic (input, countdown, notification)
├── save_deep_work_session.py # CSV persistence
├── progress.py               # Entry point for the graph
├── graph.py                  # CSV → matplotlib chart
├── timer_over                # Audio file played when the session ends
└── deep_work_output.csv      # Created automatically on first save
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
pip install pygame plyer tqdm matplotlib
```

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev libdbus-1-dev libglib2.0-dev

# Inside the project folder:
python3.12 -m venv venv
source venv/bin/activate
pip install pygame plyer dbus-python tqdm matplotlib
```

> `dbus-python` is Linux-only and is needed for desktop notifications. It requires `python3.12-dev` and the dbus system libraries to compile correctly.

### macOS

```bash
brew install python@3.12

# Inside the project folder:
python3.12 -m venv venv
source venv/bin/activate
pip install pygame plyer tqdm matplotlib
```

> On the first run, macOS will prompt you to allow the terminal to send notifications and access the speakers. Click **Allow**.

---

## Usage

### Start a session

```bash
python main.py
```

You will be asked how long to work (in minutes). A green progress bar fills as time passes. When it reaches 100%:
- A sound plays from `timer_over`
- A desktop notification appears
- You are asked whether to save the session

After saving, you can immediately start another session or exit.

### View your progress

```bash
python progress.py
```

This opens a line chart of your total work time aggregated by month. To switch to a daily view, open `progress.py` and change `"month"` to `"day"`:

```python
# progress.py
show_progress = CsvToGraph("day")
```

---

## Data format

Sessions are stored in `deep_work_output.csv`:

```
hour,date
90,2026-05-25
60,2026-05-26
```

| Column | Description                        |
|--------|------------------------------------|
| `hour` | Duration of the session in minutes |
| `date` | Date of the session (YYYY-MM-DD)   |

Multiple sessions on the same day are summed automatically in the graph.

---

## Dependencies

| Library      | Purpose                             |
|--------------|-------------------------------------|
| `tqdm`       | Terminal progress bar               |
| `pygame`     | Audio playback at session end       |
| `plyer`      | Cross-platform desktop notification |
| `matplotlib` | Line chart for progress view        |

Install all at once using the provided `requirements.txt` (after activating your venv):

```bash
pip install -r requirements.txt
```

On Linux, also install `dbus-python` for desktop notifications:

```bash
pip install -r requirements.txt dbus-python
```
