# 🏎️ F1 Data Analysis – FP2 Pace vs. Race Result

A Python-based Formula 1 data analysis tool that correlates **Free Practice 2 lap times** with **final race results** to evaluate how well practice performance predicts race outcomes.

---

## 📌 Project Overview

This project uses the [FastF1](https://docs.fastf1.dev/) library to load and process official F1 session data. For a given Grand Prix and season, it:

- Loads FP2 session data and calculates each driver's **average lap time**
- Loads the **race result** for the same event
- Merges both datasets by driver abbreviation
- Visualizes the correlation in a scatter plot with a trend line
- Calculates and displays the **Pearson correlation coefficient (R)**

The chart uses official **team colors** from FastF1 and is rendered in a dark theme to match the F1 aesthetic.

---

## 📊 Example Output

The output is an interactive matplotlib chart showing:

- Each driver as a colored dot (team color)
- Driver abbreviation labels
- A dashed yellow trend line
- The correlation value (R) in a highlighted box
- X-axis formatted as `M:SS:ms` for lap time readability

---

## 🛠️ Requirements

### Python Version
- Python **3.8+** recommended

### Dependencies

Install all required packages via pip:
```bash
pip install fastf1 pandas seaborn matplotlib
```

| Package      | Purpose                                      |
|--------------|----------------------------------------------|
| `fastf1`     | Load official F1 session and timing data     |
| `pandas`     | Data manipulation and merging                |
| `seaborn`    | Regression/trend line plotting               |
| `matplotlib` | Chart rendering and formatting               |

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/f1-data-analysis.git
cd f1-data-analysis
```

### 2. Configure the cache path

FastF1 caches downloaded session data locally to speed up repeated runs. In `app.py`, update the cache path to a valid directory on your machine:
```python
fastf1.Cache.enable_cache(r'YOUR\PATH\TO\F1_Cache')
```

### 3. Run the script
```bash
python app.py
```

You will be prompted to enter:
- **Season** (e.g. `2023`)
- **Grand Prix** (e.g. `Silverstone`)

---

## 🚧 Planned Improvements (To-Do)

- [ ] **Data cleaning** – Handle missing values, outliers, and ensure data consistency across drivers and sessions
- [ ] **Multi-session analysis** – Incorporate FP1 and FP3 data to analyze pace consistency across all practice sessions
- [ ] **Interactive UI** – Replace CLI prompts with a proper interface using buttons, dropdowns, or a web frontend (e.g. Streamlit or Tkinter)
- [ ] **Correlation quality indicator** – Visually communicate what the R value means (e.g. R > 0.7 = strong, R < 0.3 = weak) directly in the chart
- [ ] **DNF highlighting** – Mark drivers who retired from the race (DNF) or did not participate in FP2 with a distinct color or marker

---

## 📁 Project Structure
```
f1-data-analysis/
│
├── app.py              # Main analysis and visualization script
├── F1_Cache/           # Local cache directory for FastF1 data (not committed)
└── README.md           # This file
```
