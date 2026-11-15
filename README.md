# ⊛ Earth2Orbit — Planetary Analog Explorer

> **"Connecting Earth's Landscapes to Other Worlds."**  
> **Challenge:** *Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars.*  
> **Event:** NASA Space Apps Challenge 2026  
> **Team:** QuantumBoyzz  

[![Python 3.12](https://img.shields.io/badge/Python-3.12-775da6.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-202020.svg)](https://streamlit.io/)
[![NASA Space Apps 2026](https://img.shields.io/badge/NASA%20Space%20Apps-2026-f9837c.svg)](https://www.spaceappschallenge.org/)
[![Team: QuantumBoyzz](https://img.shields.io/badge/Team-QuantumBoyzz-70b6c1.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-f3cc5c.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Overview

**Earth2Orbit — Planetary Analog Explorer** is a professional geospatial research and scientific visualization platform developed for the **NASA Space Apps Challenge 2026**. 

The platform identifies, characterizes, and quantitatively benchmarks terrestrial environments that share critical geological, topographical, and environmental characteristics with candidate permanent Moon base exploration regions (Lunar South Pole: Shackleton Crater Rim and Malapert Mountain) and Mars (Jezero Crater delta and floor).

Through an evidence-based multi-criteria framework—the **Analog Compatibility Index (ACI)**—Earth2Orbit enables mission planners, geoscientists, and students to evaluate domain-specific terrestrial analogs with transparent parameter distance metrics, geodetic datum reconciliation, and direct integration with NASA planetary datasets.

---

## ✨ Main Features Across Application Modules

Earth2Orbit features an integrated 8-page architecture adapted from the **Rhombus** dashboard design system (styled with tokens `#775da6` Purple, `#f9837c` Coral, `#70b6c1` Teal, and `#f3cc5c` Gold):

1. **Overview Dashboard (`modules/home_dashboard.py`):**
   - Executive mission greeting and research kit specifications.
   - 4-card KPI metric grid (Highest ACI Score `81.4%`, 3 Indian Terrestrial Analogs, 2 Planetary Reference Regions, 12 NASA Datasets).
   - Responsive candidate analog cards (Lonar Impact Crater, Tso Kar High-Altitude Basin, Sambhar Salt Lake) with process analogies, eliminating horizontal scrolling.
   - Candidate planetary target research cards (Lunar South Pole & Jezero Crater).
   - Expandable Global Reference Standards tray (Atacama Desert, McMurdo Dry Valleys, Iceland Volcanic Fields).

2. **Earth Analog Explorer (`modules/earth_explorer.py`):**
   - Interactive Leaflet/Folium geospatial map supporting OpenStreetMap and Esri World Imagery basemaps.
   - Multi-criteria filtering by country, planetary target affinity, and free-text search with a safe filter reset mechanism.
   - Core site metrics: Verified coordinates, verified elevation above sea level (SRTM DEM a.s.l.), Köppen-Geiger biome, and terrain slope/roughness.
   - **Concise Site Summary Card**: Target affinity badge and 1–2 sentence terrain classification.
   - Collapsible `🔬 Detailed Scientific Documentation & In-Situ Parameters` tray providing mineralogical phases, lithological stratigraphy, extended environmental parameters, NASA POWER API live queries, and peer-reviewed citations.

3. **Planetary Targets (`modules/planetary_targets.py`):**
   - Planetary body selector (The Moon & Mars).
   - Target showcase cards featuring authentic NASA public domain photography (Apollo 17, LRO, Perseverance rover, Mars Global Surveyor).
   - Physical orbital parameters, celestial coordinates, and surface thermal environments.
   - Collapsible `🔬 Detailed Lithology, Mineralogy, Instruments & Scientific Questions` tray detailing priority mission questions, diagnostic mineral suites, and past/active mission instruments.

4. **Comparison Laboratory (`modules/comparison_engine.py`):**
   - Side-by-side comparative pairing selector (`Pairing: {Earth Site} ⟷ {Planetary Target}`).
   - Analog Compatibility Index (ACI) gauge with Measurement Coverage (%) and Evidence Availability (%) indicators.
   - Interactive multi-parameter radar chart and feature distance contribution breakdown.
   - Automated scientific evaluation highlighting physical concordance and domain divergence.
   - Collapsible `📋 Detailed Parameter Compatibility Matrix & Distance Values (d_j)` tray displaying exact normalized parameter distances ($d_j$) and weights ($w_j$).

5. **Terrain Analysis (`modules/terrain_analysis.py` & `modules/visualizations.py`):**
   - Topographic cross-sectional elevation transects (SRTM 30m vs. LOLA vs. MOLA).
   - Topographic slope gradient histograms and sub-kilometer RMS roughness curves.
   - Explicit scientific geodetic notice clarifying independent planetary reference datums and distinct horizontal profile spans.

6. **NASA Data Observatory (`modules/nasa_data_observatory.py`):**
   - Structured catalog of 12 planetary and Earth-observing datasets across 3 discipline categories (Earth Observing, Lunar Science, Mars Exploration).
   - Standardized dataset cards with mission/instrument attribution, 1-sentence scientific use summaries, live integration badges, and direct links to official NASA PDS archives.
   - Collapsible metadata specification panels containing PDS node assignments, product IDs, spatial/temporal resolutions, measurement units, and academic citations.
   - Collapsible `📊 Complete Dataset Integration Status Audit Matrix` tray.

7. **Research Reports (`modules/research_report.py`):**
   - Formal scientific report viewer serving as the academic archive for the platform.
   - Complete mathematical derivations of the ACI algorithm and normalized distance formulas.
   - Full parameter distance comparison matrix and technical integration status audit.
   - Documented scientific caveats and peer-reviewed literature citations.
   - Full export suite: Downloadable vector scientific dossier in **PDF** format (built via ReportLab), structured **JSON** schema, and tabular **CSV** metrics.

8. **About Earth2Orbit (`modules/about_page.py`):**
   - Project motivation, engineering objectives, and NASA challenge framing.
   - End-to-end modular system architecture and data processing pipeline.
   - Physical constraints and analog modeling boundaries.
   - Collapsible `📄 Open-Source Licenses & Software Credits` crediting Hummingbird UI (MIT License) and foundational scientific libraries.
   - Collapsible `🚀 Planned Future Enhancements` development roadmap.

---

## 🛠️ Technology Stack

- **Language:** Python 3.12
- **Core Web Framework:** [Streamlit](https://streamlit.io/) (>=1.35.0)
- **Geospatial & Mapping:** [Folium](https://python-visualization.github.io/folium/) (>=0.16.0), [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium) (>=0.20.0)
- **Data Visualization:** [Plotly](https://plotly.com/python/) (>=5.18.0)
- **Numerical Computing & Analysis:** [NumPy](https://numpy.org/) (>=1.24.0), [Pandas](https://pandas.pydata.org/) (>=2.0.0)
- **Document & Dossier Generation:** [ReportLab](https://www.reportlab.com/) (>=4.0.0)
- **Web Services & APIs:** [Requests](https://requests.readthedocs.io/) (>=2.31.0)
- **Design System:** Adapted from Rhombus CRM Dashboard System (Hummingbird UI under MIT License)

---

## 📐 Scientific Methodology: Analog Compatibility Index (ACI)

Earth2Orbit uses an empirical, multi-criteria normalized distance framework to quantify comparability across verified parameters without fabricating missing data:

### Normalized Distance Metric
For each evaluated parameter $j$, the normalized difference $d_j \in [0.0, 1.0]$ between Earth analog value $x_{\text{Earth}, j}$ and planetary target value $x_{\text{Target}, j}$ is defined by:

$$d_j = \min\left(1.0, \frac{|x_{\text{Earth}, j} - x_{\text{Target}, j}|}{R_j}\right)$$

Where $R_j$ is the physically bounded parameter range scale:

| Parameter Domain | Units | Range Scale ($R_j$) | Weight ($w_j$) | Scientific Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Topographic Relief** | meters | $5,000\text{ m}$ | 1.0 | Bounds terrestrial mountain relief and planetary crater rim depths. |
| **Mean Regional Slope** | degrees | $35.0^\circ$ | 1.0 | Angle of repose for dry silicate regolith and scree slopes. |
| **Terrain Roughness** | m RMS | $2.0\text{ m}$ | 1.0 | Root-mean-square surface height deviation at sub-kilometer baseline. |
| **Diurnal Thermal Swing** | K / °C | $260.0\text{ K}$ | 1.0 | Maximum diurnal surface thermal swing on airless lunar polar rims. |
| **Lithology Affinity** | Score (0–1) | $1.0$ | 1.5 | Petrological process concordance (impact, volcanism, evaporites). |
| **Mineral Jaccard Index** | Index (0–1) | $1.0$ | 1.5 | Overlap ratio of diagnostic mineral classes: $\frac{\|M_E \cap M_P\|}{\|M_E \cup M_P\|}$. |
| **Surface Pressure** | hPa | $1,000\text{ hPa}$ | 0.8 | Standard sea-level pressure. **Excluded for airless vacuum regimes.** |

### Composite ACI Calculation
Individual parameter similarity is $s_j = 1.0 - d_j$. The composite index evaluates only over parameters with verified, physically valid data ($j \in \text{Available}$):

$$\text{ACI} = 100 \times \left(1.0 - \frac{\sum_{j \in \text{Available}} w_j \cdot d_j}{\sum_{j \in \text{Available}} w_j}\right)$$

### Missing Data & Evidence Availability
- **Missing Data Exclusion:** When a parameter is physically absent (e.g., atmospheric pressure on the Moon) or unmeasured, it is excluded from both numerator and denominator rather than assigned zero.
- **Measurement Coverage (%):** The proportion of evaluated domains with valid data: $\frac{N_{\text{included}}}{N_{\text{total}}} \times 100$.
- **Evidence Availability (%):** A reliability weighting based on whether data originates from in-situ ground truth ($0.95$), calibrated orbital altimetry/spectroscopy ($0.85$), or regional modeling ($0.70$).

---

## 🏔️ Topographic Geodetic Datums

Comparing raw elevations between planets is invalid without understanding separate planetary reference datums:
1. **Earth:** Orthometric heights referenced to the **EGM96 Geoid** (Mean Sea Level).
2. **The Moon:** Radial displacement referenced to the **1,737.4 km Mean Radius Sphere** (NASA LOLA).
3. **Mars:** Orthometric elevations referenced to the **MOLA Areoid** (equipotential gravity surface at 6.1 mbar mean atmospheric pressure).

Earth2Orbit compares scale-invariant geomorphic metrics: **relative relief ($\Delta h$)**, **local slope gradients**, and **sub-kilometer RMS roughness**, clearly labeling transects as illustrative cross-sections.

---

## 🛰️ NASA & International Data Sources

All planetary and terrestrial datasets used or referenced by Earth2Orbit originate from authoritative scientific archives:

- **NASA LOLA (Lunar Orbiter Laser Altimeter):** Polar laser altimetry profiles across Shackleton Crater and Malapert Mountain via the NASA PDS Geosciences Node.
- **NASA MOLA (Mars Orbiter Laser Altimeter):** High-resolution topography across Jezero Crater delta and crater rim.
- **NASA SRTM (Shuttle Radar Topography Mission):** 30-meter digital elevation models for Lonar Crater, Tso Kar Basin, and Sambhar Lake.
- **NASA POWER Climatology API v2.0:** Live on-demand queries for surface temperature, insolation, and pressure.
- **NASA LROC (Lunar Reconnaissance Orbiter Camera):** High-resolution morphologic observations and crater dimensions.
- **NASA CRISM (Compact Reconnaissance Imaging Spectrometer for Mars):** Diagnostic phyllosilicate and carbonate mineralogy of Jezero Crater.
- **NASA THEMIS (Thermal Emission Imaging System):** Day/night thermal inertia grids.
- **ESA Copernicus Sentinel-2 MSI:** Calibrated multispectral imagery.

---

## ⚠️ Scientific Limitations & Disclaimers

1. **Process-Level Analog Distinction:** No terrestrial analog replicates the total planetary environment. Terrestrial sites serve as models for specific geological or physical sub-processes (e.g., basaltic impact cratering, hypersaline evaporites, permafrost polythermal dynamics), but cannot simulate lunar vacuum, Martian atmospheric chemistry, or fractional gravity ($0.16\text{ g}$ Moon / $0.38\text{ g}$ Mars).
2. **Exploration Candidacy Status:** Lunar reference locations (Shackleton Crater Rim, Malapert Mountain) represent candidate landing zones under active evaluation by the NASA Artemis program, not confirmed or operational permanent Moon bases.
3. **Academic Evaluation Index:** The Analog Compatibility Index (ACI) is an empirical research heuristic developed for comparative science; it is not an official NASA metric or mission qualification standard.
4. **Zero Fabricated Data Guarantee:** Parameters without published or measured data are marked as "Not Available" and omitted from index denominators.

---

## 💻 Installation & Local Execution

### Prerequisites
- Python 3.12 (recommended) or Python 3.10+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/QuantumBoyzz/Earth2Orbit.git
cd Earth2Orbit
```

### 2. Create and Activate a Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run Automated Test Suite
```bash
python -m unittest test_suite.py test_audit_comprehensive.py verify_all_pages_render.py test_reset_and_filters.py
```
*Expected: 32 tests passing with 0 failures.*

### 5. Launch the Streamlit Application
```bash
streamlit run app.py
```
Open your web browser and navigate to `http://localhost:8501`.

---

## ☁️ Deployment to Streamlit Community Cloud

Earth2Orbit is fully configured for zero-configuration deployment on **Streamlit Community Cloud**:

1. **Push Repository to GitHub:**
   - Ensure your repository is named `Earth2Orbit` with the default branch set to `main`.
2. **Connect to Streamlit Cloud:**
   - Log into [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
3. **Create New App:**
   - Select **Repository:** `your-username/Earth2Orbit`
   - Select **Branch:** `main`
   - Set **Main file path:** `app.py`
4. **Deploy:**
   - Click **Deploy!**
   - Streamlit Cloud will read `requirements.txt` and launch the application.

---

## 📄 License & Attribution

- **Project License:** Open-source under the [MIT License](LICENSE).
- **UI Design System:** Adapted from Hummingbird UI / Rhombus Dashboard Template (MIT License).
- **Public Domain Imagery:** NASA public domain photography courtesy of NASA, JPL-Caltech, MSSS, and the LROC Science Operations Center.
- **Team:** Developed by Team **QuantumBoyzz** for the NASA Space Apps Challenge 2026.
