# Screen Time Tracker

A simple Windows application to track your active window usage time, ignoring idle periods. Built with Python and Tkinter, this app logs how long you spend on each active window and provides an easy-to-use graphical interface to start/stop tracking and view your usage logs.

---

## Features

- Tracks active window usage time in real-time
- Skips logging when idle for a configurable threshold (default 60 seconds)
- Logs start time, end time, and duration per window session to a CSV file
- Simple Tkinter GUI to start/stop tracking and view logs
- Displays total tracked screen time after stopping the tracker

---

## Technologies Used

- **Python 3.x** — Programming language
- **Tkinter** — For the graphical user interface (GUI)
- **pywin32** — Access Windows API to get active window titles
- **ctypes** — Detect user idle time on Windows
- **threading** — Run screen time tracker in the background
- **csv** — Log and read usage data

---

## Getting Started

### Prerequisites

- Windows OS
- Python 3.6 or higher installed
- Pip package manager

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/screen-time-tracker.git
   cd screen-time-tracker
   ```

2. Install dependencies:

   ```bash
   pip install pywin32
   ```

### Running the App

Run the Python script:

```bash
python index.py
```

---

## Usage

- Click **Start Tracking** to begin logging your active window usage
- Click **Stop Tracking** to stop and view your total tracked time
- Click **View Log** to see a detailed table of all recorded sessions
- The logs are saved in `app_usage_log.csv` in the current directory

---

## Building Executable

To build a standalone `.exe` for Windows:

1. Install PyInstaller if you haven't already:

   ```bash
   pip install pyinstaller
   ```

2. Run PyInstaller:

   ```bash
   pyinstaller --noconsole --onefile index.py
   ```

3. Find your executable in the `dist/` folder.

---

## Future Improvements

- Add app-specific filtering (only track selected apps)
- Display per-app time summaries and charts
- Add auto-start on Windows boot
- Create an installer for easier setup
- Add notifications or reminders for long screen time

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

Created by [Your Name](https://github.com/yourusername).  
Feel free to open issues or submit pull requests!

---

## Acknowledgments

- Inspired by personal need to track screen time
- Uses Windows APIs via `pywin32` and `ctypes`
- Tkinter for simple but effective GUI
