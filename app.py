import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Macro-Health Debt Dashboard", page_icon="⚖️", layout="wide")

# --- Sidebar ---
st.sidebar.header("🕹️ Strategic Controls")
total_capital = st.sidebar.slider("Capital Allocation ($ Billion)", 0.1, 10.0, 1.2)
restructure_rate = st.sidebar.slider("Restructuring Favorability (%)", 0, 100, 75)

# --- Macro Logic Calculations ---
roi = (100 - restructure_rate) * (total_capital / 15) + 3.5
health_index = min(100, (restructure_rate * 0.7) + (total_capital * 3))
inflation = max(1.8, 6.0 - (health_index / 18))
tax_avoided = (total_capital * (restructure_rate / 100)) * 1.25

# --- Impact Scores for Agents ---
households_score = 80 if inflation < 3 else 40
firms_score = 85 if health_index > 70 else 45
state_score = 90 if tax_avoided > 2 else 50

# --- Main Interface ---
st.title("⚖️ Sovereign & Corporate Debt Restructuring Dashboard")

tab1, tab2 = st.tabs(["📊 Live Dashboard", "🧬 Technical Logic & Math"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Portfolio ROI", f"{roi:.2f}%")
    col2.metric("Economic Health", f"{health_index:.1f}/100")
    col3.metric("Inflation Rate", f"{inflation:.2f}%")
    col4.metric("Tax Burden Avoided", f"${tax_avoided:.2f}B")

    st.divider()
    
    l_chart, r_chart = st.columns([2, 1])
    with l_chart:
        st.subheader("📈 Systemic Equilibrium")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        h_trend = np.linspace(health_index * 0.8, health_index, 12) + np.random.normal(0, 1, 12)
        r_trend = np.linspace(roi * 0.9, roi, 12) + np.random.normal(0, 0.2, 12)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=h_trend, name="Health Index", line=dict(color='#2ecc71', width=4)))
        fig.add_trace(go.Scatter(x=months, y=r_trend, name="ROI (%)", line=dict(color='#3498db', dash='dot')))
        st.plotly_chart(fig, use_container_width=True)
    
    with r_chart:
        st.subheader("🧘 Tranquility Report")
        if restructure_rate > 70:
            st.success("Systemic Integrity High. No fiscal intervention required.")
        else:
            st.error("Systemic Distress. High risk of tax hikes")

    st.divider()
    st.subheader("🏛️ Impact sur les Agents Économiques")

    # Radar Chart with color-coded zones
    categories = ["Ménages", "Entreprises", "État"]
    values = [households_score, firms_score, state_score]
    values += values[:1]  # fermer le polygone

    radar_fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name='Impact',
                line=dict(color="green" if min(values) > 70 else "red")
            )
        ],
        layout=go.Layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True
        )
    )

    # Ajouter une légende colorée manuelle
    radar_fig.add_trace(go.Scatterpolar(
        r=[0], theta=[0], mode='markers',
        marker=dict(color="red", size=10),
        name="Zone vulnérable (<50)"
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=[0], theta=[0], mode='markers',
        marker=dict(color="yellow", size=10),
        name="Zone intermédiaire (50-70)"
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=[0], theta=[0], mode='markers',
        marker=dict(color="green", size=10),
        name="Zone favorable (>70)"
    ))

    st.plotly_chart(radar_fig, use_container_width=True)

with tab2:
    st.header("The Mathematical Framework")
    st.write("This dashboard is powered by the **Fiscal Offset Equation**:")
    
    st.latex(r"T_a = (D_r \times \alpha) + (S_c \times \beta)")
    
    st.markdown("""
    ### Variable Definitions:
    * **$T_a$ (Tax Burden Avoided):** The total financial relief provided to the State's treasury.
    * **$D_r$ (Restructured Debt):** Principal amount moved from predatory terms to sustainable terms.
    * **$alpha$ (Solvency Multiplier):** Constant (1.15) representing the avoided costs of legal bankruptcy and liquidation.
    * **$S_c$ (Social Cost):** Saved public spending on unemployment and welfare.
    * **$beta$ (Velocity Factor):** The multiplier effect of keeping capital within productive SMEs.
    
    ### Inflation Anchor Logic:
    Our model assumes that **Inflation** is a function of **Supply Scarcity**. By preventing defaults, we maintain the Aggregate Supply ($AS$), ensuring that:
    """)
    st.latex(r"P = \frac{M \times V}{Y}")
    st.write("Where $Y$ (Output) is stabilized by private debt restructuring, keeping $P$ (Prices) constant without raising taxes.")
