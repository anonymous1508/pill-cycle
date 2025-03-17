import streamlit as st
from datetime import datetime, timedelta

# Initialize session state
if 'cycle_start_date' not in st.session_state:
    st.session_state.cycle_start_date = datetime(2025, 3, 17)  # Future date for testing
if 'pill_status' not in st.session_state:
    st.session_state.pill_status = [False] * 28

def calculate_cycle_info(start_date):
    today = datetime.today()
    days_elapsed = (today - start_date).days
    days_remaining = max(28 - days_elapsed, 0)  # Prevent negative values
    next_cycle_start = start_date + timedelta(days=28)
    current_phase = "Active Pill" if days_elapsed < 24 else "Placebo Pill"
    return days_elapsed, days_remaining, next_cycle_start, current_phase

def calculate_adherence_rate(pill_status):
    taken = sum(pill_status)
    return (taken / 28) * 100 if 28 > 0 else 0

# App layout
st.title("💊 Pill Tracker")

# Current Cycle Section
st.header("Current Cycle")
start_date = st.session_state.cycle_start_date
days_elapsed, days_remaining, next_cycle_start, current_phase = calculate_cycle_info(start_date)

st.write(f"**Started:** {start_date.strftime('%Y-%m-%d')}")
st.write(f"**Days Remaining:** {days_remaining}")
st.write(f"**Next Cycle Starts:** {next_cycle_start.strftime('%Y-%m-%d')}")
st.write(f"**Current Phase:** {current_phase}")

# Adherence Rate
st.write(f"**Adherence Rate:** {calculate_adherence_rate(st.session_state.pill_status):.1f}%")

# Pill Grid (4 rows x 7 columns)
st.header("Pill Tracker")
for row in range(4):
    cols = st.columns(7)
    for col in range(7):
        pill_number = row * 7 + col
        with cols[col]:
            st.checkbox(
                str(pill_number + 1),
                key=f"pill_{pill_number}",
                value=st.session_state.pill_status[pill_number],
                on_change=lambda pn=pill_number: st.session_state.pill_status.__setitem__(pn, not st.session_state.pill_status[pn])
            )

# Reset Button
if st.button("🔄 Reset Cycle"):
    st.session_state.cycle_start_date = datetime.today()
    st.session_state.pill_status = [False] * 28
    st.experimental_rerun()