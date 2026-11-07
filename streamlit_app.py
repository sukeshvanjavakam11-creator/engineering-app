import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

# =====================================================================
# ENGINE CORE: CORE MATH SUBSYSTEMS
# =====================================================================

def track_space_junk(debris_radius, velocity_magnitude):
    """Calculates space debris tracking properties."""
    ALUMINUM_DENSITY = 2700
    volume = (4/3) * math.pi * (debris_radius ** 3)
    mass = volume * ALUMINUM_DENSITY
    kinetic_energy = 0.5 * mass * (velocity_magnitude ** 2)
    cross_section = math.pi * (debris_radius ** 2)
    return {"mass_kg": mass, "kinetic_energy_joules": kinetic_energy, "collision_area_m2": cross_section}

def analyze_thermal_sensor(signal_matrix, noise_floor, calibration_factor):
    """Filters noise and highlights high-intensity thermal signatures."""
    signals = np.array(signal_matrix)
    filtered_signals = np.where(signals > noise_floor, signals, 0)
    calibrated_flux = filtered_signals * calibration_factor
    peak_index = np.unravel_index(np.argmax(calibrated_flux), calibrated_flux.shape)
    peak_value = calibrated_flux[peak_index]
    return {"processed_flux_grid": calibrated_flux, "peak_flux_value": peak_value, "target_coordinates": peak_index}

def simulate_car_aerodynamics(drag_coeff, frontal_area, air_velocity_m_s):
    """Calculates aerodynamic resistance profiles over a chassis."""
    RHO_AIR = 1.225
    drag_force = 0.5 * drag_coeff * RHO_AIR * frontal_area * (air_velocity_m_s ** 2)
    power_loss_watts = drag_force * air_velocity_m_s
    power_loss_hp = power_loss_watts / 745.7
    return {"drag_force_newtons": drag_force, "power_loss_hp": power_loss_hp}


# =====================================================================
# STREAMLIT WEB UI INTERFACE
# =====================================================================

st.set_page_config(page_title="Space & Aerodynamics Analysis Suite", layout="wide")
st.title("Sukesh's Space & Aerodynamics Analysis Suite")

tab1, tab2, tab3 = st.tabs(["1. Space Junk Tracker", "2. Thermal Detector", "3. Car Aerodynamics"])

# --- TAB 1: SPACE JUNK DESIGN ---
with tab1:
    st.header("Debris Parameters")
    col1, col2 = st.columns(2)
    with col1:
        junk_radius = st.number_input("Debris Radius (meters):", value=0.05, format="%.4f")
    with col2:
        junk_velocity = st.number_input("Orbital Velocity (m/s):", value=7500.0)
        
    if st.button("Analyze Threat Profile"):
        res = track_space_junk(junk_radius, junk_velocity)
        st.subheader("=== RE-ENTRY & COLLISION PROFILE ===")
        st.write(f"**Calculated Mass:** {res['mass_kg']:.4f} kg")
        st.write(f"**Collision Cross-Sectional Area:** {res['collision_area_m2']:.5f} m²")
        st.write(f"**Kinetic Energy Impact Potential:** {res['kinetic_energy_joules']:.2f} Joules")

# --- TAB 2: THERMAL RADIATION DESIGN ---
with tab2:
    st.header("Matrix Controls")
    floor = st.number_input("Noise Floor Level:", value=20.0)
    
    if st.button("Process Thermal Matrix"):
        # Fixed complete numeric matrix layout to prevent compilation syntax errors
        mock_matrix = [
            [12.5, 14.2, 18.1, 15.0],
            [10.2, 85.4, 22.1, 19.3],
            [11.0, 16.8, 14.5, 12.2],
            [14.1, 13.9, 17.2, 16.0]
        ]
        res = analyze_thermal_sensor(mock_matrix, floor, calibration_factor=0.045)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        im = ax.imshow(res['processed_flux_grid'], cmap='inferno', interpolation='nearest')
        fig.colorbar(im, ax=ax, label="Radiant Flux (W/m²)")
        ax.set_title(f"Target Peak Hotspot at Node Matrix: {res['target_coordinates']}")
        st.pyplot(fig)

# --- TAB 3: CAR AERODYNAMICS DESIGN ---
with tab3:
    st.header("Hull Specification")
    col1, col2 = st.columns(2)
    with col1:
        car_cd = st.number_input("Drag Coefficient (Cd):", value=0.28, format="%.2f")
    with col2:
        car_area = st.number_input("Frontal Cross Area (m²):", value=2.2, format="%.2f")
        
    if st.button("Compute Performance Curve"):
        velocities = np.linspace(1, 45, 50)
        drag_forces = [simulate_car_aerodynamics(car_cd, car_area, v)["drag_force_newtons"] for v in velocities]
        power_losses = [simulate_car_aerodynamics(car_cd, car_area, v)["power_loss_hp"] for v in velocities]
        
        fig, ax1 = plt.subplots(figsize=(8, 4))
        color = 'tab:red'
        ax1.set_xlabel('Wind Velocity / Airflow speed (m/s)')
        ax1.set_ylabel('Total Drag Force (N)', color=color)
        ax1.plot(velocities, drag_forces, color=color, linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Power Lost to Resisting Drag (HP)', color=color)
        ax2.plot(velocities, power_losses, color=color, linestyle='dashed', linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color)
        
        fig.tight_layout()
        ax1.set_title("Fluid Resistance Dynamics Performance Profile")
        st.pyplot(fig)
