# 🏎️ F1 Data Correlation – Free Practice Pace vs. Race Result

A Python-based, interactive web application built with **Streamlit** and **FastF1**. This tool analyzes the correlation between **Free Practice lap times** and **final race results** to evaluate how well practice performance predicts actual race outcomes.

---

## 📌 Project Overview

This project uses the [FastF1](https://docs.fastf1.dev/) library to load and process official F1 session data. Through an interactive web interface, users can select a specific year, Grand Prix, and tire compound. The tool then:

- Automatically determines the correct practice session (FP2 for standard weekends, FP1 for Sprint weekends).
- Cleans the telemetry data (removes in/out laps, yellow/red flags, and statistical outliers using the IQR method).
- Calculates each driver's **average pace** in clean air.
- Merges practice data with the official **race classification**.
- Renders a highly detailed, vector-based (SVG) scatter plot with a regression trend line.
- Calculates and displays the **Pearson correlation coefficient (R)**.

---

## ✨ Key Features

- **🖥️ Interactive Web UI:** Built with Streamlit for easy selection of seasons, tracks, and tire compounds.
- **🧹 Advanced Data Cleaning:** Automatically filters out pit stops, non-green flag conditions, and lap time outliers for accurate pace representation.
- **🏃‍♂️ Sprint Weekend Support:** Automatically detects Sprint formats and uses FP1 data when FP2 is run under Parc Fermé conditions.
- **💥 DNF Handling:** Drivers who Did Not Finish (DNF) are clearly marked with an `✖` and can be dynamically included or excluded from the statistical correlation via a toggle switch.
- **🏎️ Dynamic Grid Size:** Adapts to the grid size changes automatically (e.g., 20 drivers up to 2025, expanding to 22 drivers from 2026 onwards).
- **📊 High-Quality Visuals:** Uses official FastF1 team colors, generates razor-sharp SVG graphics, and features comprehensive side-legends for teams, drivers, and correlation quality guides.

---

## 🛠️ Requirements

### Python Version
- Python **3.8+** recommended

### Dependencies

Install all required packages via pip:
```bash
pip install fastf1 pandas seaborn matplotlib streamlit
```

| Package      | Purpose                                      |
|--------------|----------------------------------------------|
| `streamlit`  | Interactive web frontend interface           |
| `fastf1`     | Load official F1 session and timing data     |
| `pandas`     | Data manipulation, cleaning, and merging     |
| `seaborn`    | Regression/trend line plotting               |
| `matplotlib` | Chart rendering, formatting, and SVG export  |

---

## ⚙️ Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/your-username/F1_Data_Correlation.git
cd F1_Data_Correlation
```

### 2. Configure the cache path

FastF1 caches downloaded session data locally to drastically speed up repeated runs. Open `analysis.py` and update the cache path to a valid directory on your machine:
```python
fastf1.Cache.enable_cache(r'YOUR\PATH\TO\F1_Cache')
```

### 3. Run the application
Since the project now uses a Streamlit frontend, start the app by running:
```bash
streamlit run main_menu.py
```

A local web server will start, and the application will open automatically in your default web browser (usually at `http://localhost:8501`).

---

## 📁 Project Structure
```text
F1_Data_Correlation/
│
├── main_menu.py        # Streamlit frontend, UI layout, and visualization logic
├── analysis.py         # Data fetching, cleaning, and FastF1 backend logic
├── F1_Cache/           # Local cache directory for FastF1 data (not committed)
└── README.md           # This project documentation file
```

---

## 🚧 Planned Improvements (To-Do)

- [x] **Interactive UI** – Replaced CLI prompts with a Streamlit web frontend.
- [x] **Data cleaning** – Handled missing values, outliers (IQR), and removed invalid laps.
- [x] **DNF highlighting** – Marked DNF drivers with distinct markers and added correlation toggles.
- [x] **Correlation quality indicator** – Added visual guides for R values (Strong, Moderate, Weak).
- [x] **Sprint Event Logic** – Added auto-fallback to FP1 for Sprint weekends.
- [ ] **Multi-session analysis** – Incorporate FP1 and FP3 data to analyze pace consistency across all practice sessions in a single view.
- [ ] **Long Run vs. Short Run Separation** – Identify and isolate true race simulations (stints > 5 laps) from qualifying simulations to improve race outcome predictions.
- [ ] **Tire Degragation** – Integrate Tire Degragation throughout laps.
- [ ] **Quali vs. Race & FP3 vs. Quali** – Integrate Correlation between Quali and Race & FP3 and Quali.
- [ ] **Weather Conditions** – Improve data by including weather conditions throughout laps.
- [ ] **Interactive Hover Charts** – Migrate from Matplotlib to Plotly to allow users to hover over data points and see specific driver telemetry (exact pace, tire age, stint length).
- [ ] **Qualifying Correlation** – Add a toggle to correlate practice pace against Qualifying positions instead of just Final Race outcomes.
- [ ] **Season-Wide Trend Analysis** – Create a macro-view that calculates the R-value for every race in a season to find out which tracks are the most predictable.