import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Reel Virality Simulator", layout="wide")

st.title(" Instagram Reel Virality Simulator")

# Session states
if "history" not in st.session_state:
    st.session_state.history = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "show_comparison" not in st.session_state:
    st.session_state.show_comparison = False

# Sidebar Inputs
st.sidebar.header(" Input Parameters")

v0_input = st.sidebar.text_input("Initial Viewers (V0)")
total_pop_input = st.sidebar.text_input("Total Audience (N)")
growth_input = st.sidebar.text_input("Growth Rate")
decay_input = st.sidebar.text_input("Decay Rate")
duration_input = st.sidebar.text_input("Time Duration (T)")

run_button = st.sidebar.button(" Run Simulation")

# Simulation Function (with rounding)
def simulate_virality(V0, g, d, T, N):
    t = np.arange(0, int(T))
    viewers_list = []
    table_data = []

    V = float(V0)

    for i in t:
        current_V = round(V, 2)

        growth = round(g * current_V * (1 - current_V / N), 2)
        decay = round(d * current_V, 2)

        next_V = round(current_V + growth - decay, 2)
        next_V = max(0, min(next_V, N))

        table_data.append({
            "Day": i,
            "V(t)": current_V,
            "Growth": growth,
            "Decay": decay,
            "V(t+1)": next_V
        })

        viewers_list.append(current_V)
        V = next_V

    return t, viewers_list, table_data


# Run Simulation
if run_button:
    try:
        v0 = int(v0_input)
        total_pop = int(total_pop_input)
        growth_rate = float(growth_input)
        decay_rate = float(decay_input)
        duration = int(duration_input)

        t, viewers, table = simulate_virality(
            v0, growth_rate, decay_rate, duration, total_pop
        )

        peak_val = max(viewers)
        peak_time = viewers.index(peak_val)
        final_val = viewers[-1]

        st.session_state.history.append({
            "Growth": growth_rate,
            "Decay": decay_rate,
            "Peak": int(peak_val),
            "Peak Time": int(peak_time),
            "Final": int(final_val),
            "graph_data": viewers
        })

        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric(" Peak Viewers", f"{int(peak_val):,}")
        col2.metric(" Time to Peak", f"{int(peak_time)} units")
        col3.metric(" Final Status", f"{int(final_val):,}")

        # ✅ GRAPH FIRST (NO DOTS)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, viewers, linewidth=3)
        ax.fill_between(t, viewers, alpha=0.1)

        ax.set_xlabel("Time (Days)")
        ax.set_ylabel("Viewers")
        ax.set_title("Viral Growth Curve")
        ax.grid(True, linestyle='--', alpha=0.5)

        st.pyplot(fig)

        # ✅ TABLE BELOW GRAPH
        st.subheader(" Step-wise Calculation")
        df = pd.DataFrame(table)
        st.dataframe(df, use_container_width=True)

    except:
        st.error(" Please enter valid numeric values")

# History Section
history_count = len(st.session_state.history)

colA, colB = st.columns(2)

with colA:
    if history_count >= 1:
        if st.button(" Show Simulation History"):
            st.session_state.show_history = not st.session_state.show_history

with colB:
    if history_count >= 2:
        if st.button(" Show Comparison"):
            st.session_state.show_comparison = True

if st.session_state.show_history:
    st.subheader(" Simulation History")

    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history).drop(columns=['graph_data'])
        st.dataframe(history_df, use_container_width=True)

        if st.button(" Clear All History"):
            st.session_state.history = []
            st.session_state.show_history = False
            st.session_state.show_comparison = False
            st.rerun()

# Comparison Graph (NO DOTS)
if st.session_state.show_comparison:
    st.subheader(" Comparison")

    if len(st.session_state.history) > 1:
        fig_comp, ax_comp = plt.subplots(figsize=(10, 4))

        for i, run in enumerate(st.session_state.history):
            ax_comp.plot(run['graph_data'], linewidth=2, label=f"Run {i+1}")

        ax_comp.set_title("Comparison of Runs")
        ax_comp.grid(True, linestyle='--', alpha=0.6)
        ax_comp.legend()

        st.pyplot(fig_comp)
    else:
        st.warning("Run at least 2 times")
