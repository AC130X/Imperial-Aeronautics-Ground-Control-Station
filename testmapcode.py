from nicegui import ui
import math
import random

# London center
LONDON_LAT = 51.5074
LONDON_LON = -0.1278
RADIUS_KM = 20.0

def generate_gps_point():
    """Generates a random GPS point within a radius."""
    radius_in_degrees = RADIUS_KM / 111.0
    u, v = random.random(), random.random()
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v

    delta_lat = w * math.cos(t)
    delta_lon = (w * math.sin(t)) / math.cos(math.radians(LONDON_LAT))

    lat = LONDON_LAT + delta_lat
    lon = LONDON_LON + delta_lon
    alt = random.uniform(50.0, 250.0)
    return lat, lon, alt

@ui.page('/')
def main_page():
    # --- Top Control Panel ---
    # Using a card to make it look like a neat control dashboard
    with ui.card().classes('w-full flex-row items-center justify-between p-4'):
        ui.label("Ground Control Station - London Sector").classes('text-2xl font-bold')
        telemetry_label = ui.label("GPS Status: Initializing...").classes('text-lg font-mono font-bold text-blue-600')

    # --- Map Widget ---
    # ui.leaflet integrates Leaflet.js directly into the browser
    map_widget = ui.leaflet(center=(LONDON_LAT, LONDON_LON), zoom=11).classes('w-full h-[600px] mt-4 rounded-lg shadow-md')
    
    # Place initial vehicle marker
    marker = map_widget.marker(latlng=(LONDON_LAT, LONDON_LON))

    def update_telemetry():
        """Simulates receiving a new GPS packet and updates the web UI."""
        lat, lon, alt = generate_gps_point()

        # Update marker on map to new position
        marker.move(lat, lon)

        # Update UI telemetry readout
        telemetry_label.set_text(f"Lat: {lat:.5f} | Lon: {lon:.5f} | Alt: {alt:.1f}m")

    # --- Live Telemetry Loop ---
    # NiceGUI handles background loops natively with ui.timer
    ui.timer(2.0, update_telemetry)

# Run the web application
if __name__ in {"__main__", "__mp_main__"}:

    ui.run(title="Desktop GCS", native=True, window_size=(1000, 700))