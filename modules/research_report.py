"""
Earth2Orbit — Research Reports Module
Formal scientific report viewer and export system adapted to the Rhombus Design System:
- Rhombus Page Header and Pairing Selectors
- Native container presentation with ZERO HTML leakage
- Publication-grade ReportLab Vector PDF generation
- Structured JSON and CSV dataset export buttons
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timezone
from utils.metrics import calculate_planetary_similarity, FEATURE_METADATA
from modules.pdf_generator import generate_dossier_pdf
from utils.ui_components import render_rhombus_page_header, render_rhombus_card_header, render_html


def render_research_report(earth_analogs: list, planetary_bodies: list, data_sources: dict):
    """Generates structured scientific research dossiers and export files without HTML leakage."""

    render_rhombus_page_header(
        title="Research Reports",
        subtitle="Formal publication-ready research dossiers summarizing quantitative metrics, datasets, and limitations"
    )

    # Selection controls in native container
    with st.container(border=True):
        render_rhombus_card_header("Select Pair for Dossier Generation", "Choose a terrestrial field site and a planetary target")
        col_e, col_p = st.columns(2)
        with col_e:
            earth_names = [a["name"] for a in earth_analogs]
            sel_e_name = st.selectbox("Earth Analog Field Site:", earth_names, key="rep_e")
            selected_earth = next((a for a in earth_analogs if a["name"] == sel_e_name), earth_analogs[0])

        with col_p:
            target_options = []
            target_map = {}
            for body in planetary_bodies:
                for t in body.get("targets", []):
                    label = f"{body['body_name']} — {t['name']}"
                    target_options.append(label)
                    target_map[label] = (body, t)

            default_pair = (planetary_bodies[0], planetary_bodies[0]["targets"][0]) if planetary_bodies and planetary_bodies[0].get("targets") else (None, None)
            sel_p_label = st.selectbox("Planetary Target Region:", target_options, key="rep_p")
            selected_body, selected_target = target_map.get(sel_p_label, default_pair)

    # Calculate comparison data
    results = calculate_planetary_similarity(selected_earth, selected_target, selected_body)
    timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    report_id = f"E2O-{results['earth_id'].upper()}-{results['target_id'].upper()}"

    # Dossier Document Presentation (Native Streamlit Container)
    with st.container(border=True):
        st.caption(f"EARTH2ORBIT RESEARCH DOSSIER // REPORT ID: {report_id} // {timestamp_str}")
        render_html(
            f"""
            <h2 style='font-size: 1.6rem; font-weight: 700; color: #202020; margin-top: 0; margin-bottom: 0.5rem;'>
                Planetary Analog Compatibility Evaluation Report
            </h2>
            <p style='font-size: 0.9rem; color: #555555; margin-bottom: 1rem;'>
                <strong>Field Site:</strong> {selected_earth['name']} ({selected_earth['region']}, {selected_earth['country']}) ⟷ 
                <strong>Target Region:</strong> {selected_target['name']} ({selected_body['body_name']})
            </p>
            """
        )
        st.divider()

        # Section 1: Executive Summary
        st.markdown("### 1. Executive Summary & Compatibility Assessment")
        st.write(results["scientific_interpretation"])

        # Metric Tiles (High-Contrast)
        aci_val = results["aci_score_pct"]
        cov_val = results["measurement_coverage_pct"]
        evi_val = results["evidence_availability_pct"]

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Analog Compatibility Index (ACI)", f"{aci_val:.1f}%", "Normalized Multi-criteria Metric")
        with m_col2:
            st.metric("Measurement Coverage", f"{cov_val:.1f}%", f"{results['available_count']} of {results['total_potential_count']} parameters")
        with m_col3:
            st.metric("Evidence Availability", f"{evi_val:.1f}%", "Verified Orbital / In-situ Data")

        st.divider()

        # Section 2: Mathematical Methodology & ACI Scoring Engine
        st.markdown("### 2. Mathematical Methodology & ACI Scoring Engine")
        st.markdown(
            """
            The **Analog Compatibility Index (ACI)** is an empirical multi-criteria framework that quantifies 
            concordance between terrestrial field sites and planetary targets across topography, slope, roughness, 
            thermal dynamics, lithology, and mineralogy.

            **Mathematical Formulation:**
            - **Normalized Parameter Distance:**
              $$d_j = \\min\\left(1.0, \\frac{|x_{\\text{Earth},j} - x_{\\text{Target},j}|}{R_j}\\right)$$
              where $x_{\\text{Earth},j}$ and $x_{\\text{Target},j}$ are observed measurements, and $R_j$ is the calibrated dynamic normalization range.
            - **Domain Concordance Score:**
              $$S_j = 1.0 - d_j$$
            - **Weighted Aggregate ACI Score:**
              $$\\text{ACI} = 100 \\times \\left(1.0 - \\frac{\\sum_{j \\in \\mathcal{A}} w_j d_j}{\\sum_{j \\in \\mathcal{A}} w_j}\\right)$$
              where $\\mathcal{A}$ denotes the subset of verified parameters, and $w_j$ represents domain sensitivity weights.
            - **Missing Data & Atmospheric Exclusion:**
              Parameters lacking empirical measurement or physically absent (e.g. atmospheric pressure on the Moon) 
              are strictly excluded from the denominator set $\\mathcal{A}$ to prevent mathematical distortion.
            """
        )

        st.divider()

        # Section 3: Parameter Breakdown
        st.markdown("### 3. Physical & Geochemical Parameter Breakdown")
        
        rep_rows = []
        for k, feat in results["features"].items():
            rep_rows.append({
                "Parameter Domain": feat["name"],
                "Earth Analog Measurement": feat["earth_val"],
                "Planetary Target Measurement": feat["target_val"],
                "Distance (d_j)": f"{feat['norm_distance']:.2f}",
                "Compatibility Score": f"{feat['similarity']*100:.1f}%",
                "Weight (w_j)": f"{feat['weight']:.1f}",
                "Status": "Included"
            })
        for ex in results["excluded_features"]:
            rep_rows.append({
                "Parameter Domain": ex["name"],
                "Earth Analog Measurement": f"{selected_earth.get(ex['key'], 'N/A')}",
                "Planetary Target Measurement": "Not Available (Excluded)",
                "Distance (d_j)": "N/A",
                "Compatibility Score": "Excluded",
                "Weight (w_j)": "0.0",
                "Status": "Insufficient Data"
            })

        df_rep = pd.DataFrame(rep_rows)
        st.dataframe(df_rep, use_container_width=True)

        st.divider()

        # Section 4: Observational Datasets
        st.markdown("### 4. NASA & ESA Source Observational Datasets")
        c_src1, c_src2 = st.columns(2)
        with c_src1:
            st.markdown("**Terrestrial Earth Observation Datasets:**")
            st.markdown(
                "- **NASA SRTM 30m Global DEM:** Space Shuttle Endeavour STS-99 (NASA/JPL/NGA)\n"
                "- **NASA POWER Agroclimatology:** Climatology Point API v2.0 (NASA Langley)\n"
                "- **ESA Copernicus Sentinel-2 MSI:** 10m/20m Bottom-of-Atmosphere Reflectance"
            )
        with c_src2:
            st.markdown(f"**{selected_body['body_name']} Mission Instrumentation:**")
            for instr in selected_target.get("instruments", []):
                st.markdown(f"- **{instr['instrument']}** ({instr['spacecraft']}) — `{instr['dataset_id']}`")

        with st.expander("Complete Planetary & Terrestrial Dataset Integration Audit Matrix", expanded=False):
            audit_rows = []
            for s in data_sources.get("planetary_sources", []):
                inst = s.get("instrument") or s.get("name", "Instrument")
                craft = s.get("spacecraft") or s.get("mission", "")
                audit_rows.append({
                    "Body": s.get("body", "Planetary"),
                    "Dataset / Sensor": f"{inst} ({craft})" if craft else inst,
                    "Technical Status": s.get("status_label", "Referenced"),
                    "Spatial Resolution": s.get("resolution", "Variable"),
                    "Archive Node": s.get("pds_node", "NASA PDS Node")
                })
            for s in data_sources.get("earth_sources", []):
                name = s.get("name", "Dataset")
                sensor = s.get("sensor", "")
                audit_rows.append({
                    "Body": "Earth",
                    "Dataset / Sensor": f"{name} ({sensor})" if sensor and sensor != name else name,
                    "Technical Status": s.get("status_label", "Referenced"),
                    "Spatial Resolution": s.get("spatial_resolution", "Variable"),
                    "Archive Node": s.get("provider", "NASA Earthdata")
                })
            st.dataframe(pd.DataFrame(audit_rows), use_container_width=True)

        st.divider()

        # Section 5: Limitations
        st.markdown("### 5. Scientific Caveats & Research Limitations")
        for lim in results["limitations"]:
            st.markdown(f"- ⚠️ {lim}")

        st.divider()

        # Section 6: References
        st.markdown("### 6. Peer-Reviewed Literature & Field Citations")
        for ref in selected_earth.get("references", []):
            st.markdown(f"- {ref['citation']}")

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Export Suite in native container
    with st.container(border=True):
        render_rhombus_card_header("Download Research Dossier", "Export publication-ready documents in vector PDF, JSON, or CSV formats")

        # Prepare JSON Payload
        export_payload = {
            "dossier_metadata": {
                "title": "Earth2Orbit — Planetary Analog Compatibility Dossier",
                "report_id": report_id,
                "timestamp_utc": timestamp_str,
                "earth_analog": selected_earth["name"],
                "planetary_target": selected_target["name"],
                "planetary_body": selected_body["body_name"],
                "team": "QuantumBoyzz",
                "challenge": "NASA Space Apps Challenge 2026"
            },
            "quantitative_results": results,
            "earth_analog_profile": selected_earth,
            "planetary_target_profile": selected_target
        }
        json_str = json.dumps(export_payload, indent=2)
        csv_str = df_rep.to_csv(index=False)

        # Generate PDF in memory via ReportLab
        pdf_bytes = generate_dossier_pdf(results, selected_earth, selected_target, selected_body)

        # Export Buttons
        col_pdf, col_json, col_csv = st.columns(3)
        with col_pdf:
            st.download_button(
                label="📄 Download PDF Dossier",
                data=pdf_bytes,
                file_name=f"Earth2Orbit_{results['earth_id']}_{results['target_id']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col_json:
            st.download_button(
                label="📥 Download JSON Data",
                data=json_str,
                file_name=f"Earth2Orbit_{results['earth_id']}_{results['target_id']}.json",
                mime="application/json",
                use_container_width=True
            )
        with col_csv:
            st.download_button(
                label="📊 Download CSV Matrix",
                data=csv_str,
                file_name=f"Earth2Orbit_Matrix_{results['earth_id']}_{results['target_id']}.csv",
                mime="text/csv",
                use_container_width=True
            )
