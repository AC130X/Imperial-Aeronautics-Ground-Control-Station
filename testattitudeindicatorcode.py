from nicegui import ui
import random

# --- FLIGHT STATE ---
class Telemetry:
    armed = False
    pitch = 0.0      # degrees (-90 to 90)
    roll = 0.0       # degrees (-180 to 180)
    heading = 0.0    # degrees
    alt = 150.0      # meters
    airspeed = 45.0  # m/s
    vsi = 0.0        # m/s
    alpha = 0.0      # degrees
    g_force = 1.0    # Gs

telemetry = Telemetry()

# --- HELPER FUNCTION FOR GAUGES ---
def instrument_box(label_text, default_val, text_color="text-white"):
    """Creates a styled box for numerical values with the label below it."""
    with ui.column().classes('items-center gap-1 mb-3 w-28'):
        # The Box
        with ui.element('div').classes('bg-black border-2 border-slate-600 rounded-lg py-2 w-full flex justify-center items-center shadow-inner'):
            val_label = ui.label(default_val).classes(f'text-2xl font-mono font-bold {text_color}')
        # The Text Below
        ui.label(label_text).classes('text-slate-400 font-bold text-xs tracking-widest uppercase')
    return val_label

@ui.page('/')
def main_page():
    ui.dark_mode().enable()
    
    # Main container
    with ui.row().classes('w-full justify-center items-start gap-12 p-10 min-h-screen text-white bg-slate-900'):
        
        # ==========================================
        # LEFT: INSTRUMENT PANEL
        # ==========================================
        with ui.column().classes('items-center bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700'):
            
            with ui.row().classes('items-center gap-8'):
                
                # --- LEFT COLUMN (Speed & Aerodynamics) ---
                with ui.column().classes('items-center'):
                    spd_label = instrument_box('SPD (m/s)', '0.0')
                    vsi_label = instrument_box('VSI (m/s)', '0.0')
                    alpha_label = instrument_box('ALPHA (°)', '0.0')
                    g_label = instrument_box('G-FORCE', '1.0')
                    
                # --- CENTER COLUMN (Artificial Horizon) ---
                with ui.column().classes('items-center justify-center h-full'):
                    with ui.element('div').classes('w-[350px] h-[350px] rounded-2xl overflow-hidden relative border-4 border-slate-600 bg-black shadow-inner'):
                        
                        # Moving horizon plane
                        horizon = ui.element('div').classes('absolute w-[1000px] h-[1000px] left-[-325px] top-[-325px]')
                        horizon.style('background: linear-gradient(to bottom, #1E5C99 50%, #7A4B29 50%); transition: transform 0.05s linear;')
                        
                        with horizon:
                            # Pitch Ladder
                            svg_ladder = '''
                            <svg width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">
                                <g stroke="white" stroke-width="3" fill="none">
                                    <line x1="0" y1="500" x2="1000" y2="500" stroke-width="5"/> <line x1="450" y1="450" x2="550" y2="450"/> <line x1="450" y1="450" x2="450" y2="460"/> <line x1="550" y1="450" x2="550" y2="460"/>
                                    <line x1="420" y1="400" x2="580" y2="400"/> <line x1="420" y1="400" x2="420" y2="410"/> <line x1="580" y1="400" x2="580" y2="410"/>
                                    <line x1="450" y1="350" x2="550" y2="350"/> <line x1="450" y1="350" x2="450" y2="360"/> <line x1="550" y1="350" x2="550" y2="360"/>
                                    
                                    <line x1="450" y1="550" x2="550" y2="550"/> <line x1="450" y1="550" x2="450" y2="540"/> <line x1="550" y1="550" x2="550" y2="540"/>
                                    <line x1="420" y1="600" x2="580" y2="600"/> <line x1="420" y1="600" x2="420" y2="590"/> <line x1="580" y1="600" x2="580" y2="590"/>
                                    <line x1="450" y1="650" x2="550" y2="650"/> <line x1="450" y1="650" x2="450" y2="640"/> <line x1="550" y1="650" x2="550" y2="640"/>
                                </g>
                            </svg>
                            '''
                            ui.html(svg_ladder)
                            
                        # Static Yellow Crosshair
                        crosshair = '''
                        <svg width="350" height="350" class="absolute top-0 left-0" xmlns="http://www.w3.org/2000/svg">
                            <g stroke="yellow" stroke-width="4">
                                <line x1="120" y1="175" x2="160" y2="175"/>
                                <line x1="190" y1="175" x2="230" y2="175"/>
                                <line x1="175" y1="160" x2="175" y2="190"/>
                                <circle cx="175" cy="175" r="4" fill="red" stroke="none"/>
                            </g>
                        </svg>
                        '''
                        ui.html(crosshair)

                # --- RIGHT COLUMN (Altitude & Navigation) ---
                with ui.column().classes('items-center'):
                    alt_label = instrument_box('ALT (m)', '0.0')
                    hdg_label = instrument_box('HDG (°)', '000', text_color="text-teal-400")
                    
                    # Compass Graphic
                    with ui.element('div').classes('w-28 h-28 rounded-full border-4 border-slate-600 bg-black relative overflow-hidden flex justify-center items-center mt-2 shadow-inner'):
                        
                        # Rotating compass card
                        compass_card = ui.element('div').classes('absolute w-full h-full flex justify-center items-center')
                        compass_card.style('transition: transform 0.05s linear;')
                        
                        compass_svg = '''
                        <svg width="100%" height="100%" viewBox="0 0 100 100">
                            <line x1="50" y1="5" x2="50" y2="12" stroke="white" stroke-width="2"/>
                            <line x1="95" y1="50" x2="88" y2="50" stroke="white" stroke-width="2"/>
                            <line x1="50" y1="95" x2="50" y2="88" stroke="white" stroke-width="2"/>
                            <line x1="5" y1="50" x2="12" y2="50" stroke="white" stroke-width="2"/>
                            
                            <text x="50" y="26" fill="white" font-size="14" font-family="monospace" font-weight="bold" text-anchor="middle">N</text>
                            <text x="79" y="55" fill="white" font-size="14" font-family="monospace" font-weight="bold" text-anchor="middle">E</text>
                            <text x="50" y="84" fill="white" font-size="14" font-family="monospace" font-weight="bold" text-anchor="middle">S</text>
                            <text x="21" y="55" fill="white" font-size="14" font-family="monospace" font-weight="bold" text-anchor="middle">W</text>
                        </svg>
                        '''
                        with compass_card:
                            ui.html(compass_svg)
                            
                        # Static Lubber Line (Yellow Pointer)
                        ui.html('''
                        <svg width="100%" height="100%" class="absolute top-0 left-0 pointer-events-none">
                            <polygon points="45,5 55,5 50,15" fill="yellow" />
                        </svg>
                        ''')

        # ==========================================
        # RIGHT: CONTROLS
        # ==========================================
        with ui.column().classes('bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700 w-72 items-center gap-6'):
            
            ui.label('SYSTEM STATUS').classes('text-slate-400 font-bold tracking-widest')
            status_label = ui.label('DISARMED').classes('text-3xl font-bold text-red-500 mb-4')
            
            def toggle_arm():
                if telemetry.armed:
                    telemetry.armed = False
                    telemetry.pitch = 0
                    telemetry.roll = 0
                    status_label.set_text('DISARMED')
                    status_label.classes(replace='text-3xl font-bold text-red-500 mb-4')
                    arm_btn.set_text('ARM SYSTEM')
                    arm_btn.classes(replace='w-full py-4 font-bold text-lg bg-red-600 hover:bg-red-700 text-white rounded-xl shadow-lg transition-colors')
                else:
                    telemetry.armed = True
                    status_label.set_text('ARMED')
                    status_label.classes(replace='text-3xl font-bold text-green-500 mb-4')
                    arm_btn.set_text('DISARM')
                    arm_btn.classes(replace='w-full py-4 font-bold text-lg bg-slate-600 hover:bg-slate-700 text-white rounded-xl shadow-lg transition-colors')
            
            arm_btn = ui.button('ARM SYSTEM', on_click=toggle_arm).classes(
                'w-full py-4 font-bold text-lg bg-red-600 hover:bg-red-700 text-white rounded-xl shadow-lg transition-colors'
            )

    # ==========================================
    # TELEMETRY LOOP
    # ==========================================
    def update_ui():
        if telemetry.armed:
            # Simulate flight dynamics and sensor noise
            telemetry.pitch += random.uniform(-1.0, 1.0)
            telemetry.roll += random.uniform(-2.0, 2.0)
            telemetry.heading = (telemetry.heading + random.uniform(-1.5, 1.5)) % 360
            
            # Limits for simulation sanity
            telemetry.pitch = max(-45, min(45, telemetry.pitch))
            telemetry.roll = max(-60, min(60, telemetry.roll))
            
            telemetry.airspeed += random.uniform(-0.5, 0.5)
            telemetry.alt += random.uniform(-1.0, 1.0)
            
            # Mocking the new sensors
            telemetry.vsi += random.uniform(-0.5, 0.5)
            telemetry.vsi = max(-15, min(15, telemetry.vsi))
            
            telemetry.alpha = max(-5, min(15, telemetry.pitch * 0.3 + random.uniform(-0.5, 0.5)))
            
            # G-Force roughly simulates 1G level flight, increasing with roll/pitch
            telemetry.g_force = max(0.5, min(3.0, 1.0 + (abs(telemetry.roll) / 60) + random.uniform(-0.1, 0.1)))
            
        # 1. Update text displays
        spd_label.set_text(f"{telemetry.airspeed:.1f}")
        vsi_label.set_text(f"{telemetry.vsi:.1f}")
        alpha_label.set_text(f"{telemetry.alpha:.1f}")
        g_label.set_text(f"{telemetry.g_force:.1f}")
        
        alt_label.set_text(f"{telemetry.alt:.1f}")
        hdg_label.set_text(f"{int(telemetry.heading):03d}")
        
        # 2. Update Horizon Graphics
        pitch_translation = telemetry.pitch * 5
        horizon.style(f'transform: rotate({-telemetry.roll}deg) translateY({pitch_translation}px);')
        
        # 3. Update Compass Graphic (Rotate negative to the heading so North moves away from the lubber line correctly)
        compass_card.style(f'transform: rotate({-telemetry.heading}deg); transition: transform 0.05s linear;')

    # Run the loop at 20 frames per second (0.05s)
    ui.timer(0.05, update_ui) 

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Desktop GCS", native=True, window_size=(1100, 700))