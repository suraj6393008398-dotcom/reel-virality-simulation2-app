import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Reel Virality Simulator", layout="wide")
st.title(" Instagram Reel Virality Simulator")
st.write("")
if "history" not in st.session_state:
    st.session_state.history = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "show_comparison" not in st.session_state:
    st.session_state.show_comparison = False
st.sidebar.header(" Input Parameters")
v0_input = st.sidebar.text_input("Initial Viewers (V0)", placeholder="Enter initial viewers")
s0_input = st.sidebar.text_input("Initial Sharers (S0)", placeholder="Enter initial shares")
total_pop_input = st.sidebar.text_input("Total Audience (N)", placeholder="Enter total audience")
growth_input = st.sidebar.text_input("Growth Rate", placeholder="Enter growth rate")
decay_input = st.sidebar.text_input("Decay Rate", placeholder="Enter decay rate")
duration_input = st.sidebar.text_input("Time Duration (T)", placeholder="Enter total duration")
run_button = st.sidebar.button(" Run Simulation")
def simulate_virality(V0, S0, g, d, T, N):
    t = np.arange(0, int(T))
    viewers_list = []
    V = V0   
    for i in t:
        new_views = g * V * (1 - V / N)
        drop_off = d * V     
        V = V + new_views - drop_off
        V = max(0, min(V, N))       
        viewers_list.append(V)    
    return t, viewers_list
if run_button:
    try:
        v0 = int(v0_input)
        s0 = int(s0_input)
        total_pop = int(total_pop_input)
        growth_rate = float(growth_input)
        decay_rate = float(decay_input)
        duration = int(duration_input)
        t, viewers = simulate_virality(v0, s0, growth_rate, decay_rate, duration, total_pop)     
        peak_val = max(viewers)
        peak_time = t[viewers.index(peak_val)]
        final_val = viewers[-1]
        st.session_state.history.append({
            "Growth": growth_rate,
            "Decay": decay_rate,
            "Peak": int(peak_val),
            "Peak Time": int(peak_time),
            "Final": int(final_val),
            "graph_data": viewers
        })
        col1, col2, col3 = st.columns(3)
        col1.metric(" Peak Viewers", f"{int(peak_val):,}")
        col2.metric(" Time to Peak", f"{int(peak_time)} units")
        col3.metric(" Final Status", f"{int(final_val):,}")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, viewers, color='#833AB4', linewidth=3)
        ax.fill_between(t, viewers, color='#FD1D1D', alpha=0.1)     
        ax.set_xlabel("Time")
        ax.set_ylabel("Viewers")
        ax.set_title("Reel Growth Curve")
        ax.grid(True, linestyle='--', alpha=0.5)     
        st.pyplot(fig)
    except:
        st.error(" Please enter valid numeric values in all fields")
st.write("")  
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
        for i, run in enumerate(st.session_state.history):
            if st.button(f"Show Graph for Run {i+1}", key=f"run_{i}"):
                fig_single, ax_single = plt.subplots(figsize=(10, 4))
                ax_single.plot(run['graph_data'], linewidth=3)
                ax_single.fill_between(range(len(run['graph_data'])), run['graph_data'], alpha=0.1)
                ax_single.set_title(f"Run {i+1}")
                ax_single.grid(True, linestyle='--', alpha=0.5) 
                st.pyplot(fig_single)
    else:
        st.info("No history available. Run simulation first.")
if st.session_state.show_comparison:
    st.subheader(" Comparison")
    if len(st.session_state.history) > 1:
        fig_comp, ax_comp = plt.subplots(figsize=(10, 4))   
        for i, run in enumerate(st.session_state.history):
            ax_comp.plot(run['graph_data'], linewidth=2,
                         label=f"Run {i+1}")
        ax_comp.set_title("Comparison of Runs")
        ax_comp.grid(True, linestyle='--', alpha=0.6)
        ax_comp.legend()
        st.pyplot(fig_comp)
    else:
        st.warning("Run at least 2 times for comparison")