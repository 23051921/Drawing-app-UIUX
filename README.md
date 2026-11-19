# 🎨 Python Desktop Productivity & Creative Suite (UI/UX)

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![GUI: Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow.svg)](https://docs.python.org/3/library/tkinter.html)
[![Storage: SQLite3](https://img.shields.io/badge/Database-SQLite3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Charts: Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-11557C.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A collection of lightweight, self-contained desktop applications featuring clean graphical user interfaces (UI/UX), intuitive workflows, and local data persistence. Built using Python's native GUI toolkit `tkinter`, `ttk`, `Pillow`, `matplotlib`, and `sqlite3`.

---

## 📦 Application Suite Overview

```
Drawing-app-UIUX/
├── DRAWINGAPP.py        # Interactive digital drawing canvas & raster exporter
├── expense tracker.py   # Personal financial ledger with SQLite & Matplotlib analytics
├── todo.py              # Minimalist task & workflow organizer
└── README.md            # Suite documentation
```

---

## 🖌️ 1. Digital Drawing Canvas Studio (`DRAWINGAPP.py`)

An interactive digital canvas designed for sketching, drafting, and rapid graphic generation.

### Key Capabilities
* **Dynamic Brush Controls:** Adjustable stroke width with continuous anti-aliased interpolation.
* **Full-Spectrum Color Picker:** Integrated native RGB palette chooser via `tkinter.colorchooser.askcolor`.
* **Geometric Primitives:** Built-in drawing modes for freehand sketches, straight lines, rectangles, and ovals.
* **Precision Eraser & Canvas Reset:** Instant clearing and localized erasing with synchronized coordinate tracking.
* **Dual-Layer Raster Export:** Mirrors all vector canvas primitives onto an off-screen `PIL.ImageDraw` buffer, enabling lossless export to PNG and JPEG image formats.

```bash
python DRAWINGAPP.py
```

---

## 💰 2. Personal Expense Tracker & Analytics (`expense tracker.py`)

A desktop financial manager providing categorical expense tracking, local SQLite persistence, and visual spending breakdowns.

### Key Capabilities
* **Local Relational Storage:** Automated schema creation and persistence via embedded `sqlite3` database (`expenses.db`).
* **Categorical Budgeting:** Classifies expenditures across predefined buckets (Food, Transportation, Housing, Entertainment, Utilities, Healthcare, Other).
* **Interactive Data Table:** `ttk.Treeview` tabular ledger displaying expense IDs, dates, descriptions, categories, and amounts.
* **Graphical Spending Breakdown:** One-click generation of Matplotlib pie charts and category distributions for instant financial health audits.
* **CSV Data Portability:** Export full historical spending records to `.csv` for external analysis in Excel or Google Sheets.

```bash
python "expense tracker.py"
```

---

## ✅ 3. Minimalist Task & Workflow Manager (`todo.py`)

A distraction-free to-do list manager adhering to the Getting Things Done (GTD) methodology for daily task prioritization.

### Key Capabilities
* **Quick Task Entry:** Fast keyboard-driven input field with automated list focus.
* **Scrollable Task Ledger:** Listbox with dynamic vertical scrolling for managing large backlogs.
* **State Management:** One-click task completion status toggles and batch deletion.
* **Input Validation:** Error prevention preventing empty submissions via pop-up alert dialogs.

```bash
python todo.py
```

---

## ⚡ Installation & Setup

### Prerequisites
* Python 3.8 or higher.
* `tkinter` is bundled by default with standard Python installations on Windows and macOS.

### Dependencies
Install the required third-party libraries for imaging and chart generation:
```bash
pip install pillow matplotlib
```

### Running the Apps
Clone this repository and launch any application directly:
```bash
git clone https://github.com/23051921/Drawing-app-UIUX.git
cd Drawing-app-UIUX

# Launch the drawing studio
python DRAWINGAPP.py

# Launch the expense manager
python "expense tracker.py"

# Launch the to-do list
python todo.py
```
